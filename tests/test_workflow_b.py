import pytest
from temporalio import activity
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from workflows.workflow_b import WorkflowB
from activities.activities import activity_start_workflow_c


@pytest.mark.asyncio
async def test_workflow_b_successful_execution(workflow_environment):
    """Test WorkflowB executes successfully and calls activity_start_workflow_c."""

    @activity.defn(name="activity_start_workflow_c")
    async def mock_activity_start_workflow_c(input: str) -> str:
        return "Mocked Workflow C result"
    
    async with Worker(
        workflow_environment.client,
        task_queue="test-queue",
        workflows=[WorkflowB],
        activities=[activity_start_workflow_c]
    ):
        result = await workflow_environment.client.execute_workflow(
            WorkflowB.run,
            "test input",
            id="test-workflow-b-1",
            task_queue="test-queue"
        )
        
        assert result == "\nWorkflow B completed: \nWorkflow C completed: [MOCK] API response for: test input"