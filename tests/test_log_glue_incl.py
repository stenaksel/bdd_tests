import logging
from logging import DEBUG, INFO, WARN, LogRecord
from typing import List
from unittest import mock
from unittest.mock import call, patch

import pytest
from pytest_bdd.parser import Feature, Scenario, ScenarioTemplate, Step

from tests.common.log_glue_incl import (
    # DBG_LOG_PARAMS,
    # KEY_CURR_FEATURE,
    # KEY_DBG_LOG_GLUE,
    TEST_CONTEXT,
    # after_scenario,
    # after_step,
    before_feature,  # tested
    before_scenario,
    # before_step,
    # log_configure,
    log_dict,  # TODO Make test
    log_func_name,  # tested
    # log_func_call_info,
    log_msg,
    log_list,
    log_msg_end,
    log_msg_start,
    ret_before_or_after,
    ret_dict_info,
    ret_func_name,  # tested
    ret_item_info,  # -tested
    ret_keys,
    ret_sorted,  # tested
)

"""
    Many tests here use caplog (CAPtured LOGged messages)
    pytest caplog is a built-in fixture provided by the pytest
    testing framework in Python.
    It is used for capturing and inspecting log messages during test execution.
    The caplog fixture allows you to access log records generated by your code
    under test, making it easier to assert and analyze log output in your tests.

    When you use the caplog fixture in your test function or test method,
    pytest captures all log messages emitted by the code being tested.
    You can then access these log records through the caplog.records attribute.
"""


def _the_caller0() -> str:
    return ret_func_name()


def _the_caller(prev: int = 0) -> str:
    return ret_func_name(prev)


def _func1(prev: int = 1) -> str:
    return _the_caller(prev)


def _func2(prev: int = 2) -> str:
    return _func1(prev)


def _func3(prev: int = 3) -> str:
    # _func3: _func2 -> _func1 -> _the_caller
    return _func2(prev)


def test_just_show_test_context():
    logging.info('==> test_just_show_test_context')
    logging.info('TEST_CONTEXT: ')
    logging.info(TEST_CONTEXT)
    logging.info('<== test_just_show_test_context')


def test_ret_func_name():

    logging.info('==> test_ret_func_name')

    assert ret_func_name() == 'test_ret_func_name'
    # The different _func have a default "prev" param
    # that will be passed on to _the_caller and should return themself
    # _the_caller is the only function calling ret_func_name function.

    assert _the_caller0() == '_the_caller0'   # a caller of the ret_func_name()
    assert _the_caller() == '_the_caller'   # _the_caller of ret_func_name
    assert _func1() == '_func1'             # will only call _the_caller
    assert _func2() == '_func2'             # will only call _func1
    assert _func3() == '_func3'             # will only call _func2
    assert _func3(3) == '_func3'            # will only call _func2(prev=3)
    assert _func3(2) == '_func2'            # will only call _func2(prev=2)
    assert _func3(1) == '_func1'            # will only call _func2(prev=1)
    assert _func3(0) == '_the_caller'       # will only call _func2(prev=0)

    # log_msg_end()
    logging.info('<== test_ret_func_name')


def test_ret_func_name():
    this_file = '?'
    print(__file__)
    with mock.patch('tests.common.log_glue_incl.logging') as mock_logger:
        this_file = ret_func_name()
        mock_logger.debug.assert_called_once_with('>> ret_func_name')

    assert this_file == 'test_ret_func_name'


def test_ret_sorted():
    some_dict = {'c': 'C', 'a': 'A', 'b': 'B'}
    correct_dict = {'a': 'A', 'b': 'B', 'c': 'C'}
    some_keys = ret_keys(some_dict)
    print(some_dict)
    print(some_keys)
    sorted_dict = ret_sorted(some_dict)
    sorted_keys = ret_keys(sorted_dict)
    print(some_dict)
    print(some_keys)
    print(sorted_dict)
    print(sorted_keys)
    assert sorted_dict == correct_dict, 'The sort is NOT right'
    assert ret_keys(sorted_dict) == ret_keys(correct_dict), 'The sort is NOT right'


@pytest.mark.ok
def test_ret_dict_info():
    some_dict = {'a': 'A', 'b': 'B', 'c': 'C'}
    ret = ret_dict_info(some_dict, 'the name', '-prefix-')
    print(ret)
    assert 'the name' in ret
    assert ': [dict] (#=3)' in ret
    assert '-prefix-' in ret
    assert '-prefix- the name' in ret
    assert 'the name       : [dict] (#=3)' in ret
    assert '-prefix- the name       : [dict] (#=3)' in ret


