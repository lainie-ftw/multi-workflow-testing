import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

# Import all workflows
from parent_child.parent_workflow import ParentWorkflow
from parent_child.child_workflow import ChildWorkflow

# Import Nexus service handler
from weird_aunt.service_handler import WeirdAuntNexusServiceHandler

# TODO: make this versioned
# TODO: understand wtf this is doing: https://github.com/temporalio/samples-python/blob/main/hello_nexus/caller/app.py

async def run_worker():
    client = await Client.connect("localhost:7233")
    
    # This worker manages ParentWorkflow, ChildWorkflow, and allows ChildWorkflow to call out to WeirdAuntWorkflow via Nexus. Currently there are no activities.
    worker = Worker(
        client,
        task_queue="parent-child-task-queue",
        workflows=[ParentWorkflow, ChildWorkflow],
        nexus_service_handlers=[WeirdAuntNexusServiceHandler],
    )
    
    print("Parent and Child worker started on parent-child-task-queue'...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(run_worker())