# coding:utf-8


def main(session):
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    application = session.application
    if application == 'maya':
        import lxmaya.dcc.dcc_objects as mya_dcc_objects
        any_scene_scr_file_path = mya_dcc_objects.Scene.get_current_file_path()
    else:
        raise RuntimeError()
    #
    content = None
    if any_scene_scr_file_path:
        r = rsv_commands.get_resolver()
        rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(any_scene_scr_file_path)
        if rsv_scene_properties:
            branch = rsv_scene_properties.get('branch')
            step = rsv_scene_properties.get('step')
            import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets
            if branch == 'asset':
                if step in ['mod', 'grm']:
                    hook_option = 'file={}'.format(any_scene_scr_file_path)
                    w = utl_pnl_widgets.AssetRenderSubmitter(hook_option=hook_option)
                    w.set_window_show()
            elif branch == 'shot':
                if step in ['ani']:
                    hook_option = 'file={}'.format(any_scene_scr_file_path)
                    w = utl_pnl_widgets.ShotRenderSubmitter(hook_option=hook_option)
                    w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
