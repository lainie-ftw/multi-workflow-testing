import pytest
from temporalio.client import Client
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from workflows.workflow_a import WorkflowA
from workflows.workflow_b import WorkflowB
from workflows.workflow_c import WorkflowC
from activities.activities import activity_start_workflow_b, activity_start_workflow_c, call_expensive_api

@pytest.mark.asyncio
async def test_workflow_chain(workflow_environment):
    """Test that WorkflowA calls WorkflowB calls WorkflowC successfully."""
    async with Worker(
        workflow_environment.client,
        task_queue="test-task-queue",
        workflows=[WorkflowA, WorkflowB, WorkflowC],  # Your Workflow class
        activities=[activity_start_workflow_b, activity_start_workflow_c, call_expensive_api],  # Your Activity function
    ):
        assert "this will fail" == await workflow_environment.client.execute_workflow(
            WorkflowA.run,
            "test input",
            id="test-e2e",
            task_queue="test-task-queue"
        )