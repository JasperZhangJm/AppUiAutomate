import pytest

"""
@pytest.fixture(params=[1, 2, 3])
def param_fixture(request):
    print("aaabbbccc")
    print(request.param)
    return request.param


def test_param_fixture_11111111e(param_fixture):
    print("1112223333")
    print(param_fixture)
    # assert param_fixture in [1, 2, 3]
"""


# 在装饰的方法中可以直接使用定义的参数，例如，input_param和expected
@pytest.mark.parametrize("input_param, expected", [
    (1, 1),
    (2, 4),
    (3, 9)
])
def test_square(input_param, expected):
    print("input_param", input_param)
    print("expected", expected)
    assert input_param ** 2 == expected
