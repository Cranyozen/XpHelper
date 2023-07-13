from mcdreforged.api.types import InfoCommandSource, ConsoleCommandSource
from mcdreforged.api.decorator import new_thread

from xp_helper.utils.player_xp import get_player_xp
from xp_helper.utils.player_item import get_player_durability_value, get_player_repair_durability_value
from xp_helper.utils.xp_convert import get_level_by_point
from xp_helper.utils.item_durability import get_require_point_by_durability
from xp_helper.utils.common import tr, ask_for_sure, get_player_list, float_compile, server
from xp_helper.config import config
from xp_helper.handles.xp_drop import xp_drop_handle

import time
import threading

auto_repair_running = True

@new_thread("XpHelper_Repair")
def xp_repair_handle(src: InfoCommandSource, player: str, max_point=None):
    begin_time = time.time()
    total_point = 0
    while time.time() - begin_time <= config.repair_max_time:
        if get_player_durability_value(src, player) == 0:
            src.reply(tr("command.repair.break"))
            break
        durability = int(get_player_repair_durability_value(src, player))
        if durability == 0:
            continue
        point = int(get_require_point_by_durability(durability))
        if get_player_xp(src, player) < point:
            src.reply(tr("xp_not_enough", player=player, after=get_level_by_point(point)))
            src.reply(tr("command.repair.break"))
            break
        
        begin_time = time.time()
        xp_drop_handle(src, player, point)
        total_point += point
        if max_point and total_point >= max_point:
            break
        time.sleep(config.repair_interval)
    src.reply(tr("command.repair.success", player=player, total=total_point))

class fake_src:
    def __init__(self, player):
        self.player = player
    def reply(self, msg):
        server.tell(self.player, msg)

@new_thread("XpHelper_AutoRepair")
def xp_auto_repair():
    while auto_repair_running:
        for player in get_player_list():
            if player in config.auto_repair_player_list:
                durability = int(get_player_repair_durability_value(fake_src(player), player))
                if durability > 0:
                    point = get_require_point_by_durability(durability)
                    if get_player_xp(fake_src(player), player) < get_require_point_by_durability(durability):
                        server.tell(player, tr("xp_not_enough", player=player, after=get_level_by_point(point)))
                        continue
                    xp_drop_handle(fake_src(player), player, point)
        time.sleep(config.auto_repair_interval)
    return

def stop_xp_auto_repair():
    global auto_repair_running
    auto_repair_running = False

def xp_repair_without_player_all(src: InfoCommandSource, ctx, sure=False):
    if src.is_console:
        src.reply(tr("cannot_use_in_console"))
        return
    player = src.get_info().player
    point = get_player_xp(src, player)
    level = get_level_by_point(point)
    durability = get_player_durability_value(src, player)
    need = get_require_point_by_durability(durability)
    src.reply(tr("command.info", player=player, point=point, level=level, durability=durability, need=need))
    if point < need:
        src.reply(tr("xp_not_enough", player=player, after=get_level_by_point(point + need)))
        return
    else:
        src.reply(tr("xp_enough", player=player, after=get_level_by_point(point - need)))

    if sure:
        xp_repair_handle(src, player)
    else:
        ask_for_sure(src)

def xp_repair_without_player_rate(src: InfoCommandSource, ctx, sure=False):
    if src.is_console:
        src.reply(tr("cannot_use_in_console"))
        return
    player = src.get_info().player
    if not float_compile.match(ctx["rate/player"]): # rate
        src.reply(tr("invalid_number", num=ctx["rate/player"]))
        return
    point = get_player_xp(src, player)
    level = get_level_by_point(point)
    durability = int(get_player_durability_value(src, player) * float(ctx["rate/player"]))
    need = get_require_point_by_durability(durability)
    src.reply(tr("command.info", player=player, point=point, level=level, durability=durability, need=need))
    if point < need:
        src.reply(tr("xp_not_enough", player=player, after=get_level_by_point(point + need)))
        return
    else:
        src.reply(tr("xp_enough", player=player, after=get_level_by_point(point - need)))

    if sure:
        xp_repair_handle(src, player, int(need * config.repair_max_point_rate))
    else:
        ask_for_sure(src)

