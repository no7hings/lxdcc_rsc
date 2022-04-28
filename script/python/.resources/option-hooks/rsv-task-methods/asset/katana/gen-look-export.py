# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxkatana.dcc.dcc_objects as ktn_dcc_objects

    import lxkatana.rsv.objects as ktn_rsv_objects
    #
    import lxresolver.commands as rsv_commands

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if utl_dcc_objects.OsFile(any_scene_file_path).get_is_exists() is True:
            ktn_dcc_objects.Scene.set_file_open(any_scene_file_path)
            #
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                rsv_task = resolver.get_rsv_task_by_any_file_path(any_scene_file_path)
                # texture
                with_texture = hook_option_opt.get('with_texture') or False
                if with_texture is True:
                    ktn_rsv_objects.RsvDccTextureHookOpt(rsv_scene_properties).set_texture_export(
                        use_tx=False
                    )
                else:
                    # texture-tx
                    with_texture_tx = hook_option_opt.get('with_texture_tx') or False
                    if with_texture_tx is True:
                        ktn_rsv_objects.RsvDccTextureHookOpt(rsv_scene_properties).set_texture_export(
                            use_tx=True
                        )
                #
                with_look_klf = hook_option_opt.get('with_look_klf') or False
                if with_look_klf is True:
                    set_look_klf_export(rsv_task, rsv_scene_properties)
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


def set_look_klf_export(rsv_task, rsv_scene_properties):
    import lxkatana.fnc.builders as ktn_fnc_builders
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    #
    if workspace == 'publish':
        keyword = 'asset-look-klf-file'
    elif workspace == 'output':
        keyword = 'asset-output-look-klf-file'
    else:
        raise TypeError()
    #
    look_klf_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword
    )
    look_klf_file_path = look_klf_file_rsv_unit.get_result(
        version=version
    )
    asset_workspace = ktn_dcc_objects.AssetWorkspace()
    #
    ktn_dcc_objects.Node('rootNode').get_port('variables.camera').set('asset_free')
    #
    asset_geometries = ktn_dcc_objects.Node('asset__geometries')
    if asset_geometries.get_is_exists() is True:
        asset_geometries.get_port('lynxi_variants.look').set('asset-work')
    #
    asset_workspace.set_look_klf_file_export(look_klf_file_path)


def set_look_ass_export(rsv_task, rsv_scene_properties, force=False):
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxkatana.fnc.exporters as ktn_fnc_exporters
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = 'asset-look-ass-file'
        keyword_1 = 'asset-look-ass-sub-file'
    elif workspace == 'output':
        keyword_0 = 'asset-output-look-ass-file'
        keyword_1 = 'asset-output-look-ass-sub-file'
    else:
        raise TypeError()
    ktn_workspace = ktn_dcc_objects.AssetWorkspace()
    look_pass_names = ktn_workspace.get_look_pass_names()
    #
    for i_look_pass_name in look_pass_names:
        if i_look_pass_name == 'default':
            i_look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
            i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(version=version)
        else:
            i_look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_1)
            i_look_ass_file_path = i_look_ass_file_rsv_unit.get_result(
                version=version, extend_variants=dict(look_pass=i_look_pass_name)
            )
        #
        i_look_ass_file = utl_dcc_objects.OsFile(i_look_ass_file_path)
        if i_look_ass_file.get_is_exists() is False or force is True:
            i_look_pass_source_obj = ktn_workspace.get_pass_source_obj(i_look_pass_name)
            if i_look_pass_source_obj is not None:
                ktn_fnc_exporters.LookAssExporter(
                    file_path=i_look_ass_file_path,
                    root=root,
                    option=dict(
                        output_obj=i_look_pass_source_obj.path
                    )
                ).set_run()
        else:
            utl_core.Log.set_module_warning_trace(
                'look-ass export',
                u'file="{}" is exists'.format(i_look_ass_file_path)
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
