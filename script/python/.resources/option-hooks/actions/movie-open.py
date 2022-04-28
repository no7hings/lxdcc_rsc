# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    from lxutil import utl_core

    hook_option_opt = session.option_opt

    file_path = hook_option_opt.get('file')
    if file_path:
        if bsc_core.SystemMtd.get_is_linux():
            utl_core.RvLauncher().set_file_open(
                file_path
            )
        else:
            bsc_core.SubProcessMtd.set_run_with_result(
                'pgrv "{}"'.format(file_path)
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)