from mcdreforged.api.types import PluginServerInterface, InfoCommandSource
from mcdreforged.api.rtext import RText, RTextList, RAction

import re

server = PluginServerInterface.get_instance()

float_compile = re.compile(r'^0\.\d*$')

def tr(tag: str, *args, **kwargs):
    return PluginServerInterface.get_instance().tr(f'xp_helper.{tag}', *args, **kwargs)

def run_command_with_rcon(command: str) -> str:
    if not server.is_rcon_running():
        server.logger.warning("Please config rcon of server correctly.")
        return None
    return server.rcon_query(command)

def get_player_list() -> list:
    res = run_command_with_rcon('list').split(": ")[1]
    if res:
        return res.split(", ")
    else:
        return []

def get_player_info(src: InfoCommandSource, player: str, path: str):
    MCDataAPI = server.get_plugin_instance('minecraft_data_api')
    res = run_command_with_rcon(f'data get entity {player} {path}')
    if res.startswith("Found no elements"):
        return None
    else:
        return MCDataAPI.convert_minecraft_json(res)

def ask_for_sure(src):
    if src.is_console:
        src.reply(RTextList(tr("ask_sure"), "\n",
            RText(tr("confirm_in_console", command=src.get_info().content + " SURE")),
        ))
    else:
        src.reply(RTextList(tr("ask_sure"), "\n",
            RText(tr("click_to_confirm")).c(RAction.suggest_command, src.get_info().content + " SURE"),
        ))
