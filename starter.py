import asyncio
import uuid
from temporalio.client import Client
from workflows.workflow_a import WorkflowA

async def start_workflow():
    client = await Client.connect("localhost:7233")

    workflowID = "workflow-a-" + str(uuid.uuid4())
    
    handle = await client.start_workflow(
        WorkflowA.run,
        "Start Workflow A",
        id=workflowID,
        task_queue="my-task-queue"
    )
    
    print(f"Started Workflow A: {handle.id}")
    result = await handle.result()
    print(f"Final Result: \n{result}")

if __name__ == "__main__":
    asyncio.run(start_workflow())