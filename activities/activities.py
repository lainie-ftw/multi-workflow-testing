import os
import uuid
from temporalio import activity
from shared.client import get_temporal_client

@activity.defn
async def activity_start_workflow_b(input: str) -> str:
    # Import here to avoid circular dependency issues
    from workflows.workflow_b import WorkflowB
    
    # Get client and start Workflow B
    client = await get_temporal_client()
    workflowID = "workflow-b-" + str(uuid.uuid4())
    
    workflow_b_handle = await client.start_workflow(
        WorkflowB.run,
        input,
        id=workflowID,
        task_queue="my-task-queue"
    )
    
    # Wait for Workflow B to complete - you could also return the workflow handle and not wait for it to complete.
    result = await workflow_b_handle.result()
    return result

@activity.defn
async def activity_start_workflow_c(input: str) -> str:
    # Import here to avoid circular dependency issues
    from workflows.workflow_c import WorkflowC
    
    # Get client and start Workflow C
    client = await get_temporal_client()
    workflowID = "workflow-c-" + str(uuid.uuid4())
    
    workflow_c_handle = await client.start_workflow(
        WorkflowC.run,
        input,
        id=workflowID,
        task_queue="my-task-queue"
    )
    
    # Wait for Workflow C to complete - you could also return the workflow handle and not wait for it to complete.
    result = await workflow_c_handle.result()
    return result

@activity.defn
async def call_expensive_api(input: str) -> str:
    """Activity that calls an expensive API"""
    env = os.getenv("ENVIRONMENT", "test")
    
    if env == "test" or env == "development":
        # Mock implementation for testing
        return await _mock_expensive_api_call(input)
    else:
        # Real implementation for production
        return await _real_expensive_api_call(input)

async def _mock_expensive_api_call(input: str) -> str:
    """Mock implementation - returns fake data"""
    activity.logger.info(f"[MOCK] Calling expensive API with: {input}")
    # Simulate API response
    return f"[MOCK] API response for: {input}"

async def _real_expensive_api_call(input: str) -> str:
    """Real implementation - calls actual API"""
    activity.logger.info(f"[REAL] Calling expensive API with: {input}")
    # Make real API call
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://expensive-api.example.com/endpoint",
            json={"data": input}
        )
        return response.json()["result"]
    
# Can do without mocks, and just activity that checks env 