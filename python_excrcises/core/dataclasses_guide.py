"""Complete dataclass reference - runnable, self-checking, ruff-clean.

Covers every ``@dataclass`` decorator parameter, every ``field()`` parameter, the
inheritance default-order problem with its three fixes, the frozen pitfalls, and
the five limits that push teams toward Pydantic at the system boundary.

Every demonstration of a deliberate error is wrapped in ``try/except`` so the
script always runs end to end.

Requires Python 3.10+ (``slots`` and ``kw_only`` were added in 3.10).

Run::

    python dataclass_full_guide.py
    ruff check dataclass_full_guide.py
"""

from __future__ import annotations

import json
import uuid
from dataclasses import (
    FrozenInstanceError,
    InitVar,
    asdict,
    astuple,
    dataclass,
    field,
    fields,
    replace,
)
from datetime import datetime, timezone
from enum import Enum
from typing import ClassVar

SEPARATOR_WIDTH = 70


def section(title: str) -> None:
    """Print a visual separator so each demo block is easy to find in the output."""
    print(f"\n{'=' * SEPARATOR_WIDTH}\n{title}\n{'=' * SEPARATOR_WIDTH}")


# ============================================================================
# 1. init / repr / eq - the three defaults
# ============================================================================


@dataclass
class Point:
    """Default dataclass: gets ``__init__``, ``__repr__`` and ``__eq__`` for free."""

    x: int
    y: int


@dataclass(repr=False)
class NoRepr:
    """Without ``repr`` the class falls back to the default object representation."""

    x: int


class PlainClass:
    """Regular class for contrast - its ``__eq__`` compares identity, not values."""

    def __init__(self, x: int, y: int) -> None:
        """Store the coordinates by hand, the way dataclass would generate for us."""
        self.x = x
        self.y = y


def demo_basics() -> None:
    """Show what the three default-on parameters actually generate."""
    section("1. init / repr / eq")

    print("repr        :", Point(3, 4))
    print("no repr     :", NoRepr(3))

    # eq=True compares by VALUE
    print("dataclass eq:", Point(1, 2) == Point(1, 2))
    # a plain class compares by IDENTITY (memory address)
    print("plain eq    :", PlainClass(1, 2) == PlainClass(1, 2))


# ============================================================================
# 2. order - generates __lt__, __le__, __gt__, __ge__
# ============================================================================


@dataclass(order=True)
class Version:
    """Comparison works like a tuple: field by field, in declaration order."""

    major: int
    minor: int
    patch: int


def demo_order() -> None:
    """Show tuple-style comparison and what happens without ``order``."""
    section("2. order - comparison and sorting")

    print("1.2.0 < 1.3.0 :", Version(1, 2, 0) < Version(1, 3, 0))
    print("sorted        :", sorted([Version(2, 0, 0), Version(1, 5, 0), Version(1, 5, 3)]))

    # without order=True the comparison operators do not exist at all
    try:
        _ = Point(1, 2) < Point(3, 4)  # type: ignore[operator]
    except TypeError as exc:
        print("no order      :", exc)


# ============================================================================
# 3. frozen - immutability and hashing
# ============================================================================


@dataclass(frozen=True)
class Config:
    """``frozen`` blocks assignment after ``__init__`` and enables ``__hash__``."""

    base_url: str
    timeout: int = 30


@dataclass(frozen=True)
class ShallowFreeze:
    """PITFALL: freezing is shallow, so the list inside stays mutable."""

    name: str
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DeepFreeze:
    """FIX: a tuple instead of a list keeps the object truly immutable and hashable."""

    name: str
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class FrozenComputed:
    """A frozen dataclass cannot assign in ``__post_init__`` without a bypass."""

    duration_ms: float
    duration_sec: float = field(init=False)

    def __post_init__(self) -> None:
        """Set the derived field through ``object`` - the standard frozen idiom."""
        object.__setattr__(self, "duration_sec", self.duration_ms / 1000)


