from mcdreforged.api.types import InfoCommandSource


from xp_helper.utils.player_xp import get_player_xp
from xp_helper.utils.xp_convert import get_level_by_point
from xp_helper.utils.item_durability import get_require_point_by_durability
from xp_helper.utils.player_item import get_player_durability_value
from xp_helper.utils.common import get_player_list, tr, server

def xp_info_handle(src: InfoCommandSource, player: str):
    point = get_player_xp(src, player)
    level = get_level_by_point(point)
    durability = get_player_durability_value(src, player)
    need = get_require_point_by_durability(durability)
    src.reply(tr("command.info", player=player, point=point, level=level, durability=durability, need=need))
    if point >= need:
        src.reply(tr("xp_enough", player=player, after=get_level_by_point(point - need)))
    else:
        src.reply(tr("xp_not_enough", player=player, after=get_level_by_point(point + need)))

def xp_info_without_player(src: InfoCommandSource):
    if src.is_console:
        src.reply(tr("cannot_use_in_console"))
        return
    xp_info_handle(src, src.get_info().player)

def xp_info_with_player(src: InfoCommandSource, ctx):
    if ctx["player"] in get_player_list():
        xp_info_handle(src, ctx["player"])
    else:
        src.reply(tr("player_not_found"))