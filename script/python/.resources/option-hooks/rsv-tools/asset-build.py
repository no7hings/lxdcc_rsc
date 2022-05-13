# coding:utf-8


def main(session):
    def build_fnc(project_, asset_):
        import lxmaya.fnc.builders as mya_fnc_builders
        #
        _option = w.get_options_as_kwargs()
        _option['project'] = project_
        _option['asset'] = asset_
        #
        _render_resolution = _option.pop('render.resolution')
        _option['render_resolution'] = _render_resolution
        #
        mya_fnc_builders.AssetBuilder(
            option=_option
        ).set_run()
    #
    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    option_opt = session.option_opt

    project = option_opt.get('project')
    asset = option_opt.get('asset')

    r = rsv_commands.get_resolver()

    content = None
    rsv_entity = r.get_rsv_entity(project=project, asset=asset)
    if rsv_entity:
        w = utl_core.DialogWindow.set_create(
            session.gui_name,
            content=u'build "{}"\npress "Yes" to continue'.format(asset),
            #
            yes_method=lambda *args, **kwargs: build_fnc(project, asset),
            #
            options_configure=session.configure.get('build.node.options'),
            window_size=(480, 480),
            use_exec=False,
            use_thread=False,
        )
    else:
        content = u'"Asset" is non-exists, please call for TD get more help'
    #
    if content is not None:
        utl_core.DialogWindow.set_create(
            session.gui_name,
            content=content,
            status=utl_core.DialogWindow.GuiStatus.Error,
            #
            yes_label='Close',
            #
            no_visible=False, cancel_visible=False,
            use_exec=False
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