def test_ret_before_or_after():

    with pytest.raises(AssertionError) as excinfo:
        ret_before_or_after(None)
    assert str(excinfo.value) == 'No param "func_name"'
    with pytest.raises(AssertionError) as excinfo:
        ret_before_or_after('')
    assert str(excinfo.value) == 'No param "func_name"'
    # with pytest.raises(AssertionError) as excinfo:
    #     ret_before_or_after('before-or-after')
    # assert str(excinfo.value) == 'No _ char found in "func_name". (Expects _)'

    assert 'Before' == ret_before_or_after('before_')
    assert 'Before' == ret_before_or_after('beforehand')
    assert 'Before' == ret_before_or_after('before_some_text')
    assert 'Before' == ret_before_or_after('beforesometext')
    assert 'Before' == ret_before_or_after('some_text_before')
    assert 'Before' == ret_before_or_after('sometextbefore')
    assert 'After' == ret_before_or_after('after')
    assert 'After' == ret_before_or_after('after_some_text')
    assert 'After' == ret_before_or_after('some_text_after')
    assert 'After' == ret_before_or_after('hereafterlife')


def _clear_caplog(caplog):
    """
    Function used in test to clear the caplog log while running the test.
    """
    # Clear the captured log records and formatted log output
    caplog.clear()

    # Assert that the log is cleared
    assert len(caplog.records) == 0
    assert caplog.text == ''


def _is_increasing_sequence(lst):
    for i in range(len(lst) - 1):
        if lst[i] >= lst[i + 1]:
            return False
    return True


def _assert_messages(caplog, level, messages: List, in_sequence: bool = False):
    print('#### messages:')
    for msg in messages:
        print(msg)
    # Access the captured log records based on log level
    filtered_records = [record for record in caplog.records if record.levelno == level]
    messages_found = []
    lines: List[int] = []
    rest = messages.copy()

    for record in filtered_records:
        assert isinstance(record, logging.LogRecord)
        # Inspect and assert the log records as needed
        for msg in rest:
            assert record.levelno == level, f'record.levelname = {record.levelname}'
            if msg in record.message:
                print('\nSeeked&found: ' + msg)
                messages_found += [msg]
                lines += [record.lineno]
                # print('#### found messages:')
                # print(messages_found)
                break
            else:
                print("\n Didn't find: " + msg)

            print('#### found message lines:')
            print(lines)
            #
        #
        print('#### rest messages before:')
        print(rest)
        print('#### messages_found messages before:')
        print(messages_found)
        rest = [message for message in rest if message not in messages_found]
        # print('#### found messages:')
        # print(messages_found)
        print('#### rest messages after:')
        print(rest)
    #

    # print('#### rest messages (in end):')
    print(rest)
    level_name = logging.getLevelName(level)
    assert len(rest) == 0, f"Couldn't find wanted {level_name} log messages: {rest}"
    assert not rest, f"Couldn't find wanted {level_name} log messages: {rest}"


@pytest.mark.ok
def test_log_func_name_caplog(caplog):
    assert caplog, '*** No caplog param! ***'
    # Background:
    # Given a function (that log messages):
    #  def log_func_name(prev: int = 0, inRow: bool = True, fillchar: str = '#')
    #####################################
    # When called with an empty fillchar
    with pytest.raises(AssertionError) as assert_msg:
        log_func_name(inRow=False, fillchar=None)
    assert str(assert_msg.value) == 'No fillchar! (Got: None)'
    # Then I will get an assert
    #####################################
    # When called with an empty fillchar, length != 1
    with pytest.raises(AssertionError) as assert_msg:
        log_func_name(inRow=False, fillchar='')
    assert str(assert_msg.value) == "No fillchar! (Got '' <- empty)"
    #####################################
    # When called with a fillchar sting that is not a char (length != 1)
    with pytest.raises(AssertionError) as assert_msg:
        log_func_name(inRow=False, fillchar='***')
    assert str(assert_msg.value) == "No fillchar! (Got '***')"
    # Then I will get an assert

    # When called without a fillchar
    _clear_caplog(caplog)
    log_func_name(inRow=False)
    # Then I will see that the log uses the default fillchar
    expeced = [
        '#' * 75,
        f'  {ret_func_name()}  '.center(75, '#'),
        '#' * 75,
        # 'Not find'
    ]

    _assert_messages(caplog, level=INFO, messages=expeced, in_sequence=True)

    # When called with an empty fillchar
    _clear_caplog(caplog)

    # Then I will get an assert

    _clear_caplog(caplog)
    # When called with a non-default fillchar
    plus = '+'
    # Then I will see that the log uses that fillchar instead of the default
    log_func_name(inRow=False, fillchar=plus)
    # Then I will see that the log uses the wanted fillchar ('+')
    expeced = [f'  {ret_func_name()}  '.center(75, plus)]
    _assert_messages(caplog, level=INFO, messages=expeced)