def demo_frozen() -> None:
    """Show immutability, hashing, and the three frozen pitfalls."""
    section("3. frozen - immutable objects")

    cfg = Config("https://qa.example.com")
    print("read ok      :", cfg.timeout)

    try:
        cfg.timeout = 60  # type: ignore[misc]
    except FrozenInstanceError as exc:
        print("write blocked:", exc)

    # "changing" a frozen object means creating a copy
    print("original     :", cfg)
    print("replaced     :", replace(cfg, base_url="https://staging.example.com"))

    # frozen + eq gives __hash__, so it works as a dict key or set member
    cache = {cfg: "session-1"}
    print("as dict key  :", cache[Config("https://qa.example.com")])

    # a non-frozen dataclass is unhashable on purpose
    try:
        _ = {Point(1, 2): "value"}
    except TypeError as exc:
        print("unhashable   :", exc)

    # PITFALL 1: the freeze is shallow
    shallow = ShallowFreeze("api", ["smoke"])
    shallow.tags.append("critical")  # allowed - the list object itself is not frozen
    print("shallow      :", shallow)
    try:
        hash(shallow)
    except TypeError as exc:
        print("hash broken  :", exc)

    print("deep hash ok :", isinstance(hash(DeepFreeze("api", ("smoke",))), int))
    print("computed     :", FrozenComputed(1500))


# ============================================================================
# 4. unsafe_hash - why you almost never want it
# ============================================================================


@dataclass(unsafe_hash=True)
class RiskyKey:
    """Hashable but mutable - mutating it after insertion loses the entry."""

    x: int


def demo_unsafe_hash() -> None:
    """Show how a mutated key makes its own dict entry unreachable."""
    section("4. unsafe_hash - the dangerous option")

    key = RiskyKey(1)
    lookup = {key: "value"}
    print("before mutate:", lookup.get(RiskyKey(1)))

    key.x = 99  # the hash changed, so the entry can no longer be found
    print("after mutate :", lookup.get(RiskyKey(99)))
    print("still inside :", list(lookup.values()))


# ============================================================================
# 5. slots - memory and speed
# ============================================================================


@dataclass(slots=True)
class SlottedPoint:
    """``__slots__`` removes ``__dict__``: less memory, faster access, no new attributes."""

    x: int
    y: int


def demo_slots() -> None:
    """Show that slots block dynamic attribute creation."""
    section("5. slots - memory optimization")

    slotted = SlottedPoint(1, 2)
    print("works        :", slotted)

    try:
        slotted.z = 5  # type: ignore[attr-defined]
    except AttributeError as exc:
        print("no new attrs :", exc)

    plain = Point(1, 2)
    plain.z = 5  # type: ignore[attr-defined]
    print("plain allows :", plain.z)  # type: ignore[attr-defined]


# ============================================================================
# 6. The inheritance problem and its three solutions
# ============================================================================

INHERITANCE_PROBLEM = """
@dataclass
class Base:
    name: str
    timeout: int = 30

@dataclass
class Child(Base):
    retries: int

Generated signature: def __init__(self, name, timeout=30, retries)
Result: TypeError: non-default argument 'retries' follows default argument

The merged field order is "Base fields first, then Child fields", and Python
never allows a non-default parameter to follow a defaulted one.
"""


@dataclass
class BaseA:
    """Shared base used by solution 1 and solution 3."""

    name: str
    timeout: int = 30


@dataclass
class ChildA(BaseA):
    """Solution 1 - give it a default. Simple, but the field becomes OPTIONAL."""

    retries: int = 0


@dataclass(kw_only=True)
class BaseB:
    """Base for solution 2 - the whole hierarchy is keyword-only."""

    name: str
    timeout: int = 30


@dataclass(kw_only=True)
class ChildB(BaseB):
    """Solution 2 - the field stays REQUIRED, but nothing can be passed positionally."""

    retries: int


@dataclass
class ChildC(BaseA):
    """Solution 3 - the field stays REQUIRED and the other fields stay positional."""

    retries: int = field(kw_only=True)


