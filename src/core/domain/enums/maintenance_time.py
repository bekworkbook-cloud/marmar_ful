from datetime import time
from enum import Enum


class MaintenanceTime(Enum):
    DAY_START = time(7, 0)
    DAY_END = time(17, 0)
