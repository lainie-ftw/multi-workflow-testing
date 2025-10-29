
"""
This is a Nexus service definition.

A service definition defines a Nexus service as a named collection of operations, each
with input and output types.

A Nexus service definition is used by Nexus callers (e.g. a Temporal workflow) to create
type-safe clients, and it is used by Nexus handlers to validate that they implement
correctly-named operation handlers with the correct input and output types.

The service defined in this file exposes one operation - workflow_run_operation.
"""

from dataclasses import dataclass

import nexusrpc


@dataclass
class WeirdAuntInput:
    parent_advice: str


@dataclass
class WeirdAuntOutput:
    aunt_advice: str


@nexusrpc.service
class WeirdAuntNexusService:
    workflow_run_operation: nexusrpc.Operation[WeirdAuntInput, WeirdAuntOutput]