def demo_inheritance() -> None:
    """Compare the three fixes for the default-order problem side by side."""
    section("6. Inheritance - the default-order problem")
    print(INHERITANCE_PROBLEM)

    print("-- Solution 1: default value (field becomes optional) --")
    print(ChildA("api-suite"))  # retries silently defaults to 0
    print(ChildA("api-suite", 60, 3))  # fully positional

    print("\n-- Solution 2: kw_only on the class (everything named) --")
    print(ChildB(name="api-suite", retries=3))
    print(ChildB(retries=3, name="api-suite"))  # order is irrelevant
    try:
        ChildB("api-suite", retries=3)  # type: ignore[misc]
    except TypeError as exc:
        print("positional blocked:", exc)
    try:
        ChildB(name="api-suite")  # type: ignore[call-arg]
    except TypeError as exc:
        print("required field    :", exc)

    print("\n-- Solution 3: kw_only on one field (mixed) --")
    print(ChildC("api-suite", 60, retries=3))  # name and timeout stay positional
    print(ChildC("api-suite", retries=3))  # timeout uses its default
    try:
        ChildC("api-suite", 60, 3)  # type: ignore[misc]
    except TypeError as exc:
        print("retries by name   :", exc)


# ============================================================================
# 7. field() and ClassVar - every parameter in one class
# ============================================================================


class Status(Enum):
    """Test outcome, used to show that Enum breaks naive JSON serialization."""

    PASS = "PASS"  # a test status, not a credential
    FAIL = "FAIL"
    SKIP = "SKIP"


@dataclass(order=True)
class TestResult:
    """Uses every ``field()`` parameter at least once, plus ClassVar and InitVar."""

    # ClassVar is NOT a field: shared by all instances, skipped by __init__ and __eq__
    total_created: ClassVar[int] = 0

    # init=False + repr=False: computed internally, drives sorting
    sort_index: float = field(init=False, repr=False, default=0.0)

    # compare=False: excluded from __eq__ and from the order operators
    test_name: str = field(compare=False)

    status: Status
    duration_ms: float

    # a plain default is fine because str is immutable
    error_message: str = field(default="", compare=False)

    # default_factory is MANDATORY for mutable defaults (list / dict / set)
    tags: list[str] = field(default_factory=list, compare=False)

    # repr=False keeps secrets out of logs and test reports
    auth_token: str = field(default="", repr=False, compare=False)

    # the factory can be any callable, including a lambda
    run_id: str = field(
        default_factory=lambda: str(uuid.uuid4())[:8],
        compare=False,
        repr=False,
    )

    # metadata changes no behavior - it is read back through fields()
    created_at: datetime = field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        compare=False,
        repr=False,
        metadata={"json_key": "createdAt", "export": True},
    )

    # hash=False excludes the field from __hash__ specifically
    debug_note: str = field(default="", compare=False, hash=False, repr=False)

    # InitVar reaches __init__ and __post_init__ but is never stored as an attribute
    retry_count: InitVar[int] = 0

    def __post_init__(self, retry_count: int) -> None:
        """Validate input and fill the derived fields right after ``__init__``."""
        if self.duration_ms < 0:
            message = "duration_ms cannot be negative"
            raise ValueError(message)
        self.sort_index = self.duration_ms
        if retry_count > 0:
            self.tags.append(f"retried-{retry_count}")
        TestResult.total_created += 1  # write through the class, never through self


def demo_field() -> None:
    """Exercise every ``field()`` parameter and show why each one exists."""
    section("7. field() - all parameters")

    passed = TestResult("login", Status.PASS, 342.5, auth_token="dummy-token")
    failed = TestResult("checkout", Status.FAIL, 891.2, error_message="Timeout", retry_count=2)

    print("repr hides token  :", passed)
    print("token still there :", passed.auth_token[:5])
    print("InitVar not stored:", hasattr(passed, "retry_count"))
    print("post_init tag     :", failed.tags)
    print("ClassVar counter  :", TestResult.total_created)

    # compare=False means only status and duration_ms take part in __eq__
    left = TestResult("login", Status.PASS, 100.0)
    right = TestResult("checkout", Status.PASS, 100.0)
    print("eq ignores name   :", left == right)
    print("sorted by duration:", [t.test_name for t in sorted([failed, passed])])

    # default_factory gives every object its own list
    first = TestResult("a", Status.PASS, 1.0)
    second = TestResult("b", Status.PASS, 1.0)
    first.tags.append("smoke")
    print("independent lists :", first.tags, second.tags)

    # a mutable default is rejected at class creation time - this is exactly why
    try:

        @dataclass
        class Broken:
            """Illegal on purpose: every instance would share the same list."""

            tags: list = []  # noqa: RUF008

    except ValueError as exc:
        print("mutable default   :", exc)

    try:
        TestResult("bad", Status.FAIL, -5.0)
    except ValueError as exc:
        print("post_init check   :", exc)


