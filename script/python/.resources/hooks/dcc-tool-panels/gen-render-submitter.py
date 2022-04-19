# coding:utf-8


def main(session):
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    content = None
    #
    application = session.application
    any_scene_scr_file_path = None
    if application == 'maya':
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        any_scene_scr_file_path = mya_dcc_objects.Scene.get_current_file_path()
    elif application == 'katana':
        import lxkatana.dcc.dcc_objects as ktn_dcc_objects
        any_scene_scr_file_path = ktn_dcc_objects.Scene.get_current_file_path()
    elif application == 'houdini':
        import lxhoudini.dcc.dcc_objects as hou_dcc_objects
        any_scene_scr_file_path = hou_dcc_objects.Scene.get_current_file_path()
    else:
        content = u'application "{}" is not supported'.format(application)
    #
    if any_scene_scr_file_path:
        r = rsv_commands.get_resolver()
        rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(any_scene_scr_file_path)
        if rsv_scene_properties:
            branch = rsv_scene_properties.get('branch')
            step = rsv_scene_properties.get('step')
            #
            import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets
            if branch == 'asset':
                if step in ['mod', 'grm', 'srf']:
                    hook_option = 'file={}'.format(any_scene_scr_file_path)
                    w = utl_pnl_widgets.AssetRenderSubmitter(hook_option=hook_option)
                    w.set_window_show()
                else:
                    content = u'step "{}" is not supported'.format(step)
            elif branch == 'shot':
                if step in ['rlo', 'ani', 'flo']:
                    hook_option = 'file={}'.format(any_scene_scr_file_path)
                    w = utl_pnl_widgets.ShotRenderSubmitter(hook_option=hook_option)
                    w.set_window_show()
                else:
                    content = u'step "{}" is not supported'.format(step)
            else:
                content = u'branch "{}" is not supported'.format(branch)
        else:
            content = u'task file "{}" is not available'.format(any_scene_scr_file_path)
    else:
        content = u'please open a task file.'

    if content is not None:
        utl_core.DialogWindow.set_create(
            session.gui_name,
            content=content,
            status=utl_core.DialogWindow.GuiStatus.Error,
            #
            yes_label='Close',
            #
            no_visible=False, cancel_visible=False
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
