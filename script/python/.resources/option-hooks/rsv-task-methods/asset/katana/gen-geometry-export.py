# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
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
                #
                with_geometry_usd = hook_option_opt.get('with_geometry_usd') or False
                if with_geometry_usd is True:
                    set_geometry_usd_export(rsv_task, rsv_scene_properties)
                #
                with_geometry_uv_map_usd = hook_option_opt.get('with_geometry_uv_map_usd') or False
                if with_geometry_uv_map_usd is True:
                    set_geometry_uv_map_usd_export(rsv_task, rsv_scene_properties)
            else:
                raise RuntimeError
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_geometry_usd_export(rsv_task, rsv_scene_properties):
    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    #
    if workspace == 'work':
        keyword = 'asset-work-geometry-usd-var-file'
    elif workspace == 'publish':
        keyword = 'asset-geometry-usd-var-file'
    elif workspace == 'output':
        keyword = 'asset-output-geometry-usd-var-file'
    else:
        raise TypeError()

    geometry_usd_var_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword
    )
    geometry_usd_var_file_path = geometry_usd_var_file_rsv_unit.get_result(
        version=version, extend_variants=dict(var='hi')
    )
    #
    geometry_uv_map_usd_source_file_path = ktn_dcc_objects.AssetWorkspace().get_geometry_uv_map_usd_source_file()
    if geometry_uv_map_usd_source_file_path:
        utl_dcc_objects.OsFile(geometry_uv_map_usd_source_file_path).set_copy_to_file(
            geometry_usd_var_file_path
        )


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
