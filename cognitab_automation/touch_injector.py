#!/usr/bin/env python3
# touch_injector.py

import os
import time
import random
import subprocess
import shutil

class TouchInjector:
    def __init__(self, device="/dev/input/event1", adb_path=None):
        self.device = device
        # Try to find adb: use provided path, or search in PATH
        if adb_path:
            self.adb_path = adb_path
        else:
            # Try to find adb in PATH
            self.adb_path = shutil.which("adb")
            if not self.adb_path:
                # Fallback: use "adb" and let shell find it
                self.adb_path = os.path.join(os.path.dirname(__file__), "adb.exe")
        
        # Khởi tạo persistent ADB shell một lần
        self._shell = subprocess.Popen(
            [self.adb_path, "shell"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
    
    def __del__(self):
        """Đóng ADB shell khi đối tượng bị hủy"""
        if hasattr(self, '_shell') and self._shell:
            self._shell.stdin.close()
            self._shell.terminate()
            self._shell.wait()
        
    def send_event(self, event_type, event_code, value):
        """Gửi một input event"""
        cmd = f"sendevent {self.device} {event_type} {event_code} {value}\n"
        self._shell.stdin.write(cmd.encode())
        self._shell.stdin.flush()
    
    def hex_to_dec(self, hex_str):
        """Chuyển hex string sang decimal"""
        return int(hex_str, 16)
    
    def tap(self, x, y, duration=0.05):
        """Thực hiện tap tại tọa độ (x, y)"""
        # Touch down
        self.send_event(3, 57, 1)      # ABS_MT_TRACKING_ID
        self.send_event(3, 53, x)      # ABS_MT_POSITION_X
        self.send_event(3, 54, y)      # ABS_MT_POSITION_Y
        self.send_event(3, 48, 30)     # ABS_MT_TOUCH_MAJOR
        self.send_event(0, 2, 0)       # SYN_MT_REPORT
        self.send_event(0, 0, 0)       # SYN_REPORT
        
        # Giữ
        time.sleep(duration)
        
        # Touch up
        self.send_event(3, 57, -1)     # ABS_MT_TRACKING_ID = -1
        self.send_event(0, 2, 0)       # SYN_MT_REPORT
        self.send_event(0, 0, 0)       # SYN_REPORT
    
    def swipe(self, x1, y1, x2, y2, duration=0.5):
        """Thực hiện swipe từ (x1,y1) đến (x2,y2)"""
        steps = int(duration * 100)
        
        for i in range(steps):
            progress = i / steps
            # Bezier curve để mượt mà hơn
            current_x = int(x1 + (x2 - x1) * progress)
            current_y = int(y1 + (y2 - y1) * progress)
            
            # Thêm jitter nhỏ
            current_x += random.randint(-2, 2)
            current_y += random.randint(-2, 2)
            
            self.send_event(3, 57, 1)
            self.send_event(3, 53, current_x)
            self.send_event(3, 54, current_y)
            self.send_event(0, 2, 0)
            self.send_event(0, 0, 0)
            
            time.sleep(duration / steps)
        
        # Kết thúc
        self.send_event(3, 57, -1)
        self.send_event(0, 2, 0)
        self.send_event(0, 0, 0)

# Sử dụng
if __name__ == "__main__":
    injector = TouchInjector()
    
    # Click tại tọa độ 20, 330
    injector.tap(20, 330)
    
    # Swipe
    injector.swipe(100, 500, 900, 500, duration=0.3)