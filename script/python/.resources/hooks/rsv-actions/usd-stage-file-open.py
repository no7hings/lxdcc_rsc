# coding:utf-8


def main(session):
    from lxutil import utl_core
    #
    file_path = session.rsv_unit.get_result(
        version='latest'
    )
    #
    if file_path:
        project = session.variants['project']
        #
        app_launcher = utl_core.UsdViewLauncher(
            project=project
        )
        app_launcher.set_file_open(
            file_path
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
