from __future__ import annotations

import uuid

import nexusrpc
from temporalio import nexus

from service import WeirdAuntInput, WeirdAuntNexusService, WeirdAuntOutput
from weird_aunt.weird_aunt_workflow import WeirdAuntWorkflow

@nexusrpc.handler.service_handler(service=WeirdAuntNexusService)
class WeirdAuntNexusServiceHandler:
    # You can create an __init__ method accepting what is needed by your operation
    # handlers to handle requests. You typically instantiate your service handler class
    # when starting your worker. See hello_nexus/basic/handler/worker.py.

    # This is a nexus operation that is backed by a Temporal workflow. The start method
    # starts a workflow, and returns a nexus operation token. Meanwhile, the workflow
    # executes in the background; Temporal server takes care of delivering the eventual
    # workflow result (success or failure) to the calling workflow.
    #
    # The token will be used by the caller if it subsequently wants to cancel the Nexus
    # operation.
    @nexus.workflow_run_operation
    async def workflow_run_operation(
        self, ctx: nexus.WorkflowRunOperationContext, input: WeirdAuntInput
    ) -> nexus.WorkflowHandle[WeirdAuntOutput]:
        return await ctx.start_workflow(
            WeirdAuntWorkflow.run,
            input,
            id=str(uuid.uuid4()),
        )