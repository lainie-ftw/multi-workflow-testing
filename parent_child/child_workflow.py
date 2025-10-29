from temporalio import workflow
from datetime import timedelta

with workflow.unsafe.imports_passed_through():
    from service import WeirdAuntInput, WeirdAuntOutput, WeirdAuntNexusService

# The child gets advice from the parent and then asks the weird aunt what she thinks (via Nexus). Returns the weird aunt's advice back to the parent.
@workflow.defn
class ChildWorkflow:

    # An __init__ method is always optional on a workflow class. Here we use it to set the
    # nexus client, but that could alternatively be done in the run method.
    def __init__(self):
        self.nexus_client = workflow.create_nexus_client(
            service=WeirdAuntNexusService,
            endpoint="weird-aunt-endpoint",
        )

    @workflow.run
    async def run(self, advice: str) -> str:

        # Ask the weird aunt what she thinks about the advice from the parent via Nexus
        aunt_result = await self.nexus_client.execute_operation(
            WeirdAuntNexusService.workflow_run_operation,
            WeirdAuntInput(advice),
        )


        return aunt_result.aunt_advice