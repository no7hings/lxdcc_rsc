# coding:utf-8
import collections

import functools

from lxbasic import bsc_configure, bsc_core

import lxbasic.objects as bsc_objects

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil_gui import utl_gui_core

from lxutil_gui.qt import utl_gui_qt_core

import lxutil_gui.proxy.widgets as prx_widgets

import lxutil_gui.proxy.operators as prx_operators

import lxutil.dcc.dcc_operators as utl_dcc_operators


def set_startup():
    from lxutil import utl_setup
    utl_setup.OcioSetup(
        bsc_core.StoragePathMtd.set_map_to_platform(
            '/l/packages/pg/third_party/ocio/aces/1.2'
        )
    ).set_run()

    from lxarnold import and_setup
    and_setup.MtoaSetup(
        bsc_core.StoragePathMtd.set_map_to_platform(
            '/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019'
        )
    ).set_run()


class TextureTxConverter(prx_widgets.PrxToolWindow):
    NAMESPACE = 'storage'
    def __init__(self, session, *args, **kwargs):
        super(TextureTxConverter, self).__init__(*args, **kwargs)
        self._session = session
        self._session.set_configure_reload()

        self._name_width = 240
        # noinspection PyUnresolvedReferences
        utl_gui_configure = self._session.gui_configure
        self.set_window_title(utl_gui_configure.get('name'))
        self.set_definition_window_size(utl_gui_configure.get('size'))
        #
        self._viewer_group = prx_widgets.PrxExpandedGroup()
        self.set_widget_add(self._viewer_group)
        self._viewer_group.set_name('textures')
        self._viewer_group.set_expanded(True)
        #
        self._tree_view = prx_widgets.PrxTreeView()
        self._viewer_group.set_widget_add(self._tree_view)
        self._tree_view.set_header_view_create(
            [('name)', 4)],
            self.get_definition_window_size()[0] - 16
        )
        self._tree_view_add_opt = prx_operators.PrxStgTextureTreeViewAddOpt(
            self._tree_view,
            prx_tree_item_cls=prx_widgets.PrxStgObjTreeItem,
        )

        self._options_prx_node = prx_widgets.PrxNode_('options')
        self.set_widget_add(self._options_prx_node)
        self._options_prx_node.set_ports_create_by_configure(
            self._session.configure.get('build.node.options'),
        )

        self._options_prx_node.get_port('directory').set_show_history_latest()
        self._options_prx_node.get_port('output_directory').set_show_history_latest()

        self._options_prx_node.set(
            'refresh', self._set_gui_refresh_
        )
        self._options_prx_node.set(
            'match_pattern', '*.<udim>.####.<ext>, *.<udim>.<ext>, *.<ext>'
        )
        self._options_prx_node.set(
            'convert', self.set_convert_run
        )

        self._options_prx_node.set(
            'convert_use_deadline', self.set_convert_run_use_deadline
        )

        self._options_prx_node.get_port('convert').set_finished_connect_to(
            self._set_gui_texture_refresh_1_
        )

        self._gui_data = []
        self._convert_data = []
    @classmethod
    def _set_file_args_update_0_(cls, file_dict, file_opt, include_patterns, include_exts):
        name_patterns_ = []
        for i_name_pattern in include_patterns:
            if i_name_pattern.endswith('<ext>'):
                for j_ext in include_exts:
                    j_name_pattern = i_name_pattern.replace('.<ext>', j_ext)
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
    @classmethod
    def _get_directory_paths_(cls, directory_path, below_enable):
        if directory_path:
            if below_enable is True:
                return bsc_core.DirectoryMtd.get_all_directory_path__(directory_path)
            else:
                return [directory_path]
        return []

    def _set_gui_refresh_(self):
        def post_fnc_():
            pass

        directory_path = self._options_prx_node.get('directory')
        below_enable = self._options_prx_node.get('below_enable')
        output_directory_path = self._options_prx_node.get('output_directory')
        match_patterns = self._options_prx_node.get('match_pattern')
        match_exts = self._options_prx_node.get('match_ext')

        include_exts = map(lambda x: '.' + x, map(lambda x: x.rstrip().lstrip(), match_exts.split(',')))
        include_patterns = map(lambda x: x.rstrip().lstrip(), match_patterns.split(','))

        directory_paths = self._get_directory_paths_(directory_path, below_enable)
        self._tree_view_add_opt.set_restore()
        self._tree_view_add_opt.set_output_directory(output_directory_path)

        if directory_paths:
            t_r = utl_gui_qt_core.QtBuildThreadsRunner(self.widget)
            t_r.run_finished.connect(post_fnc_)
            for i_directory_path in directory_paths:
                t_r.set_register(
                    functools.partial(self._set_cache_textures_, i_directory_path, include_patterns, include_exts),
                    self._set_gui_add_textures_
                )

            t_r.set_start()

    def _set_cache_textures_(self, directory_path, include_patterns, include_exts):
        file_paths = bsc_core.DirectoryMtd.get_file_paths__(directory_path, include_exts)
        dict_ = collections.OrderedDict()
        for i_file_path in file_paths:
            i_file_opt = bsc_core.StorageFileOpt(i_file_path)
            self._set_file_args_update_0_(
                dict_, i_file_opt, include_patterns, include_exts
            )
        return dict_.keys()

    def _set_gui_add_textures_(self, file_paths):
        for i_k in file_paths:
            i_texture = utl_dcc_objects.OsTexture(i_k)

            _, i_prx_item = self._tree_view_add_opt.set_prx_item_add_as(
                i_texture,
                mode='list',
                use_show_thread=True
            )

    def _set_gui_texture_refresh_1_(self):
        output_directory_path = self._options_prx_node.get('output_directory')

        for k, v in self._tree_view._item_dict.items():
            i_prx_item = v
            i_texture = i_prx_item.get_gui_dcc_obj(namespace='storage-file')
            if i_texture is not None:
                if i_texture._get_is_exists_as_tgt_ext_by_src_(
                    i_texture.path,
                    directory_path_tgt=output_directory_path,
                    ext_tgt=i_texture.TX_EXT
                ) is False:
                    i_prx_item.set_state(utl_gui_core.State.WARNING)
                else:
                    i_prx_item.set_state(utl_gui_core.State.NORMAL)

    def _get_checked_textures_(self):
        list_ = []
        for k, v in self._tree_view._item_dict.items():
            i_texture = v.get_gui_dcc_obj(namespace='storage-file')
            if i_texture is not None:
                if v.get_is_checked() is True:
                    if v.get_is_hidden(ancestors=True) is False:
                        list_.append(i_texture)
        return list_

    def _set_convert_data_update_(self, output_directory_path, force_enable):
        self._convert_data = []

        contents = []
        textures = self._get_checked_textures_()
        if textures:
            with utl_core.gui_progress(maximum=len(textures)) as g_p:
                for i_texture in textures:
                    g_p.set_update()
                    #
                    i_texture_tiles = i_texture.get_exists_files_()
                    for j_texture_tile in i_texture_tiles:
                        if force_enable is True:
                            j_texture_tx_tile = j_texture_tile.get_tx()
                            j_texture_tx_tile.set_delete()
                            self._convert_data.append(j_texture_tile.path)
                        else:
                            if j_texture_tile._get_unit_is_exists_as_tgt_ext_by_src_(
                                    j_texture_tile.path,
                                    directory_path_tgt=output_directory_path,
                                    ext_tgt=j_texture_tile.TX_EXT
                            ) is False:
                                self._convert_data.append(j_texture_tile.path)
        else:
            contents = [
                'non-texture(s) to converted, you can click refresh or enter a new "directory" and click "refresh"'
            ]
        #
        if contents:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.GuiStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
            return False
        else:
            return True

    def _set_convert_by_data_(self):
        def finished_fnc_(index, status):
            item_prx.set_finished_at(index, status)

        def status_update_at_fnc_(index, status):
            item_prx.set_status_update_at(index, status)

        def run_fnc_():
            for i_index, i_file_path in enumerate(self._convert_data):
                i_cmd = utl_dcc_objects.OsTexture._get_unit_tx_create_cmd_by_src_(
                    i_file_path,
                    directory_path_tgt=output_directory_path,
                )
                if item_prx.get_is_stopped():
                    break
                if i_cmd:
                    bsc_core.CmdSubProcessThread.set_wait()
                    i_t = bsc_core.CmdSubProcessThread.set_start(i_cmd, i_index)
                    i_t.status_changed.set_connect_to(status_update_at_fnc_)
                    i_t.finished.set_connect_to(finished_fnc_)
                else:
                    status_update_at_fnc_(
                        i_index, bsc_configure.Status.Completed
                    )
                    finished_fnc_(
                        i_index, bsc_configure.Status.Completed
                    )

        output_directory_path = self._options_prx_node.get(
            'output_directory'
        )

        contents = []
        item_prx = self._options_prx_node.get_port('convert')
        if self._convert_data:
            if output_directory_path:
                utl_dcc_objects.OsDirectory_(
                    output_directory_path
                ).set_create()

            item_prx.set_stopped(False)

            c = len(self._convert_data)

            item_prx.set_status(bsc_configure.Status.Waiting)
            item_prx.set_initialization(c, bsc_configure.Status.Waiting)

            t = utl_gui_qt_core.QtMethodThread(self.widget)
            t.set_method_add(
                run_fnc_
            )
            t.start()
        else:
            item_prx.set_restore()

            contents = [
                'non-texture(s) to converted, you can checked "force enable" or enter a new "output directory"'
            ]

        if contents:
            utl_core.DialogWindow.set_create(
                self._session.gui_name,
                content=u'\n'.join(contents),
                status=utl_core.DialogWindow.GuiStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
            return False
        else:
            return True

    def set_convert_run(self):
        output_directory_path = self._options_prx_node.get('output_directory')

        force_enable = self._options_prx_node.get('force_enable')

        method_args = [
            (self._set_convert_data_update_, (output_directory_path, force_enable)),
            (self._set_convert_by_data_, ())
        ]
        with utl_core.gui_progress(maximum=len(method_args)) as g_p:
            for i_fnc, i_args in method_args:
                g_p.set_update()
                i_result = i_fnc(*i_args)
                if i_result is False:
                    break

    def set_convert_run_use_deadline(self):
        import lxsession.commands as ssn_commands

        directory_path = self._options_prx_node.get('directory')
        output_directory_path = self._options_prx_node.get('output_directory')

        j_option_opt = bsc_core.KeywordArgumentsOpt(
            option=dict(
                option_hook_key='methods/texture/texture-tx-convert',
                directory=directory_path,
                output_directory=output_directory_path,
                #
                td_enable=self._session.get_td_enable(),
                rez_beta=self._session.get_rez_beta(),
            )
        )
        #
        session = ssn_commands.set_option_hook_execute_by_deadline(
            option=j_option_opt.to_string()
        )
        ddl_job_id = session.get_ddl_job_id()
        utl_core.DialogWindow.set_create(
            self._session.gui_name,
            content='texture-convert job is send to deadline job-id is "{}", more information you see in deadline monitor'.format(
                ddl_job_id
            ),
            status=utl_core.DialogWindow.GuiStatus.Correct,
            #
            yes_label='Close',
            #
            no_visible=False, cancel_visible=False,
            use_exec=False
        )


def main(session):
    w = TextureTxConverter(session)
    w.set_window_show()


if __name__ == '__main__':
    set_startup()
    # noinspection PyUnresolvedReferences
    main(session)
