from bits.exceptions import BitError
import pytest
import bits

def test_sign_bit():
    assert bits.sign_bit(1) == 0
    assert bits.sign_bit(-1) == 1

def test_min_bits():
    assert bits.min_bits(255) == 8
    assert bits.min_bits(-255) == 9

def test_min_bytes():
    assert bits.min_bytes(255) == 1
    assert bits.min_bytes(-255) == 2

def test_max_uvalue():
    assert bits.max_uvalue(8) == 255
    assert bits.max_uvalue(nbytes=1) == 255

def test_max_svalue():
    assert bits.max_svalue(8) == 127
    assert bits.max_svalue(nbytes=1) == 127

def test_uint():
    assert bits.uint(50) == 50
    assert bits.uint(-1) == 255
    assert bits.uint(-1, nbits=2) == 3
    assert bits.uint(-1, nbytes=2) == 65535

def test_sint():
    assert bits.sint(-1) == -1
    assert bits.sint(0b1111_1111) == -1
    assert bits.sint(0b11, nbits=2) == -1
    assert bits.sint(0b1111_1111, nbytes=2) == 255

def test_bits_initialization():
    with pytest.raises(TypeError):
        bits.Bits(1.1)

    with pytest.raises(BitError):
        bits.Bits(1, nbits=0)

    with pytest.raises(BitError):
        bits.Bits(1, nbytes=0)

    with pytest.raises(BitError):
        bits.Bits(1, nbits=0, nbytes=1)

    b = bits.Bits(127)
    assert b.value == 127
    assert b.nbits == 7

    b = bits.Bits(-255)
    assert b.value == -255
    assert b.nbits == 16

@pytest.fixture
def b():
    return bits.Bits(15)

def test_bits_comparison(b):
    assert (b <= 2) == False
    assert (b <  2) == False
    assert (b == 2) == False
    assert (b != 2) == True
    assert (b >= 2) == True
    assert (b >  2) == True

def test_bits_add(b):
    b2 = b + 1
    assert b2.value == 16
    assert b2.nbits == 5

def test_bits_sub(b):
    b2 = b - 1
    assert b2.value == 14
    assert b2.nbits == 4
