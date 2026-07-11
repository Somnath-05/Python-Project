# ui.py - Shared visual styling toolkit for ARC HUNTER
# Centralizes colors, borders and the logo so every screen looks consistent.

import os
import re
import sys

# ---------------------------------------------------------------------------
# Terminal setup - make sure Windows consoles understand ANSI colour codes
# ---------------------------------------------------------------------------
def _enable_windows_ansi():
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass


_enable_windows_ansi()

# Colour is only used when we're actually attached to a terminal - this keeps
# logs/redirected output clean instead of full of escape codes.
SUPPORTS_COLOR = sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"


class C:
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"
    DIM = "\x1b[2m"
    GOLD = "\x1b[38;5;220m"
    CYAN = "\x1b[38;5;51m"
    RED = "\x1b[38;5;203m"
    GREEN = "\x1b[38;5;83m"
    YELLOW = "\x1b[38;5;226m"
    PURPLE = "\x1b[38;5;135m"
    GREY = "\x1b[38;5;245m"
    WHITE = "\x1b[38;5;255m"


def style(text, *codes):
    """Wrap text in ANSI codes, but only if color is supported."""
    if not SUPPORTS_COLOR:
        return text
    return "".join(codes) + str(text) + C.RESET


# ---------------------------------------------------------------------------
# Width-safe helpers - ANSI codes don't take up visible space, so plain
# len()/ljust()/center() would misalign every box. These strip codes first.
# ---------------------------------------------------------------------------
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text):
    return _ANSI_RE.sub("", text)


def vlen(text):
    return len(strip_ansi(text))


def pad(text, width):
    extra = width - vlen(text)
    return text + (" " * max(0, extra))


def center_pad(text, width):
    extra = max(0, width - vlen(text))
    left = extra // 2
    right = extra - left
    return (" " * left) + text + (" " * right)


# ---------------------------------------------------------------------------
# Box drawing - double-line unicode borders instead of plain +/-/|
# ---------------------------------------------------------------------------
WIDTH = 78  # inner content width used across every screen


def top(width=WIDTH):
    return style("╔" + "═" * width + "╗", C.CYAN)


def bottom(width=WIDTH):
    return style("╚" + "═" * width + "╝", C.CYAN)


def mid(width=WIDTH):
    return style("╠" + "═" * width + "╣", C.CYAN)


def line(content="", width=WIDTH):
    bar = style("║", C.CYAN)
    return f"{bar} {pad(content, width - 2)} {bar}"


def line_center(content="", width=WIDTH):
    bar = style("║", C.CYAN)
    return f"{bar}{center_pad(content, width)}{bar}"


def rule(width=WIDTH, char="─"):
    return style(char * width, C.GREY)


def box(lines, title=None, width=WIDTH):
    """Print a full box. `lines` is a list of plain/styled strings."""
    print(top(width))
    if title:
        print(line_center(style(title, C.BOLD, C.GOLD), width))
        print(mid(width))
    for entry in lines:
        print(line(entry, width))
    print(bottom(width))


# ---------------------------------------------------------------------------
# Logo - big banner for the intro, compact banner for every other screen
# ---------------------------------------------------------------------------
LOGO = r"""
     ___    ____  ______   __  ____  ___   __________________
   /   |  / __ \/ ____/  / / / / / / / / | / /_  __/ ____/ __ \
  / /| | / /_/ / /      / /_/ / / / /  |/ / / / / __/ / /_/ /
 / ___ |/ _, _/ /___   / __  / /_/ / /|  / / / / /___/ _, _/
/_/  |_/_/ |_|\____/  /_/ /_/\____/_/ |_/ /_/ /_____/_/ |_|
"""


def print_logo():
    print(style(LOGO, C.BOLD, C.GOLD))


def print_banner(subtitle=""):
    """Compact logo strip used at the top of menus/battle/shop screens."""
    print(top())
    title = style("⚔  A R C   H U N T E R  ⚔", C.BOLD, C.GOLD)
    print(line_center(title))
    if subtitle:
        print(line_center(style(subtitle, C.CYAN)))
    print(bottom())


# ---------------------------------------------------------------------------
# HP bar - solid block fill with colour that shifts as health drops, instead
# of a plain "#" hash-mark bar.
# ---------------------------------------------------------------------------
def hp_bar(cur, mx, length=20):
    ratio = max(0, min(1, cur / mx)) if mx > 0 else 0
    filled = int(ratio * length)
    if ratio > 0.5:
        color = C.GREEN
    elif ratio > 0.25:
        color = C.YELLOW
    else:
        color = C.RED
    bar = style("█" * filled, color) + style("░" * (length - filled), C.GREY)
    return f"[{bar}] {cur}/{mx}"


def gold_tag(amount):
    return style(f"◆ {amount}g", C.GOLD)
