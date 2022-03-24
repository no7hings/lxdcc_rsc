# coding:utf-8


def main(session):
    import lxsession.commands as ssn_commands

    from lxmaya import ma_setup

    from lxutil_gui.qt import utl_gui_qt_core

    configure = session.configure

    hooks = configure.get('hooks')

    menu_content = ssn_commands.get_menu_content_by_hooks(hooks)

    menu = ma_setup.MayaMenuSetup.get_menu(
        session.gui_name
    )
    utl_gui_qt_core.QtMenuOpt(menu).set_create_by_content(
        menu_content
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
