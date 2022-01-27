# coding:utf-8


def main(session):
    import lxmaya_fnc.scripts as mya_fnc_scripts
    #
    mya_fnc_scripts.set_look_preview_export_by_any_scene_file(
        session.option
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
