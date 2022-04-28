# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.commands as rsv_commands

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if utl_dcc_objects.OsFile(any_scene_file_path).get_is_exists() is True:
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                rsv_task = resolver.get_rsv_task_by_any_file_path(any_scene_file_path)
                root = rsv_scene_properties.get('dcc.root')
                with_version = hook_option_opt.get('with_version') or False
                if with_version is True:
                    pass
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_version_export():
    pass


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
