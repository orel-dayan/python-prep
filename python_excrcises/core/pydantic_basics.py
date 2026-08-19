"""pydantic — data validation from type hints, enforced at runtime.

A dataclass documents types; pydantic checks them. A dict from a config file
or an API response gets no guarantee its fields exist or have the right type
until something reads it wrong three layers away. A BaseModel raises
immediately, at the boundary, with a precise error.

Requires: pip install pydantic
"""

from pydantic import BaseModel, Field, ValidationError, field_validator


class DeviceConfig(BaseModel):
    port: str
    baudrate: int = 115200
    timeout: float = Field(default=5.0, gt=0, le=60)  # 0 < timeout <= 60
    retries: int = Field(default=3, ge=0)

    @field_validator("port")
    @classmethod
    def port_must_look_valid(cls, v: str) -> str:
        if not v.startswith(("/dev/", "COM")):
            raise ValueError(f"port must be a device path, got {v!r}")
        return v


if __name__ == "__main__":
    config = DeviceConfig(port="COM3", timeout="2.5")  # "2.5" is coerced to 2.5
    print(config)
    print(type(config.timeout))  # <class 'float'> - coerced, not left as str

    try:
        DeviceConfig(port="not-a-port", timeout=-1)
    except ValidationError as e:
        for err in e.errors():
            print(f"{err['loc'][0]}: {err['msg']}")
