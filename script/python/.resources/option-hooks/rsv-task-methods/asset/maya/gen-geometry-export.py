# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxresolver.commands as rsv_commands

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
                #
                with_geometry_usd = hook_option_opt.get('with_geometry_usd') or False
                if with_geometry_usd is True:
                    set_geometry_usd_export(rsv_task, rsv_scene_properties)
                #
                with_geometry_uv_map_usd = hook_option_opt.get('with_geometry_uv_map_usd') or False
                if with_geometry_uv_map_usd is True:
                    set_geometry_uv_map_usd_export(rsv_task, rsv_scene_properties)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_geometry_usd_export(rsv_task, rsv_scene_properties):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxobj.core_objects as core_objects
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    from lxmaya import ma_configure
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    mya_root_dat_opt = bsc_core.DccPathDagOpt(root).set_translate_to(
        pathsep='|'
    )
    mya_root = mya_dcc_objects.Group(
        mya_root_dat_opt.get_value()
    )
    if mya_root.get_is_exists() is True:
        if workspace == 'work':
            keyword = 'asset-work-geometry-usd-var-file'
        elif workspace == 'publish':
            keyword = 'asset-geometry-usd-var-file'
        elif workspace == 'output':
            keyword = 'asset-output-geometry-usd-var-file'
        else:
            raise TypeError()
        # location_names = [i.name for i in mya_root.get_children()]
        # use white list
        location_names = ['hi', 'shape', 'hair']
        with utl_core.gui_progress(maximum=len(location_names)) as g_p:
            for i_location_name in location_names:
                g_p.set_update()
                #
                i_geometry_usd_var_file_rsv_unit = rsv_task.get_rsv_unit(
                    keyword=keyword
                )
                i_geometry_usd_var_file_path = i_geometry_usd_var_file_rsv_unit.get_result(
                    version=version, extend_variants=dict(var=i_location_name)
                )
                #
                i_location = '{}/{}'.format(root, i_location_name)
                i_sub_root_dag_path = core_objects.ObjDagPath(i_location)
                i_mya_sub_root_dag_path = i_sub_root_dag_path.set_translate_to(
                    pathsep=ma_configure.Util.OBJ_PATHSEP
                )
                #
                sub_root_mya_obj = mya_dcc_objects.Group(i_mya_sub_root_dag_path.path)
                if sub_root_mya_obj.get_is_exists() is True:
                    mya_fnc_exporters.GeometryUsdExporter_(
                        file_path=i_geometry_usd_var_file_path,
                        root=i_location,
                        option=dict(
                            default_prim_path=root,
                            with_uv=True,
                            with_mesh=True,
                            use_override=False
                        )
                    ).set_run()


def set_geometry_uv_map_usd_export(rsv_task, rsv_scene_properties):
    from lxbasic import bsc_core

    import lxusd.fnc.exporters as usd_fnc_exporters
    #
    step = rsv_scene_properties.get('step')
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'work':
        keyword_0 = 'asset-work-geometry-usd-var-file'
        keyword_1 = 'asset-work-geometry-uv_map-usd-file'
    elif workspace == 'publish':
        keyword_0 = 'asset-geometry-usd-var-file'
        keyword_1 = 'asset-geometry-uv_map-usd-file'
    elif workspace == 'output':
        keyword_0 = 'asset-output-geometry-usd-var-file'
        keyword_1 = 'asset-output-geometry-uv_map-usd-file'
    else:
        raise TypeError()
    #
    geometry_usd_hi_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    geometry_usd_var_file_path = geometry_usd_hi_file_rsv_unit.get_exists_result(
        version=version, extend_variants=dict(var='hi')
    )
    if geometry_usd_var_file_path:
        geometry_uv_map_usd_file_rsv_unit = rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        geometry_uv_map_usd_file_path = geometry_uv_map_usd_file_rsv_unit.get_result(
            version=version
        )
        usd_fnc_exporters.GeometryUvMapExporter(
            file_path=geometry_uv_map_usd_file_path,
            root=root,
            option=dict(
                file_0=geometry_usd_var_file_path,
                file_1=geometry_usd_var_file_path,
                display_color=bsc_core.TextOpt(step).to_rgb(maximum=1.0)
            )
        ).set_run()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
