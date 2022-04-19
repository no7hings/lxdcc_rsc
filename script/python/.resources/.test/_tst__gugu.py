# coding:utf-8


def set_send_to_gugu(user, file_path):
    import urllib

    from lxbasic import bsc_core

    windows_file_path = bsc_core.StoragePathMtd.set_map_to_windows(file_path)

    linux_file_path = bsc_core.StoragePathMtd.set_map_to_linux(file_path)

    windows_cmd = '{} {}'.format('pgrv', windows_file_path)

    linux_cmd = '{} {}'.format('pgrv', linux_file_path)

    c = '{}::{}::{}'.format(
        'open movie',
        linux_cmd,
        windows_cmd
    )

    c = c.decode('utf-8')

    flag_dict = {
        'from': user,
        'to': user,
        'content': 'PG Render task is completed\nmovie is\n"{}"\n"{}'.format(
            windows_file_path, linux_file_path
        ),
        'command': c,
        'msg_type': 'command'
    }

    notify_url = 'http://cg-ark.papegames.com:61112/notify'
    flag = urllib.urlencode(flag_dict)
    url = '?'.join([notify_url, flag])

    urllib.urlopen(url)


if __name__ == '__main__':
    user = 'dongchangbao'
    file_path = '/l/prod/cgm/output/assets/chr/nn_4y_test/mod/modeling/nn_4y_test.mod.modeling.v012/render/katana-images/main/close_up.master.all.white_disp.custom.mov'
    set_send_to_gugu(user, file_path)
