import pytest
from temporalio.worker import Worker
from activities.activities import call_expensive_api
from workflows.workflow_c import WorkflowC


@pytest.mark.asyncio
async def test_workflow_c_successful_execution(workflow_environment):
    """Test WorkflowC executes successfully and calls call_expensive_api."""
    
    async with Worker(
        workflow_environment.client,
        task_queue="test-queue",
        workflows=[WorkflowC],
        activities=[call_expensive_api] # Calls the real activity
    ):
        result = await workflow_environment.client.execute_workflow(
            WorkflowC.run,
            "test input",
            id="test-workflow-c-1",
            task_queue="test-queue"
        )
        
        assert result == "\nWorkflow C completed: [MOCK] API response for: test input"
