from jarvis.core.validators import is_safe_host, sanitize_text
from jarvis.services.security_service import SecurityService


def test_sanitize_text_trims_and_limits():
    raw = '  hello   world   ' * 40
    cleaned = sanitize_text(raw, max_len=20)
    assert cleaned == 'hello world hello wo'


def test_safe_host_validation():
    assert is_safe_host('8.8.8.8')
    assert is_safe_host('example.com')
    assert not is_safe_host('8.8.8.8;rm -rf')


def test_password_strength_levels():
    svc = SecurityService()
    weak = svc.password_strength('abc')
    strong = svc.password_strength('Abcdef!23456')
    assert weak['level'] == 'weak'
    assert strong['level'] in {'moderate', 'strong'}
