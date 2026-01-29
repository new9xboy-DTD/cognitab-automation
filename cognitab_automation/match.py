from dataclasses import dataclass
from cognitab_automation.region import Region
import numpy as np

@dataclass
class Match:
    """
    Represents a match result with its location and confidence score.
    
    Attributes:
        region (Region): The region where the match was found.
        confidence (float): The confidence score of the match (0.0 to 1.0).
        img (np.ndarray): The image in which the match was found (optional).
    """
    
    region: Region
    confidence: float
    img: np.ndarray