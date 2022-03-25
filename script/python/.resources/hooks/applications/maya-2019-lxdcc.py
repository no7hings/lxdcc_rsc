# coding:utf-8


def main(session):
    from lxutil import utl_core
    #
    utl_core.SubProcessRunner.set_run_with_result_use_thread(
        'rez-env lxdcc usd mtoa maya-2019 aces-1.2 -- maya'
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
