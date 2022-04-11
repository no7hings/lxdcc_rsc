# coding:utf-8


def main(session):
    import lxutil_gui.panel.utl_pnl_widgets as utl_pnl_widgets
    file_path = session.rsv_unit.get_result(
        version='latest'
    )
    if file_path:
        hook_option = 'file={}'.format(file_path)
        w = utl_pnl_widgets.AssetRenderSubmitter(hook_option=hook_option)
        w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)


'rez-env lxdcc -- lxhook-engine -o "application=katana&asset=heidong&cameras=close_up+full_body&choice_scheme=asset-surface-katana-output&file=/l/prod/xkt/work/assets/chr/heidong/srf/surfacing/katana/heidong.srf.surfacing.v078.katana&hook_engine=python&layers=master&light_passes=all&look_passes=default+plastic&option_hook_key=rsv-task-batchers/asset/gen-cmb-render-submit&project=xkt&qualities=custom&render_asset_frames=1001+1011+1021+1031+1041+1051+1061+1071+1081+1091+1101+1111+1121+1131+1141+1151+1161+1171+1181+1191+1201+1211+1221+1231+1240&render_shot_frames=1001+1002+1003+1004+1005+1006+1007+1008+1009+1010+1011+1012+1013+1014+1015+1016+1017+1018+1019+1020+1021+1022+1023+1024+1025+1026+1027+1028+1029+1030+1031+1032+1033+1034+1035+1036+1037+1038+1039+1040+1041+1042+1043+1044+1045+1046+1047+1048+1049+1050+1051+1052+1053+1054+1055+1056+1057+1058+1059+1060+1061+1062+1063+1064+1065+1066+1067+1068+1069+1070+1071+1072+1073+1074+1075+1076+1077+1078+1079+1080+1081+1082+1083+1084+1085+1086+1087+1088+1089+1090+1091+1092+1093+1094+1095+1096+1097+1098+1099+1100+1101+1102+1103+1104+1105+1106+1107+1108+1109+1110+1111+1112+1113+1114+1115+1116+1117+1118+1119+1120+1121+1122+1123+1124+1125+1126+1127+1128+1129+1130+1131+1132+1133+1134+1135+1136+1137+1138+1139+1140+1141+1142+1143+1144+1145+1146+1147+1148+1149+1150+1151+1152+1153+1154+1155+1156+1157+1158+1159+1160+1161+1162+1163+1164+1165+1166+1167+1168+1169+1170+1171+1172&rez_beta=True&shot=s10170&shot_asset=&step=srf&task=surfacing&time_tag=2022_0404_1831_13_847910&user=dongchangbao&version=v078&workspace=work&start_index=<STARTFRAME>&end_index=<ENDFRAME>"'
'rez-env lxdcc -- lxhook-engine -o "application=katana&asset=heidong&choice_scheme=asset-surface-katana-output&choice_scheme_includes=asset-*-maya-output+asset-*-katana-output&dependencies=../maya/gen-scene-export+../maya/gen-geometry-export+../maya/gen-hair-export+../katana/gen-geometry-export+../katana/gen-look-export+rsv-task-batchers/asset/gen-cmb-render-submit&file=/l/prod/xkt/output/assets/chr/heidong/srf/surfacing/heidong.srf.surfacing.v005/scene/heidong.katana&hook_engine=usd&option_hook_key=rsv-task-methods/asset/usd/gen-usd-create&project=xkt&rez_beta=True&step=srf&task=surfacing&td_enable=False&time_tag=2022_0404_1831_13_847910&user=dongchangbao&version=v005&with_component_usd=True&workspace=output&start_index=<STARTFRAME>&end_index=<ENDFRAME>"'
