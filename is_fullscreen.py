#!/usr/bin/env python3
import sys
import i3ipc

i3 = i3ipc.Connection()

focus = i3.get_tree().find_focused()
sys.exit(not (focus.fullscreen_mode and focus.window_class is not None))
