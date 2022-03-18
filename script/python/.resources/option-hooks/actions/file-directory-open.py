# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    hook_option_opt = session.option_opt

    file_path = hook_option_opt.get('file')
    if file_path:
        bsc_core.StorageFileOpt(
            file_path
        ).set_open_in_system()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
