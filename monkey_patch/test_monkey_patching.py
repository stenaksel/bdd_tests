import inspect

import pytest
from pytest_bdd import given


def ret_dict_info(the_dict: dict, name: str, prefix: str = '::') -> str:
    """
    Function ret_dict_info returns a string with info
    about the named dictionary and its content
        Param 1: name: str
        Param 2: it: dict
    """
    assert isinstance(the_dict, dict), 'A dict was not given!'
    the_length = '--EMPTY!'
    if the_dict:
        the_length = len(the_dict)
    caller: str = inspect.stack()[1][3]

    ret = f'{prefix} {name:<15}: [dict] (#={the_length}) (<< "{caller}")\n\n'

    ret += ret_item_info('____key____', '____value____', '____')
    for key, value in ret_sorted(the_dict).items():
        ret += ret_item_info(key, value)

    return '\x1b[90m' + ret + '\x1b[0m'


def ret_item_info(name: str, item, prefix: str = 'i') -> str:
    """
    Function ret_item_info returns a string with info
    about the named item, its type and its content
        Param 1: name: str
        Param 2: item
    """
    item_type = f'[{type(item).__name__}]'
    if len(prefix) > 0 and prefix[0] == 'p':   # p => param
        return f'{prefix}\t{name:<20} : {item_type:>10}: {item}\n'
    else:
        return f'{prefix}\t{name.rjust(20, " ")} : {item_type:>10}: {item}\n'
        # return f'{prefix}{name:>20} : {item_type:>10}: {item}\n'


@given('I have a step with glue code')
def step_with_glue_code(*args, **kwargs):
    return 'Original glue code'


def test_my_monkeypatch(monkeypatch):

    print('Calling original function: ')
    result = step_with_glue_code(None, None)
    print(result)

    def replacement_function(*args, **kwargs):
        for key, value in kwargs.items():
            print(ret_item_info(key, value))

        return 'Patched glue code'

    module_name = inspect.getmodule(step_with_glue_code).__name__
    # print('module_name: ')
    # print(module_name)

    function_name = 'step_with_glue_code'

    # Create a callable object from the function name using eval()
    # callable_object = eval(step_with_glue_code)
    callable_object = eval(function_name)
    sig = inspect.signature(callable_object)

    # Get the parameters of the original function
    params = sig.parameters
    print(callable_object(**params))

    the_path = module_name + '.step_with_glue_code'
    print('the_path: ')
    print(the_path)
    print('\n"Monkey patching": ' + the_path)
    monkeypatch.setattr(the_path, replacement_function)
    # Get the signature of the original function
    # sig = inspect.signature(the_path)

    print(ret_dict_info(param, 'params'))

    print('Calling original function again: ')
    # Test code that calls the glue code function
    result = step_with_glue_code(None, params)
    print(result)

    assert result == 'Patched glue code'
