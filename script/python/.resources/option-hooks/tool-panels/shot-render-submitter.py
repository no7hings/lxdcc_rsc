# coding:utf-8


def main(session):
    from lxusd import usd_setup

    usd_setup.UsdSetup.set_environs_setup()

    from lxutil_gui.qt import utl_gui_qt_core

    option_opt = session.option_opt

    import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

    utl_gui_qt_core.set_window_show_standalone(
        utl_pnl_widgets.ShotRenderSubmitter, hook_option=option_opt.to_string()
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
