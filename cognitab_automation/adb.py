import time
from typing import Union
import psutil, os, subprocess

from cognitab_automation.region import Region
from cognitab_automation.match import Match
from .point import Point
import cv2
import numpy as np
from cognitab_automation.config import Config

class Device:
    """
    Represents an LDPlayer device instance.
    Attributes:
        index (int): The index of the device.
        name (str): The name of the device.
        pid (int): The process ID of the device.
        vm_pid (int): The virtual machine process ID.
        running (bool): Whether the device is running.
        adb_port (int): The ADB port for the device.
        adb_port2 (int): The secondary ADB port for the device.
        width (int): The width of the device screen.
        height (int): The height of the device screen.
        dpi (int): The DPI of the device screen.
    """
    
    def __init__(self, index, name, pid, vm_pid, running, adb_port, adb_port2, width, height, dpi, ldconsole_path=None):
        self.index = index
        self.name = name
        self.pid = pid
        self.vm_pid = vm_pid
        self.running = running
        self.adb_port = adb_port
        self.adb_port2 = adb_port2
        self.width = width
        self.height = height
        self.dpi = dpi
        self.ldconsole_path = ldconsole_path
        self.adb_path = os.path.join(os.path.dirname(ldconsole_path), "adb.exe") if ldconsole_path else None
        self.desc = "" # Description or additional info about the device.
        
    def _check_ldconsole(self):
        if not self.ldconsole_path:
            raise RuntimeError("ldconsole_path is not set for this device.")
        
    def tap(self, target: Union[Point, Region, tuple[int, int], Match]):
        """Simulate a tap on the device at coordinates (x, y)."""
        self._check_ldconsole()
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
            raise ValueError("Invalid target type for tap. Must be Point, Region, Match, or (x, y) tuple.")
        
        subprocess.run([
                self.ldconsole_path, 'adb', 
                '--index', str(self.index), 
                '--command', f"shell input tap {x} {y}"
            ],
            capture_output=True,
            text=True
        )
        
    def swipe(self, p1: Point, p2: Point, duration_ms: int = 500):
        """Simulate a swipe on the device from point p1 to point p2 over duration_ms milliseconds."""
        self._check_ldconsole()
        subprocess.run([
                self.ldconsole_path, 'adb', 
                '--index', str(self.index), 
                '--command', f"shell input swipe {p1.x} {p1.y} {p2.x} {p2.y} {duration_ms}"
            ],
            capture_output=True,
            text=True
        )
    
    def capture(self, save=False, path=None) -> np.ndarray:
        """Capture a screenshot from the device and return it as bytes."""
        self._check_ldconsole()
        result = subprocess.run([
                self.adb_path, '-s', f"emulator-{5554 + self.index * 2}",
                "exec-out", "screencap", "-p"
            ],
            capture_output=True,
            text=False
        )
        data = np.frombuffer(result.stdout, np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        
        if img is None:
            print(f"Failed to decode screenshot from device {self.index}: Invalid image data")
            return None
        
        if save:
            cv2.imwrite(path if path else f"screenshot_device_{self.index}.png", img)
        return img
    
    def find(self, region: Region, template_path: str, threshold: float = 0.7, click=False, delay=0, wait_next=100) -> Match | None:
        """Find the template image within the specified region on the device screen.
        
        Args:
            region (Region): The region of the screen to search within.
            template_path (str): The file path to the template image.
            threshold (float): The matching threshold (default is 0.7).
            click (bool): Whether to perform a tap on the matched region (default is False).
            delay (int): Delay in milliseconds before performing the tap (default is 0).
            wait_next (int): Wait time in milliseconds after the tap (default is 100).
        
        Returns:
            Match | None: The matched region and confidence if found, else None.
        """
        screenshot = self.capture()
        if screenshot is None:
            return None
        
        # Crop to the specified region
        x, y, w, h = region.x, region.y, region.width, region.height
        cropped = screenshot[y:y+h, x:x+w]
        
        template = cv2.imread(template_path)
        
        cropped = cv2.resize(cropped, (0, 0), fx=Config.SCALE, fy=Config.SCALE, interpolation=cv2.INTER_AREA)
        template = cv2.resize(template, (0, 0), fx=Config.SCALE, fy=Config.SCALE, interpolation=cv2.INTER_AREA)
        if template is None:
            print(f"Failed to load template image from {template_path}")
            return None
        
        res = cv2.matchTemplate(cropped, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        
        if len(loc[0]) > 0:
            match_region = Region(x=int(loc[1][0] / Config.SCALE) + x, y=int(loc[0][0] / Config.SCALE) + y, width=int(template.shape[1] / Config.SCALE), height=int(template.shape[0] / Config.SCALE))
            confidence = res[loc[0][0], loc[1][0]]
            if click:
                self.tap(match_region)
                if delay > 0:
                    time.sleep(delay / 1000)
                if wait_next > 0:
                    time.sleep(wait_next / 1000)
            print(f"Template found on device {self.index} at region {match_region} with confidence {confidence:.2f}")
            return Match(region=match_region, confidence=confidence)
        else:
            return None
    
    def global_action(self, action: str):
        """
        Perform a global action on the device using ldconsole.
        Arguments:
            action (str): The action to perform (e.g., 'HOME', 'BACK', 'MENU').
        """
        self._check_ldconsole()
        key = ""
        value = ""
        if action.upper() == "HOME":
            key = "call.keyboard"
            value = "home"
        elif action.upper() == "BACK":
            key = "call.keyboard"
            value = "back"
        elif action.upper() == "MENU":
            key = "call.keyboard"
            value = "menu"
        
        subprocess.run([
                self.ldconsole_path, 'action', 
                '--index', str(self.index), 
                '--key', key,
                '--value', value
            ],
            capture_output=True,
            text=True
        )
        print(f"Action '{action}' performed on device {self.index}")
    
    def plot(self, region: Region):
        """Plot region on this device."""
        self._check_ldconsole()
        img = self.capture()
        if img is None:
            return None
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.rectangle(img, (int(region.x * 0.5), int(region.y * 0.5)), (int((region.x + region.width) * 0.5), int((region.y + region.height) * 0.5)), (0, 255, 0), 2)
        cv2.imshow(f"Device {self.index} - {self.name}", img)
        cv2.waitKey(0)
    
    def __repr__(self):
        return f"Device(index={self.index}, name={self.name}, pid={self.pid}, vm_pid={self.vm_pid}, running={self.running}, adb_port={self.adb_port}, adb_port2={self.adb_port2}, width={self.width}, height={self.height}, dpi={self.dpi}, desc={self.desc})"
        

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

def get_devices(ldconsole_path: str = None) -> list[Device]:
    """Return list of devices"""
    if not ldconsole_path:
        ldconsole_path = find_ldconsole_from_process()
    devices = list()
    
    if ldconsole_path:
        print(f"LDPlayer console path: {ldconsole_path}")
        
        p = subprocess.run(
            [ldconsole_path, 'list2'],
            capture_output=True,
            text=True
        )
        
        # print("Running instances:")
        # print(p.stdout)
        
        for device in p.stdout.strip().split("\n"):
            cols = device.split(',')
            d = Device(
                index = int(cols[0]),
                name = cols[1].encode('latin1').decode('utf-8'),
                pid = int(cols[2]),
                vm_pid = int(cols[3]),
                running = cols[4] == '1',
                adb_port = int(cols[5]),
                adb_port2 = int(cols[6]),
                width = int(cols[7]),
                height = int(cols[8]),
                dpi = int(cols[9]),
                ldconsole_path = ldconsole_path
            )
            
            devices.append(d)
    return devices

if __name__ == "__main__":
    devices = get_devices()
    for device in devices:
        print(device)
        if device.running:
            img = device.capture(save=True)
            if img is not None:
                print(f"Captured screenshot from device {device.index}, shape: {img.shape}")