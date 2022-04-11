# coding:utf-8


def main(session):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxutil.ssn.objects as utl_ssn_objects
    #
    import lxsession.commands as ssn_commands
    #
    option_opt = session.option_opt

    file_path = option_opt.get('file')

    file_ = utl_dcc_objects.OsFile(file_path)
    if file_.get_is_exists() is False:
        raise IOError(
            utl_core.Log.set_module_error_trace(
                'option-hook execute',
                u'file="{}" is non-exists.'.format(file_path)
            )
        )

    bsc_core.EnvironMtd.set(
        'RSV_SCENE_FILE', file_path
    )

    rsv_application = utl_ssn_objects.SsnRsvApplication()

    scene_src_file_path = rsv_application.get_scene_src_file()

    if scene_src_file_path:
        option_opt.set(
            'file', scene_src_file_path
        )
    #
    ssn_commands.set_session_option_hooks_execute_by_deadline(
        session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
