# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.commands as rsv_commands

    import lxmaya.rsv.objects as mya_rsv_objects
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    cmds.stackTrace(state=1)

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if utl_dcc_objects.OsFile(any_scene_file_path).get_is_exists() is True:
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                mya_rsv_objects.RsvDccShotSceneHookOpt(
                    rsv_scene_properties,
                    hook_option_opt,
                ).set_asset_shot_scene_open()
                #
                with_shot_hair_xgen = hook_option_opt.get('with_shot_hair_xgen') or False
                if with_shot_hair_xgen is True:
                    mya_rsv_objects.RsvDccShotHairHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_asset_shot_xgen_export()
                #
                with_shot_hair_xgen_usd = hook_option_opt.get('with_shot_hair_xgen_usd') or False
                if with_shot_hair_xgen_usd is True:
                    pass

            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
