# coding:utf-8
import lxsession.commands as ssn_commands

session, fnc = ssn_commands.get_option_hook_args(
    'option_hook_key=*/maya'
)

hs = session.get_extra_hook_options()
print hs

ssn_commands.get_menu_content_by_hook_options(hs)

