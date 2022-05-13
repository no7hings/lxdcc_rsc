# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxresolver.commands as rsv_commands

    import lxmaya.rsv.objects as mya_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if utl_dcc_objects.OsFile(any_scene_file_path).get_is_exists() is True:
            mya_dcc_objects.Scene.set_file_open(any_scene_file_path)
            #
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                with_camera_main_abc = hook_option_opt.get('with_camera_main_abc') or False
                if with_camera_main_abc is True:
                    mya_rsv_objects.RsvDccCameraHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_asset_camera_main_abc_export()
                #
                create_camera_persp_abc = hook_option_opt.get('create_camera_persp_abc') or False
                if create_camera_persp_abc is True:
                    pass
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