@pytest.mark.ok
def test_log_func_name_logging():
    assert ret_func_name() == 'test_log_func_name_logging'
    fillchar = '#'

    with patch('logging.info') as mock_info:
        log_func_name(inRow=False, fillchar=fillchar)
        # Assert that the mock_info was called 3 times with the expected arguments
        # mock_info.assert_has_calls([
        mock_info.assert_has_calls(
            [
                call('%s', fillchar * 75),
                call('%s', '  test_log_func_name_logging  '.center(75, fillchar)),
                call('%s', fillchar * 75),
            ]
        )



@pytest.mark.skip
def test_log_msg_start():

    with patch('logging.info') as mock_info:
        fillchar = '¤'
        log_msg_start()
        # Assert that the mock_info was called 3 times with the expected arguments
        # mock_info.assert_has_calls([
        mock_info.assert_has_calls(
            [
                # call('%s', fillchar * 75),
                call('%s', '  test_log_func_name_logging  '.center(75, fillchar)),
                # call('%s', fillchar * 75),
            ]
        )


@pytest.fixture
def feature_mock(mocker):
    # Create a mock object for the ExternalService class
    mock_service = mocker.Mock()
    # Set the return value for the get_data() method
    mock_service.get_data.return_value = 'Mocked data'
    return mock_service


# @mock.patch('tests.common.log_glue_incl.log_msg_start')
# @mock.patch('tests.common.log_glue_incl.log_msg')
# @mock.patch('tests.common.log_glue_incl.log_feature')
# @mock.patch('tests.common.log_glue_incl.log_msg_end')


@pytest.mark.ok
def test_before_feature():
    #### No feature
    with pytest.raises(AssertionError) as assert_msg:
        before_feature(None, None)
    assert str(assert_msg.value) == 'No feature param!'
    #### Empty feature name
    feature = Feature(None, '', '', '', set(), None, 1, '')
    assert feature.name == ''
    with pytest.raises(AssertionError) as assert_msg:
        before_feature(None, feature)
        assert str(assert_msg.value) == 'Feature unknown!'
    # ####

    feature = Feature(None, '', '', 'Feature_name', set(), None, 1, '')
    # feature = Feature(
    #     {'scenario.name'}, 'filename', 'rel_filename', 'Feature_name', set(), None, 1, 'descr.'
    # )
    # scenario = Scenario(feature, '', 11, None, None)
    # #### Assert functions called
    module = 'tests.common.log_glue_incl'
    with patch(module + '.log_msg_start') as mock_log_msg_start, patch(
        module + '.log_feature'
    ) as mock_log_feature, patch(module + '.log_msg_end') as mock_log_msg_end:
        # When I call
        logging.info('When I call: before_feature(None, feature)')
        before_feature(None, feature)

        # Then assert that the mocked functions were called
        logging.info('Then assert that the mocked functions were called')
        mock_log_msg_start.assert_called_once()
        mock_log_feature.assert_called_once()
        mock_log_msg_end.assert_called_once()


@pytest.mark.wipz
def test_before_feature_2():
    feature = Feature(None, '', '', 'Feature_name', set(), None, 1, '')
    logging.info('-> Created feature with name "%s"', feature.name)

    # #### Assert functions called
    module = 'tests.common.log_glue_incl'
    with patch(f'{module}.log_msg_start') as mock_log_msg_start, patch(
        f'{module}.log_feature'
    ) as mock_log_feature, patch(f'{module}.log_msg_end') as mock_log_msg_end:
        # When I call
        logging.info('When I call: before_feature(None, feature)')
        before_feature(None, feature)

        # Then assert that the mocked functions were called
        logging.info('Then assert that the mocked functions were called')
        mock_log_msg_start.assert_called_once()
        # mock_log_feature.assert_called_once()
        mock_log_msg_end.assert_called_once()
        # And expect sequence of calls:
        logging.info('And expect sequence of calls:')
        expected_calls = [
            # call.log_msg('Found feature: '),  #
            # call.log_msg('Found feature: '),  #
            call.log_msg_start(),  #
            # call.log_feature(feature),  #
            # # call.log_feature(),  #
            call.log_msg_end(),  #
        ]
        # expected_calls:
        for func in expected_calls:
            logging.info('  %s', func)
        mock_log_msg_end.assert_has_calls(expected_calls)


@pytest.mark.skip   # TODO Not working yet
def test_log_msg():
    with patch('logging.info') as mock_info:
        log_msg('Testing')

        # Assert that the mock_info was called times with the expected arguments
        mock_info.assert_has_calls(
            [
                call('%s', '#' * 75),
                call('%s', '  test_log_func_name  '.center(75, '#')),
                call('%s', '#' * 75),
            ]
        )


@pytest.mark.wipz
def test_log_func_name():
    with patch('logging.info') as mock_info:
        log_func_name(inRow=True)

        # Assert that the mock_info was called times with the expected arguments
        mock_info.assert_has_calls(
            [
                call('%s', '#' * 75),
                call('%s', '  test_log_func_name  '.center(75, '#')),
                call('%s', '#' * 75),
            ]
        )
