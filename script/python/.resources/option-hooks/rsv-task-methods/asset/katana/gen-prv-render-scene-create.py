# coding:utf-8


def main(session):
    import lxresolver.commands as rsv_commands

    import lxkatana.rsv.objects as ktn_rsv_objects

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        resolver = rsv_commands.get_resolver()
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
        if rsv_scene_properties:
            create_scene = hook_option_opt.get_as_boolean('create_scene')
            if create_scene is True:
                ktn_rsv_objects.RsvDccSceneHookOpt(
                    rsv_scene_properties,
                    hook_option_opt,
                ).set_asset_scene_create()
            #
            with_scene_src_link = hook_option_opt.get_as_boolean('with_scene_src_link')
            if with_scene_src_link is True:
                ktn_rsv_objects.RsvDccSceneHookOpt(
                    rsv_scene_properties,
                    hook_option_opt,
                ).set_scene_src_link()
        else:
            raise RuntimeError(
                'option-hook execute',
                u'file="{}" is not available'.format(
                    any_scene_file_path
                )
            )
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
