# coding:utf-8


def main(session):
    from lxutil import utl_core

    utl_core.SubProcessRunner.set_run_with_result_use_thread(
        'rez-env lxdcc -- lxhook-command -o "option_hook_key=tool-panels/asset-render-submitter&file=/l/prod/cgm/work/assets/chr/nn_14y_test/mod/modeling/maya/scenes/nn_14y_test.mod.modeling.v006.ma"'
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
