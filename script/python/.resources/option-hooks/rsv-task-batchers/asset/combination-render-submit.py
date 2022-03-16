# coding:utf-8


def main(session):
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxsession.commands as ssn_commands
    #
    import lxresolver.commands as rsv_commands
    #
    option_opt = session.option_opt

    file_path = option_opt.get('file')
    file_ = utl_dcc_objects.OsFile(file_path)
    if file_.get_is_exists() is False:
        raise IOError(
            utl_core.Log.set_module_error_trace(
                'rsv-task-batcher run',
                'file="{}" is non-exists.'.format(file_path)
            )
        )
    #
    r = rsv_commands.get_resolver()
    render_file_path = option_opt.get('render_file')
    rsv_task_properties = r.get_rsv_task_properties_by_any_scene_file_path(render_file_path)
    rsv_task = r.get_rsv_task_by_any_file_path(render_file_path)
    metadata_file_unit = rsv_task.get_rsv_unit(
        keyword='asset-output-render-info-yaml-file'
    )
    metadata_file_path = metadata_file_unit.get_result(
        version=rsv_task_properties.get('version')
    )
    utl_core.File.set_write(
        metadata_file_path, option_opt.get_raw()
    )
    #
    ssn_commands.set_session_option_hooks_execute_by_deadline(
        session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
