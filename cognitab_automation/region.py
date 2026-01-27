
from dataclasses import dataclass
from cognitab_automation.config import Config


@dataclass
class Region():
    """
    Represents a rectangular region on the screen.
    
    Attributes:
        x (int): The x-coordinate of the top-left corner of the region.
        y (int): The y-coordinate of the top-left corner of the region.
        width (int): The width of the region.
        height (int): The height of the region.
    """
    
    x: int
    y: int
    width: int
    height: int
    
    def __post_init__(self):
        if self.x + self.width > Config.TARGET_WIDTH:
            self.width = self.width - (self.x + self.width - Config.TARGET_WIDTH)
        if self.y + self.height > Config.TARGET_HEIGHT:
            self.height = self.height - (self.y + self.height - Config.TARGET_HEIGHT)
    
    
if __name__ == "__main__":
    reg = Region(10, 20, 300, 400)
    print(reg)