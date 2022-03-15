# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    import lxsession.commands as ssn_commands

    option_opt = session.option_opt

    katana_render_hook_key = 'rsv-task-renders/asset/katana-render'

    render_option_opt = bsc_core.KeywordArgumentsOpt(
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
            renderer='renderer__shot__master__all__plastic__custom',
            render_frames=[1001],
            batch_key='render_frames'
        )
    )

    ssn_commands.set_option_hook_execute_by_deadline(
        render_option_opt.to_string()
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
