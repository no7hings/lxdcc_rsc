# coding:utf-8
import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets

hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_14y_test/mod/modeling/maya/scenes/nn_14y_test.mod.modeling.v006.ma')

w = utl_pnl_widgets.AssetRenderSubmitter(
    option=hook_option
)

w.set_window_show()
