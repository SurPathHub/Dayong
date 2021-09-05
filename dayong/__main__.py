"""
Dayong's entry point.
"""
from dayong.cli import SetupCLI, command_line, display_banner

if __name__ == "__main__":
    args = command_line()
    display_banner()
    setup = SetupCLI()
    setup.check_configs()
    setup.run_dayong()
