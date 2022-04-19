# coding:utf-8


def main(session):
    import lxmaya.fnc.importers as mya_fnc_importers
    #
    file_path = session.rsv_unit.get_result(
        version='latest'
    )
    if file_path:
        _properties = session.rsv_properties
        _branch = _properties.get('branch')
        _look_pass_name = _properties.get(_branch)
        mya_fnc_importers.LookAssImporter(
            option=dict(
                file=file_path,
                location='/master',
                look_pass=_look_pass_name,
                assign_selection=True
            )
        ).set_run()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