def xp_repair_with_player_all(src: InfoCommandSource, ctx, sure=False):
    player = ctx["rate/player"]
    if player not in get_player_list():
        src.reply(tr("player_not_found"))
        return
    point = get_player_xp(src, player)
    level = get_level_by_point(point)
    durability = get_player_durability_value(src, player)
    need = get_require_point_by_durability(durability)
    src.reply(tr("command.info", player=player, point=point, level=level, durability=durability, need=need))
    if point < need:
        src.reply(tr("xp_not_enough", player=player, after=get_level_by_point(point + need)))
        return
    else:
        src.reply(tr("xp_enough", player=player, after=get_level_by_point(point - need)))

    if sure:
        xp_repair_handle(src, player)
    else:
        ask_for_sure(src)

def xp_repair_with_player_rate(src: InfoCommandSource, ctx, sure=False):
    player = ctx["rate/player"]
    if player not in get_player_list():
        src.reply(tr("player_not_found"))
        return
    point = get_player_xp(src, player)
    level = get_level_by_point(point)
    durability = int(get_player_durability_value(src, player) * ctx["rate"])
    need = get_require_point_by_durability(durability)
    src.reply(tr("command.info", player=player, point=point, level=level, durability=durability, need=need))
    if point < need:
        src.reply(tr("xp_not_enough", player=player, after=get_level_by_point(point + need)))
        return
    else:
        src.reply(tr("xp_enough", player=player, after=get_level_by_point(point - need)))

    if sure:
        xp_repair_handle(src, player, int(need * config.repair_max_point_rate))
    else:
        ask_for_sure(src)

def xp_auto_repair_without_player_status(src: InfoCommandSource):
    player = src.get_info().player
    if player in config.auto_repair_player_list:
        src.reply(tr("command.auto_repair.info", player=player, status=tr("command.auto_repair.status.on")))
    else:
        src.reply(tr("command.auto_repair.info", player=player, status=tr("command.auto_repair.status.off")))

def xp_auto_repair_without_player_set_status(src: InfoCommandSource, ctx):
    player = src.get_info().player
    if ctx["value"]:
        if player in config.auto_repair_player_list:
            src.reply(tr("command.auto_repair.already", player=player, status=tr("command.auto_repair.status.on")))
        else:
            config.auto_repair_player_list.append(player)
            src.reply(tr("command.auto_repair.set", player=player, status=tr("command.auto_repair.status.on")))
    else:
        if player in config.auto_repair_player_list:
            config.auto_repair_player_list.remove(player)
            src.reply(tr("command.auto_repair.set", player=player, status=tr("command.auto_repair.status.off")))
        else:
            src.reply(tr("command.auto_repair.already", player=player, status=tr("command.auto_repair.status.off")))
    server.as_plugin_server_interface().save_config_simple(config)

def xp_auto_repair_with_player_status(src: InfoCommandSource, ctx):
    player = ctx["rate/player"]
    if player in config.auto_repair_player_list:
        src.reply(tr("command.auto_repair.info", player=player, status=tr("command.auto_repair.status.on")))
    else:
        src.reply(tr("command.auto_repair.info", player=player, status=tr("command.auto_repair.status.off")))

def xp_auto_repair_with_player_set_status(src: InfoCommandSource, ctx):
    player = ctx["rate/player"]
    if ctx["value"]:
        if player in config.auto_repair_player_list:
            src.reply(tr("command.auto_repair.already", player=player, status=tr("command.auto_repair.status.on")))
        else:
            config.auto_repair_player_list.append(player)
            src.reply(tr("command.auto_repair.set", player=player, status=tr("command.auto_repair.status.on")))
    else:
        if player in config.auto_repair_player_list:
            config.auto_repair_player_list.remove(player)
            src.reply(tr("command.auto_repair.set", player=player, status=tr("command.auto_repair.status.off")))
        else:
            src.reply(tr("command.auto_repair.already", player=player, status=tr("command.auto_repair.status.off")))
    server.as_plugin_server_interface().save_config_simple(config)