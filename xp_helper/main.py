from mcdreforged.api.types import PluginServerInterface, InfoCommandSource
from mcdreforged.api.command import Integer, Float, Text, Boolean, Literal
from mcdreforged.api.rtext import RText, RTextList, RAction

from xp_helper.handles.xp_info import xp_info_with_player, xp_info_without_player
from xp_helper.handles.xp_drop import xp_drop_with_player_all, xp_drop_with_player_amount_rate, \
                                        xp_drop_without_player_all, xp_drop_without_player_amount_rate
from xp_helper.handles.xp_move import xp_move_with_source, xp_move_without_source
from xp_helper.handles.xp_repair import xp_repair_with_player_all, xp_repair_with_player_rate, \
                                        xp_repair_without_player_all, xp_repair_without_player_rate, \
                                        xp_auto_repair_without_player_status, xp_auto_repair_without_player_set_status, \
                                        xp_auto_repair_with_player_status, xp_auto_repair_with_player_set_status, \
                                        xp_auto_repair, stop_xp_auto_repair
from xp_helper.utils.common import tr, server
from xp_helper.config import config

PERFIX = "!!xp"


def on_load(server: PluginServerInterface, prev_module):
    server.register_help_message(PERFIX, tr("desc"))
    register_command()
    if server.is_server_startup():
        xp_auto_repair()

def on_unload(server: PluginServerInterface):
    stop_xp_auto_repair()

def on_server_startup(server: PluginServerInterface):
    xp_auto_repair()

def on_server_stop(server: PluginServerInterface, server_return_code: int):
    stop_xp_auto_repair()

def print_help_msg(src: InfoCommandSource):
    helper_msg = player_msg = RText("")

    if src.has_permission_higher_than(config.helper_permission): # helper
        helper_msg = RTextList(
            "§a------------- %s -------------§r\n" % (tr("helper-command")),
            RText(f"§7{PERFIX} info <player>: §r").c(RAction.suggest_command, f"{PERFIX} info "), tr('command-desc.info-helper'), "\n",
            RText(f"§7{PERFIX} move <target> <source> <amount>: §r").c(RAction.suggest_command, f"{PERFIX} move "), tr('command-desc.move-helper'), "\n",
            RText(f"§7{PERFIX} drop <player> <all|amount|rate>: §r").c(RAction.suggest_command, f"{PERFIX} drop "), tr('command-desc.drop-helper'), "\n",
            RText(f"§7{PERFIX} repair <player> <all|rate>: §r").c(RAction.suggest_command, f"{PERFIX} repair "), tr('command-desc.repair-helper'), "\n",
            RText(f"§7{PERFIX} repair <player> auto (true|false): §r").c(RAction.suggest_command, f"{PERFIX} repair "), tr('command-desc.repair-auto-helper'), "\n",
            RText(f"§7{PERFIX} reload: §r").c(RAction.suggest_command, f"{PERFIX} reload"), tr('command-desc.reload'), "\n",
        )
    
    if src.is_player:
        player_msg = RTextList(
            RText(f"§7{PERFIX}: §r").c(RAction.suggest_command, f"{PERFIX}"), tr('command-desc.root'), "\n",
            RText(f"§7{PERFIX} info: §r").c(RAction.suggest_command, f"{PERFIX} info"), tr('command-desc.info'), "\n",
            RText(f"§7{PERFIX} move <target> <amount>: §r").c(RAction.suggest_command, f"{PERFIX} move "), tr('command-desc.move'), "\n",
            RText(f"§7{PERFIX} drop <all|amount|rate>: §r").c(RAction.suggest_command, f"{PERFIX} drop "), tr('command-desc.drop'), "\n",
            RText(f"§7{PERFIX} repair <all|rate>: §r").c(RAction.suggest_command, f"{PERFIX} repair all"), tr('command-desc.repair'), "\n",
            RText(f"§7{PERFIX} repair auto (true|false): §r").c(RAction.suggest_command, f"{PERFIX} repair auto "), tr('command-desc.repair-auto'), "\n",
        )
    
    src.reply(RTextList(
        "§a================= Xp Helper =================§r\n",
        player_msg,
        helper_msg,
        "§9§o======= Powered by Xp Helper v%s  =======§r" % (server.as_plugin_server_interface().get_self_metadata().version)
    ))

def sure_func(func: callable):
    def ret(src, ctx):
        func(src, ctx, True)
    return ret

def register_command():
    permission_check = lambda src: src.has_permission_higher_than(config.helper_permission)
    is_player = lambda src: src.is_player
    server.as_plugin_server_interface().register_command(
        Literal(PERFIX).runs(print_help_msg).
        then(
            Literal("info").runs(xp_info_without_player).
            then(
                Text("player").requires(permission_check).runs(xp_info_with_player)
            )
        ).then(
            Literal("move").then(
                Text("target").then(
                    Text("amount/source").runs(xp_move_without_source).
                    then(
                        Literal("SURE").runs(sure_func(xp_move_without_source))
                    ).then(
                        Integer("amount").requires(permission_check).runs(xp_move_with_source).
                        then(
                            Literal("SURE").runs(sure_func(xp_move_with_source))
                        )
                    )
                )
            )
        ).then(
            Literal("drop").then(
                Literal("all").requires(is_player).runs(xp_drop_without_player_all).
                then(
                    Literal("SURE").runs(sure_func(xp_drop_without_player_all))
                )
            ).then(
                Text("amount/rate/player").runs(xp_drop_without_player_amount_rate).
                then(
                    Literal("SURE").runs(sure_func(xp_drop_without_player_amount_rate))
                ).then(
                    Literal("all").requires(permission_check).runs(xp_drop_with_player_all).
                    then(
                        Literal("SURE").runs(sure_func(xp_drop_with_player_all))
                    )
                ).then(
                    Text("amount/rate").requires(permission_check).runs(xp_drop_with_player_amount_rate).
                    then(
                        Literal("SURE").runs(sure_func(xp_drop_with_player_amount_rate))
                    )
                )
            )
        ).then(
            Literal("repair").then(
                Literal("all").requires(is_player).runs(xp_repair_without_player_all).
                then(
                    Literal("SURE").runs(sure_func(xp_repair_without_player_all))
                )
            ).then(
                Literal("auto").requires(is_player).runs(xp_auto_repair_without_player_status).
                then(
                    Boolean("value").runs(xp_auto_repair_without_player_set_status)
                )
            ).then(
                Text("rate/player").runs(xp_repair_without_player_rate).
                then(
                    Literal("SURE").requires(is_player).runs(sure_func(xp_repair_without_player_rate))
                ).then(
                    Literal("all").requires(permission_check).runs(xp_repair_with_player_all).
                    then(
                        Literal("SURE").runs(sure_func(xp_repair_with_player_all))
                    )
                ).then(
                    Literal("auto").requires(permission_check).runs(xp_auto_repair_with_player_status).then(
                        Boolean("value").runs(xp_auto_repair_with_player_set_status)
                    )
                ).then(
                    Float("rate").requires(permission_check).runs(xp_repair_with_player_rate).
                    then(
                        Literal("SURE").runs(sure_func(xp_repair_with_player_rate))
                    )
                )
            )
        ).then(
            Literal("reload").requires(permission_check).runs(lambda src: server.
            reload_plugin(server.as_plugin_server_interface().get_self_metadata().id))
        )
    )
