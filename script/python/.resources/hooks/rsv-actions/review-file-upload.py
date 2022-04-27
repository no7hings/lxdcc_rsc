# coding:utf-8
from lxutil import utl_core

import lxutil.modifiers as utl_modifiers

import lxutil_gui.proxy.widgets as prx_widgets


class UploadReview(prx_widgets.PrxToolWindow):
    def __init__(self, *args, **kwargs):
        super(UploadReview, self).__init__(*args, **kwargs)


def yes_method():
    w = UploadReview()
    w.set_window_show()


@utl_modifiers.set_method_exception_catch
def main(session):
    rsv_task = session.rsv_obj
    branch = rsv_task.get('branch')
    #
    window_title = 'Upload Review'
    #
    rsv_task_version_unit = rsv_task.get_rsv_unit(
        keyword='{}-version-dir'.format(branch)
    )
    #
    version = rsv_task_version_unit.get_new_version()
    kwargs = rsv_task.properties.get_copy_value()
    kwargs['version'] = version
    if branch == 'asset':
        content = (
            'upload review to\n'
            'version: "{asset}.{step}.{task}.{version}"\n'
            'press "Yes" to continue...'
        ).format(
            **kwargs
        )
    elif branch == 'shot':
        content = (
            'upload review to\n'
            'version: "{shot}.{step}.{task}.{version}"\n'
            'press "Yes" to continue...'
        ).format(
            **kwargs
        )
    else:
        raise TypeError()

    w = utl_core.DialogWindow.set_create(
        window_title,
        content=content,
        yes_method=yes_method,
        window_size=(480, 320),
        use_exec=False
    )
    # w.set_options_group_enable()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
