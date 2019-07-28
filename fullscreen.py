#!/usr/bin/env python3

from argparse import ArgumentParser
from subprocess import call
import i3ipc

i3 = i3ipc.Connection()

parser = ArgumentParser(prog='disable-standby-fs',
        description='''
        Disable standby (dpms) and screensaver when a window becomes fullscreen
        or exits fullscreen-mode. Requires `xorg-xset`.
        ''')

args = parser.parse_args()
state = True

def find_fullscreen(con):
    # XXX remove me when this method is available on the con in a release
    focus = con.find_focused()
    return (focus.fullscreen_mode and focus.window_class is not None)

def set_dpms(state):
    if state:
        print('setting dpms on')
        call(["notify-send", "-u", "low", "-t", "500", "Fullscreen off"])
        call(['xset', 's', 'on'])
        call(['xset', '+dpms'])
    else:
        print('setting dpms off')
        call(["notify-send", "-u", "low", "-t", "500", "Fullscreen on"])
        call(['xset', 's', 'off'])
        call(['xset', '-dpms'])

def on_fullscreen_mode(i3, e):
    global state
    nstate = not find_fullscreen(i3.get_tree())
    if(nstate != state):
        state = nstate
        set_dpms(state)


i3.on('window::fullscreen_mode', on_fullscreen_mode)
i3.on('window::close', on_fullscreen_mode)
i3.on('workspace::focus', on_fullscreen_mode)
i3.on("window::focus", on_fullscreen_mode)

i3.main()
