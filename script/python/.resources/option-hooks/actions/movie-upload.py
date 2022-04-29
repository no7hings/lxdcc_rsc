# coding:utf-8


def main(session):
    def yes_fnc(qc_rsv_task_, file_path_):
        from lxbasic import bsc_core

        import lxshotgun.rsv.objects as stg_rsv_objects
        #
        _branch = qc_rsv_task_.get('branch')
        _qc_version_rsv_unit = qc_rsv_task_.get_rsv_unit(
            keyword='{}-version-dir'.format(_branch)
        )
        #
        _qc_version = _qc_version_rsv_unit.get_new_version()

        options_kwargs = window.get_options_as_kwargs()
        # _qc_version = 'v001'
        _qc_review_file_rsv_unit = qc_rsv_task_.get_rsv_unit(
            keyword='{}-review-file'.format(_branch)
        )
        _qc_review_file_path = _qc_review_file_rsv_unit.get_result(version=_qc_version)
        #
        utl_dcc_objects.OsFile(file_path_).set_copy_to_file(_qc_review_file_path)
        #
        _qc_stg_rsv_task_opt = stg_rsv_objects.RsvStgTaskOpt(qc_rsv_task_)
        #
        _qc_stg_rsv_task_opt.set_stg_version_create(
            version=_qc_version,
            version_type='daily',
            movie_file=_qc_review_file_path,
            user=bsc_core.SystemMtd.get_user_name(),
            description=options_kwargs['user.description']
        )

    from lxutil import utl_core

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxresolver.commands as rsv_commands

    hook_option_opt = session.option_opt

    r = rsv_commands.get_resolver()
    file_path = hook_option_opt.get('file')
    rsv_task = r.get_rsv_task_by_any_file_path(file_path)
    if rsv_task is not None:
        step = rsv_task.get('step')
        task = rsv_task.get('task')
        rsv_entity = rsv_task.get_rsv_entity()
        qc_rsv_task = rsv_entity.get_rsv_task(
            step='{}_qc'.format(step), task='{}_qc'.format(task)
        )
        if qc_rsv_task is not None:
            window = utl_core.DialogWindow.set_create(
                session.gui_name,
                content=u'upload "{}" to shotgun qc\nentry user description and press "Yes" to continue'.format(file_path),
                status=utl_core.DialogWindow.GuiStatus.Warning,
                #
                yes_method=lambda *args: yes_fnc(qc_rsv_task, file_path),
                use_exec=False,
                options_configure=session.configure.get('build.node.options'),
                window_size=(480, 480)
            )
        else:
            utl_core.DialogWindow.set_create(
                session.gui_name,
                content='"qc task" is non-exists, call for TD get more help',
                status=utl_core.DialogWindow.GuiStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                use_exec=False
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
