# coding:utf-8


def main(session):
    import collections

    from lxbasic import bsc_core

    import lxsession.commands as ssn_commands

    option_opt = session.option_opt

    katana_render_hook_key = 'rsv-task-renders/asset/katana-render'

    variable_keys = [
        'camera',
        'layer',
        'light_pass',
        'look_pass',
        'quality'
    ]

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

    combinations = bsc_core.VariablesMtd.get_all_combinations(
        variants_dic
    )
    for i_seq, i_variants in enumerate(combinations):
        print i_variants
        i_renderer = 'renderer__{}'.format(
            '__'.join(['{}'.format(v) for k, v in i_variants.items()])
        )
        camera = i_variants['camera']
        if camera in ['shot']:
            render_frames = option_opt.get('render_shot_frames')
        else:
            render_frames = option_opt.get('render_asset_frames')

        i_render_option_opt = bsc_core.KeywordArgumentsOpt(
            dict(
                option_hook_key=katana_render_hook_key,
                #
                batch_file=option_opt.get('batch_file'),
                # python option
                file=option_opt.get('file'),
                #
                user=option_opt.get('user'), time_tag=option_opt.get('time_tag'),
                #
                td_enable=option_opt.get('td_enable') or False,
                rez_beta=option_opt.get('rez_beta') or False,
                #
                render_file=option_opt.get('render_file'),
                render_output_directory=option_opt.get('render_output_directory'),
                renderer=i_renderer,
                #
                render_frames=render_frames
            )
        )

        ssn_commands.set_option_hook_execute_by_deadline(
            i_render_option_opt.to_string()
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
