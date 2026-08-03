"""
Async HTTP client with concurrency control, retries, and Pydantic validation.

Demonstrates the full asyncio pattern for automation against a REST API:
bounded concurrency via semaphore, retry with backoff, blocking file I/O
offloaded with to_thread, and typed response models.

Usage:
    python api_client.py fetch --ids 1 2 3 --save
    python api_client.py fetch --all --output ./data
"""

import argparse
import asyncio
import json
from dataclasses import dataclass
from pathlib import Path

import httpx
from pydantic import BaseModel, Field

BASE_URL = "https://jsonplaceholder.typicode.com"


# ── Models ────────────────────────────────────────────────────────────────────

class Address(BaseModel):
    street: str
    city: str
    zipcode: str


class User(BaseModel):
    id: int | None = None
    name: str
    username: str
    email: str
    address: Address | None = None

    def save_to_file(self, directory: Path) -> Path:
        """Blocking file write - must be called via asyncio.to_thread."""
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"user_{self.id}.json"
        path.write_text(self.model_dump_json(indent=2))
        return path

    @classmethod
    def load_from_file(cls, path: Path) -> "User":
        return cls.model_validate_json(path.read_text())


class Post(BaseModel):
    id: int | None = None
    user_id: int = Field(alias="userId")
    title: str
    body: str

    model_config = {"populate_by_name": True}


# ── Client ────────────────────────────────────────────────────────────────────

@dataclass
class ClientConfig:
    base_url: str = BASE_URL
    max_concurrent: int = 10
    timeout: float = 10.0
    max_retries: int = 3


class ApiClient:
    def __init__(self, config: ClientConfig | None = None):
        self._config = config or ClientConfig()
        self._semaphore = asyncio.Semaphore(self._config.max_concurrent)
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "ApiClient":
        self._client = httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout,
        )
        return self

    async def __aexit__(self, *args) -> None:
        if self._client:
            await self._client.aclose()

    async def _get_with_retry(self, path: str) -> dict | list:
        """Fetch with bounded concurrency and exponential backoff.

        The semaphore caps in-flight requests. Without it, gathering 1000
        coroutines would open 1000 sockets simultaneously - exhausting file
        descriptors and likely triggering server-side rate limiting.
        """
        if self._client is None:
            raise RuntimeError("ApiClient must be used as an async context manager")

        delay = 1.0
        last_error: Exception | None = None

        async with self._semaphore:
            for attempt in range(1, self._config.max_retries + 1):
                try:
                    response = await self._client.get(path)
                    response.raise_for_status()
                    return response.json()
                except (httpx.HTTPStatusError, httpx.RequestError) as e:
                    last_error = e
                    if attempt == self._config.max_retries:
                        break
                    await asyncio.sleep(delay)
                    delay *= 2

        raise last_error  # type: ignore[misc]

    async def get_user(self, user_id: int) -> User:
        data = await self._get_with_retry(f"/users/{user_id}")
        return User.model_validate(data)

    async def get_users(self, user_ids: list[int] | None = None) -> list[User]:
        """Fetch multiple users concurrently.

        gather runs all coroutines at once rather than sequentially - total
        time approaches the slowest single request instead of their sum.
        """
        if user_ids is None:
            data = await self._get_with_retry("/users")
            return [User.model_validate(u) for u in data]

        tasks = [self.get_user(uid) for uid in user_ids]
        return await asyncio.gather(*tasks)

    async def get_user_posts(self, user_id: int) -> list[Post]:
        data = await self._get_with_retry(f"/users/{user_id}/posts")
        return [Post.model_validate(p) for p in data]

    async def get_users_with_posts(
        self, user_ids: list[int]
    ) -> dict[int, tuple[User, list[Post]]]:
        """Fetch users and their posts, all concurrently."""
        user_task = self.get_users(user_ids)
        post_tasks = [self.get_user_posts(uid) for uid in user_ids]

        users, *post_lists = await asyncio.gather(user_task, *post_tasks)
        return {
            user.id: (user, posts)
            for user, posts in zip(users, post_lists)
            if user.id is not None
        }


# ── Commands ──────────────────────────────────────────────────────────────────

async def cmd_fetch(args: argparse.Namespace) -> None:
    config = ClientConfig(max_concurrent=args.concurrent)

    async with ApiClient(config) as client:
        user_ids = None if args.all else args.ids
        users = await client.get_users(user_ids)

        print(f"Fetched {len(users)} users\n")
        for user in users:
            city = user.address.city if user.address else "unknown"
            print(f"  [{user.id}] {user.name} <{user.email}> - {city}")

        if args.save:
            # save_to_file is blocking; to_thread keeps the event loop free
            paths = await asyncio.gather(
                *[asyncio.to_thread(u.save_to_file, args.output) for u in users]
            )
            print(f"\nSaved {len(paths)} files to {args.output}")


async def cmd_posts(args: argparse.Namespace) -> None:
    async with ApiClient() as client:
        data = await client.get_users_with_posts(args.ids)

        for user_id, (user, posts) in data.items():
            print(f"\n{user.name} ({len(posts)} posts)")
            for post in posts[:3]:
                print(f"  - {post.title[:60]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Async API client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch = subparsers.add_parser("fetch", help="Fetch users")
    fetch.add_argument("--ids", type=int, nargs="+", default=[1, 2, 3])
    fetch.add_argument("--all", action="store_true", help="Fetch all users")
    fetch.add_argument("--save", action="store_true", help="Save to JSON files")
    fetch.add_argument("--output", type=Path, default=Path("./data"))
    fetch.add_argument("--concurrent", type=int, default=10)
    fetch.set_defaults(func=cmd_fetch)

    posts = subparsers.add_parser("posts", help="Fetch users with their posts")
    posts.add_argument("--ids", type=int, nargs="+", default=[1, 2])
    posts.set_defaults(func=cmd_posts)

    args = parser.parse_args()
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()
