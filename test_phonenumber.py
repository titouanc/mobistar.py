from phonenumber import PhoneNumber
from pytest import raises

def test_invalid():
    with raises(PhoneNumber.Invalid):
        PhoneNumber("caca")
        PhoneNumber("+32")

def test_str():
    p = PhoneNumber('0470123456')
    assert str(p) == '+32470123456'
    assert repr(p) == '+32 470 12 34 56'

def test_is_belgian_gsm():
    assert PhoneNumber('+32477123456').is_belgian_gsm()

    # Second digit is not in 7,8,9
    assert not PhoneNumber('+32422123456').is_belgian_gsm()

    # French number
    assert not PhoneNumber('+33612345678').is_belgian_gsm()

    # Not a mobile
    assert not PhoneNumber('+3221234567').is_belgian_gsm()

    # Missing digit
    assert not PhoneNumber('+32412345').is_belgian_gsm()

    # Too much digits
    assert not PhoneNumber('+3241234567').is_belgian_gsm()

def test_transitivity():
    number = "+32494123456"
    assert str(PhoneNumber(number)) == number