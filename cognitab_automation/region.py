
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
        if self.x + self.width > Config.MACRO_WIDTH:
            self.width = self.width - (self.x + self.width - Config.MACRO_WIDTH)
        if self.y + self.height > Config.MACRO_HEIGHT:
            self.height = self.height - (self.y + self.height - Config.MACRO_HEIGHT)
            
    def left(self, percent: float = 0.5) -> "Region":
        """Resize the region to its left part by the given percentage."""
        return Region(
            x=self.x,
            y=self.y,
            width=self.width - int(self.width * percent),
            height=self.height
        )
    
    def right(self, percent: float = 0.5) -> "Region":
        """Resize the region to its right part by the given percentage."""
        return Region(
            x=self.x + int(self.width * percent),
            y=self.y,
            width=int(self.width * (1 - percent)),
            height=self.height
        )
    
    def top(self, percent: float = 0.5) -> "Region":
        """Resize the region to its top part by the given percentage."""
        return Region(
            x=self.x,
            y=self.y,
            width=self.width,
            height=int(self.height * (1 - percent))
        )
    
    def bottom(self, percent: float = 0.5) -> "Region":
        """Resize the region to its bottom part by the given percentage."""
        return Region(
            x=self.x,
            y=self.y + int(self.height * percent),
            width=self.width,
            height=int(self.height * (1 - percent))
        )
    
    def middle(self, percent_w: float = 0.5, percent_h: float = 0.5) -> "Region":
        """Resize the region to its middle part by the given width and height percentages."""
        new_width = int(self.width * (1 - percent_w))
        new_height = int(self.height * (1 - percent_h))
        return Region(
            x=self.x + (self.width - new_width) // 2,
            y=self.y + (self.height - new_height) // 2,
            width=new_width,
            height=new_height
        )
    
    @classmethod
    def full(cls) -> "Region":
        """Return the full region."""
        return Region(
            x=0,
            y=0,
            width=Config.TARGET_WIDTH,
            height=Config.TARGET_HEIGHT
        )
        
        
    
    
if __name__ == "__main__":
    Config.config(macro_width=1080, macro_height=1920, macro_dpi=320)
    print(Region.full().left(0.7).middle(0, 0.3))