import psutil, os, subprocess
from point import Point

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
        
    def _check_ldconsole(self):
        if not self.ldconsole_path:
            raise RuntimeError("ldconsole_path is not set for this device.")
        
    def tap(self, point: Point):
        """Simulate a tap on the device at coordinates (x, y)."""
        self._check_ldconsole()
        subprocess.run([
                self.ldconsole_path, 'adb', 
                '--index', str(self.index), 
                '--command', f"shell input tap {point.x} {point.y}"
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
    
    def capture(self):
        """Capture a screenshot from the device and return it as bytes."""
        self._check_ldconsole()
        result = subprocess.run([
                self.ldconsole_path, 'adb', 
                '--index', str(self.index), 
                '--command', "exec-out screencap -p"
            ],
            capture_output=True,
            text=False
        )
        return result.stdout
        
    def __repr__(self):
        return f"Device(index={self.index}, name={self.name}, pid={self.pid}, vm_pid={self.vm_pid}, running={self.running}, adb_port={self.adb_port}, adb_port2={self.adb_port2}, width={self.width}, height={self.height}, dpi={self.dpi})"
        

def find_ldconsole_from_process():
    """Find the ldconsole.exe path of LDPlayer from running processes."""
    for p in psutil.process_iter(['name', 'exe']):
        if p.info['name'] and 'dnplayer' in p.info['name'].lower():
            base = os.path.dirname(p.info['exe'])
            print(p.info)
            ldconsole = os.path.join(base, "ldconsole.exe")
            if os.path.exists(ldconsole):
                return ldconsole
    
    return None

def get_devices():
    """Return list of devices"""
    ldconsole_path = find_ldconsole_from_process()
    devices = dict()
    
    if ldconsole_path:
        print(f"LDPlayer console path: {ldconsole_path}")
        
        p = subprocess.run(
            [ldconsole_path, 'list2'],
            capture_output=True,
            text=True
        )
        
        print("Running instances:")
        print(p.stdout)
        
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
            
            devices[d.index] = d
            d.tap(Point(100, 100))  # Test tap at (100, 100)
    return devices

if __name__ == "__main__":
    devices = get_devices()
    for index, device in devices.items():
        print(device)