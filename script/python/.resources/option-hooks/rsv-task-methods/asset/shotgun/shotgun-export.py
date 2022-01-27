# coding:utf-8


def main(session):
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    stg_fnc_scripts.set_shotgun_export_by_any_scene_file(
        session.option
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
