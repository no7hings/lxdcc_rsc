# coding:utf-8
name = 'lxdcc_rsc'

version = '0.0.111'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    import platform
    # resources
    env.LYNXI_RESOURCES.append('{root}/script/python/.resources')
    # arnold-setup
    env.ARNOLD_PLUGIN_PATH.append('{root}/script/python/.setup/arnold/shaders')
    # maya-arnold-resources
    env.LYNXI_MAYA_RESOURCES.append('{root}/script/python/.setup/arnold/maya')
    # customize-arnold-shaders
    if platform.system() == 'Linux':
        env.ARNOLD_PLUGIN_PATH.append('/l/resource/osl_shader')
    elif platform.system() == 'Windows':
        env.ARNOLD_PLUGIN_PATH.append('l:/resource/osl_shader')


timestamp = 1639363837

format_version = 2
