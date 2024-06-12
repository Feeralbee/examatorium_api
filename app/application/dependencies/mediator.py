from di import ScopeState
from didiator import MediatorImpl
from didiator.interface.utils.di_builder import DiBuilder
from didiator.utils.di_builder import DiBuilderImpl
from fastapi import Depends

from application.constants import DIScopes


def get_di_state():
    pass


def get_mediator():
    pass


def get_di_builder() -> DiBuilder:
    pass


def get_di_state_override(di_builder: DiBuilderImpl):
    async def _get_di_state():
        async with di_builder.enter_scope(DIScopes.request) as di_state:
            yield di_state

    return _get_di_state


def get_mediator_override(mediator: MediatorImpl) -> MediatorImpl:
    def _get_mediator(di_state: ScopeState = Depends(get_di_state)):
        yield mediator.bind(di_state=di_state)

    return _get_mediator
