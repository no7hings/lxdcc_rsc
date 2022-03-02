# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets


class TestForDialog(prx_widgets.PrxToolWindow):
    NAMESPACE = 'storage'
    def __init__(self, *args, **kwargs):
        super(TestForDialog, self).__init__(*args, **kwargs)

        self._node = prx_widgets.PrxNode_()
        self.set_widget_add(self._node)

        # noinspection PyUnresolvedReferences
        self._node.set_ports_create_by_configure(
            session.configure.get('option.node')
        )

        self._node.get_port('create').set(self.__set_test_)

    def __set_test_(self):
        print self._node.get_as_kwargs()


def main():
    w = TestForDialog()
    w.set_window_show()


if __name__ == '__main__':
    main()
