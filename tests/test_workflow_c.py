import pytest
from temporalio import activity
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from activities.activities import call_expensive_api
from workflows.workflow_c import WorkflowC


@pytest.mark.asyncio
async def test_workflow_c_successful_execution(workflow_environment):
    """Test WorkflowC executes successfully and calls call_expensive_api."""
    
    @activity.defn(name="call_expensive_api")
    async def mock_activity_call_expensive_api(input: str) -> str:
        return f"[MOCK] API response for: {input}"
    
    async with Worker(
        workflow_environment.client,
        task_queue="test-queue",
        workflows=[WorkflowC],
        activities=[mock_activity_call_expensive_api]
    ):
        result = await workflow_environment.client.execute_workflow(
            WorkflowC.run,
            "test input",
            id="test-workflow-c-1",
            task_queue="test-queue"
        )
        
        assert result == "\nWorkflow C completed: [MOCK] API response for: test input"
