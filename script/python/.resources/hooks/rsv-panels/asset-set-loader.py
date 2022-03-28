# coding:utf-8


def main(session):
    from lxutil_gui.qt import utl_gui_qt_core

    import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

    utl_gui_qt_core.set_window_show_standalone(
        utl_pnl_widgets.RsvEntitiesLoader, session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
