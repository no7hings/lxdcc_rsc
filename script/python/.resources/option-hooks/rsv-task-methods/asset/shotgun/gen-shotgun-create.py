# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.commands as rsv_commands

    import lxshotgun.rsv.objects as rsv_stg_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if utl_dcc_objects.OsFile(any_scene_file_path).get_is_exists() is True:
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                #
                create_shotgun_task = hook_option_opt.get('create_shotgun_task') or False
                if create_shotgun_task is True:
                    rsv_stg_objects.RsvShotgunHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).set_task_create()

                create_shotgun_version = hook_option_opt.get('create_shotgun_version') or False
                if create_shotgun_version is True:
                    rsv_stg_objects.RsvShotgunHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).set_version_create()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
