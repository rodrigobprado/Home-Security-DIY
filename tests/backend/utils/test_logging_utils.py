from app.utils.logging_utils import mask_url, mask_sensitive_string

def test_mask_url_basic_auth():
    url = "http://user:password123@localhost:8123"
    masked = mask_url(url)
    assert "password123" not in masked
    assert "user:****@" in masked

def test_mask_url_query_params():
    url = "https://example.com/api?token=secret123&user=admin"
    masked = mask_url(url)
    assert "secret123" not in masked
    assert "token=****" in masked
    assert "user=admin" in masked

def test_mask_url_no_secrets():
    url = "https://example.com/api?page=1"
    masked = mask_url(url)
    assert masked == url

def test_mask_sensitive_string():
    text = "Connecting with token abc-123-def and key xyz-789"
    secrets = ["abc-123-def", "xyz-789"]
    masked = mask_sensitive_string(text, secrets)
    assert "abc-123-def" not in masked
    assert "xyz-789" not in masked
    assert "****" in masked

def test_mask_url_invalid():
    assert mask_url(None) is None
    # urlparse will parse "not a url ::::" as a path, and it has no sensitive parts
    assert mask_url("not a url ::::") == "not a url ::::"
