from dataclasses import dataclass
from cognitab_automation.region import Region

@dataclass
class Match:
    """
    Represents a match result with its location and confidence score.
    
    Attributes:
        region (Region): The region where the match was found.
        confidence (float): The confidence score of the match (0.0 to 1.0).
    """
    
    region: Region
    confidence: float