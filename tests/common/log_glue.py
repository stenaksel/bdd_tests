# content of src/common/log_glue.py
import inspect
import logging

from tests.common.log_glue_incl import (
    COL_GLUE,
    COL_RESET,
    DBG_LOG_PARAMS,
    DO_INCL_CURR_INFO,
    KEY_CONTEXT,
    KEY_CURR_GLUE,
    KEY_DBG_LOG_GLUE,
    KEY_FUNC,
    TEST_CONTEXT,
    ret_dict_info,
    ret_item_info,
    ret_keys,
    ret_sorted,
)


def xlog_glue(**params) -> None:
    """
    Function "log_glue" should be passed all parameters in the glue function.
    The params you pass is a dictionary (**params)

    Example use - glue function with no params:
        def the_glue_func():
    Then to print info about your glue function you write:
        log_glue()
    Example use - glue function with one [or more params]:
        def the_glue_func(parOne [, parTwo, parThree]):
    Then to print info about your glue function you write:
        log_glue(parOne=parOne [, parTwo=parTwo, parThree=parThree])

    Hint: If the glue function is using a "context" param,
          then it it's normally the first param.
    """
    glue_function = inspect.stack()[1][3]
    logging.info('----> Entered log_glue(**params) in %s', glue_function)    # TODO => debug
    logging.info('TEST_CONTEXT:\t%s', ret_sorted(TEST_CONTEXT))

    debug_this = not True
    found_dbg = '?'
    ctx = params.get(KEY_CONTEXT)
    if ctx:
        logging.warning('ctx11:\t%s', ret_dict_info(ctx, 'ctx:\t'))

        debug_this = ctx.get(KEY_DBG_LOG_GLUE, False)
        if debug_this:
            found_dbg = KEY_CONTEXT
            if params.get(KEY_DBG_LOG_GLUE, False):
                found_dbg += '(and in param)'
    else:
        debug_this = params.get(KEY_DBG_LOG_GLUE, False)
        if debug_this:
            found_dbg = 'param'

    if debug_this:
        logging.debug('----> Entered log_glue(**params)')
        logging.info(' -> debug_this=%s', debug_this)    # TODO => debug

    debug_params = params.get(DBG_LOG_PARAMS, False)
    glue_function = inspect.stack()[1][3]

    ret = glue_function + '('
    param_info_ret = '\n'
    # List all params in glue function
    if len(params) > 0:
        ret += ret_keys(params)

    ret += ')'
    ret_func = ret

    logging.warning('TEST_CONTEXT:\t%s', ret_sorted(TEST_CONTEXT))
    ctx = params.get(KEY_CONTEXT)
    if ctx is None:
        logging.debug("(No '%s' in params!)", KEY_CONTEXT)
        ctx = ''    # No need to have "None" logged
    elif DO_INCL_CURR_INFO:
        # TODO Add to context
        # ctx[KEY_CURR_GLUE] = glue_function
        ctx[KEY_CURR_GLUE] = ret    # ret now includes params
        logging.debug('ctx1:\t%s', ret_dict_info(ctx, 'ctx:\t'))
        logging.debug('ctx2:\t%s', ret_dict_info(ret_sorted(ctx), 'ctx:\t'))

    if debug_params:
        # Then show each param below:
        for key, value in params.items():
            if isinstance(value, dict):
                param_info_ret += ret_dict_info(value, key, 'pd:\t')
            else:
                param_info_ret += ret_item_info(key, value, 'p:\t')
        ret += param_info_ret

    if debug_this:
        logging.debug('\t==> log_glue(**params):')
        logging.debug('\t\t%s', ret_dict_info(params, '**params', 'p_____p'))
        logging.debug('\t%s', ret)
        logging.debug('\t%s', '-' * (len(ret)))
        for key, value in params.items():
            logging.debug('dbg*\t%s = %s', key, value)
        logging.debug('dbg5\t%s', '=' * (len(ret)))

    if debug_this:
        logging.debug('<--\t%s', ret)

    if isinstance(ctx, dict):
        if KEY_FUNC in ctx:
            ctx[KEY_FUNC].append(glue_function)
        else:
            ctx[KEY_FUNC] = [glue_function]

    logging.debug('%s%s%s', COL_GLUE, '=' * (len(ret_func) + 2), COL_RESET)
    logging.info('glue: "%s%s%s"\nctx1>', COL_GLUE, ret_func, COL_RESET)
    logging.info(' => %s context: %s)', glue_function, ret_dict_info(ret_sorted(ctx), 'ctx'))
    logging.debug('%s%s%s', COL_GLUE, '=' * (len(ret_func) + 2), COL_RESET)
    logging.info(' "%s%s%s"\nctx2\t%s', COL_GLUE, ret, COL_RESET, ret_sorted(TEST_CONTEXT))
    logging.debug('%s%s%s', COL_GLUE, '=' * (len(ret_func) + 2), COL_RESET)


# pylint: disable=dangerous-default-value
def xlog_glue_end(ctx: dict = {}, print_prefix='<== ') -> None:
    debug_this = ctx.get('dbg_log_glue', True)   # TODO False
    if debug_this:
        logging.debug('----> Entered xlog_glue_end')

    glue_function = inspect.stack()[1][3]
    if ctx is None:
        logging.info('%s%s => (context: N/A)', print_prefix, glue_function)
        logging.info('%s%s => (context: %s)', print_prefix, glue_function, TEST_CONTEXT)
        return
    else:
        logging.info(' => %s context: %s)', glue_function, ctx)
        logging.info(' => %s context: %s)', glue_function, ret_dict_info(ctx, 'ctx'))

    if ctx and ctx.get(KEY_CURR_GLUE, False):
        # then remove "recorded" function in context
        assert ctx.get(KEY_CURR_GLUE, DO_INCL_CURR_INFO), f"Couldn't find {KEY_CURR_GLUE} in {ctx}"
        popped = ctx.pop(KEY_CURR_GLUE, None)
        logging.info(
            'Removed \'%s\' from context (while in "%s%s%s")',
            KEY_CURR_GLUE,
            COL_GLUE,
            popped,
            COL_RESET,
        )
    else:
        logging.info(
            "(Couldn't find %s in %s%s%s: %s)!",
            KEY_CURR_GLUE,
            COL_GLUE,
            KEY_CONTEXT,
            COL_RESET,
            ctx,
        )

    logging.debug(
        '%s%s%s%s => "end" context: %s', print_prefix, COL_GLUE, glue_function, COL_RESET, ctx
    )
