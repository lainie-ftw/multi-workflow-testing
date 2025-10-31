import asyncio
import uuid
from temporalio.client import Client
from parent_child.parent_workflow import ParentWorkflow
#from weird_aunt.weird_aunt_workflow import WeirdAuntWorkflow
#from service import WeirdAuntInput, WeirdAuntOutput

async def start_workflow():
    client = await Client.connect("localhost:7233")

    #workflowID = "weird-aunt-" + str(uuid.uuid4())
    
    #input = WeirdAuntInput(parent_advice="Always look both ways before crossing the street.")

    #handle = await client.start_workflow(
    #    WeirdAuntWorkflow.run,
    #    input,
    #    id=workflowID,
    #    task_queue="weird-aunt-task-queue"
    #)
    
    #print(f"Started Weird Aunt Workflow: {handle.id}")
    #result = await handle.result()
    #print(f"Final Result: \n{result}")
    
    workflowID = "parent-child-" + str(uuid.uuid4())
    
    input = "Always look both ways before crossing the street."

    handle = await client.start_workflow(
        ParentWorkflow.run,
        input,
        id=workflowID,
        task_queue="parent-child-task-queue"
    )
    
    print(f"Started Parent Workflow: {handle.id}")
    result = await handle.result()
    print(f"Final Result: \n{result}")

if __name__ == "__main__":
    asyncio.run(start_workflow())