import re
from urllib.parse import urlparse, urlunparse

def mask_url(url: str) -> str:
    """
    Masks sensitive parts of a URL, specifically the password in basic auth
    and common query parameters that might contain tokens.
    """
    if not url:
        return url

    try:
        parsed = urlparse(url)
        if parsed.password:
            # Mask the password in basic auth (e.g., http://user:pass@host)
            netloc = parsed.netloc.replace(f":{parsed.password}@", ":****@")
            parsed = parsed._replace(netloc=netloc)

        # Mask common token-like query parameters
        if parsed.query:
            query_params = []
            for param in parsed.query.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    if any(secret_key in key.lower() for secret_key in ['token', 'key', 'secret', 'pass', 'auth']):
                        query_params.append(f"{key}=****")
                    else:
                        query_params.append(param)
                else:
                    query_params.append(param)
            parsed = parsed._replace(query="&".join(query_params))

        return urlunparse(parsed)
    except Exception:
        # If parsing fails, return a safe string or a heavily masked version
        return "****"

def mask_sensitive_string(text: str, secrets: list[str]) -> str:
    """
    Masks specific secrets found in a string.
    """
    if not text or not secrets:
        return text

    masked_text = text
    for secret in secrets:
        if secret and len(secret) > 3: # Only mask secrets of reasonable length
            masked_text = masked_text.replace(secret, "****")

    return masked_text
