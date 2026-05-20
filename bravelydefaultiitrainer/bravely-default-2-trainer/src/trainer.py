"""
Main trainer logic for Bravely Default II.
Provides cheat functionalities with hotkey support.
"""

import time
import threading
import keyboard
from src.memory_reader import BD2MemoryReader


class BD2Trainer:
    """Trainer class that manages cheat features and hotkeys."""

    def __init__(self):
        self.memory = BD2MemoryReader()
        self.running = False
        self.hotkeys = {
            "f1": self._toggle_infinite_hp,
            "f2": self._toggle_infinite_mp,
            "f3": self._add_gold,
            "f4": self._max_level,
            "f5": self._max_job_points,
        }
        self.infinite_hp = False
        self.infinite_mp = False
        self.thread = None

    def start(self):
        """Start the trainer - attach to process and listen for hotkeys."""
        if not self.memory.attach():
            print("Failed to attach to Bravely Default II process.")
            return False

        print("Trainer attached successfully.")
        print("Hotkeys:")
        print("  F1 - Toggle Infinite HP")
        print("  F2 - Toggle Infinite MP")
        print("  F3 - Add 99999 Gold")
        print("  F4 - Max Level (99)")
        print("  F5 - Max Job Points (9999)")
        print("  ESC - Exit")

        self.running = True

        # Register hotkeys
        for key, callback in self.hotkeys.items():
            keyboard.add_hotkey(key, callback)
        keyboard.add_hotkey("esc", self.stop)

        # Start background thread for infinite HP/MP
        self.thread = threading.Thread(target=self._infinite_loop, daemon=True)
        self.thread.start()

        # Keep main thread alive
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

        return True

    def stop(self):
        """Stop the trainer and cleanup."""
        print("\nShutting down trainer...")
        self.running = False
        keyboard.unhook_all()
        self.memory.detach()
        print("Trainer stopped.")

    def _toggle_infinite_hp(self):
        """Toggle infinite HP on/off."""
        self.infinite_hp = not self.infinite_hp
        status = "ON" if self.infinite_hp else "OFF"
        print(f"Infinite HP: {status}")

    def _toggle_infinite_mp(self):
        """Toggle infinite MP on/off."""
        self.infinite_mp = not self.infinite_mp
        status = "ON" if self.infinite_mp else "OFF"
        print(f"Infinite MP: {status}")

    def _add_gold(self):
        """Add 99999 gold to current amount."""
        try:
            current = self.memory.get_gold()
            new_gold = current + 99999
            self.memory.set_gold(new_gold)
            print(f"Gold added: {current} -> {new_gold}")
        except Exception as e:
            print(f"Error adding gold: {e}")

    def _max_level(self):
        """Set character level to 99."""
        try:
            self.memory.set_level(99)
            print("Level set to 99.")
        except Exception as e:
            print(f"Error setting level: {e}")

    def _max_job_points(self):
        """Set job points to 9999."""
        try:
            self.memory.set_job_points(9999)
            print("Job points set to 9999.")
        except Exception as e:
            print(f"Error setting job points: {e}")

    def _infinite_loop(self):
        """Background loop to maintain infinite HP/MP."""
        while self.running:
            try:
                if self.infinite_hp:
                    # Write max HP value (example address)
                    hp_addr = self.memory.base_address + self.memory.HP_BASE_OFFSET
                    self.memory.write_float(hp_addr, 9999.0)
                if self.infinite_mp:
                    mp_addr = self.memory.base_address + self.memory.MP_BASE_OFFSET
                    self.memory.write_float(mp_addr, 999.0)
            except Exception:
                pass
            time.sleep(0.05)
