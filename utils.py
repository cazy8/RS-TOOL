# utils.py
# DISCLAIMER: This script is for educational purposes only. Do not use against any system without explicit permission.

import json
import os
import sys

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"

# 256-color palette (fallback to no color if not supported)
PALETTE = [
    "\033[38;5;196m",  # red
    "\033[38;5;208m",  # orange
    "\033[38;5;226m",  # yellow
    "\033[38;5;46m",   # green
    "\033[38;5;51m",   # cyan
    "\033[38;5;33m",   # blue
    "\033[38;5;135m",  # magenta
]

ACCENT = "\033[38;5;45m"   # teal/cyan accent
SUBTLE = "\033[38;5;245m"  # gray

def _color_enabled():
    # Disable color if stdout is not a TTY or NO_COLOR is set
    if not sys.stdout.isatty():
        return False
    if os.environ.get("NO_COLOR"):
        return False
    term = os.environ.get("TERM", "")
    return any(t in term for t in ["xterm", "screen", "vt100", "ansi", "rxvt", "linux"])

COLOR_ON = _color_enabled()

def _c(code):
    return code if COLOR_ON else ""

def print_banner():
    """
    Prints a cool ASCII art banner for the tool spelling 'RS TOOL'.
    """
    # Letter blocks (6 lines each)
    R = [
        "██████╗ ",
        "██╔══██╗",
        "██████╔╝",
        "██╔══██╗",
        "██║  ██║",
        "╚═╝  ╚═╝",
    ]
    S = [
        " ██████╗",
        "██╔════╝",
        "╚█████╗ ",
        " ╚═══██╗",
        "██████╔╝",
        "╚═════╝ ",
    ]
    T = [
        "████████╗",
        "╚══██╔══╝",
        "   ██║   ",
        "   ██║   ",
        "   ██║   ",
        "   ╚═╝   ",
    ]
    O = [
        " ██████╗ ",
        "██╔═══██╗",
        "██║   ██║",
        "██║   ██║",
        "╚██████╔╝",
        " ╚═════╝ ",
    ]
    L = [
        "██╗     ",
        "██║     ",
        "██║     ",
        "██║     ",
        "███████╗",
        "╚══════╝",
    ]

    # Compose "RS TOOL" across 6 rows
    lines = [
        f"{R[0]}  {S[0]}    {T[0]}  {O[0]}  {O[0]}  {L[0]}",
        f"{R[1]}  {S[1]}    {T[1]}  {O[1]}  {O[1]}  {L[1]}",
        f"{R[2]}  {S[2]}    {T[2]}  {O[2]}  {O[2]}  {L[2]}",
        f"{R[3]}  {S[3]}    {T[3]}  {O[3]}  {O[3]}  {L[3]}",
        f"{R[4]}  {S[4]}    {T[4]}  {O[4]}  {O[4]}  {L[4]}",
        f"{R[5]}  {S[5]}    {T[5]}  {O[5]}  {O[5]}  {L[5]}",
    ]

    # Print with a soft gradient across lines
    for i, line in enumerate(lines):
        color = _c(PALETTE[i % len(PALETTE)])
        print(f"{color}{line}{_c(RESET)}")

    # Title and subtitle
    title = "RS TOOL"
    subtitle = "A simple recon tool by Harsh Gupta."

    deco = f"{_c(SUBTLE)}{'─' * 78}{_c(RESET)}"
    print(deco)
    print(f"{_c(BOLD)}{_c(ACCENT)}>> {title} <<{_c(RESET)}")
    print(f"{_c(SUBTLE)}{subtitle}{_c(RESET)}")
    print(deco)

def print_results(title, results):
    """
    Prints a formatted section for results.
    """
    print(f"\n--- {title} ---")
    if not results:
        print("No results found.")
    elif isinstance(results, list):
        for item in results:
            print(f"[+] {item}")
    elif isinstance(results, dict):
        for key, value in results.items():
            print(f"[+] {key}: {value}")
    print("-" * (len(title) + 6))

def save_results(filepath, data):
    """
    Saves the collected data to a JSON file.
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
