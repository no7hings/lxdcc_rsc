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
                    mya_rsv_objects.RsvDccTextureHookOpt(rsv_scene_properties).set_texture_export(
                        location=root, use_tx=False
                    )
                else:
                    # texture-tx
                    with_texture_tx = hook_option_opt.get('with_texture_tx') or False
                    if with_texture_tx is True:
                        mya_rsv_objects.RsvDccTextureHookOpt(rsv_scene_properties).set_texture_export(
                            location=root, use_tx=True
                        )
                #
                with_look_ass = hook_option_opt.get('with_look_ass') or False
                if with_look_ass is True:
                    set_look_ass_export(rsv_task, rsv_scene_properties)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_look_ass_export(rsv_task, rsv_scene_properties):
    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxmaya.fnc.exporters as mya_fnc_exporters

    import lxmaya.dcc.dcc_objects as mya_dcc_objects

    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    pathsep = rsv_scene_properties.get('dcc.pathsep')

    if workspace == 'publish':
        keyword_0 = 'asset-look-ass-file'
        keyword_1 = 'asset-look-ass-sub-file'
    elif workspace == 'output':
        keyword_0 = 'asset-output-look-ass-file'
        keyword_1 = 'asset-output-look-ass-sub-file'
    else:
        raise TypeError()

    root_dag_opt = bsc_core.DccPathDagOpt(root)
    mya_root_dag_opt = root_dag_opt.set_translate_to(pathsep)
    mya_root = mya_dcc_objects.Group(mya_root_dag_opt.value)
    if mya_root.get_is_exists() is True:
        _look_pass_names = mya_root.get_port('pg_lookpass').get_enumerate_strings() or None
        if _look_pass_names is not None:
            look_pass_names = _look_pass_names
        else:
            look_pass_names = ['default']
        # sequence-file(s) export per frame
        start_frame, end_frame = (
            mya_root.get_port('pg_start_frame').get(),
            mya_root.get_port('pg_end_frame').get()
        )
        # export per look-pass
        for i_look_pass_name in look_pass_names:
            mya_root.get_port('pg_lookpass').set(i_look_pass_name)
            if i_look_pass_name == 'default':
                i_look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
                i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(version=version)
            else:
                i_look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_1)
                i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(
                    version=version, extend_variants=dict(look_pass=i_look_pass_name)
                )
            # main-file(s)
            i_look_ass_file = utl_dcc_objects.OsFile(i_look_ass_file_path)
            if i_look_ass_file.get_is_exists() is False:
                mya_fnc_exporters.LookAssExporter(
                    file_path=i_look_ass_file_path,
                    root=root
                ).set_run()
            else:
                utl_core.Log.set_module_warning_trace(
                    'look-ass export',
                    u'file="{}" is exists'.format(i_look_ass_file_path)
                )
            #
            if start_frame is not None and end_frame is not None:
                i_frame = start_frame, end_frame
                #
                mya_fnc_exporters.LookAssExporter(
                    file_path=i_look_ass_file_path,
                    root=root,
                    frame=i_frame
                ).set_run()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
