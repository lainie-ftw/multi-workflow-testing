import asyncio
import logging
from typing import Optional
from temporalio.client import Client
from temporalio.worker import Worker

# Import all workflows
from weird_aunt.weird_aunt_workflow import WeirdAuntWorkflow

# Import all activities
from activities.activities import random_fun_things_activity

# Import Nexus service handler
from weird_aunt.service_handler import WeirdAuntNexusServiceHandler

interrupt_event = asyncio.Event()

# TODO: make this versioned

async def main(client: Optional[Client] = None):
    client = client or await Client.connect("localhost:7233")
    
    async with Worker(
        client,
        task_queue="weird-aunt-task-queue",
        workflows=[WeirdAuntWorkflow],
        nexus_service_handlers=[WeirdAuntNexusServiceHandler()],
        activities=[
            random_fun_things_activity,
        ]
    ): 
        logging.info("Weird Aunt Worker started on task queue 'weird-aunt-task-queue'...")
        await interrupt_event.wait()
        logging.info("Shutting donw.")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())