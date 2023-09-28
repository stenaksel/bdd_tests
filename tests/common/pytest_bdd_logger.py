
from tests.common.pytest_bdd_tracer import PytestBddTracer
from pytest_bdd.parser import Feature #, Scenario, ScenarioTemplate, Step

class PytestBddLogger(PytestBddTracer):
    """
    PytestBddLogger is a class for logging Pytest BDD testing.
    It implements needed abstract PytestBddTracer methods.
    #TODO: You may pass a False value to the constructor to disable "context logging".
    """
    #TODO: You may pass a False value to the constructor to disable "context logging".

    def __init__(self, show_context: bool = True):
        super().__init__(show_context)
        #TODO self.show_context = show_context

    def log_feature(self, feature: Feature) -> None:
        super().log_feature(feature)
        self.log_func_name(msg=feature.name, fillchar='@')
        self.log(f'\t {self.COL_MSG}Feature: "{feature.name}"')
        # logging.info(
        #     f'%sFeature: "%s" %s',
        #     self.COL_MSG,
        #     feature.name,
        #     self.ret_context_info(1)
        # )
        # ret_context = self.get_context_info()
