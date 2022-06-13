# coding:utf-8


def main(session):
    def yes_method():
        for i in assets:
            _i_rsv_task = rsv_project.get_rsv_task(
                asset=i, step='mod', task='modeling'
            )

            i_work_scene_src_rsv_unit = _i_rsv_task.get_rsv_unit(
                keyword='asset-work-maya-scene-src-file'
            )
            i_work_scene_src_file_path = i_work_scene_src_rsv_unit.get_result(
                version='v000'
            )

            _i_option_opt = bsc_core.KeywordArgumentsOpt(
                option=dict(
                    option_hook_key='rsv-task-batchers/asset/gen-prv-render-submit',
                    file=i_work_scene_src_file_path,
                    #
                    td_enable=True,
                    # rez_beta=True,
                )
            )
            #
            ssn_commands.set_option_hook_execute_by_deadline(
                option=_i_option_opt.to_string()
            )

    from lxbasic import bsc_core

    from lxutil import utl_core

    from lxbasic import bsc_configure

    import lxsession.commands as ssn_commands

    rsv_asset = session.rsv_obj

    rsv_project = rsv_asset.get_rsv_project()
    #
    project = rsv_asset.get('project')
    #
    tree_item = rsv_asset.get_obj_gui()
    tree_view = tree_item.get_view()

    all_items = tree_view.get_selected_items()

    assets = []
    for i_item in all_items:
        i_rsv_obj = i_item.get_gui_dcc_obj(namespace='resolver')
        if i_rsv_obj:
            if i_rsv_obj.type_name == 'asset':
                if i_item.get_state() not in [
                    i_item.State.ERROR, i_item.State.WARNING
                ]:
                    assets.append(
                        i_rsv_obj.name
                    )
                else:
                    utl_core.Log.set_module_warning_trace(
                        'asset="{}" is not available'.format(i_rsv_obj)
                    )
    #
    if assets:
        utl_core.DialogWindow.set_create(
            session.gui_name,
            content=(
                'submit selected asset(s) preview render:\n'
                '{}\n'
                'press "Yes" to continue...'
            ).format(
                ',\n'.join(map(lambda x: '"{}"'.format(x), assets))
            ),
            yes_method=yes_method
        )
    else:
        utl_core.DialogWindow.set_create(
            session.gui_name,
            content='no available asset(s) had be selected',
            status=bsc_configure.GuiStatus.Error
        )


# noinspection PyUnresolvedReferences
main(session)
