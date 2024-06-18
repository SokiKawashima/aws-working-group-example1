import pytest
from app.core.fibonacci import fast_doubling_fibonacci


def test_fast_doubling_fibonacci():
    assert fast_doubling_fibonacci(2) == 1, "Test failed for n=2"
    assert fast_doubling_fibonacci(3) == 2, "Test failed for n=3"
    assert (
        fast_doubling_fibonacci(1000)
        == 43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875
    ), "Test failed for n=1000"
