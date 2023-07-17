"""物品耐久工具"""
from xp_helper.config import *

# Data from https://minecraft.fandom.com/wiki/Durability

# Armor durability
# Material	Helmet	Chestplate	Leggings	Boots
# Turtle Shell	275	N/A	N/A	N/A
# Leather	55	80	75	65
# Golden	77	112	105	91
# Chainmail	165	240	225	195
# Iron	165	240	225	195
# Diamond	363	528	495	429
# Netherite	407	592	555	481

ARMOR_DURABILITY = {
    "turtle": {
        "helmet": 275
    },
    "leather": {
        "helmet": 55, "chestplate": 80, "leggings": 75, "boots": 65
    },
    "golden": {
        "helmet": 77, "chestplate": 112, "leggings": 105, "boots": 91
    },
    "chainmail": {
        "helmet": 165, "chestplate": 240, "leggings": 225, "boots": 195
    },
    "iron": {
        "helmet": 165, "chestplate": 240, "leggings": 225, "boots": 195
    },
    "diamond": {
        "helmet": 363, "chestplate": 528, "leggings": 495, "boots": 429
    },
    "netherite": {
        "helmet": 407, "chestplate": 592, "leggings": 555, "boots": 481
    }
}

COMMON_ARMOR_TYPE = ["helmet", "chestplate", "leggings", "boots"]

# Tool durability
# Materials
# Gold: 32 uses
# Wood: 59 uses
# Stone: 131 uses
# Iron: 250 uses
# Diamond: 1561 uses
# Netherite: 2031 uses
# Specific tools
# Fishing rod: 64 uses ‌[Java Edition only] or 384 uses ‌‌[Bedrock Edition only]
# Flint and steel: 64 uses
# Brush: 64 uses
# Carrot on a stick: 25 uses
# Shears: 238 uses
# Shield: 336 uses
# Bow: 384 uses
# Trident: 250 uses
# Elytra: 432 uses
# Crossbow: 465 uses ‌[Java Edition only] or 464 uses ‌[Bedrock Edition only]
# Warped Fungus on a Stick: 100 uses
# Sparkler ‌[Bedrock Edition and Minecraft Education only] : 100 uses
# Glow Stick ‌[Bedrock Edition and Minecraft Education only] : 100 uses

TOOL_DURABILITY = {
    "golden": 32,
    "wooden": 59,
    "stone": 131,
    "iron": 250,
    "diamond": 1561,
    "netherite": 2031,
    "fishing_rod": 64,
    "flint_and_steel": 64,
    "brush": 64,
    "carrot_on_a_stick": 25,
    "shears": 238,
    "shield": 336,
    "bow": 384,
    "trident": 250,
    "elytra": 432,
    "crossbow": 465,
    "warped_fungus_on_a_stick": 100
}

COMMON_TOOL_TYPE = ["sword", "pickaxe", "axe", "shovel", "hoe"]

def get_durability_by_id(item_id: str) -> int:
    """使用物品 ID 查找耐久度
    仅尝试适配: 1.20.1 其他版本适配情况未知

    Args:
        item_id (str): 物品 ID 

    Raises:
        KeyError: 未知的物品 ID

    Returns:
        int: 对应的耐久
    """
    # pylint: disable=C0201 # Consider iterating the dictionary directly instead of calling .keys()
    if item_id.startswith("minecraft:"):
        item_id = item_id[10:]
    parts = item_id.split("_")
    if len(parts) == 2:
        if  parts[0] in ARMOR_DURABILITY.keys() and parts[1] in COMMON_ARMOR_TYPE:
            return ARMOR_DURABILITY[parts[0]][parts[1]]
        elif parts[0] in TOOL_DURABILITY.keys() and parts[1] in COMMON_TOOL_TYPE:
            return TOOL_DURABILITY[parts[0]]
        else:
            raise KeyError
    elif item_id in TOOL_DURABILITY.keys():
        return TOOL_DURABILITY[item_id]
    else:
        raise KeyError

def get_require_point_by_id(item_id: str, current_durability: int) -> int:
    """获取修复物品所需的经验点数

    Args:
        item_id (str): 物品 ID
        current_durability (int): 当前耐久

    Returns:
        int: 所需点数
    """
    total_durability = get_durability_by_id(item_id)
    return int((total_durability - current_durability) * config.mending_rate)

def get_require_point_by_durability(durability: int) -> int:
    """获取修复物品所需的经验点数

    Args:
        durability (int): 耐久

    Returns:
        int: 所需点数
    """
    return int((durability) * config.mending_rate) + 1

def check_item(item_id: str) -> bool:
    """检查物品是否为可修复物品

    Args:
        item_id (str): 物品 ID

    Returns:
        bool: 是否为可修复物品
    """
    # pylint: disable=C0201 # Consider iterating the dictionary directly instead of calling .keys()
    if item_id.startswith("minecraft:"):
        item_id = item_id[10:]
    parts = item_id.split("_")
    if len(parts) == 2:
        if (parts[0] in ARMOR_DURABILITY.keys() and parts[1] in COMMON_ARMOR_TYPE) or \
                (parts[0] in TOOL_DURABILITY.keys() and parts[1] in COMMON_TOOL_TYPE):
            return True
        else:
            return False
    elif item_id in TOOL_DURABILITY.keys():
        return True
    else:
        return False
