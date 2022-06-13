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
            with_render = hook_option_opt.get_as_boolean('with_render')
            if with_render is True:
                ktn_rsv_objects.RsvDccRenderHookOpt(
                    rsv_scene_properties,
                    hook_option_opt
                ).set_asset_render_create()
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
