from mcdreforged.api.types import InfoCommandSource

from xp_helper.utils.item_durability import check_item
from xp_helper.utils.common import get_player_info
from xp_helper.config import config

REPAIR_SLOT = ["100", "101", "102", "103", "-106"]

def get_player_all_item(src: InfoCommandSource, player: str) -> list:
    return list(get_player_info(src, player, "Inventory"))

def get_player_durability_item(src: InfoCommandSource, player: str) -> list:
    item_list = []

    for item in get_player_all_item(src, player):
        if check_item(item["id"]):
            item_list.append(item)
    return item_list

def get_player_durability_value(src: InfoCommandSource, player: str) -> int:
    total_value = 0

    for item in get_player_all_item(src, player):
        if check_item(item["id"]) and item.get("tag", False) and item["tag"].get("Enchantments", False) and \
                "minecraft:mending" in list(map(lambda x: x["id"], item["tag"]["Enchantments"])):
            total_value += item["tag"]["Damage"]
    return int(total_value * config.repair_rate)

def get_player_selected_item_slot(src: InfoCommandSource, player: str) -> int:
    return int(get_player_info(src, player, "SelectedItemSlot"))

def get_player_slot_item(src: InfoCommandSource, player: str, slot: int) -> dict:
    return get_player_info(src, player, f'Inventory[{{Slot:{slot}b}}]')

def get_player_hand_item_id(src: InfoCommandSource, player: str) -> dict:
    return get_player_slot_item(src, player, get_player_selected_item_slot(src, player))

def get_player_repair_durability_value(src: InfoCommandSource, player: str) -> int:
    total_value = 0

    item = get_player_hand_item_id(src, player)
    if item and check_item(item["id"]) and item.get("tag", False) and item["tag"].get("Enchantments", False) and \
            "minecraft:mending" in list(map(lambda x: x["id"], item["tag"]["Enchantments"])):
        total_value += item["tag"]["Damage"]

    for slot in REPAIR_SLOT:
        item = get_player_slot_item(src, player, slot)
        if item and check_item(item["id"]) and item.get("tag", False) and item["tag"].get("Enchantments", False) and \
                "minecraft:mending" in list(map(lambda x: x["id"], item["tag"]["Enchantments"])):
            total_value += item["tag"]["Damage"]
    
    return int(total_value * config.repair_rate)
