from mcdreforged.api.types import InfoCommandSource


from xp_helper.utils.player_xp import move_player_xp
from xp_helper.utils.common import get_player_list, tr, server, ask_for_sure




def xp_move_handle(src: InfoCommandSource, target: str, source: str, amount: int):
    player_list = get_player_list()
    move_player_xp(src, target, source, amount)

def xp_move_without_source(src: InfoCommandSource, ctx, sure=False):
    if src.is_console:
        src.reply(tr("cannot_use_in_console"))
        return

    if ctx["target"] not in get_player_list():
        src.reply(tr("player_not_found"))
        return

    if not ctx["amount/source"].isdigit():
        src.reply(tr("invalid_number", num=ctx["amount/source"]))
        return

    if sure:
        xp_move_handle(src, ctx["target"], src.get_info().player, int(ctx["amount/source"]))
    else:
        ask_for_sure(src)

def xp_move_with_source(src: InfoCommandSource, ctx, sure=False):
    player_list = get_player_list()
    if not (ctx["target"] in player_list and ctx["amount/source"] in player_list):
        src.reply(tr("player_not_found"))
        return
    
    if sure:
        xp_move_handle(src, ctx["target"], ctx["amount/source"], int(ctx["amount"]))
    else:
        ask_for_sure(src)