# ============================================================================
# 8. Introspection helpers: fields / asdict / astuple / replace
# ============================================================================


def demo_helpers() -> None:
    """Show the four module-level helpers and a metadata-driven serializer."""
    section("8. fields / asdict / astuple / replace")

    result = TestResult("login", Status.PASS, 342.5, tags=["smoke"])
    wanted = ("test_name", "duration_ms", "tags")

    print("asdict  :", {k: v for k, v in asdict(result).items() if k in wanted})
    print("astuple :", astuple(result)[:4])
    print("replace :", replace(result, status=Status.FAIL).status)

    # metadata drives a generic exporter without hardcoding any field name
    exported = {
        spec.metadata["json_key"]: getattr(result, spec.name)
        for spec in fields(result)
        if spec.metadata.get("export")
    }
    print("metadata export:", list(exported))

    print("\nfield introspection:")
    for spec in list(fields(TestResult))[:5]:
        flags = f"init={spec.init!s:<5} repr={spec.repr!s:<5} compare={spec.compare}"
        print(f"  {spec.name:<14} {flags}")


# ============================================================================
# 9. Where dataclass stops being enough
# ============================================================================


@dataclass
class ApiUser:
    """Type hints are NOT enforced at runtime - this is the core limitation."""

    user_id: int
    email: str
    is_active: bool = True


@dataclass
class RetryPolicy:
    """Nested model that a plain dataclass will never build for you."""

    count: int
    delay_sec: float


@dataclass
class SuiteConfig:
    """Holds a nested dataclass to show that no conversion happens."""

    base_url: str
    retries: RetryPolicy


def demo_limits() -> None:
    """Prove the five gaps that make teams reach for Pydantic."""
    section("9. dataclass limits - why teams move to Pydantic")

    # 1. no runtime type validation - three wrong types, zero errors
    wrong_types = ApiUser(user_id="not-a-number", email=12345, is_active="yes")  # type: ignore[arg-type]
    print("1. no validation  :", wrong_types)

    # 2. no coercion - JSON commonly delivers numbers as strings
    from_api = ApiUser(user_id="42", email="qa@example.com")  # type: ignore[arg-type]
    print("2. no coercion    :", type(from_api.user_id).__name__, "- expected int")

    # 3. nested structures are not converted into their dataclass type
    raw = {"base_url": "https://qa.example.com", "retries": {"count": 3, "delay_sec": 1.0}}
    cfg = SuiteConfig(**raw)  # type: ignore[arg-type]
    print("3. nested is dict :", type(cfg.retries).__name__, "- expected RetryPolicy")

    # 4. __post_init__ raises on the first problem instead of collecting them all
    print("4. errors surface one at a time, not as a structured list")

    # 5. asdict cannot serialize Enum or datetime, and there is no schema output
    try:
        json.dumps(asdict(TestResult("x", Status.PASS, 1.0)))
    except TypeError as exc:
        print("5. json fails     :", exc)

    print("\nPydantic covers all five: validation, coercion, nested parsing,")
    print("structured ValidationError, JSON serialization, aliases and JSON Schema.")
    print("Rule of thumb: Pydantic at the system boundary, dataclass inside.")


# ============================================================================


def main() -> None:
    """Run every demo in order."""
    demo_basics()
    demo_order()
    demo_frozen()
    demo_unsafe_hash()
    demo_slots()
    demo_inheritance()
    demo_field()
    demo_helpers()
    demo_limits()
    print("\nAll demos completed without crashing.")


if __name__ == "__main__":
    main()