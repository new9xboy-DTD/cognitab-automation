
from dataclasses import InitVar, dataclass
from cognitab_automation.config import Config


@dataclass
class Point:
    """
    Represents a point in 2D space.
    
    Attributes:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
    """
    
    x: int
    y: int
    
    def __post_init__(self):
        self.x = int(self.x * Config.COOR_SCALE)
        self.y = int(self.y * Config.COOR_SCALE)