# coding:utf-8


def main(session):
    import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets
    file_path = session.rsv_unit.get_result(
        version='latest'
    )
    if file_path:
        hook_option = 'file={}'.format(file_path)
        w = utl_pnl_widgets.AssetRenderSubmitter(option=hook_option)
        w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
