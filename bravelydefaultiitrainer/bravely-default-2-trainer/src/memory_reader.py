"""
Memory reader module for Bravely Default II.
Handles reading and writing process memory via PyMem.
"""

import pymem
import pymem.process


class BD2MemoryReader:
    """Manages memory operations for Bravely Default II process."""

    PROCESS_NAME = "BravelyDefault2.exe"

    # Known offsets (example - would need reverse engineering for real use)
    # These are illustrative placeholders
    GOLD_OFFSET = 0x00A1B2C0
    HP_BASE_OFFSET = 0x00D3E4F0
    MP_BASE_OFFSET = 0x00D3E4F4
    LEVEL_OFFSET = 0x00B5C6D0
    JOB_POINTS_OFFSET = 0x00C7D8E0

    def __init__(self):
        self.pm = None
        self.process = None
        self.base_address = None

    def attach(self) -> bool:
        """Attach to the Bravely Default II process."""
        try:
            self.pm = pymem.Pymem(self.PROCESS_NAME)
            self.process = pymem.process.module_from_name(
                self.pm.process_handle, self.PROCESS_NAME
            )
            self.base_address = self.process.lpBaseOfDll
            return True
        except pymem.exception.ProcessNotFound:
            return False
        except Exception as e:
            print(f"Error attaching: {e}")
            return False

    def detach(self):
        """Detach from the process."""
        if self.pm:
            self.pm.close_process()
            self.pm = None
            self.process = None
            self.base_address = None

    def read_int(self, address: int) -> int:
        """Read a 4-byte integer from memory."""
        if not self.pm:
            raise RuntimeError("Not attached to process")
        return self.pm.read_int(address)

    def write_int(self, address: int, value: int):
        """Write a 4-byte integer to memory."""
        if not self.pm:
            raise RuntimeError("Not attached to process")
        self.pm.write_int(address, value)

    def read_float(self, address: int) -> float:
        """Read a 4-byte float from memory."""
        if not self.pm:
            raise RuntimeError("Not attached to process")
        return self.pm.read_float(address)

    def write_float(self, address: int, value: float):
        """Write a 4-byte float to memory."""
        if not self.pm:
            raise RuntimeError("Not attached to process")
        self.pm.write_float(address, value)

    def get_gold(self) -> int:
        """Read current gold amount."""
        addr = self.base_address + self.GOLD_OFFSET
        return self.read_int(addr)

    def set_gold(self, value: int):
        """Set gold amount."""
        addr = self.base_address + self.GOLD_OFFSET
        self.write_int(addr, value)

    def get_level(self) -> int:
        """Read current character level."""
        addr = self.base_address + self.LEVEL_OFFSET
        return self.read_int(addr)

    def set_level(self, value: int):
        """Set character level."""
        addr = self.base_address + self.LEVEL_OFFSET
        self.write_int(addr, value)

    def get_job_points(self) -> int:
        """Read current job points."""
        addr = self.base_address + self.JOB_POINTS_OFFSET
        return self.read_int(addr)

    def set_job_points(self, value: int):
        """Set job points."""
        addr = self.base_address + self.JOB_POINTS_OFFSET
        self.write_int(addr, value)
