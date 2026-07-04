from mcdreforged import Serializable, ServerInterface

class Config(Serializable):
    repair_max_time: int = 5
    repair_interval: float = 0.2
    repair_max_point_rate: float = 1.05
    repair_rate: float = 1.05
    auto_repair_player_list: list[str] = []
    auto_repair_interval: int = 60
    mending_rate: float = 0.5
    orb_value: list[int] = [149, 73, 37, 17, 7, 3, 1]
    summon_interval: float = 0.1
    helper_permission: int = 2
    summon_orb_direct: bool = True

config: Config = None  # type: ignore[assignment]

def load_config() -> Config:
    global config
    config = ServerInterface.psi().load_config_simple(target_class=Config)
    return config

def save_config() -> None:
    ServerInterface.psi().save_config_simple(config)
