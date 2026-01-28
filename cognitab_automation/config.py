

class Config():
    """A class to hold configuration settings."""
    
    # =========== Macro Device Info =============
    MACRO_WIDTH = None  # Width of the macro device
    MACRO_HEIGHT = None  # Height of the macro device
    MACRO_DPI = None  # DPI of the macro device
    
    # =========== Target Device Info ============
    TARGET_WIDTH = None  # Width of the target device
    TARGET_HEIGHT = None  # Height of the target device
    TARGET_DPI = None  # DPI of the target device
    
    # =========== Scaling Factors =============
    # use this scale for point, region
    SCALE_X = 1.0 # Scaling factor between macro and target device, default is 1.0 (no scaling)
    SCALE_Y = 1.0 # Scaling factor between macro and target device, default is 1.0 (no scaling)
    
    #use this scale for template and image matching
    SCALE = 1.0 # Scaling factor for image/template matching, default is 1.0 (no scaling)
    
    RANDOM_PX = 0  # Random offset in pixels for click positions to simulate human behavior
    
    @classmethod
    def config(cls, macro_width: int, macro_height: int, macro_dpi: int,
               target_width: int = None, target_height: int = None, target_dpi: int = None):
        """Configure the device settings and calculate scaling factors."""
        cls.MACRO_WIDTH = macro_width
        cls.MACRO_HEIGHT = macro_height
        cls.MACRO_DPI = macro_dpi
        
        cls.TARGET_WIDTH = target_width if target_width else macro_width
        cls.TARGET_HEIGHT = target_height if target_height else macro_height
        cls.TARGET_DPI = target_dpi if target_dpi else macro_dpi
        
        # Calculate scaling factor based on width and height ratios
        # scale for point, region
        cls.SCALE_X = cls.TARGET_WIDTH / cls.MACRO_WIDTH
        cls.SCALE_Y = cls.TARGET_HEIGHT / cls.MACRO_HEIGHT
        
        # scale for template, image matching
        if min(macro_width, macro_height) > 540:
            cls.SCALE = 0.7