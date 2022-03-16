# coding:utf-8


def main(session):
    from lxutil import utl_core

    hook_option_opt = session.option_opt

    cmd = '/opt/rv/bin/rvio "{image_file}" -overlay frameburn .4 1.0 30.0 -dlut "{lut_directory}" -o "{movie_file}" -comment "{user}" -outparams timecode={start_frame}'.format(
        **hook_option_opt.get_raw()
    )

    utl_core.SubProcessRunner.set_run_with_result(
        cmd
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
