# coding:utf-8


def main(session):
    file_path = session.rsv_unit.get_result(
        version='latest'
    )
    if file_path:
        import lxmaya.fnc.importers as mya_fnc_importers

        mya_fnc_importers.CameraAbcImporter(
            option=dict(
                file=file_path,
                location='/cameras'
            )
        ).set_run()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
