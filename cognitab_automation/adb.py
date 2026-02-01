import shutil
import tempfile
import time, random
from typing import Union
import psutil, os, subprocess

from cognitab_automation.region import Region
from cognitab_automation.match import Match
from cognitab_automation.point import Point
import cv2
import numpy as np
from cognitab_automation.config import Config

class Device:
    """
    Represents an LDPlayer device instance.
    Attributes:
        index (int): The index of the device.
        name (str): The name of the device.
        top_level_handle (int): The top-level window handle of the device.
        bindwindow_handle (str): The handle of the bound window.
        running (bool): Whether the device is running.
        pid (int): The process ID of the device.
        pid_vbox (int): The process ID of the virtual box.
        width (int): The width of the device screen.
        height (int): The height of the device screen.
        dpi (int): The DPI of the device screen.
    """
    
    def __init__(self, index, name, top_level_handle, bindwindow_handle: str, running, pid, pid_vbox, width, height, dpi, ldconsole_path=None):
        self.index = index
        self.name = name
        self.top_level_handle = top_level_handle
        self.bindwindow_handle = str(bindwindow_handle)
        self.running = running
        self.pid = pid
        self.pid_vbox = pid_vbox
        self.width = width
        self.height = height
        self.dpi = dpi
        self.ldconsole_path = ldconsole_path
        self.adb_path = os.path.join(os.path.dirname(ldconsole_path), "adb.exe") if ldconsole_path else None
        self.desc = "" # Description or additional info about the device.
        self.adb_port_str = ""
        
    def get_adb_port(self) -> str:
        """Return the ADB port of this device."""
        assert self.adb_path, "adb_path is not set for this device."
        assert self.ldconsole_path, "ldconsole_path is not set for this device."
        result = subprocess.run([
                self.adb_path, "devices"
            ],
            capture_output=True,
            text=True
        )
        devices = result.stdout.strip().split("\n")[1:]  # Skip the first line
        # print("ADB devices output:", result.stdout)
        for line in devices:
            device_port = line.split("\t")[0]
            result2 = subprocess.run([
                    self.adb_path, '-s', device_port,
                    "shell", "getprop", "ro.serialno"
                ],
                capture_output=True,
                text=True
            )
            result3 = subprocess.run([
                    self.ldconsole_path, 'getprop', '--index', str(self.index)
                    , '--key', 'ro.serialno'
                ],
                capture_output=True,
                text=True
            )
            # print(f"Predicted Serialno: {result3.stdout.strip()}")
            # print(f"ADB Serialno: {result2.stdout.strip()}")
            if result2.stdout.strip() == result3.stdout.strip():
                # print(f"Device {self.name} ADB port: {device_port}")
                self.adb_port_str = device_port
                return device_port
        self.adb_port_str = f"127.0.0.1:{5555 + self.index * 2}"
        return self.adb_port_str
    
    def tap(self, target: Union[Point, Region, tuple[int, int]], random_px: int = Config.RANDOM_PX, auto_hotkey: bool = True, wait_next: int = 100):
        """Simulate a tap on the device at coordinates (x, y)."""
        assert self.ldconsole_path, "ldconsole_path is not set for this device."
        x, y = None, None
        if isinstance(target, Point):
            x, y = target.x, target.y
        elif isinstance(target, Region):
            x, y = target.x + target.width // 2, target.y + target.height // 2
        elif isinstance(target, tuple) and len(target) == 2:
            x, y = target
        elif isinstance(target, Match):
            x, y = target.region.x + target.region.width // 2, target.region.y + target.region.height // 2
        else:
            raise ValueError("Invalid target type for tap. Must be Point, Region, or (x, y) tuple.")
        assert x is not None and y is not None
        
        if random_px > 0:
            x += random.randint(-random_px, random_px)
            y += random.randint(-random_px, random_px)
        if Config.RANDOM_TIME > 0:
            time.sleep(random.randint(0, Config.RANDOM_TIME) / 1000)
        if auto_hotkey:
            script = r"""
                WinGetPos, X, Y, W, H, ahk_pid {2}
                CoordMode, Mouse, Client
                clickX := {0} * (W-40) / {3}
                clickY := {1} * (H-30) / {4} + 30
                ControlClick, x%clickX% y%clickY%, ahk_pid {2}
            """.format(x, y, self.pid, self.width, self.height)
            path = rf"R:\temp_{self.pid}.ahk"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(script)
            exe = shutil.which("autohotkeyu64")
            print("AHK exe =", exe)
            if exe is None:
                raise RuntimeError("AutoHotkey executable not found in PATH.")
            subprocess.run([exe, path], check=True)
        else:
            subprocess.run([
                    self.ldconsole_path, 'adb', 
                    '--index', str(self.index), 
                    '--command', f"shell input swipe {x} {y} {x + random.choice([-1, 1]) * random.randint(5, 30)} {y + random.choice([-1, 1]) * random.randint(5, 30)} {random.randint(40, 200)}"
                ],
                capture_output=True,
                text=True
            )
        # subprocess.run([
        #         self.ldconsole_path, 'action',
        #         '--index', str(self.index),
        #         '--swipe', f"{x} {y} {x + random.choice([-1, 1]) * random.randint(5, 30)} {y + random.choice([-1, 1]) * random.randint(5, 30)} {random.randint(40, 200)}"
        #     ],
        #     capture_output=True,
        #     text=True
        # )
        if wait_next > 0:
            time.sleep(wait_next / 1000)
        
        if Config.RANDOM_TIME > 0:
            time.sleep(random.randint(0, Config.RANDOM_TIME) / 1000)
        
    def swipe(self, p1: Point, p2: Point, duration_ms: int = 500):
        """Simulate a swipe on the device from point p1 to point p2 over duration_ms milliseconds."""
        assert self.ldconsole_path is not None, "ldconsole_path is not set for this device."
        subprocess.run([
                self.ldconsole_path, 'adb', 
                '--index', str(self.index), 
                '--command', f"shell input swipe {p1.x} {p1.y} {p2.x} {p2.y} {duration_ms}"
            ],
            capture_output=True,
            text=True
        )
    
    def capture(self, save=False, path=None) -> np.ndarray | None:
        """Capture a screenshot from the device and return it as bytes."""
        assert self.ldconsole_path, "ldconsole_path is not set for this device."
        if not self.adb_path:
            raise RuntimeError("adb_path is not set for this device.")
        result = subprocess.run([
                self.adb_path, '-s', self.adb_port_str,
                "exec-out", "screencap", "-p"
            ],
            capture_output=True,
            text=False
        )
        if result.returncode != 0:
            print(f"Failed to capture screenshot from device {self.index}: {result.stderr.decode('utf-8')}")
            return None
        data = np.frombuffer(result.stdout, np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        
        if img is None:
            print(f"Failed to decode screenshot from device {self.index}: Invalid image data")
            return None
        
        if save:
            cv2.imwrite(path if path else f"screenshot_device_{self.index}.png", img)
        return img
    
    def find(self, region: Region, template_path: str, threshold: float = 0.7, click=False, delay=0, wait_next=100, mask=False) -> Match | None:
        """Find the template image within the specified region on the device screen.
        
        Args:
            region (Region): The region of the screen to search within.
            template_path (str): The file path to the template image.
            threshold (float): The matching threshold (default is 0.7).
            click (bool): Whether to perform a tap on the matched region (default is False).
            delay (int): Delay in milliseconds before performing the tap (default is 0).
            wait_next (int): Wait time in milliseconds after the tap (default is 100).
            mask (bool): Whether to use a mask for template matching (default is False).
        Returns:
            Match | None: The matched region and confidence if found, else None.
        """
        screenshot = self.capture()
        if screenshot is None:
            return None
        
        # Crop to the specified region
        x, y, w, h = int(region.x), int(region.y), int(region.width), int(region.height)
        cropped = screenshot[y:y+h, x:x+w]
        
        if not os.path.exists(template_path):
            print(f"Template image not found at {template_path}")
            return None
        template = cv2.imread(template_path)
        if template is None:
            print(f"Failed to load template image from {template_path}")
            return None
        if mask:
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            _, mask_img = cv2.threshold(template_gray, 1, 255, cv2.THRESH_BINARY)
        
        # phóng to cả 2 ảnh nếu độ phân giải thấp hơn 340
        scale = Config.SCALE
        # if self.width < 340:
        #     scale = scale * 1.5
        
        cropped = cv2.resize(cropped, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        template = cv2.resize(template, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        
        if mask:
            res = cv2.matchTemplate(cropped, template, cv2.TM_CCOEFF_NORMED, mask=mask_img)
        else:
            res = cv2.matchTemplate(cropped, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val > threshold:
            match_region = Region(x=int(max_loc[0] / scale) + x, y=int(max_loc[1] / scale) + y, width=int(template.shape[1] / scale), height=int(template.shape[0] / scale), scale=False)
            confidence = max_val
            if click:
                self.tap(match_region)
                if delay > 0:
                    time.sleep(delay / 1000)
                if wait_next > 0:
                    time.sleep(wait_next / 1000)
            print(f"Template {os.path.basename(template_path)} found on device {self.index} at region {match_region} with confidence {confidence:.2f}")
            return Match(region=match_region, confidence=confidence, img=screenshot, point=Point(x=match_region.x + match_region.width // 2, y=match_region.y + match_region.height // 2, scale=False))
        else:
            return None
    
    def global_action(self, action: str):
        """
        Perform a global action on the device using adb.
        Arguments:
            action (str): The action to perform (e.g., 'HOME', 'BACK', 'MENU').
        """
        assert self.adb_path, "adb_path is not set for this device."
        key = 0
        if action.upper() == "HOME":
            key = 3
        elif action.upper() == "BACK":
            key = 4
        elif action.upper() == "RECENT":
            key = 187
            
        assert self.adb_path, "adb_path is not set for this device."
        
        subprocess.run([
                self.adb_path, '-s', self.adb_port_str,
                "shell", "input", "keyevent", str(key)
            ],
            capture_output=True,
            text=True
        )
        print(f"Action '{action}' performed on device {self.index}")
    
    def plot(self, region: Region):
        """Plot region on this device."""
        img = self.capture()
        if img is None:
            return None
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.rectangle(img, (int(region.x * 0.5), int(region.y * 0.5)), (int((region.x + region.width) * 0.5), int((region.y + region.height) * 0.5)), (0, 255, 0), 2)
        cv2.imshow(f"Device {self.index} - {self.name}", img)
        cv2.waitKey(0)
    
    def __repr__(self):
        return f"Device(index={self.index}, name='{self.name}', top_level_handle={self.top_level_handle}, bindwindow_handle='{self.bindwindow_handle}', running={self.running}, pid={self.pid}, pid_vbox={self.pid_vbox}, width={self.width}, height={self.height}, dpi={self.dpi})"

def find_ldconsole_from_process():
    """Find the ldconsole.exe path of LDPlayer from running processes."""
    for p in psutil.process_iter(['name', 'exe']):
        if p.info['name'] and 'dnplayer' in p.info['name'].lower():
            base = os.path.dirname(p.info['exe'])
            # print(p.info)
            ldconsole = os.path.join(base, "ldconsole.exe")
            if os.path.exists(ldconsole):
                return ldconsole
    
    return None

def get_devices(ldconsole_path: str | None = None) -> list[Device]:
    """Return list of devices"""
    if not ldconsole_path:
        ldconsole_path = find_ldconsole_from_process()
    devices = list()
    
    if ldconsole_path:
        # print(f"LDPlayer console path: {ldconsole_path}")
        
        p = subprocess.run(
            [ldconsole_path, 'list2'],
            capture_output=True,
            text=True
        )
        print("ldconsole list2 output:", p.stdout)
        
        for device in p.stdout.strip().split("\n"):
            cols = device.split(',')
            d = Device(
                index = int(cols[0]) if cols[0].isdigit() else -1,
                name = cols[1].encode('latin1').decode('utf-8'),
                top_level_handle = int(cols[2]),
                bindwindow_handle = cols[3],
                running = cols[4] == '1',
                pid = int(cols[5]),
                pid_vbox = int(cols[6]),
                width = int(cols[7]),
                height = int(cols[8]),
                dpi = int(cols[9]),
                ldconsole_path = ldconsole_path
            )
            d.get_adb_port()
            
            devices.append(d)
    return devices

if __name__ == "__main__":
    devices = get_devices()
    for device in devices:
        print(device)