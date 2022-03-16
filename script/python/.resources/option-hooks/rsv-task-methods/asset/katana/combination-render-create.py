# coding:utf-8


def main(session):
    import collections
    #
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxsession.commands as ssn_commands
    #
    option_opt = session.option_opt
    #
    katana_render_hook_key = 'rsv-task-methods/asset/render/katana-render'
    rv_movie_convert_hook_key = 'rsv-task-methods/asset/rv/movie-convert'
    #
    variable_keys = [
        'camera',
        'layer',
        'light_pass',
        'look_pass',
        'quality'
    ]
    #
    variable_mapper = {
        'camera': 'cameras',
        'layer': 'layers',
        'light_pass': 'light_passes',
        'look_pass': 'look_passes',
        'quality': 'qualities',
    }
    variants_dic = collections.OrderedDict()
    for i_variable_key in variable_keys:
        variants_dic[i_variable_key] = option_opt.get(
            variable_mapper[i_variable_key], as_array=True
        )
    #
    combinations = bsc_core.VariablesMtd.get_all_combinations(
        variants_dic
    )
    with utl_core.log_progress(maximum=len(combinations), label='combination-render-create') as l_p:
        for i_seq, i_variants in enumerate(combinations):
            l_p.set_update()
            #
            i_option_hook_key = '-'.join(
                i_variants.values()
            )
            i_renderer = 'renderer__{}'.format(
                '__'.join(['{}'.format(v) for k, v in i_variants.items()])
            )
            #
            i_camera = i_variants['camera']
            if i_camera in ['shot']:
                i_render_frames = option_opt.get('render_shot_frames')
            else:
                i_render_frames = option_opt.get('render_asset_frames')
            #
            i_batch_file_path = option_opt.get('batch_file')
            i_file_path = option_opt.get('file')
            i_user = option_opt.get('user')
            i_time_tag = option_opt.get('time_tag')
            #
            i_td_enable = option_opt.get('td_enable') or False
            i_rez_beta = option_opt.get('rez_beta') or False
            #
            i_render_output_directory_path = option_opt.get('render_output_directory')

            i_render_file_path = option_opt.get('render_file')

            i_image_file_path = '{}/main/{}/beauty.####.exr'.format(
                i_render_output_directory_path, i_option_hook_key
            )
            i_movie_file_path = '{}/main/{}.mov'.format(
                i_render_output_directory_path, i_option_hook_key
            )

            i_katana_render_hook_option_opt = bsc_core.KeywordArgumentsOpt(
                dict(
                    option_hook_key=katana_render_hook_key,
                    #
                    batch_file=i_batch_file_path,
                    # python option
                    file=i_file_path,
                    #
                    user=i_user, time_tag=i_time_tag,
                    #
                    td_enable=i_td_enable, rez_beta=i_rez_beta,
                    #
                    render_file=i_render_file_path,
                    render_output_directory=i_render_output_directory_path,
                    renderer=i_renderer,
                    #
                    render_frames=i_render_frames,
                    #
                    option_hook_key_extend=[i_option_hook_key],
                )
            )
            #
            i_katana_render_session = ssn_commands.set_option_hook_execute_by_deadline(
                i_katana_render_hook_option_opt.to_string()
            )

            i_katana_render_ddl_job_id = i_katana_render_session.get_ddl_job_id()

            i_rv_movie_convert_hook_option_opt = bsc_core.KeywordArgumentsOpt(
                option=dict(
                    option_hook_key=rv_movie_convert_hook_key,
                    #
                    file=i_file_path,
                    #
                    user=i_user, time_tag=i_time_tag,
                    td_enable=i_td_enable, rez_beta=i_rez_beta,
                    #
                    image_file=i_image_file_path,
                    movie_file=i_movie_file_path,
                    #
                    option_hook_key_extend=[i_option_hook_key],
                    #
                    start_frame=i_render_frames[0],
                    end_frame=i_render_frames[-1],
                    #
                    dependent_ddl_job_id_extend=[i_katana_render_ddl_job_id]
                )
            )
            ssn_commands.set_option_hook_execute_by_deadline(
                i_rv_movie_convert_hook_option_opt.to_string()
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
