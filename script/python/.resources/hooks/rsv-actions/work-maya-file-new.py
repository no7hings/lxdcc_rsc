# coding:utf-8


def main(session):
    from lxutil import utl_core
    #
    rsv_task = session.rsv_obj
    #
    rsv_unit = rsv_task.get_rsv_unit(
        keyword='{branch}-work-maya-scene-src-file'.format(
            **session.variants
        )
    )
    #
    file_path = rsv_unit.get_result(
        version='new'
    )
    #
    project = session.variants['project']
    #
    app_launcher = utl_core.MayaLauncher(
        project=project
    )
    app_launcher.set_file_new(
        file_path
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)

