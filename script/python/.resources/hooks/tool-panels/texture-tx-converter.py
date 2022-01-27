# coding:utf-8
import collections

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui import utl_gui_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxutil_gui.proxy.operators as prx_operators

import lxutil.dcc.dcc_operators as utl_dcc_operators


def set_startup():
    from lxarnold import and_setup

    and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

    utl_core.Environ.set_add(
        'OCIO', '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'
    )


class TextureTxConverter(prx_widgets.PrxToolWindow):
    NAMESPACE = 'storage'
    def __init__(self, *args, **kwargs):
        super(TextureTxConverter, self).__init__(*args, **kwargs)
        self._name_width = 240
        # noinspection PyUnresolvedReferences
        utl_gui_configure = session.utl_gui_configure
        self.set_window_title(utl_gui_configure.get('name'))
        self.set_definition_window_size(utl_gui_configure.get('size'))
        #
        self._viewer_group = prx_widgets.PrxExpandedGroup()
        self.set_widget_add(self._viewer_group)
        self._viewer_group.set_name('Viewer(s)')
        self._viewer_group.set_expanded(True)
        #
        self._tree_view = prx_widgets.PrxTreeView()
        self._viewer_group.set_widget_add(self._tree_view)
        self._tree_view.set_header_view_create(
            [('Name(s)', 4)],
            self.get_definition_window_size()[0] - 16
        )
        self._tree_view_add_opt = prx_operators.PrxStgObjTreeViewAddOpt(
            self._tree_view,
            prx_tree_item_cls=prx_widgets.PrxStgObjTreeItem,
        )
        #
        self._configure_group = prx_widgets.PrxExpandedGroup()
        self._configure_group.set_name('Configure(s)')
        self.set_widget_add(self._configure_group)
        self._configure_group.set_expanded(True)
        self._configure_node = prx_widgets.PrxNode()
        self._configure_group.set_widget_add(self._configure_node)
        self._configure_node.set_name_width(self._name_width)
        self._directory_port = self._configure_node.set_port_add(
            prx_widgets.PrxDirectoryOpenPort(
                'directory', 'Directory'
            )
        )
        self._directory_port.set(
            '/depts/lookdev/YZQ/to'
        )
        #
        self._name_patterns_port = self._configure_node.set_port_add(
            prx_widgets.PrxStringPort(
                'name_patterns', 'Name-pattern(s)'
            )
        )
        self._name_patterns_port.set('*.<udim>.####.<ext>, *.<udim>.<ext>, *.<ext>')
        #
        self._exts_port = self._configure_node.set_port_add(
            prx_widgets.PrxStringPort(
                'exts', 'Ext(s)'
            )
        )
        self._exts_port.set('exr, tga')
        #
        self._refresh_port = self._configure_node.set_port_add(
            prx_widgets.PrxButtonPort(
                'refresh', 'Refresh'
            )
        )
        self._refresh_port.set(
            self._set_texture_guis_build_
        )
        #
        self._convert_port = self._configure_node.set_port_add(
            prx_widgets.PrxStatusPort(
                'convert', 'Convert Texture-tx(s)'
            )
        )
        self._convert_port.set(
            self._set_convert_run_
        )

    def _set_data_update_(self):
        array_dict = collections.OrderedDict()
        self._file_dict = collections.OrderedDict()
        #
        directory_path = self._directory_port.get()
        e = self._exts_port.get()
        s = self._name_patterns_port.get()
        if e and s:
            exts = map(lambda x: x.rstrip().lstrip(), e.split(','))
            name_patterns = map(lambda x: x.rstrip().lstrip(), s.split(','))
            if name_patterns and exts:
                _ = bsc_core.DirectoryMtd.get_all_file_paths(directory_path)
                if _:
                    g_p = utl_core.GuiProgressesRunner(
                        maximum=len(_)
                    )
                    for i_file_path in _:
                        g_p.set_update()
                        #
                        i_file_opt = bsc_core.StorageFileOpt(i_file_path)
                        self._set_file_args_update_0_(
                            self._file_dict, i_file_opt, name_patterns, exts
                        )
                    #
                    g_p.set_stop()
    @classmethod
    def _set_file_args_update_0_(cls, file_dict, file_opt, name_patterns, exts):
        name_patterns_ = []
        for i_name_pattern in name_patterns:
            if i_name_pattern.endswith('<ext>'):
                for j_ext in exts:
                    j_name_pattern = i_name_pattern.replace('<ext>', j_ext)
                    name_patterns_.append(j_name_pattern)
            else:
                name_patterns_.append(i_name_pattern)
        #
        for i_name_pattern_ in name_patterns_:
            i_enable = cls._set_file_args_update_1_(file_dict, file_opt, i_name_pattern_)
            if i_enable is True:
                break
    @classmethod
    def _set_file_args_update_1_(cls, file_dict, file_opt, name_pattern):
        if bsc_core.MultiplyPatternMtd.get_is_valid(name_pattern):
            match_args = bsc_core.MultiplyFileNameMtd.get_match_args(
                file_opt.name, name_pattern
            )
            if match_args:
                file_name_, numbers = match_args
                #
                file_path_ = '{}/{}'.format(file_opt.directory_path, file_name_)
                file_dict.setdefault(
                    file_path_, []
                ).append(file_opt.path)
                return True
        else:
            if file_opt.get_is_match_name_pattern(name_pattern):
                file_dict.setdefault(
                    file_opt.path, []
                ).append(file_opt.path)
                return True
        return False

    def _set_texture_guis_build_(self):
        self._set_data_update_()
        #
        self._tree_view_add_opt.set_restore()
        #
        for i_k, i_v in self._file_dict.items():
            i_texture = utl_dcc_objects.OsTexture(i_k)

            _, i_texture_gui = self._tree_view_add_opt.set_item_prx_add_as(i_texture, mode='list')

            if i_texture.get_tx_is_exists() is False:
                i_texture_gui.set_state(utl_gui_core.State.WARNING)

    def _set_texture_guis_refresh_(self):
        for k, v in self._tree_view._item_dict.items():
            i_texture_gui = v
            i_texture = i_texture_gui.get_gui_dcc_obj(namespace='storage-file')
            if i_texture is not None:
                if i_texture.get_tx_is_exists() is False:
                    i_texture_gui.set_state(utl_gui_core.State.WARNING)
                else:
                    i_texture_gui.set_state(utl_gui_core.State.NORMAL)

    def _get_checked_textures_(self):
        lis = []
        for k, v in self._tree_view._item_dict.items():
            i_texture = v.get_gui_dcc_obj(namespace='storage-file')
            if i_texture is not None:
                if v.get_is_checked() is True:
                    if v.get_is_hidden(ancestors=True) is False:
                        lis.append(i_texture)
        return lis

    def _set_convert_run_(self):
        def set_processing_update(time_cost):
            c = 'Convert Texture-tx(s) [ {} ] [ {} ]'.format(
                str(p_m.get_status()),
                bsc_core.IntegerMtd.second_to_time_prettify(time_cost)
            )
            item_prx.set_name(c)

        def set_status_changed_update(status):
            c = 'Convert Texture-tx(s) [ {} ] [ {} ]'.format(
                str(status),
                bsc_core.IntegerMtd.second_to_time_prettify(p_m.get_running_time_cost())
            )
            item_prx.set_name(c)
            item_prx.set_status(status)

        def set_element_status_changed_update(element_statuses):
            item_prx.set_element_statuses(element_statuses)

        def set_logging_update(text):
            pass
        #
        item_prx = self._convert_port
        #
        lis = []
        textures = self._get_checked_textures_()
        for i_texture in textures:
            i_texture_tiles = i_texture.get_exists_files()
            for j_texture_tile in i_texture_tiles:
                if j_texture_tile.get_tx_is_exists() is False:
                    lis.append(j_texture_tile.path)
        #
        utl_dcc_operators.TextureTxMainProcess.PROCESS_COUNT = 0
        p = utl_dcc_operators.TextureTxMainProcess(lis)
        p.set_name('texture-tx create')
        p_m = bsc_objects.ProcessMonitor(p)
        p_m.logging.set_connect_to(set_logging_update)
        p_m.processing.set_connect_to(set_processing_update)
        p_m.status_changed.set_connect_to(set_status_changed_update)
        p_m.element_statuses_changed.set_connect_to(set_element_status_changed_update)
        p_m.set_start()
        p.set_start()
        self.set_window_close_connect_to(p_m.set_stop)
        p_m.completed.set_connect_to(self._set_texture_guis_refresh_)


def main():
    w = TextureTxConverter()
    w.set_window_show()


if __name__ == '__main__':
    set_startup()
    main()
