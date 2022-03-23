# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    bsc_core.EnvironMtd.set_add(
        'PXR_AR_DEFAULT_SEARCH_PATH',
        bsc_core.StoragePathMtd.set_map_to_platform('/l/prod')
    )

    from lxutil_gui.qt import utl_gui_qt_core

    option_opt = session.option_opt

    import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

    utl_gui_qt_core.set_window_show_standalone(
        utl_pnl_widgets.ShotRenderSubmitter, hook_option=option_opt.to_string()
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
