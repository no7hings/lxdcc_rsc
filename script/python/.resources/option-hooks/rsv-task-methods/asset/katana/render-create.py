# coding:utf-8


def main(session):
    import lxkatana_fnc.scripts as ktn_fnc_scripts
    #
    ktn_fnc_scripts.set_render_create_by_any_scene_file(
        session.option
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
