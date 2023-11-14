from beartype import beartype

from timeit import timeit

from pydantic import validate_call, BaseModel


class Foo:
    def __init__(self, a, b, c):
        assert isinstance(a, int)
        assert isinstance(b, str)
        assert isinstance(c, list)
        for i in c:
            assert isinstance(i, str)

        self.a = a
        self.b = b
        self.c = c


class FooBeartype:
    @beartype
    def __init__(self, a: int, b: str, c: list[str]):
        self.a = a
        self.b = b
        self.c = c


class FooPydantic(BaseModel):
    a: int
    b: str
    c: list[str]


def main_assert(arg01, arg02, arg03):
    assert isinstance(arg01, str)
    assert isinstance(arg02, int)
    assert isinstance(arg03, Foo)

    str_len = len(arg01) + arg02
    assert isinstance(str_len, int)

    return ("duck_bar", str_len, arg03)


@beartype
def main_beartype(arg01: str, arg02: int, arg03: FooBeartype) -> tuple[str, int, FooBeartype]:
    str_len = len(arg01) + arg02
    arg03.c.append(arg03.b * arg03.a)
    return ("bear_bar", str_len, arg03)


@validate_call(validate_return=True)
def main_pydantic(arg01: str, arg02: int, arg03: FooPydantic) -> tuple[str, int, FooPydantic]:
    str_len = len(arg01) + arg02
    arg03.c.append(arg03.b * arg03.a)
    return ("pydantic_bar", str_len, arg03)


if __name__ == "__main__":
    num_loops = 100000

    duck_result_assert = timeit(
        'main_assert("foo", 1, Foo(a=2, b="foo", c=["bazz"]))',
        setup="from __main__ import main_assert, Foo",
        number=num_loops,
    )
    print("timeit assert       time:", round(duck_result_assert, 4), "seconds")

    bear_result = timeit(
        'main_beartype("foo", 1, FooBeartype(a=2, b="foo", c=["bazz"]))',
        setup="from __main__ import main_beartype, FooBeartype",
        number=num_loops,
    )
    print("timeit beartype     time:", round(bear_result, 4), "seconds")

    pydantic_result = timeit(
        'main_pydantic("foo", 1, FooPydantic(a=2, b="foo", c=["bazz"]))',
        setup="from __main__ import main_pydantic, FooPydantic",
        number=num_loops,
    )
    print("timeit pydantic     time:", round(pydantic_result, 4), "seconds")
