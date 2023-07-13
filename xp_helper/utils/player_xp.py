from mcdreforged.api.types import InfoCommandSource

from xp_helper.utils.xp_convert import get_level_by_point
from xp_helper.utils.common import tr, get_player_info, server

def get_player_xp(src: InfoCommandSource, player: str) -> int:
    return int(get_player_info(src, player, "XpTotal"))

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
