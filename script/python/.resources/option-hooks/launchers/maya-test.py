# coding:utf-8


def main(session):
    from lxutil import utl_core
    #
    hook_option_opt = session.option_opt

    cmd = hook_option_opt.get('cmd')
    #
    utl_core.SubProcessRunner.set_run_with_result_use_thread(
        cmd
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
