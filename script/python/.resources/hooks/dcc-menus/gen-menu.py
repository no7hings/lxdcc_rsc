# coding:utf-8


def main(session):
    import lxsession.commands as ssn_commands

    from lxutil_gui.qt import utl_gui_qt_core

    configure = session.configure

    application = session.application
    if application == 'maya':
        from lxmaya import ma_setup
        menu = ma_setup.MayaMenuSetup.get_menu(
            session.gui_name
        )
    elif application == 'katana':
        from lxkatana import ktn_setup
        menu = ktn_setup.KatanaMenuSetup.get_menu(
            session.gui_name
        )
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
