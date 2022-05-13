# coding:utf-8
from lxbasic import bsc_core
import lxsession.commands as ssn_commands

bsc_core.EnvironMtd.set_td_enable(True)
bsc_core.EnvironMtd.set('REZ_BETA', '1')

ssn_commands.set_hook_execute("*/asset-loader")
