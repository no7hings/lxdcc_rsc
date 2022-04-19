# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    from lxutil import utl_core
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
                render_frames = hook_option_opt.get('render_frames')
                render_frame_step = int(hook_option_opt.get('render_frame_step'))
                if render_frame_step > 1:
                    render_frame_range = bsc_core.TextOpt(render_frames).to_frame_range()
                    render_frames_ = bsc_core.FrameRangeMtd.get(
                        render_frame_range, render_frame_step
                    )
                    hook_option_opt.set(
                        'render_frames', ','.join(map(str, render_frames_))
                    )
                    hook_option_opt.set(
                        'render_frame_step', 1
                    )
                #
                cache_workspace = hook_option_opt.get('cache_workspace')
                if cache_workspace == 'publish':
                    hook_option_opt.set('cache_use_output_enable', 0)
                elif cache_workspace == 'output':
                    hook_option_opt.set('cache_use_output_enable', 1)
                #
                cache_cfx_scheme = hook_option_opt.get('cache_cfx_scheme')
                if cache_cfx_scheme == '0-hair-cloth':
                    hook_option_opt.set('xiaov', 0)
                elif cache_cfx_scheme == '1-animation-hair':
                    hook_option_opt.set('xiaov', 1)
                #
                cmd_pattern = 'rez-env python pg_tools -- python /l/packages/pg/prod/pg_production_lib/9.9.9/lib/production/cfx/auto_pipe/submit_prerender.py send_xiaov --proj="{project}" --shot="{shot}" --task="{task}" --user="{user}" --xiaov={xiaov}'
                #
                cmd = cmd_pattern.format(
                    **hook_option_opt.value
                )
                # print cmd
                utl_core.SubProcessRunner.set_run_with_result(
                    cmd
                )
            else:
                raise RuntimeError()
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
