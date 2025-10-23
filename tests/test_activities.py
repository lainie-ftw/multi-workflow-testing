import pytest
from activities.activities import call_expensive_api


@pytest.mark.asyncio
async def test_call_expensive_api():
    """Test call_expensive_api processes input correctly."""
    result = await call_expensive_api("test")
    assert result == "[MOCK] API response for: test"


# Note: Tests for activity_start_workflow_b and activity_start_workflow_c are better handled in integration tests since they require a full 
# Temporal environment to properly test workflow starting behavior and activity context.
# Unit testing these activities in isolation requires complex mocking that doesn't provide significant value over integration testing.
