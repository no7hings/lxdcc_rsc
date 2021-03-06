# coding:utf-8


def main(session):
    def create_and_publish_fnc_(file_path_):
        _rez_beta = session.get_rez_beta()
        _td_enable = session.get_td_enable()
        _option_opt = bsc_core.KeywordArgumentsOpt(
            option=dict(
                option_hook_key='rsv-task-batchers/asset/gen-camera-export',
                choice_scheme='asset-maya-create-and-publish',
                #
                file=file_path_,
                #
                td_enable=_td_enable,
                rez_beta=_rez_beta,
            )
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=_option_opt.to_string()
        )
    #
    def publish_fnc_(file_path_):
        _rez_beta = session.get_rez_beta()
        _td_enable = session.get_td_enable()
        _option_opt = bsc_core.KeywordArgumentsOpt(
            option=dict(
                option_hook_key='rsv-task-batchers/asset/gen-camera-export',
                choice_scheme='asset-maya-publish',
                #
                file=file_path_,
                #
                td_enable=_td_enable,
                rez_beta=_rez_beta,
            )
        )
        #
        ssn_commands.set_option_hook_execute_by_deadline(
            option=_option_opt.to_string()
        )
    #
    from lxbasic import bsc_core
    #
    from lxutil import utl_core

    import lxsession.commands as ssn_commands

    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    option_opt = session.option_opt

    project = option_opt.get('project')
    asset = option_opt.get('asset')
    content = None
    rsv_entity = r.get_rsv_entity(project=project, asset=asset)
    if rsv_entity:
        camera_rsv_task = rsv_entity.get_rsv_task(
            step='cam', task='camera'
        )
        model_rsv_task = rsv_entity.get_rsv_task(
            step='mod', task='modeling'
        )
        #
        if camera_rsv_task is not None:
            camera_work_scene_src_file_rsv_unit = camera_rsv_task.get_rsv_unit(
                keyword='asset-work-maya-scene-src-file'
            )
            camera_work_scene_src_file_path = camera_work_scene_src_file_rsv_unit.get_result(
                version='latest'
            )
            if camera_work_scene_src_file_path:
                camera_scene_src_file_rsv_unit = camera_rsv_task.get_rsv_unit(
                    keyword='asset-maya-scene-src-file'
                )
                camera_scene_src_file_path = camera_scene_src_file_rsv_unit.get_result(
                    version='latest'
                )
                if bsc_core.StorageFileOpt(
                    camera_work_scene_src_file_path
                ).get_is_same_timestamp_to(camera_scene_src_file_path) is False:
                    utl_core.DialogWindow.set_create(
                        session.gui_name,
                        content=(
                            u'publish "Asset Camera" for "{}"\n'
                            u'press "Yes" to continue...'
                        ).format(asset),
                        yes_method=lambda *args, **kwargs: publish_fnc_(camera_work_scene_src_file_path),
                        use_exec=False
                    )
                else:
                    content = u'"Asset Camera Work Scene-src" is non-changed'
            else:
                if model_rsv_task is not None:
                    geometry_usd_var_rsv_unit = model_rsv_task.get_rsv_unit(
                        keyword='asset-geometry-usd-var-file'
                    )
                    geometry_usd_hi_file_path = geometry_usd_var_rsv_unit.get_exists_result(
                        version='latest', extend_variants=dict(var='hi')
                    )
                    if geometry_usd_hi_file_path is not None:
                        camera_work_scene_src_file_path = camera_work_scene_src_file_rsv_unit.get_result(
                            version='new'
                        )
                        utl_core.DialogWindow.set_create(
                            session.gui_name,
                            content=(
                                u'create and publish "Asset Camera" for "{}"\n'
                                u'press "Yes" to continue...'
                            ).format(asset),
                            yes_method=lambda *args, **kwargs: create_and_publish_fnc_(camera_work_scene_src_file_path),
                            use_exec=False
                        )
                    else:
                        content = u'"Asset Model USD(hi)" is non-exists, please call for TD get more help'
                else:
                    content = u'"Asset Model Task" is non-exists, please call for TD get more help'
        else:
            content = u'"Asset Camera Task" is non-exists, please call for TD get more help'
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
