import pytest
import time
from unittest.mock import AsyncMock, patch, MagicMock
from app.security import _is_rate_limited

@pytest.mark.anyio
async def test_is_rate_limited_allowed():
    # Mocking get_redis and its pipeline
    mock_redis = MagicMock() # pipeline() is a normal method
    mock_pipe = AsyncMock()  # it returns an object used as async context manager
    
    # Results for: zremrangebyscore, zadd, zcard, expire
    # results[2] is zcard (event_count)
    mock_pipe.execute.return_value = [0, 1, 5, True]
    mock_redis.pipeline.return_value.__aenter__.return_value = mock_pipe
    
    with patch("app.security.get_redis", return_value=mock_redis):
        limited = await _is_rate_limited(
            category="test",
            key="127.0.0.1",
            window_seconds=60,
            max_events=10
        )
        
    assert limited is False
    assert mock_pipe.zremrangebyscore.called
    assert mock_pipe.zadd.called
    assert mock_pipe.zcard.called
    assert mock_pipe.expire.called

@pytest.mark.anyio
async def test_is_rate_limited_blocked():
    mock_redis = MagicMock()
    mock_pipe = AsyncMock()
    
    # event_count = 11, max_events = 10 -> limited = True
    mock_pipe.execute.return_value = [0, 1, 11, True]
    mock_redis.pipeline.return_value.__aenter__.return_value = mock_pipe
    
    with patch("app.security.get_redis", return_value=mock_redis):
        limited = await _is_rate_limited(
            category="test",
            key="127.0.0.1",
            window_seconds=60,
            max_events=10
        )
        
    assert limited is True
