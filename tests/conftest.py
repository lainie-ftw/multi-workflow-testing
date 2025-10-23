import pytest
import pytest_asyncio
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from unittest.mock import AsyncMock, MagicMock

@pytest_asyncio.fixture(scope="function")
async def workflow_environment():
    """Provides a test workflow environment with time skipping."""
    async with await WorkflowEnvironment.start_time_skipping() as env:
        yield env

@pytest.fixture
def mock_temporal_client():
    """Provides a mocked Temporal client for activity testing."""
    client = AsyncMock()
    return client
