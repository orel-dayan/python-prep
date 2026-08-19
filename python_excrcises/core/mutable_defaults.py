def add_items_to_list(item: int, lst: list[int] | None = None) -> list[int]:
    """Best practice: default to None, build the mutable object fresh inside the function."""
    if lst is None:
        lst = []
    lst.append(item)
    return lst


# ---------------------------------------------------------------------------
# Best practice: never use a mutable object (list, dict, set, or any mutable
# class instance) as a default argument value.
#
# `add_items_to_list` above already applies the fix. Below is the anti-pattern
# it avoids, plus a demonstration of why it breaks.
# ---------------------------------------------------------------------------

# bad — a mutable default is evaluated ONCE, when the function is DEFINED
# (at import time), not on each call. That single list object is stored in
# add_items_to_list_bad.__defaults__ and reused by every call that omits `lst`.
def add_items_to_list_bad(item: int, lst: list[int] = []) -> list[int]:
    lst.append(item)
    return lst


if __name__ == "__main__":
    # good: every call that omits `lst` gets a brand new, independent list
    print(add_items_to_list(1))  # [1]
    print(add_items_to_list(2))  # [2]  -- unaffected by the previous call

    # bad: state silently leaks between calls, because `lst` is the SAME
    # list object every time — this is rarely what the caller intended
    print(add_items_to_list_bad(1))  # [1]
    print(add_items_to_list_bad(2))  # [1, 2]  -- leftover item from the first call!

    # proof: the default list is one shared object, reused across calls
    print(add_items_to_list_bad.__defaults__[0])  # [1, 2] -- the shared default itself

    # The rule generalizes to any mutable default: list, dict, set, or a
    # mutable class instance. The fix is always the same pattern used in
    # add_items_to_list(): default to an immutable sentinel (conventionally
    # None), then create the mutable object fresh inside the function body.