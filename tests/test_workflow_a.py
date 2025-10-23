import pytest
from temporalio import activity
from temporalio.worker import Worker
from workflows.workflow_a import WorkflowA
from activities.activities import activity_start_workflow_b


@pytest.mark.asyncio
async def test_workflow_a_successful_execution(workflow_environment):
    """Test WorkflowA executes successfully and calls activity_start_workflow_b."""
    
    # Mock activity that returns a known value
    @activity.defn(name="activity_start_workflow_b")
    async def mock_activity_start_workflow_b(input: str) -> str:
        return "Mocked Workflow B result"
    
    async with Worker(
        workflow_environment.client,
        task_queue="test-queue",
        workflows=[WorkflowA],
        activities=[activity_start_workflow_b]
    ):
        result = await workflow_environment.client.execute_workflow(
            WorkflowA.run,
            "test input",
            id="test-workflow-a-1",
            task_queue="test-queue"
        )
        
        assert result == "Workflow A completed: Mocked Workflow B result"


@pytest.mark.asyncio
async def test_workflow_a_with_different_inputs(workflow_environment):
    """Test WorkflowA handles various input types."""
    
    # You can do this with a mocked activity, but it may not be necessary depending on what else the workflow does.
    @activity.defn(name="activity_start_workflow_b")
    async def mock_activity_start_workflow_b(input: str) -> str:
        return f"Processed: {input}"
    
    async with Worker(
        workflow_environment.client,
        task_queue="test-queue",
        workflows=[WorkflowA],
        activities=[mock_activity_start_workflow_b]
    ):
        # Test with empty string
        result = await workflow_environment.client.execute_workflow(
            WorkflowA.run,
            "",
            id="test-workflow-a-2",
            task_queue="test-queue"
        )
        assert "Workflow A completed" in result
        
        # Test with special characters
        result = await workflow_environment.client.execute_workflow(
            WorkflowA.run,
            "test@#$%",
            id="test-workflow-a-3",
            task_queue="test-queue"
        )
        assert "Workflow A completed" in result