"""
Entry point for the Bravely Default II Trainer.
Launches the trainer with command-line argument support.
"""

import sys
import argparse
from src.trainer import BD2Trainer


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Bravely Default II Trainer - Memory editor and cheat tool"
    )
    parser.add_argument(
        "--no-hotkeys",
        action="store_true",
        help="Disable hotkey registration (manual control only)",
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()

    print("=" * 50)
    print("  Bravely Default II Trainer v1.0.0")
    print("=" * 50)
    print()

    trainer = BD2Trainer()

    if args.no_hotkeys:
        print("Hotkeys disabled. Use script API directly.")
        # Allow programmatic control
        return

    print("Attempting to attach to Bravely Default II...")
    success = trainer.start()

    if not success:
        print("\nCould not attach to game. Make sure Bravely Default II is running.")
        sys.exit(1)


if __name__ == "__main__":
    main()
