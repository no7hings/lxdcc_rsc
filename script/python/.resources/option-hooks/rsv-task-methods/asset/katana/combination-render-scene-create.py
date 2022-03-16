# coding:utf-8


def main(session):
    import fnmatch

    from lxkatana import ktn_core

    import lxkatana.dcc.dcc_objects as ktn_dcc_objects

    import lxkatana.fnc.creators as ktn_fnc_creators

    hook_option_opt = session.option_opt
    render_file_path = hook_option_opt.get('render_file')
    ktn_dcc_objects.Scene.set_file_save_to(render_file_path)
    ktn_fnc_creators.LookWorkspaceCreator().set_run()

    shot_name = hook_option_opt.get('shot')
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


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
