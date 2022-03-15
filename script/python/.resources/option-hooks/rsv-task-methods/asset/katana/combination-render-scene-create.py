# coding:utf-8


def main(session):
    from lxkatana import ktn_core

    import lxkatana.dcc.dcc_objects as ktn_dcc_objects

    import lxkatana.fnc.creators as ktn_fnc_creators

    option_opt = session.option_opt

    render_file_path = option_opt.get('render_file')

    ktn_dcc_objects.Scene.set_file_save_to(render_file_path)

    ktn_fnc_creators.LookWorkspaceCreator().set_run()

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
            ', '.join(option_opt.get(i_variable_key, as_array=True))
        )

    renderer_node_opt.set_port_execute('create')

    ktn_dcc_objects.Scene.set_file_save()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
