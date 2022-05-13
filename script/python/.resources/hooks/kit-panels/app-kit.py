# coding:utf-8
import os

from lxbasic import bsc_core

from lxutil import utl_core

from lxutil_gui import utl_gui_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxsession.commands as ssn_commands


class AppKit(prx_widgets.PrxToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(AppKit, self).__init__(*args, **kwargs)
        self._session = session
        self._ssn_configure = self._session.configure
        #
        self._utl_gui_configure = self._session.utl_gui_configure
        #
        self.set_window_title(self._utl_gui_configure.get('name'))
        if self._session.get_rez_beta():
            self.set_window_title(
                '[BETA] {}'.format(self._utl_gui_configure.get('name'))
            )
        self.set_definition_window_size(self._utl_gui_configure.get('size'))
        self.set_window_icon_name(self._utl_gui_configure.get('icon_name'))
        #
        self._item_frame_size = self._utl_gui_configure.get('item_frame_size')
        self._item_name_frame_size = self._utl_gui_configure.get('item_name_frame_size')
        self._tab_view = prx_widgets.PrxTabView()
        self.set_widget_add(self._tab_view)
        #
        self._set_panel_build_()
        self.get_log_bar().set_expanded(True)
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tools_build_
        )

        self._tool_menu = self.set_menu_add('Debug(s)')
        self._tool_menu.set_menu_raw(
            [
                ('Show Environ', None, self._set_environ_show_)
            ]
        )

    def _set_environ_show_(self):
        utl_core.DialogWindow.set_create(
            'Environ',
            content=u'\n'.join([u'{} = {}'.format(k, v) for k, v in os.environ.items()]),
        )

    def _set_panel_build_(self):
        pass

    def _set_tools_build_(self):
        self.set_window_loading_end()
        self._set_hooks_build_()
        self._set_option_hooks_build_()

    def _set_hooks_build_(self):
        hook_keys = self._ssn_configure.get('app.hooks') or []
        #
        self._list_view_dict = {}
        #
        item_frame_size = self._utl_gui_configure.get('item_frame_size')
        item_name_frame_size = self._utl_gui_configure.get('item_name_frame_size')
        #
        for i_key in hook_keys:
            i_hook_args = ssn_commands.get_hook_args(
                i_key
            )
            if i_hook_args is not None:
                i_session, i_execute_fnc = i_hook_args
                if i_session.get_is_loadable() is True:
                    i_gui_configure = i_session.utl_gui_configure
                    #
                    i_group_name = i_gui_configure.get('group_name')
                    if i_group_name in self._list_view_dict:
                        i_list_view = self._list_view_dict[i_group_name]
                    else:
                        i_list_view = prx_widgets.PrxListView()
                        # i_group.set_widget_add(i_list_view)
                        #
                        self._tab_view.set_item_add(
                            i_list_view,
                            name=i_group_name,
                            icon_name_text=i_group_name,
                        )
                        #
                        i_list_view.set_item_frame_size(*item_frame_size)
                        i_list_view.set_item_name_frame_size(*item_name_frame_size)
                        #
                        self._list_view_dict[i_group_name] = i_list_view
                    #
                    i_list_item = i_list_view.set_item_add()
                    i_name = i_gui_configure.get('name')
                    i_icon_name = i_gui_configure.get('icon_name')
                    i_tool_tip = i_gui_configure.get('tool_tip')
                    i_list_item.set_name(i_name)
                    if i_icon_name:
                        i_list_item.set_image_by_file(utl_gui_core.RscIconFile.get(i_icon_name))
                    else:
                        i_list_item.set_image_by_name(i_name)
                    #
                    i_list_item.set_press_db_clicked_connect_to(
                        i_execute_fnc
                    )
                    i_list_item.set_tool_tip(i_tool_tip)

                    # i_list_item.set_menu_raw(
                    #     [
                    #         ('edit python-file', None, i_session.set_hook_python_file_open),
                    #         ('edit yaml-file', None, i_session.set_hook_yaml_file_open),
                    #     ]
                    # )

    def _set_option_hooks_build_(self):
        option_hook_keys = self._ssn_configure.get('app.option-hooks') or []
        for i in option_hook_keys:
            if isinstance(i, (str, unicode)):
                i_hook_key = i
            elif isinstance(i, dict):
                i_hook_key = i.keys()[0]
            else:
                raise RuntimeError()
            #
            i_hook_option = 'option_hook_key={}'.format(i_hook_key)
            i_hook_args = ssn_commands.get_option_hook_args(
                i_hook_option
            )
            if i_hook_args:
                i_session, i_execute_fnc = i_hook_args
                if i_session.get_is_loadable() is True:
                    i_gui_configure = i_session.utl_gui_configure
                    #
                    i_group_name = i_gui_configure.get('group_name')
                    if i_group_name in self._list_view_dict:
                        i_list_view = self._list_view_dict[i_group_name]
                    else:
                        # i_group = prx_widgets.PrxExpandedGroup()
                        # self.set_widget_add(i_group)
                        # i_group.set_name(i_group_name)
                        # i_group.set_expanded(True)
                        # #
                        i_list_view = prx_widgets.PrxListView()
                        # i_group.set_widget_add(i_list_view)
                        #
                        self.set_widget_add(self._tab_view)
                        self._tab_view.set_item_add(
                            i_list_view,
                            name=i_group_name,
                            icon_name_text=i_group_name,
                        )
                        #
                        i_list_view.set_item_frame_size(*self._item_frame_size)
                        i_list_view.set_item_name_frame_size(*self._item_name_frame_size)
                        #
                        self._list_view_dict[i_group_name] = i_list_view
                    #
                    i_list_item = i_list_view.set_item_add()
                    i_name = i_gui_configure.get('name')
                    i_icon_name = i_gui_configure.get('icon_name')
                    i_tool_tip = i_gui_configure.get('tool_tip')
                    i_list_item.set_name(i_name)
                    if i_icon_name:
                        i_list_item.set_image_by_file(utl_gui_core.RscIconFile.get(i_icon_name))
                    else:
                        i_list_item.set_image_by_name(i_name)
                    #
                    i_list_item.set_press_db_clicked_connect_to(
                        i_execute_fnc
                    )
                    i_list_item.set_tool_tip(i_tool_tip)
                    #
                    i_hs = i_session.get_extra_hook_options()

                    i_menu_content = ssn_commands.get_menu_content_by_hook_options(i_hs)

                    i_list_item.set_menu_content(
                        i_menu_content
                    )


def main(session):
    from lxusd import usd_setup

    from lxutil_gui.qt import utl_gui_qt_core

    usd_setup.UsdSetup.set_environs_setup()
    #
    # tp = utl_gui_qt_core.QtWidgets.QSystemTrayIcon(w.widget)
    # a = utl_gui_qt_core.QtWidgets.QAction('show', triggered=w.widget.show)
    utl_gui_qt_core.set_window_show_standalone(
        AppKit, session=session
    )
    # tp.setIcon(w.widget.windowIcon())
    # tp.show()
    #
    shell_start_m = bsc_core.EnvironMtd.get('shell_start_m')
    shell_start_s = bsc_core.EnvironMtd.get('shell_start_s')
    if shell_start_m and shell_start_s:
        end_m = bsc_core.SystemMtd.get_minute()
        end_s = bsc_core.SystemMtd.get_second()
        #
        utl_core.Log.set_module_result_trace(
            'window show',
            'cost: {}s'.format(
                (end_m - int(shell_start_m)) * 60 + (end_s - int(shell_start_s))
            )
        )
    #
    hook_start_m = bsc_core.EnvironMtd.get('hook_start_m')
    hook_start_s = bsc_core.EnvironMtd.get('hook_start_s')


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
