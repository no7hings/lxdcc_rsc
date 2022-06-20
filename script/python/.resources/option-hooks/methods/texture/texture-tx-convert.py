# coding:utf-8


def main(session):
    def setup_fnc_():
        from lxutil import utl_setup
        utl_setup.OcioSetup(
            bsc_core.StoragePathMtd.set_map_to_platform(
                '/l/packages/pg/third_party/ocio/aces/1.2'
            )
        ).set_run()

        from lxarnold import and_setup
        and_setup.MtoaSetup(
            bsc_core.StoragePathMtd.set_map_to_platform(
                '/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019'
            )
        ).set_run()

    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    hook_option_opt = session.option_opt

    setup_fnc_()

    directory_path = hook_option_opt.get('directory')
    output_directory_path = hook_option_opt.get('output_directory')

    below_enable = hook_option_opt.get_as_boolean('below_enable')
    force_enable = hook_option_opt.get_as_boolean('force_enable')

    include_exts = hook_option_opt.get_as_array('include_exts')

    if directory_path:
        directory = utl_dcc_objects.OsDirectory_(directory_path)
        if directory.get_is_exists() is True:
            if below_enable is True:
                file_paths = directory.get_all_file_paths(include_exts=include_exts)
            else:
                file_paths = directory.get_file_paths(include_exts=include_exts)
            #
            if output_directory_path:
                utl_dcc_objects.OsDirectory_(
                    output_directory_path
                ).set_create()
            #
            with utl_core.log_progress_bar(
                maximum=len(file_paths), label=session.name
            ) as l_p:
                for i_file_path in file_paths:
                    l_p.set_update()

                    i_cmd = utl_dcc_objects.OsTexture._get_unit_tx_create_cmd_by_src_(
                        i_file_path,
                        directory_path_tgt=output_directory_path,
                    )
                    if i_cmd:
                        bsc_core.CmdSubProcessThread.set_wait()
                        bsc_core.CmdSubProcessThread.set_start(i_cmd)

        else:
            raise RuntimeError(
                utl_core.Log.set_module_error_trace(
                    '{} run'.format(session.name),
                    'directory="{}" is non-exists'.format(directory_path)
                )
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
