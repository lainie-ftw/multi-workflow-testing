import pytest
from temporalio import activity
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from workflows.workflow_b import WorkflowB


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
        activities=[mock_activity_start_workflow_c]
    ):
        result = await workflow_environment.client.execute_workflow(
            WorkflowB.run,
            "test input",
            id="test-workflow-b-1",
            task_queue="test-queue"
        )
        
        assert result == "\nWorkflow B completed: Mocked Workflow C result"


@pytest.mark.asyncio
async def test_workflow_b_with_different_inputs(workflow_environment):
    """Test WorkflowB handles various input types."""
    
    @activity.defn(name="activity_start_workflow_c")
    async def mock_activity_start_workflow_c(input: str) -> str:
        return f"Processed: {input}"
    
    async with Worker(
        workflow_environment.client,
        task_queue="test-queue",
        workflows=[WorkflowB],
        activities=[mock_activity_start_workflow_c]
    ):
        # Test with empty string
        result = await workflow_environment.client.execute_workflow(
            WorkflowB.run,
            "",
            id="test-workflow-b-2",
            task_queue="test-queue"
        )
        assert "Workflow B completed" in result
        
        # Test with long string
        long_input = "a" * 1000
        result = await workflow_environment.client.execute_workflow(
            WorkflowB.run,
            long_input,
            id="test-workflow-b-3",
            task_queue="test-queue"
        )
        assert "Workflow B completed" in result