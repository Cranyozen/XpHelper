from mcdreforged.api.types import InfoCommandSource

from xp_helper.utils.xp_convert import get_level_by_point, get_point_by_level
from xp_helper.utils.common import tr, get_player_info, server, run_command_with_rcon

import re

xp_query_re_compile = re.compile("^.*? has (\d*) experience (levels|points)$")

def get_player_xp(src: InfoCommandSource, player: str) -> int:
    level = xp_query_re_compile.match(run_command_with_rcon(f"xp query {player} levels"))
    point = xp_query_re_compile.match(run_command_with_rcon(f"xp query {player} points"))
    print(level.group(1), point.group(1))
    if not (level and point):
        return 0
    return int(get_point_by_level(int(level.group(1))) + int(point.group(1))) + 1

def remove_player_xp(src: InfoCommandSource, player: str, amount: int):
    if amount < 0:
        src.reply(tr("invalid_number", num=amount))

    player_point = get_player_xp(src, player)
    if player_point < amount:
        src.reply(tr("xp_not_enough", player=player, after=get_level_by_point(amount)))
        return False

    server.execute(f"xp add {player} -{amount} points")
    return True

def add_player_xp(src: InfoCommandSource, player: str, amount: int):
    if amount < 0:
        src.reply(tr("invalid_number", num=amount))

    server.execute(f"xp add {player} {amount} points")
    return True

def move_player_xp(src: InfoCommandSource, target: str, source: str, amount: int):
    if target == source:
        src.reply(tr("command.move.same_player"))
        return
    if remove_player_xp(src, source, amount):
        add_player_xp(src, target, amount)
        src.reply(tr("command.move.success", source=source, target=target, point=amount))
