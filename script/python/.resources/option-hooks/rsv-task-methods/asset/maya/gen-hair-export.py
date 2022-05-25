# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxresolver.commands as rsv_commands
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    cmds.stackTrace(state=1)

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if utl_dcc_objects.OsFile(any_scene_file_path).get_is_exists() is True:
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                rsv_task = resolver.get_rsv_task_by_any_file_path(any_scene_file_path)
                workspace = rsv_scene_properties.get('workspace')
                version = rsv_scene_properties.get('version')
                if workspace == 'publish':
                    keyword_0 = 'asset-maya-scene-file'
                elif workspace == 'output':
                    keyword_0 = 'asset-output-maya-scene-file'
                else:
                    raise TypeError()
                #
                maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
                maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)
                if bsc_core.StoragePathOpt(maya_scene_file_path).get_is_exists() is True:
                    mya_dcc_objects.Scene.set_file_open(maya_scene_file_path)
                    #
                    with_hair_xgen = hook_option_opt.get('with_hair_xgen') or False
                    if with_hair_xgen is True:
                        set_hair_xgen_export(rsv_task, rsv_scene_properties)
                    # cache/usd/xgen.usda
                    with_hair_xgen_usd = hook_option_opt.get('with_hair_xgen_usd') or False
                    if with_hair_xgen_usd is True:
                        set_hair_xgen_usd_export(rsv_task, rsv_scene_properties)
                else:
                    raise RuntimeError()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_hair_xgen_export(rsv_task, rsv_scene_properties):
    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxmaya.dcc.dcc_objects as mya_dcc_objects

    import lxmaya.fnc.exporters as mya_fnc_exporters

    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    pathsep = rsv_scene_properties.get('dcc.pathsep')
    location = '{}/hair'.format(root)
    mya_location = mya_dcc_objects.Group(
        bsc_core.DccPathDagOpt(location).set_translate_to(
            pathsep
        ).to_string()
    )
    if mya_location.get_is_exists() is True:
        if workspace == 'publish':
            keyword_0 = 'asset-version-dir'
            keyword_1 = 'asset-geometry-xgen-collection-dir'
            keyword_2 = 'asset-geometry-xgen-glow-dir'
        elif workspace == 'output':
            keyword_0 = 'asset-output-version-dir'
            keyword_1 = 'asset-output-geometry-xgen-collection-dir'
            keyword_2 = 'asset-output-geometry-xgen-glow-dir'
        else:
            raise TypeError()

        version_directory_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
        version_directory_path = version_directory_rsv_unit.get_result(version=version)

        xgen_collection_directory_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_1)
        xgen_collection_directory_path = xgen_collection_directory_rsv_unit.get_result(version=version)

        grow_mesh_directory_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_2)
        grow_mesh_directory_path = grow_mesh_directory_rsv_unit.get_result(version=version)
        #
        mya_fnc_exporters.XgenExporter(
            option=dict(
                xgen_project_directory=version_directory_path,
                xgen_collection_directory=xgen_collection_directory_path,
                grow_mesh_directory=grow_mesh_directory_path,
                #
                location=location,
                #
                with_xgen_collection=True,
                with_grow_mesh_abc=True,
            )
        ).set_run()
    else:
        raise RuntimeError(
            utl_core.Log.set_module_error_trace(
                'xgen export',
                u'obj="{}" is non-exists'.format(mya_location.path)
            )
        )


def set_hair_xgen_usd_export(rsv_task, rsv_scene_properties):
    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxmaya.dcc.dcc_objects as mya_dcc_objects

    import lxutil.fnc.exporters as utl_fnc_exporters

    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    pathsep = rsv_scene_properties.get('dcc.pathsep')
    location = '{}/hair'.format(root)

    mya_location = mya_dcc_objects.Group(
        bsc_core.DccPathDagOpt(location).set_translate_to(
            pathsep
        ).to_string()
    )
    if mya_location.get_is_exists() is True:
        if workspace == 'publish':
            keyword_0 = 'asset-maya-scene-file'
            keyword_1 = 'asset-xgen-usd-file'
        elif workspace == 'output':
            keyword_0 = 'asset-output-maya-scene-file'
            keyword_1 = 'asset-output-xgen-usd-file'
        else:
            raise TypeError()

        xgen_usd_file_rsv_unit = rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        xgen_usd_file_path = xgen_usd_file_rsv_unit.get_result(
            version=version
        )
        maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
        maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)

        utl_fnc_exporters.DotXgenUsdaExporter(
            dict(
                file=xgen_usd_file_path,
                location=location,
                maya_scene_file=maya_scene_file_path,
            )
        ).set_run()
    else:
        raise RuntimeError(
            utl_core.Log.set_module_error_trace(
                'xgen export',
                u'obj="{}" is non-exists'.format(mya_location.path)
            )
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
