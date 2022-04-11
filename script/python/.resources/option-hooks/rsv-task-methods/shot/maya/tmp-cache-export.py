# coding:utf-8


def main(session):
    from lxbasic import bsc_core
    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxresolver.commands as rsv_commands

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
                    keyword_0 = '{branch}-maya-scene-file'
                elif workspace == 'output':
                    keyword_0 = '{branch}-output-maya-scene-file'
                else:
                    raise TypeError()
                #
                cache_frames = hook_option_opt.get('cache_frames')
                frame_range = bsc_core.TextOpt(cache_frames).to_frame_range()
                #
                keyword_0 = keyword_0.format(**rsv_scene_properties.value)
                maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
                maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)
                if bsc_core.StoragePathOpt(maya_scene_file_path).get_is_exists() is True:
                    mya_dcc_objects.Scene.set_file_open(maya_scene_file_path)
                    # usd
                    with_geometry_usd = hook_option_opt.get('with_geometry_usd') or False
                    if with_geometry_usd is True:
                        set_geometry_usd_export(rsv_task, rsv_scene_properties, frame_range)
                    # abc
                    with_geometry_abc = hook_option_opt.get('with_geometry_abc') or False
                    if with_geometry_abc is True:
                        set_geometry_abc_export(rsv_task, rsv_scene_properties, frame_range)
                    #
                    with_override_usd = hook_option_opt.get('with_override_usd') or False
                    if with_override_usd is True:
                        set_override_usd_export(rsv_task, rsv_scene_properties, frame_range)
                    #
                    with_component_usd = hook_option_opt.get('with_component_usd') or False
                    if with_component_usd is True:
                        set_component_usd_export(rsv_task, rsv_scene_properties, frame_range)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_geometry_usd_export(rsv_task, rsv_scene_properties, frame_range):
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = '{branch}-version-dir'
    elif workspace == 'output':
        keyword_0 = '{branch}-output-version-dir'
    else:
        raise TypeError()
    #
    keyword_0 = keyword_0.format(**rsv_scene_properties.value)
    version_directory_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    version_directory_path = version_directory_rsv_unit.get_result(version=version)
    # noinspection PyUnresolvedReferences
    from papyUsd.maya import MayaUsdTaskExport

    for i in MayaUsdTaskExport.mayaRefRootDagPaths():
        MayaUsdTaskExport.MayaUsdTaskExport(version_directory_path, None, frame_range).cacheFile(i, True)

    MayaUsdTaskExport.MayaUsdTaskExport(version_directory_path, None, frame_range).subBranches(True)


def set_geometry_usd_export_(rsv_task, rsv_scene_properties, frame_range):
    from lxbasic import bsc_core

    import lxbasic.objects as bsc_objects

    from lxutil import utl_core

    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = '{branch}-maya-scene-file'
        keyword_1 = '{branch}-version-dir'
    elif workspace == 'output':
        keyword_0 = '{branch}-output-maya-scene-file'
        keyword_1 = '{branch}-output-version-dir'
    else:
        raise TypeError()
    #
    keyword_0 = keyword_0.format(**rsv_scene_properties.value)
    maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)
    #
    keyword_1 = keyword_1.format(**rsv_scene_properties.value)
    version_directory_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_1
    )
    version_directory_path = version_directory_rsv_unit.get_result(version=version)

    test_directory_path = '/l/temp/shanshui/pg_repo/zero_test/ani_temp_tool/anim_farm'
    test_directory = utl_dcc_objects.OsDirectory_(test_directory_path)
    if test_directory.get_is_exists() is True:
        bsc_core.EnvironMtd.set_python_add(
            test_directory_path
        )
        py_module = bsc_objects.PyModule('do_save_ani_maya_file_0')
        if py_module.get_is_exists():
            # noinspection PyUnresolvedReferences
            import do_save_ani_maya_file_0
            #
            # do_save_ani_maya_file_0.export_usd_cmd(maya_scene_file_path)
        else:
            raise RuntimeError(
                utl_core.Log.set_error_trace(
                    'python-module="{}"'
                )
            )
    else:
        raise RuntimeError(
            utl_core.Log.set_error_trace(
                'directory="{}" is non-exists'.format(test_directory_path)
            )
        )


