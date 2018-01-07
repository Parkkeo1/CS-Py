# import os
#
#
# def find(name, path):
#     for root, dirs, files in os.walk(path):
#         if name in files:
#             return os.path.join(root, name)


import winreg as registry
from shutil import copyfile

key = registry.CreateKey(registry.HKEY_CURRENT_USER, "Software\Valve\Steam")
steam_path = registry.QueryValueEx(key, "SteamPath")[0]

steam_path = steam_path + '/steamapps/common/Counter-Strike Global Offensive/csgo/cfg'

src = 'gamestate_integration_main.cfg'
dst = steam_path + '/gamestate_integration_main.cfg'

copyfile(src, dst)

