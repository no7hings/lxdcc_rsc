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
                rsv_task = resolver.get_rsv_task_by_any_file_path(any_scene_file_path)
                root = rsv_scene_properties.get('dcc.root')
                refresh_root_property = hook_option_opt.get('refresh_root_property') or False
                if refresh_root_property:
                    mya_rsv_objects.RsvDccSceneHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_asset_root_property_refresh()
                # texture
                with_texture = hook_option_opt.get('with_texture') or False
                if with_texture is True:
                    mya_rsv_objects.RsvDccTextureHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_texture_export(
                        location=root,
                        use_tx=False
                    )
                else:
                    # texture-tx
                    with_texture_tx = hook_option_opt.get('with_texture_tx') or False
                    if with_texture_tx is True:
                        mya_rsv_objects.RsvDccTextureHookOpt(
                            rsv_scene_properties,
                            hook_option_opt,
                        ).set_texture_export(
                            location=root,
                            use_tx=True
                        )
                # scene
                with_scene = hook_option_opt.get('with_scene') or False
                if with_scene is True:
                    mya_rsv_objects.RsvDccSceneHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_asset_scene_export()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
