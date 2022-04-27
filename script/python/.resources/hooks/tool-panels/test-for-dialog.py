# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets


class TestForDialog(prx_widgets.PrxToolWindow):
    NAMESPACE = 'storage'
    def __init__(self, *args, **kwargs):
        super(TestForDialog, self).__init__(*args, **kwargs)

        self._prx_node = prx_widgets.PrxNode_('asset')
        self.set_widget_add(self._prx_node)

        # noinspection PyUnresolvedReferences
        self._prx_node.set_ports_create_by_configure(
            session.configure.get('node')
        )

        self._prx_node.get_port('create').set(self.__set_test_)

    def __set_test_(self):
        print self._prx_node.get_as_kwargs()


def main():
    w = prx_widgets.PrxDialogWindow1()
    w.set_options_group_enable()
    w.set_window_show()


if __name__ == '__main__':
    main()
