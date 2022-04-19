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
    hook_option_opt = session.option_opt

    file_path = hook_option_opt.get('file')
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
    choice_scheme = hook_option_opt.get('choice_scheme')
    if bsc_core.TextOpt(choice_scheme).get_filter_by_pattern('shot-*-output'):
        # pre export use workspace: "output"
        scene_src_file_path_tgt = rsv_application.get_output_scene_src_file(
            version_scheme='new'
        )
    elif bsc_core.TextOpt(choice_scheme).get_filter_by_pattern('shot-*-custom'):
        scene_src_file_path_tgt = file_path
    else:
        raise RuntimeError(
            utl_core.Log.set_error_trace(
                'choice scheme="{}" is not available'.format(choice_scheme)
            )
        )

    if scene_src_file_path_tgt:
        hook_option_opt.set(
            'file', scene_src_file_path_tgt
        )
    else:
        raise RuntimeError()
    #
    ssn_commands.set_session_option_hooks_execute_by_deadline(
        session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
