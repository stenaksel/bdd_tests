# bdd_tests

Is a project to learn Pytest-BDD

---

Built with help from AI tools:

* [You.com](https://you.com)
* [Codeium.com](https://codeium.com)

## Classes

```mermaid

---
title: Class hierarchy showing log related classes
---
classDiagram

    note for PytestBddLogger "Wanted logger for Pytest BDD testing.\nIt implements all inherited abstract methods."

    PytestBddLoggerInterface <|-- PytestBddTracer
    PytestBddTracer <|-- PytestBddLogger

    class LogHelper {
        ret_func_name(prev: int = 0)
        ret_provider_info
        ret_keys
        ret_dict_info
        ret_item_info
        ret_sorted
        log_func_call(log_level: int = logging.INFO)
        log_func_name(prev: int = 0, informative=True)
        log(msg: str, log_level: int = logging.INFO, pre: str = '', show_caller: bool = False)
        log_func_name(prev: int = 0, fillchar: str = None, msg: str = '')
        log_dict_now
        log_headline
    }


    class PytestBddLoggerInterface {
        <<abstract>>
        Constants:
        KEY_CURR_FEATURE = 'Current feature'
        COL_INFO = ANSIColor.BLUE
        COL_MSG = ANSIColor.CYAN
        COL_RESET = ANSIColor.RESET
        COL_SCENARIO = ANSIColor.YELLOW
        COL_STEP = ANSIColor.GREEN
        COL_CONTEXT = ANSIColor.GRAY

        +log_hook()*
        +configure(config: Config)

        +before_feature(request: FixtureRequest, feature: Feature)*
        +before_scenario(request: FixtureRequest, feature: Feature, scenario: Scenario)*
        +before_step(request: FixtureRequest, _feature: Feature, _scenario: Scenario, _step: Step)*

        +after_feature(request: FixtureRequest, feature: Feature)*
        +after_scenario(request: FixtureRequest, feature: Feature, scenario: Scenario)*
        +after_step(request: FixtureRequest, feature: Feature, scenario: Scenario, step: Step)*

        +log(msg: str, log_level: int = logging.INFO, pre: str = '', show_caller: bool = False)*
        +log_func_name(prev: int = 0, fillchar: str = None, msg: str = '')*
    }

    class PytestBddTracer {
        <<abstract>>
        -show_context: bool = True
        +log_feature(feature: Feature)*
        +log_scenario(scenario: Scenario)*
        +before_feature(request: FixtureRequest, feature: Feature)
        +before_scenario(request: FixtureRequest, feature: Feature, scenario: Scenario)
        +before_step(request: FixtureRequest, _feature: Feature, _scenario: Scenario, _step: Step)

        +after_feature(request: FixtureRequest, feature: Feature)
        +after_scenario(request: FixtureRequest, feature: Feature, scenario: Scenario)
        +after_step(request: FixtureRequest, feature: Feature, scenario: Scenario, step: Step)

    }

    class PytestBddLogger {
        -show_context: bool = True
        +log_feature(feature: Feature)
        +log_scenario(scenario: Scenario) TODO
    }

    class ANSIColor {
        <<enumeration>>
        RESET
        BLACK
        RED
        GREEN
        YELLOW
        BLUE
        MAGENTA
        CYAN
        WHITE
        GRAY
    }

```

<!-- ```mermaid

---

title: Animal example

---
classDiagram
    note "From Duck till Zebra"
    Animal <|-- Duck
    note for Duck "can fly\ncan swim\ncan dive\ncan help in debugging"
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
        +String beakColor
        +swim()
        +quack()
    }
    class Fish{
        -int sizeInFeet
        -canEat()
    }
    class Zebra{
        +bool is_wild
        +run()
    }
``` -->
