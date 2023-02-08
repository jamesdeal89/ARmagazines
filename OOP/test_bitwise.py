# testing for bitwise.py using pytest
from bitwise import Bitwise

bitwise = Bitwise()

def test_binary():
    assert bitwise.decimalToBinary(10) == 1010
    assert bitwise.decimalToBinary(1) == 1
    assert bitwise.decimalToBinary(15) == 1111
    assert bitwise.decimalToBinary(255) == 11111111
