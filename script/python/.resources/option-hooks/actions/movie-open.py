# coding:utf-8


def main(session):
    from lxutil import utl_core
    hook_option_opt = session.option_opt

    file_path = hook_option_opt.get('file')
    if file_path:
        utl_core.RvLauncher().set_file_open(
            file_path
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)