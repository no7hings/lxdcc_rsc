# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.commands as rsv_commands

    import lxusd.rsv.objects as usd_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if utl_dcc_objects.OsFile(any_scene_file_path).get_is_exists() is True:
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                with_component_usd = hook_option_opt.get('with_component_usd') or False
                if with_component_usd is True:
                    usd_rsv_objects.RsvUsdHookOpt(
                        rsv_scene_properties,
                        hook_option_opt,
                    ).set_component_usd_create()
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
