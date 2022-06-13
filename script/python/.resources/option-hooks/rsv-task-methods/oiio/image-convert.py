# coding:utf-8


def main(session):
    from lxbasic import bsc_core

    from lxutil import utl_core

    hook_option_opt = session.option_opt

    image_file_path = hook_option_opt.get('image_file')
    output_image_file_path = hook_option_opt.get('output_image_file')

    if bsc_core.StorageFileOpt(
        image_file_path
    ).get_is_file() is True:
        bsc_core.ImageOpt(image_file_path).set_convert_to(
            output_image_file_path
        )
    else:
        raise RuntimeError(
            utl_core.Log.set_module_error_trace(
                'file="{}" is non-exists'.format(image_file_path)
            )
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
