# coding:utf-8

def main(session):
    from lxbasic import bsc_core
    #
    directory_path = session.rsv_unit.get_result(
        version='latest'
    )
    if directory_path:
        bsc_core.StoragePathOpt(directory_path).set_open_in_system()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
