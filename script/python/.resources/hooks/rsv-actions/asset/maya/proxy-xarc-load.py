# coding:utf-8
file_path = session.rsv_unit.get_result(
    version='latest',
    extend_variants=dict(
        look_pass='default',
        act='static'
    )
)
if file_path:
    print file_path
