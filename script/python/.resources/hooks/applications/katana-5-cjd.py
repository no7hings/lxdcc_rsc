# coding:utf-8


def main(session):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    bsc_core.EnvironMtd.set(
        'PG_SHOW', 'CJD'
    )
    utl_core.KatanaLauncher(
        project='cjd'
    ).set_run()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
