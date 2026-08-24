"""
Pydantic response models for the API client.

Each model validates raw JSON from the server into a typed, guaranteed-shape
object - if the API returns something unexpected, model_validate raises
instead of letting bad data flow silently into the rest of the program.
"""

from pathlib import Path

from pydantic import BaseModel, Field


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
