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
                component_usd_file_path = get_component_usd_file(rsv_task, rsv_scene_properties)
                if utl_dcc_objects.OsFile(component_usd_file_path).get_is_exists() is True:
                    hook_option_opt.set(
                        'component_usd_file', component_usd_file_path
                    )
                    cmd_pattern = 'rez-env python pg_tools -- python /l/packages/pg/prod/pg_production_lib/9.9.9/lib/production/set/auto_set/submit_usd_render_job.py --usd="{component_usd_file}" --proj="{project}" --shot="{shot}" --step="{step}" --task="{task}" --shading="{render_look}" --user="{user}" --frames="{render_frames}" --stepby={render_frame_step} --motion={render_motion_enable} --instance={render_instance_enable} --bokeh={render_bokeh_enable} --bg={render_background_enable} --chunk={render_chunk} --aa={render_arnold_aa_sample} --publish={user_upload_shotgun_enable} --tech_review={user_tech_review_enable} --playlist=0 --description="prerender"'
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


def get_component_usd_file(rsv_task, rsv_scene_properties):
    workspace = rsv_scene_properties.get('workspace')
    version = rsv_scene_properties.get('version')
    root = rsv_scene_properties.get('dcc.root')
    #
    if workspace == 'publish':
        keyword_0 = '{branch}-component-usd-file'
    elif workspace == 'output':
        keyword_0 = '{branch}-output-component-usd-file'
    else:
        raise TypeError()

    component_usd_file_rsv_unit = rsv_task.get_rsv_unit(
        keyword=keyword_0
    )
    component_usd_file_path = component_usd_file_rsv_unit.get_result(version=version)
    return component_usd_file_path


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
