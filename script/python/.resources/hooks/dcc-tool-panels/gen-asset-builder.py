# coding:utf-8


def main(session):
    from lxutil import utl_core
    #
    content = None
    #
    application = session.application
    if application == 'maya':
        import lxmaya_gui.panel.pnl_widgets as mya_pnl_widgets; mya_pnl_widgets.AssetBuilderPanel().set_window_show()
    else:
        content = u'application "{}" is not supported'.format(application)

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
