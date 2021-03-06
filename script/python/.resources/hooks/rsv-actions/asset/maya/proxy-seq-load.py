# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects
#
import lxmaya.dcc.dcc_objects as mya_dcc_objects
#
file_path = session.rsv_unit.get_result(
    version='latest'
)
if file_path:
    _file = utl_dcc_objects.OsFile(file_path)
    _path_base = _file.path_base
    _seq_file_path = '{}.####.ass'.format(_path_base)
    _seq_file = utl_dcc_objects.OsFile(_seq_file_path)
    _name = '{asset}__ass'.format(
        **session.variants
    )
    _obj = mya_dcc_objects.Shape(_name)
    if _obj.get_is_exists() is False:
        _obj = _obj.set_create('aiStandIn')
    #
    _seq_file_paths = _seq_file.get_exists_file_paths()
    if _seq_file_paths:
        atr_raw = dict(
            dso=_seq_file_paths[0],
            mode=6,
            useFrameExtension=1
        )
    else:
        atr_raw = dict(
            dso=file_path,
            mode=6
        )
    [_obj.get_port(k).set(v) for k, v in atr_raw.items()]
