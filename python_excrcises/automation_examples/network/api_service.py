"""
Async HTTP layer: bounded concurrency, retry with backoff, typed fetch calls.

This is the "engine" of the client - everything here is about talking to the
network safely and efficiently. It knows nothing about the CLI.
"""

import asyncio
from dataclasses import dataclass

import httpx

from api_models import Post, User

BASE_URL = "https://jsonplaceholder.typicode.com"


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
