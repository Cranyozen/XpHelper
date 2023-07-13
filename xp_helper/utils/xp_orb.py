from mcdreforged.api.types import InfoCommandSource

from xp_helper.utils.common import server
from xp_helper.config import config

import time

# config.orb_value = [2477, 1237, 617, 307, 149, 73, 37, 17, 7, 3, 1]

def summon_xp_orb_direct(src: InfoCommandSource, player: str, amount: int):
    server.execute(f"execute at {player} run summon minecraft:experience_orb ~ ~1 ~ {{Value:{amount}}}")

def summon_xp_orb(src: InfoCommandSource, player: str, amount: int):
    for value, amount in split_amount(amount).items():
        if amount == 0:
            continue
        for _ in range(amount):
            server.execute(f"execute at {player} run summon minecraft:experience_orb ~ ~1 ~ {{Value:{value}}}")
            time.sleep(config.summon_interval)

def split_amount(amount: int) -> list:
    orb_list = {}
    for value in config.orb_value:
        orb_list[value] = amount // value
        amount %= value
    return orb_list
