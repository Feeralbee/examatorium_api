from typing import Any, AsyncGenerator

from di import ScopeState
from didiator import Mediator
from didiator.interface.utils.di_builder import DiBuilder
from fastapi import Depends

from application.dependencies import get_di_state, get_mediator
from application.dependencies.mediator import get_di_builder


class MediatorProvider:
    def __init__(self, mediator: Mediator) -> None:
        self._mediator = mediator

    async def build(self, di_state: ScopeState = Depends(get_di_state)) -> Mediator:
        di_values: dict[Any, Any] = {ScopeState: di_state}
        mediator = self._mediator.bind(di_state=di_state, di_values=di_values)
        di_values |= {get_mediator: mediator}
        return mediator


class StateProvider:
    def __init__(self, di_state: ScopeState | None = None):
        self._di_state = di_state

    async def build(
            self,
            di_builder: DiBuilder = Depends(get_di_builder),
    ) -> AsyncGenerator[ScopeState, None]:
        async with di_builder.enter_scope("request", self._di_state) as di_state:
            yield di_state
