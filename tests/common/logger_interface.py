from abc import ABC, abstractmethod
import logging
from typing import Any, Callable
from pytest import Config, FixtureRequest
from pytest_bdd.parser import Feature, Scenario, Step


class LoggerInterface(ABC):    # TODO rename to BddLoggerInterface
    """
    LoggerInterface is an abstract base class (interface) for loggers
    """

    @abstractmethod
    def configure(self, config: Config) -> None:
        raise NotImplementedError()

    @abstractmethod
    def before_feature(self, _request: FixtureRequest, feature: Feature) -> None:
        raise NotImplementedError()

    @abstractmethod
    def log_context_now(self, the_dict: dict, name: str, prefix: str = '¤') -> None:
        raise NotImplementedError()

    @abstractmethod
    def before_scenario(
        self, _request: FixtureRequest, feature: Feature, scenario: Scenario
    ) -> None:
        raise NotImplementedError()

    def before_step(
        self,
        request: FixtureRequest,
        _feature: Feature,
        scenario: Scenario,
        step: Step,
        step_func: Callable,
    ) -> None:
        raise NotImplementedError()

    # TODO ???:
    # def after_feature(request: FixtureRequest, feature: Feature) -> None:
    # raise NotImplementedError()

    def after_scenario(self, request: FixtureRequest, feature: Feature, scenario: Scenario) -> None:
        raise NotImplementedError()

    def after_step(
        self,
        _request: FixtureRequest,
        _feature: Feature,
        _scenario: Scenario,
        _step: Step,
        _step_func: Callable,
        step_func_args: dict[str, Any],
    ) -> None:
        raise NotImplementedError()

    def log(
        self, msg: str, log_level: int = logging.INFO, pre: str = '', show_caller: bool = False
    ) -> None:
        raise NotImplementedError()
