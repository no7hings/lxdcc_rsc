# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

import lxsession.commands as ssn_commands

ssn_commands.set_option_hook_execute(
    bsc_core.KeywordArgumentsOpt(
        option=dict(
            option_hook_key='*/rez-graph',
            packages=utl_core.MayaLauncher(project='cgm').get_rez_packages()
            # packages=['lxdcc']
        )
    ).to_string()
)
