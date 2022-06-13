# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

ssn_commands.set_option_hook_execute(
    bsc_core.KeywordArgumentsOpt(
        option=dict(
            option_hook_key='*/asset-lineup',
        )
    ).to_string()
)
