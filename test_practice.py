import pytest
from pathlib import Path
import tempfile

import pytest


@pytest.fixture(scope="module")
def tmp_file():
    def create(contents=""):
        temp = tempfile.NamedTemporaryFile(delete=False)
        try:
            path = Path(temp.name)
        finally:
            temp.close()

        path.write_text(contents, encoding="utf-8")
        return path

    return create


@pytest.fixture
def resource(request):
    print(f"Running: {request.node.name}")
    marker = request.node.get_closest_marker("slow")
    if marker:
        print("This is a slow test")
    yield "data"

def test_fast(resource):
    assert resource == "data"

@pytest.mark.slow
def test_heavy(resource):
    assert resource == "data"

    
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError('division by zero')
    return a / b

def test_add():
    assert add(1, 2) == 3


def test_divide():
    assert divide(1, 2) == 2

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


# import pytest


# def add(a, b):
#     print(f"adding {a} and {b}")
#     return a - b

# def div(a, b):
#     print(f"dividing {a} by {b}")
#     if b == 0:
#         raise ValueError("division by zero")
#     return a / b

# @pytest.mark.smoke
# def test_add():
#     assert add(1, 1) == 2

# # def test_fail():
# #     assert add(1, 1) == 1

# def test_div_by_0():
#     with pytest.raises(ValueError, match="division by zero"):
#         div(1, 0)

# @pytest.fixture
# def mock_array():
#     return [0, 1, 2, 3]


# def test_array(mock_array):
#     assert mock_array[3] == 3


# def isPos(num):
#     return num > 0

# @pytest.mark.parametrize("num, expected", [
#     (2, True),
#     (-4, False),
#     (0, False)
# ])

# @pytest.mark.slow
# def test_isPos(num, expected):
#     assert isPos(num) == expected

