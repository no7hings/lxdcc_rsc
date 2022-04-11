# coding:utf-8


def main(session):
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.commands as rsv_commands

    hook_option_opt = session.option_opt

    any_scene_file_path = hook_option_opt.get('file')

    if any_scene_file_path is not None:
        if utl_dcc_objects.OsFile(any_scene_file_path).get_is_exists() is True:
            resolver = rsv_commands.get_resolver()
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(any_scene_file_path)
            if rsv_scene_properties:
                rsv_task = resolver.get_rsv_task_by_any_file_path(any_scene_file_path)
                #
                with_component_usd = hook_option_opt.get('with_component_usd') or False
                if with_component_usd is True:
                    set_component_usd_create(rsv_task, rsv_scene_properties)
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


def set_component_usd_create(rsv_task, rsv_scene_properties):
    from lxutil import utl_configure
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    step = rsv_scene_properties.get('step')
    #
    workspace = rsv_scene_properties.get('workspace')
    #
    if workspace == 'work':
        keyword = 'asset-work-comp-usd-dir'
    elif workspace == 'publish':
        keyword = 'asset-component-usd-dir'
    elif workspace == 'output':
        keyword = 'asset-output-component-usd-dir'
    else:
        raise TypeError()
    #
    rsv_set_usd_directory_unit = rsv_task.get_rsv_unit(
        keyword=keyword
    )
    #
    set_usd_directory_path = rsv_set_usd_directory_unit.get_result(
        version=rsv_scene_properties.get('version')
    )
    #
    key_map_dict = dict(
        mod='usda/set/model',
        srf='usda/set/surface',
        rig='usda/set/rig',
        grm='usda/set/groom',
    )
    if step in key_map_dict:
        key = key_map_dict[step]
        #
        c = utl_configure.Jinja.get_configure(key)
        c.set_update(
            rsv_scene_properties.value
        )
        #
        c.set_flatten()
        #
        usda_dict = c.get('usdas')
        #
        for k, v in usda_dict.items():
            t = utl_configure.Jinja.get_template('{}/{}'.format(key, k))
            i_raw = t.render(
                **c.value
            )
            i_usda_file_path = '{}/{}'.format(
                set_usd_directory_path, v
            )
            i_file = utl_dcc_objects.OsFile(i_usda_file_path)
            if i_file.get_is_exists() is False:
                utl_dcc_objects.OsFile(i_usda_file_path).set_write(
                    i_raw
                )
        #
        if workspace in ['publish']:
            # noinspection PyUnresolvedReferences
            import production.gen.record_set_registry as pgs
            register_file_path = '{}/registry.usda'.format(set_usd_directory_path)
            pgs.run(register_file_path)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
