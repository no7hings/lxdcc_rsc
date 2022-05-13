# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    from lxutil import utl_core

    hook_option_opt = session.option_opt

    project = hook_option_opt.get('project')

    bsc_core.EnvironMtd.set(
        'PG_SHOW', project.upper()
    )
    utl_core.MayaLauncher(
        project=project
    ).set_run()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
