# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

utl_core.Environ.set_add(
    utl_core.Resources.ENVIRON_KEY, '/data/e/myworkspace/td/lynxi/script/python/.resources'
)

user = bsc_core.SystemMtd.get_user_name()

j_option_opt = bsc_core.KeywordArgumentsOpt(
    option=dict(
        option_hook_key='methods/texture/texture-tx-convert',
        directory='/t/prod/xkt/publish/shots/s10/s10110/efx/efx_trans/s10110.efx.efx_trans.v017/texture/nngongshifu_cloth_mask',
        output_directory='/l/temp/td/dongchangbao/tx_convert_2/nngongshifu_cloth_mask_tx',
        #
        td_enable=True,
        # rez_beta=True,
    )
)
#
ssn_commands.set_option_hook_execute_by_deadline(
    option=j_option_opt.to_string()
)
