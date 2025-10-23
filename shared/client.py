import os
from typing import Optional
from temporalio.client import Client

# Module-level variable to store test client
_test_client: Optional[Client] = None

def is_running_pytest() -> bool:
    """Check if code is currently running under pytest."""
    return "PYTEST_CURRENT_TEST" in os.environ

def set_test_client(client: Optional[Client]) -> None:
    """Set the test client to be used during pytest runs."""
    global _test_client
    _test_client = client

async def get_temporal_client() -> Client:
    """
    Creates a Temporal client based on environment configuration.
    Supports local server, mTLS, and API key authentication methods.
    
    During pytest execution, returns the test client if one has been set.
    Otherwise, connects to the real Temporal server.
    """
    # If running under pytest and a test client is available, use it
    if is_running_pytest() and _test_client is not None:
        return _test_client
    
    # Default to no TLS for local development
    tls_config = False
    TEMPORAL_ADDRESS = "localhost:7233"
    TEMPORAL_NAMESPACE = "default"

    return await Client.connect(
        TEMPORAL_ADDRESS,
        namespace=TEMPORAL_NAMESPACE,
        tls=tls_config,
    )
