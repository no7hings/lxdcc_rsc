# coding:utf-8
import lxutil_gui.proxy.widgets as prx_widgets


class TestForDialog(prx_widgets.PrxDialogWindow0):
    NAMESPACE = 'storage'
    def __init__(self, *args, **kwargs):
        super(TestForDialog, self).__init__(*args, **kwargs)
        self.set_option_group_enable()

        node = self.get_options_node()
        # noinspection PyUnresolvedReferences
        node.set_ports_create_by_configure(
            session.configure.get('option.parameters')
        )

        node.get_port('create').set(self.__set_test_)

    def __set_test_(self):
        node = self.get_options_node()
        print node.get_as_kwargs()


def main():
    w = TestForDialog()
    w.set_window_show()


if __name__ == '__main__':
    main()
