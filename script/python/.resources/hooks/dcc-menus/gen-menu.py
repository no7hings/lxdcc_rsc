# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxsession.commands as ssn_commands

    from lxutil_gui.qt import utl_gui_qt_core

    configure = session.configure

    application = session.application

    gui_name = session.gui_name
    if session.get_rez_beta() is True:
        gui_name = '[BETA]{}'.format(gui_name)

    if application == 'maya':
        from lxmaya import ma_core, ma_setup
        menu = ma_setup.MayaMenuSetup.get_menu(
            gui_name
        )
        if ma_core._get_is_ui_mode_() is False:
            utl_core.Log.set_module_warning_trace(
                'dcc menu build', 'ignore for "batch" mode'
            )
            return
    elif application == 'katana':
        from lxkatana import ktn_core, ktn_setup
        menu = ktn_setup.KatanaMenuSetup.get_menu(
            gui_name
        )
        if ktn_core._get_is_ui_mode_() is False:
            utl_core.Log.set_module_warning_trace(
                'dcc menu build', 'ignore for "batch" mode'
            )
            return
    else:
        raise NotImplementedError()

    hooks = configure.get('hooks')

    menu_content = ssn_commands.get_menu_content_by_hooks(hooks)

    utl_gui_qt_core.QtMenuOpt(menu).set_create_by_content(
        menu_content
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
