# coding:utf-8


def main(session):
    import lxusd_fnc.scripts as usd_fnc_scripts
    #
    usd_fnc_scripts.set_usd_create_by_any_scene_file(
        session.option
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
