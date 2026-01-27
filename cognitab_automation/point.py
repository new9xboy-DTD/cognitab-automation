
from dataclasses import dataclass


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