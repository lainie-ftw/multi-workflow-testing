from temporalio import workflow
from datetime import timedelta

from parent_child.child_workflow import ChildWorkflow

@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, advice: str) -> str:

        # Start ChildWorkflow as a child, passing along the advice
        child_result = await workflow.execute_child_workflow(
            ChildWorkflow.run,
            advice,
        )
          
        return f"Parent's advice: {advice}. Feedback received from Child: {child_result}."