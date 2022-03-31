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
                # texture
                with_texture = hook_option_opt.get('with_texture') or False
                if with_texture is True:
                    mya_rsv_objects.RsvTexture(rsv_scene_properties).set_texture_export(
                        location=root, use_tx=False
                    )
                else:
                    # texture-tx
                    with_texture_tx = hook_option_opt.get('with_texture_tx') or False
                    if with_texture_tx is True:
                        mya_rsv_objects.RsvTexture(rsv_scene_properties).set_texture_export(
                            location=root, use_tx=True
                        )
                # scene
                with_scene = hook_option_opt.get('with_scene') or False
                if with_scene is True:
                    set_scene_export(rsv_task, rsv_scene_properties)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_scene_export(rsv_task, rsv_scene_properties):
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = 'asset-maya-scene-file'
    elif workspace == 'output':
        keyword_0 = 'asset-output-maya-scene-file'
    else:
        raise TypeError()
    #
    maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)
    mya_fnc_exporters.SceneExporter(
        file_path=maya_scene_file_path,
        root=root,
        option=dict(
            with_xgen_collection=True
        )
    ).set_run()
    return maya_scene_file_path


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)