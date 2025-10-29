import os
import uuid
from temporalio import activity
from shared.client import get_temporal_client

@activity.defn
async def random_fun_things_activity(input: str) -> str:
    """Activity that provides random fun things - used by WeirdAuntWorkflow"""
    import random
    fun_things = [
        "Stand on your head!",
        "Eat 1 cookie!",
        "Eat many cookies!",
        "Pester your sibling!"
    ]
    return random.choice(fun_things)