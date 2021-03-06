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
                with_shotgun_version = hook_option_opt.get('with_shotgun_version') or False
                if with_shotgun_version is True:
                    rsv_stg_objects.RsvShotgunHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).set_version_export()

                with_link = hook_option_opt.get('with_link') or False
                if with_link is True:
                    rsv_stg_objects.RsvShotgunHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).set_link_export()

                with_shotgun_file = hook_option_opt.get('with_shotgun_file') or False
                if with_shotgun_file is True:
                    rsv_stg_objects.RsvShotgunHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).set_publish_file_export()

                with_shotgun_dependency = hook_option_opt.get('with_shotgun_dependency') or False
                if with_shotgun_dependency is True:
                    rsv_stg_objects.RsvShotgunHookOpt(
                        rsv_scene_properties,
                        hook_option_opt
                    ).set_dependency_export()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
