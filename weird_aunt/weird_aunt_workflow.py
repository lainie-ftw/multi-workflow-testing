from temporalio import workflow
from datetime import timedelta

from activities.activities import random_fun_things_activity
from service import WeirdAuntInput, WeirdAuntOutput

# The weird aunt is called via Nexus - related, but not directly, to ParentWorkflow or ChildWorkflow. She generally gives only fun advice.
@workflow.defn
class WeirdAuntWorkflow:
    @workflow.run
    async def run(self, input: WeirdAuntInput) -> WeirdAuntOutput:

        # Get some fun advice
        result = await workflow.execute_activity(
            random_fun_things_activity,
            input,
            start_to_close_timeout=timedelta(seconds=60)
        )

        output = WeirdAuntOutput(aunt_advice=result)
        return output