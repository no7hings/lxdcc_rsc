# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets

import lxsession.commands as ssn_commands


class AppKit(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(AppKit, self).__init__(*args, **kwargs)
        # noinspection PyUnresolvedReferences
        utl_gui_configure = session.utl_gui_configure
        #
        self.set_window_title(utl_gui_configure.get('name'))
        self.set_definition_window_size(utl_gui_configure.get('size'))
        #
        self._set_panel_build_()
        self.get_log_bar().set_expanded(True)
        #
        self.set_loading_start(
            time=1000,
            method=self._set_tools_build_
        )

    def _set_panel_build_(self):
        pass

    def _set_tools_build_(self):
        self.set_window_loading_end()
        self._set_tools_refresh_()

    def _set_tools_refresh_(self):
        # noinspection PyUnresolvedReferences
        configure = session.configure
        #
        app_hook_keys = configure.get('app.hooks')
        #
        self._group_dict = {}
        self._list_view_dict = {}
        #
        self.get_log_bar().set_expanded(True)
        #
        self.set_window_title('App-kit')
        for i_key in app_hook_keys:
            i_hook_args = ssn_commands.get_hook_args(
                i_key
            )
            if i_hook_args is not None:
                i_session, i_execute_fnc = i_hook_args
                if i_session.get_is_loadable() is True:
                    i_gui_option = i_session.utl_gui_configure
                    #
                    i_group_name = i_gui_option.get('group_name')
                    if i_group_name in self._list_view_dict:
                        i_list_view = self._list_view_dict[i_group_name]
                    else:
                        #
                        i_group = prx_widgets.PrxExpandedGroup()
                        self.set_widget_add(i_group)
                        i_group.set_name(i_group_name)
                        i_group.set_expanded(True)
                        #
                        i_list_view = prx_widgets.PrxListView()
                        i_group.set_widget_add(i_list_view)
                        #
                        i_list_view.set_item_frame_size(64, 128)
                        #
                        i_list_view.set_item_name_frame_size(64, 64)
                        self._list_view_dict[i_group_name] = i_list_view
                    #
                    i_list_item = i_list_view.set_item_add()
                    i_name = i_gui_option.get('name')
                    i_tool_tip = i_gui_option.get('tool_tip')
                    i_list_item.set_name(i_name)
                    i_list_item.set_image_by_name(i_name)
                    #
                    i_list_item.set_press_db_clicked_connect_to(
                        i_execute_fnc
                    )
                    i_list_item.set_tool_tip(i_tool_tip)

                    i_list_item.set_menu_raw(
                        [
                            ('open python-file', None, i_session.set_hook_python_file_open),
                            ('open yaml-file', None, i_session.set_hook_yaml_file_open),
                        ]
                    )


if __name__ == '__main__':
    import sys
    #
    from lxutil_gui.qt import utl_gui_qt_core
    #
    app = utl_gui_qt_core.QtWidgets.QApplication(sys.argv)
    #
    w = AppKit()
    w.set_window_show()
    #
    sys.exit(app.exec_())
