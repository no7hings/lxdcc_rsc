# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

import lxresolver.commands as rsv_commands

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

r = rsv_commands.get_resolver()

rsv_project = r.get_rsv_project(project='cgm')

assets = [
    'duanf_f_bao'
]

for i in assets:
    i_rsv_task = rsv_project.get_rsv_task(
        asset=i, step='mod', task='modeling'
    )

    i_work_scene_src_rsv_unit = i_rsv_task.get_rsv_unit(
        keyword='asset-work-maya-scene-src-file'
    )
    i_work_scene_src_file_path = i_work_scene_src_rsv_unit.get_result(
        version='v000'
    )

    i_option_opt = bsc_core.KeywordArgumentsOpt(
        option=dict(
            option_hook_key='rsv-task-batchers/asset/gen-prv-render-submit',
            file=i_work_scene_src_file_path,
            #
            # td_enable=True,
            rez_beta=True,
        )
    )
    #
    ssn_commands.set_option_hook_execute_by_deadline(
        option=i_option_opt.to_string()
    )

