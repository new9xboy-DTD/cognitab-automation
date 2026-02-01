

class Config():
    """A class to hold configuration settings."""
    
    # =========== Macro Device Info =============
    MACRO_WIDTH = 0  # Width of the macro device
    MACRO_HEIGHT = 0  # Height of the macro device
    MACRO_DPI = 0  # DPI of the macro device
    
    # =========== Target Device Info ============
    TARGET_WIDTH = 0  # Width of the target device
    TARGET_HEIGHT = 0  # Height of the target device
    TARGET_DPI = 0  # DPI of the target device
    
    # =========== Scaling Factors =============
    # use this scale for point, region
    COOR_SCALE = 1.0  # Scaling factor for coordinates (points and regions), default is 1.0 (no scaling)
    
    #use this scale for template and image matching
    SCALE = 1.0 # Scaling factor for image/template matching, default is 1.0 (no scaling)
    
    RANDOM_PX = 0  # Random offset in pixels for click positions to simulate human behavior
    RANDOM_TIME = 0  # Random delay in milliseconds for actions to simulate human behavior
    
    @classmethod
    def config(cls, macro_width: int, macro_height: int, macro_dpi: int,
               target_width: int | None = None, target_height: int | None = None, target_dpi: int | None = None, random_px: int = 0, random_time: int = 0):
        """Configure the device settings and calculate scaling factors."""
        cls.MACRO_WIDTH = macro_width
        cls.MACRO_HEIGHT = macro_height
        cls.MACRO_DPI = macro_dpi
        
        cls.TARGET_WIDTH = target_width if target_width else macro_width
        cls.TARGET_HEIGHT = target_height if target_height else macro_height
        cls.TARGET_DPI = target_dpi if target_dpi else macro_dpi
        
        # Calculate scaling factor based on width and height ratios
        # scale for point, region
        cls.COOR_SCALE = min(cls.TARGET_HEIGHT, cls.TARGET_WIDTH) / min(macro_height, macro_width)
        
        # scale for template, image matching
        # if min(macro_width, macro_height) > 540:
        #     cls.SCALE = 1
        # else:
        #     cls.SCALE = 1.0
        
        
        cls.RANDOM_TIME = random_time
        cls.RANDOM_PX = random_px * int(cls.COOR_SCALE + 0.5)