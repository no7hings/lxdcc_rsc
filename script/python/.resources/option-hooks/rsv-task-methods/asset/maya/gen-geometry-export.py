# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxresolver.commands as rsv_commands

    import lxmaya.rsv.objects as mya_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if utl_dcc_objects.OsFile(any_scene_file_path).get_is_exists() is True:
            mya_dcc_objects.Scene.set_file_open(any_scene_file_path)
            #
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                with_geometry_usd = hook_option_opt.get('with_geometry_usd') or False
                if with_geometry_usd is True:
                    mya_rsv_objects.RsvDccGeometryHookOpt(
                        rsv_scene_properties
                    ).set_geometry_usd_export()
                #
                with_geometry_uv_map_usd = hook_option_opt.get('with_geometry_uv_map_usd') or False
                if with_geometry_uv_map_usd is True:
                    mya_rsv_objects.RsvDccGeometryHookOpt(
                        rsv_scene_properties
                    ).set_geometry_uv_map_usd_export()
                #
                with_geometry_abc = hook_option_opt.get('with_geometry_abc') or False
                if with_geometry_abc is True:
                    mya_rsv_objects.RsvDccGeometryHookOpt(
                        rsv_scene_properties
                    ).set_geometry_abc_export()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
