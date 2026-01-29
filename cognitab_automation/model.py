import onnxruntime as ort
import numpy as np
import cv2

class ModelLoader:
    
    _session = None
    _img_size = None
    
    