"""
ctypes example — call a C++ compiled shared library (.dll/.so) from Python.

Steps:
  1. Compile the C++ file:
       Windows:  g++ -shared -o math_lib.dll -fPIC 4_ctypes_lib.cpp
       Linux:    g++ -shared -o math_lib.so  -fPIC 4_ctypes_lib.cpp
  2. Run this script: python 4_ctypes_example.py
"""

import ctypes
import os
import sys


def load_library():
    """Load the compiled C++ shared library."""
    if sys.platform == "win32":
        lib_name = "math_lib.dll"
    else:
        lib_name = "./math_lib.so"

    lib_path = os.path.join(os.path.dirname(__file__), lib_name)
    return ctypes.CDLL(lib_path)


def setup_functions(lib):
    """Tell ctypes the argument types and return types of each C++ function."""

    # int add(int a, int b)
    lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.add.restype  = ctypes.c_int

    # double average(int* arr, int size)
    lib.average.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    lib.average.restype  = ctypes.c_double

    return lib


def demo_ctypes():
    lib = setup_functions(load_library())

    # ── call add ──────────────────────────────────────────────────────────────
    result = lib.add(3, 7)
    assert result == 10, f"expected 10, got {result}"
    print(f"add(3, 7) = {result}")

    # ── call average with a C array ───────────────────────────────────────────
    arr = (ctypes.c_int * 5)(10, 20, 30, 40, 50)   # create C int[5]
    avg = lib.average(arr, len(arr))
    print(f"average([10,20,30,40,50]) = {avg}")     # expected 30.0


if __name__ == "__main__":
    demo_ctypes()
