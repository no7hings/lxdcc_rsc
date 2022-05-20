# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    from lxutil import utl_core

    hook_option_opt = session.option_opt

    project = hook_option_opt.get('project')
    use_as_launcher = hook_option_opt.get('use_as_launcher')
    if use_as_launcher is True:
        bsc_core.EnvironMtd.set(
            'PG_SHOW', project.upper()
        )
        utl_core.KatanaLauncher(
            project=project
        ).set_run()

    use_as_graph = hook_option_opt.get('use_as_graph')
    if use_as_graph is True:
        from lxutil_gui.qt import utl_gui_qt_core

        import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

        _option_opt = bsc_core.KeywordArgumentsOpt(
            option=dict(
                option_hook_key='tool-panels/rez-graph',
                packages=utl_core.KatanaLauncher(
                    project=project
                ).get_rez_packages()
            )
        )

        utl_gui_qt_core.set_window_show_standalone(
            utl_pnl_widgets.RezGraph,
            hook_option=_option_opt.to_string()
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
