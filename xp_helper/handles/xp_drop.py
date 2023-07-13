from mcdreforged.api.types import InfoCommandSource

from xp_helper.utils.player_xp import remove_player_xp, get_player_xp
from xp_helper.utils.xp_convert import get_level_by_point
from xp_helper.utils.xp_orb import summon_xp_orb, summon_xp_orb_direct
from xp_helper.utils.common import tr, float_compile, ask_for_sure, get_player_list, server
from xp_helper.config import config




def xp_drop_handle(src: InfoCommandSource, player: str, point: int):
    remove_player_xp(src, player, point)
    src.reply(tr("command.drop.process", player=player, point=point))
    if config.summon_orb_direct:
        summon_xp_orb_direct(src, player, point)
    else:
        summon_xp_orb(src, player, point)
    src.reply(tr("command.drop.success", player=player, point=point))

def xp_drop_without_player_all(src: InfoCommandSource, ctx, sure=False):
    if src.is_console:
        src.reply(tr("cannot_use_in_console"))
        return
    
    player = src.get_info().player
    point = get_player_xp(src, player)

    if sure:
        xp_drop_handle(src, player, point)
    else:
        ask_for_sure(src)

def xp_drop_without_player_amount_rate(src: InfoCommandSource, ctx, sure=False):
    if src.is_console:
        src.reply(tr("cannot_use_in_console"))
        return
    
    player = src.get_info().player
    if float_compile.match(ctx["amount/rate/player"]): # rate
        point = int(get_player_xp(src, player) * float(ctx["amount/rate/player"]))
    elif ctx["amount/rate/player"].isdigit(): # amount
        point = int(ctx["amount/rate/player"])
        if get_player_xp(src, player) < point:
            src.reply(tr("xp_not_enough", player=player, after=get_level_by_point(point)))
            return
    else:
        src.reply(tr("invalid_number", num=ctx["amount/rate/player"]))
        return
    
    if sure:
        xp_drop_handle(src, player, point)
    else:
        ask_for_sure(src)


def xp_drop_with_player_all(src: InfoCommandSource, ctx, sure=False):
    player = ctx["amount/rate/player"]
    if player not in get_player_list():
        src.reply(tr("player_not_found"))
        return
    
    point = get_player_xp(src, player)

    if sure:
        xp_drop_handle(src, player, point)
    else:
        ask_for_sure(src)

def xp_drop_with_player_amount_rate(src: InfoCommandSource, ctx, sure=False):
    player = ctx["amount/rate/player"]
    if player not in get_player_list():
        src.reply(tr("player_not_found"))
    if float_compile.match(ctx["amount/rate"]): # rate
        point = int(get_player_xp(src, player) * float(ctx["amount/rate"]))
    elif ctx["amount/rate"].isdigit(): # amount
        point = int(ctx["amount/rate"])
        if get_player_xp(src, player) < point:
            src.reply(tr("xp_not_enough", player=player, after=get_level_by_point(point)))
            return
    else:
        src.reply(tr("invalid_number", num=ctx["amount/rate"]))
        return
    
    if sure:
        xp_drop_handle(src, player, point)
    else:
        ask_for_sure(src)