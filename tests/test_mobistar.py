import mobistarpy.sms as mobistar
from mock import MagicMock
from pytest import raises

def setup_function(*args, **kwargs):
    mobistar.requests = MagicMock()


def test_request():
    mobistar._request('Some text')
    assert mobistar.requests.post.called


def test_extract_message():
    assert mobistar._extract_message("<message><![CDATA[Some text]]></message>") == 'Some text'
    with raises(AssertionError):
        mobistar._extract_message("Some text")


def test_auth():
    class res:
        status_code = 200
        content = '''<result code="100"></result>'''
    mobistar.requests.post = MagicMock(return_value=res)

    def get_pin(a):
        res.content = '''<result code="100"><message><![CDATA[123456 123456789abcdef123456789abcdef12\r]]></message></result>'''
        return "13J7"

    assert mobistar.auth("+32499123456", get_pin) == "123456 123456789abcdef123456789abcdef12"


def test_send_sms():
    class res:
        status_code = 200
        content = '''<result code="100"><message><![CDATA[123456789]]></message></result>'''
    mobistar.requests.post = MagicMock(return_value=res)
    assert mobistar.send_sms('12345', "Hello", '0471234567') == '123456789'
