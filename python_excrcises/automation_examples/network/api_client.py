"""
CLI entry point for the async API client.

The network engine lives in api_service.py (ApiClient, ClientConfig) and the
response shapes live in api_models.py (Address, User, Post). This file only
wires argparse to that engine and prints results - it has no async retry or
concurrency logic of its own.

Usage:
    python api_client.py fetch --ids 1 2 3 --save
    python api_client.py fetch --all --output ./data
"""

import argparse
import asyncio
from pathlib import Path

from api_service import ApiClient, ClientConfig


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
