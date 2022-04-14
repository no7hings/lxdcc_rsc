# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects
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

                with_scene_create = hook_option_opt.get('with_scene_create') or False
                if with_scene_create is True:
                    set_scene_create(rsv_task, rsv_scene_properties, hook_option_opt)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_scene_create(rsv_task, rsv_scene_properties, hook_option_opt):
    import fnmatch

    from lxkatana import ktn_core

    import lxkatana.dcc.dcc_objects as ktn_dcc_objects

    import lxkatana.fnc.creators as ktn_fnc_creators
    #
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = 'asset-katana-scene-file'
    elif workspace == 'output':
        keyword_0 = 'asset-output-katana-scene-file'
    else:
        raise TypeError()

    katana_scene_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    katana_scene_file_path = katana_scene_file_rsv_unit.get_result(version=version)

    render_file_path = katana_scene_file_path
    ktn_dcc_objects.Scene.set_file_save_to(render_file_path)
    # create workspace
    ktn_fnc_creators.LookWorkspaceCreator().set_run()
    #
    set_white_disp_create(rsv_task, rsv_scene_properties)
    #
    shot_name = hook_option_opt.get('shot')
    if shot_name:
        shot_geometries_node_opt = ktn_core.NGObjOpt('shot__geometries')
        shot_paths = shot_geometries_node_opt.get_as_enumerate('options.shot')
        _ = fnmatch.filter(shot_paths, '*/{}'.format(shot_name))
        if _:
            shot_geometries_node_opt.set('options.shot', _[0])
        shot_geometries_node_opt.set_port_execute('usd.create')

    render_settings_node_opt = ktn_core.NGObjOpt('render_settings')
    render_output_directory_path = hook_option_opt.get('render_output_directory')
    render_output_file_path = '{}/main/<camera>.<layer>.<light-pass>.<look-pass>.<quality>/<render-pass>.####.exr'.format(
        render_output_directory_path
    )
    render_settings_node_opt.set(
        'lynxi_settings.render_output', render_output_file_path
    )
    #
    renderer_node_opt = ktn_core.NGObjOpt('render_outputs')

    variable_keys = [
        'cameras',
        'layers',
        'light_passes',
        'look_passes',
        'qualities',
    ]
    for i_variable_key in variable_keys:
        renderer_node_opt.set(
            'lynxi_variants.{}'.format(i_variable_key),
            ', '.join(hook_option_opt.get(i_variable_key, as_array=True))
        )

    renderer_node_opt.set_port_execute('create')
    ktn_dcc_objects.Scene.set_file_save()


def set_white_disp_create(rsv_task, rsv_scene_properties):
    import lxkatana.fnc.importers as ktn_fnc_importers

    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')

    if workspace == 'publish':
        keyword_0 = 'asset-look-ass-file'
    elif workspace == 'output':
        keyword_0 = 'asset-output-look-ass-file'
    else:
        raise TypeError()

    look_ass_file_rsv_unit = rsv_task.get_rsv_unit(keyword=keyword_0)
    look_ass_file_path = look_ass_file_rsv_unit.get_exists_result(version=version)
    if look_ass_file_path:
        ktn_fnc_importers.LookAssImporter(
            option=dict(
                file=look_ass_file_path,
                auto_white_disp_assign=True,
                look_pass='white_disp'
            )
        ).set_run()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
