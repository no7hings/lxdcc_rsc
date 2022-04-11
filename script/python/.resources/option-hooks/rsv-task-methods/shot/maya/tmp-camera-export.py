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
                    with_camera_usd = hook_option_opt.get('with_camera_usd') or False
                    if with_camera_usd is True:
                        set_camera_usd_export(rsv_task, rsv_scene_properties, frame_range)
                    # abc
                    with_camera_abc = hook_option_opt.get('with_camera_abc') or False
                    if with_camera_abc is True:
                        set_camera_abc_export(rsv_task, rsv_scene_properties, frame_range)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_camera_usd_export(rsv_task, rsv_scene_properties, frame_range):
    from lxutil import utl_core

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
    #
    utl_core.Log.set_module_result_trace(
        'usd export', 'frame-range="{}-{}"'.format(*frame_range)
    )
    #
    MayaUsdTaskExport.MayaUsdTaskExport(
        version_directory_path,
        None,
        frame_range
    ).camera()


def set_camera_abc_export(rsv_task, rsv_scene_properties, frame_range):
    pass


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
