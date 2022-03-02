# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets

from lxutil_gui.proxy.widgets import _utl_gui_prx_wdt_node
reload(_utl_gui_prx_wdt_node)


class TestForDialog(prx_widgets.PrxDialogWindow0):
    NAMESPACE = 'storage'
    def __init__(self, *args, **kwargs):
        super(TestForDialog, self).__init__(*args, **kwargs)
        self.set_option_group_enable()

        parameters_gui = self.get_options_node()
        # noinspection PyUnresolvedReferences
        parameters_gui.set_ports_create_by_configure(
            session.configure.get('option.parameters')
        )


def main():
    w = TestForDialog()
    w.set_window_show()


if __name__ == '__main__':
    main()