def set_geometry_abc_export(rsv_task, rsv_scene_properties, frame_range):
    from lxbasic import bsc_core

    import lxbasic.objects as bsc_objects

    from lxutil import utl_core

    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = '{branch}-maya-scene-file'
        keyword_1 = '{branch}-version-dir'
    elif workspace == 'output':
        keyword_0 = '{branch}-output-maya-scene-file'
        keyword_1 = '{branch}-output-version-dir'
    else:
        raise TypeError()
    #
    keyword_0 = keyword_0.format(**rsv_scene_properties.value)
    maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)
    #
    keyword_1 = keyword_1.format(**rsv_scene_properties.value)
    version_directory_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_1
    )
    version_directory_path = version_directory_rsv_unit.get_result(version=version)

    test_directory_path = '/l/temp/shanshui/pg_repo/zero_test/ani_temp_tool/anim_farm'
    test_directory = utl_dcc_objects.OsDirectory_(test_directory_path)
    if test_directory.get_is_exists() is True:
        bsc_core.EnvironMtd.set_python_add(
            test_directory_path
        )
        py_module = bsc_objects.PyModule('do_save_ani_maya_file_0')
        if py_module.get_is_exists():
            # noinspection PyUnresolvedReferences
            import do_save_ani_maya_file_0
            #
            # do_save_ani_maya_file_0.export_usd_cmd(maya_scene_file_path)
        else:
            raise RuntimeError(
                utl_core.Log.set_error_trace(
                    'python-module="{}"'
                )
            )
    else:
        raise RuntimeError(
            utl_core.Log.set_error_trace(
                'directory="{}" is non-exists'.format(test_directory_path)
            )
        )


def set_override_usd_export(rsv_task, rsv_scene_properties, frame_range):
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = '{branch}-version-dir'
    elif workspace == 'output':
        keyword_0 = '{branch}-output-version-dir'
    else:
        raise TypeError()
    #
    keyword_0 = keyword_0.format(**rsv_scene_properties.value)
    version_directory_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    version_directory_path = version_directory_rsv_unit.get_result(version=version)
    frame_samples = None
    frame_range = None
    # noinspection PyUnresolvedReferences
    from papyUsd.maya import MayaUsdTaskExport

    MayaUsdTaskExport.MayaUsdTaskExport(version_directory_path, None, frame_range).subBranches(True)

    MayaUsdTaskExport.MayaUsdTaskExport(version_directory_path, None, frame_range).cacheOver('|assets')
    MayaUsdTaskExport.MayaUsdTaskExport(version_directory_path, None, frame_range).refOver('|assets')
    MayaUsdTaskExport.MayaUsdTaskExport(version_directory_path, None, frame_range).editOver('|assets')
    MayaUsdTaskExport.MayaUsdTaskExport(version_directory_path, None, frame_range).customAttrOver('|assets')


def set_component_usd_export(rsv_task, rsv_scene_properties, frame_range):
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = '{branch}-version-dir'
    elif workspace == 'output':
        keyword_0 = '{branch}-output-version-dir'
    else:
        raise TypeError()
    #
    keyword_0 = keyword_0.format(**rsv_scene_properties.value)
    version_directory_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    version_directory_path = version_directory_rsv_unit.get_result(version=version)
    # noinspection PyUnresolvedReferences
    from papyUsd.maya import MayaUsdTaskExport

    MayaUsdTaskExport.MayaUsdTaskExport(version_directory_path, None, frame_range).sceneGraph('|assets')
    #
    MayaUsdTaskExport.MayaUsdTaskExport(version_directory_path, None, frame_range).shotIndexFile()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
