# coding:utf-8


def main(session):
    from lxutil import utl_core
    #
    utl_core.SubProcessRunner.set_run_with_result(
        'rez-env lxdcc mtoa maya-2019 maya_usd-0.6.0 aces-1.2 -- maya'
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
