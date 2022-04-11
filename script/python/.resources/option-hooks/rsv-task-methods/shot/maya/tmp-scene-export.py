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
    from lxbasic import bsc_core

    import lxbasic.objects as bsc_objects

    from lxutil import utl_core

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = '{branch}-maya-scene-file'
    elif workspace == 'output':
        keyword_0 = '{branch}-output-maya-scene-file'
    else:
        raise TypeError()
    #
    keyword_0 = keyword_0.format(**rsv_scene_properties.value)
    #
    maya_scene_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    maya_scene_file_path = maya_scene_file_rsv_unit.get_result(version=version)

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
            do_save_ani_maya_file_0.save_pub_maya_cmd(maya_scene_file_path)

            mya_dcc_objects.Scene.set_file_save_to(maya_scene_file_path)
            #
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


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
