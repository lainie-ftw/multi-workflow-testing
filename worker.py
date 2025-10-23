import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

# Import all workflows
from workflows.workflow_a import WorkflowA
from workflows.workflow_b import WorkflowB
from workflows.workflow_c import WorkflowC

# Import all activities
from activities.activities import (
    activity_start_workflow_b,
    activity_start_workflow_c,
    call_expensive_api,
)

async def run_worker():
    client = await Client.connect("localhost:7233")
    
    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[WorkflowA, WorkflowB, WorkflowC],
        activities=[
            activity_start_workflow_b,
            activity_start_workflow_c,
            call_expensive_api,
        ]
    )
    
    print("Worker started on task queue 'my-task-queue'...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(run_worker())