# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401from typing import List  # noqa: F401

from scripts import storage

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile import bar, layout, widget, hook
from libqtile.widget import base
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.command import lazy
from libqtile.utils import guess_terminal
#from libqtile.utils import guess_terminal
from MutableScratch import MutableScratch
from libqtile.config import EzKey
from plasma import Plasma

# default variables
mod = "mod4"
home_dir = os.path.expanduser("~")
terminal = f"alacritty --config-file {home_dir}/.config/qtile/alacritty/alacritty.yml"
myTerm = "kitty"      # My terminal of choice
myBrowser = "firefox" # My browser of choice
dmenu = "j4-dmenu-desktop"


win_list = []
def stick_win(qtile):
    global win_list
    win_list.append(qtile.current_window)
def unstick_win(qtile):
    global win_list
    if qtile.current_window in win_list:
        win_list.remove(qtile.current_window)
@hook.subscribe.setgroup
def move_win():
    for w in win_list:
        w.togroup(qtile.current_group.name)


keys = [

    ### The essentials
    Key([mod], "Return",lazy.spawn(myTerm),desc='Launches My Terminal'),
    Key([mod], "d",lazy.spawn(dmenu),desc='j4-dmenu'),
    Key([mod], "Menu",lazy.spawn(dmenu),desc='j4-dmenu'),
    Key([mod, "shift"], "Return",lazy.spawn("dmenu_run -p 'Run: '"),desc='Run Launcher'),
    Key([mod], "b",lazy.spawn(myBrowser),desc='Firefox'),

    Key([mod], "Tab",lazy.next_layout(),desc='Toggle through layouts'),
    Key([mod, "shift"], "q",lazy.window.kill(),desc='Kill active window'),
    Key([mod, "shift"], "r",lazy.restart(),desc='Restart Qtile'),
    Key([mod, "shift"], "e",lazy.shutdown(),desc='Shutdown Qtile'),

    Key([mod], "o", lazy.function(stick_win), desc="stick win"),
    Key([mod, "shift"], "o", lazy.function(unstick_win), desc="unstick win"),

    KeyChord([mod],"s", [
        Key([], "h",lazy.layout.mode_horizontal(),desc='mode horizontal'),
        Key([], "v",lazy.layout.mode_vertical(),desc='mode vertical'),
        Key(["shift"], "h",lazy.layout.mode_horizontal_split(),desc='mode horizontal split'),
        Key(["shift"], "v",lazy.layout.mode_vertical_split(),desc='mode vertical split')]),

    KeyChord([mod],"r", [
        Key([], "r", lazy.layout.reset_size(), desc='reset size'),
        Key([], "w", lazy.layout.grow_width(30), desc='grow width'),
        Key(["shift"], "w", lazy.layout.grow_width(-30), desc='grow width'),
        Key([], "h", lazy.layout.grow_height(30), desc='grow height'),
        Key(["shift"], "h", lazy.layout.grow_height(-30), desc='grow height')],
        mode="Resize"),


    Key(["control", "shift"], "e",lazy.spawn("emacsclient -c -a emacs"),desc='Doom Emacs'),

    Key(["control"], "space", lazy.widget["keyboardlayout"].next_keyboard(),   desc="Next keyboard layout"),

    # ### Switch focus to specific monitor (out of three)
    # Key([mod], "w",
    # lazy.to_screen(0),
    # desc='Keyboard focus to monitor 1'
    # ),
    # Key([mod], "e",
    # lazy.to_screen(1),
    # desc='Keyboard focus to monitor 2'
    # ),
    # Key([mod], "r",
    # lazy.to_screen(2),
    # desc='Keyboard focus to monitor 3'
    # ),
    ### Switch focus of monitors
    Key([mod], "period",lazy.next_screen(),desc='Move focus to next monitor'),
    Key([mod], "comma",lazy.prev_screen(),desc='Move focus to prev monitor'),



#     Key([mod, "shift"], "j",
# lazy.layout.shuffle_down(),
# lazy.layout.section_down(),
# desc='Move windows down in current stack'
#     ),
#     Key([mod, "shift"], "k",
# lazy.layout.shuffle_up(),
# lazy.layout.section_up(),
# desc='Move windows up in current stack'
#     ),
#     Key([mod], "h",
# lazy.layout.shrink(),
# lazy.layout.decrease_nmaster(),
# desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
#     ),
#     Key([mod], "l",
# lazy.layout.grow(),
# lazy.layout.increase_nmaster(),
# desc='Expand window (MonadTall), increase number in master pane (Tile)'
#     ),
#     Key([mod], "n",
# lazy.layout.normalize(),
# desc='normalize window size ratios'
#     ),

    Key([mod], "m", lazy.layout.maximize(), 
        desc='toggle window between minimum and maximum sizes'
    ),
    
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc='toggle floating'),
    
    Key([mod], "f",lazy.window.toggle_fullscreen(),desc='toggle fullscreen'),

#     ### Stack controls
#     Key([mod, "shift"], "Tab",
#         lazy.layout.rotate(),
#         lazy.layout.flip(),
#         desc='Switch which side main pane occupies (XmonadTall)'
#         ),
#     Key([mod], "space",
#         lazy.layout.next(),
#         desc='Switch window focus to other pane(s) of stack'
#         ),
#     Key([mod, "shift"], "space",
#         lazy.layout.toggle_split(),
#         desc='Toggle between split and unsplit sides of stack'
#         ),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),desc="Move window focus to other window"),
 
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.move_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.move_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.move_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.move_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "control"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Emacs programs launched using the key chord CTRL+e followed by 'key'
    KeyChord([mod],"e", [
        Key([], "e",
            lazy.spawn("emacsclient -c -a 'emacs'"),
            desc='Launch Emacs'
            ),
        Key([], "b",
            lazy.spawn("emacsclient -c -a 'emacs' --eval '(ibuffer)'"),
            desc='Launch ibuffer inside Emacs'
            ),
        Key([], "d",
            lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'"),
            desc='Launch dired inside Emacs'
            ),
        Key([], "i",
            lazy.spawn("emacsclient -c -a 'emacs' --eval '(erc)'"),
            desc='Launch erc inside Emacs'
            ),
        Key([], "m",
            lazy.spawn("emacsclient -c -a 'emacs' --eval '(mu4e)'"),
            desc='Launch mu4e inside Emacs'
            ),
        Key([], "n",
            lazy.spawn("emacsclient -c -a 'emacs' --eval '(elfeed)'"),
            desc='Launch elfeed inside Emacs'
            ),
        Key([], "s",
            lazy.spawn("emacsclient -c -a 'emacs' --eval '(eshell)'"),
            desc='Launch the eshell inside Emacs'
            ),
        Key([], "v",
            lazy.spawn("emacsclient -c -a 'emacs' --eval '(+vterm/here nil)'"),
            desc='Launch vterm inside Emacs'
            )],
    ),

]



##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 2,
                "margin": 10,
                "font": "Source Code Pro Medium",
                "font_size": 10,
                "border_focus": "#bd93f9",
                "border_normal": "#555555"
                }

# window layouts
layouts = [
    Plasma(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Stack(num_stacks=2, **layout_theme),
    layout.Bsp(**layout_theme),
    layout.Tile(**layout_theme),

    # Try more layouts by unleashing below layouts.
    # layout.Columns(**layout_theme),
    layout.Matrix(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    layout.Zoomy(**layout_theme),
]


# colors for the bar/widgets/panel
def init_colors():
    return [["#282a36", "#282a36"], # color 0 | bg
            ["#282a36", "#282a36"], # color 1 | bg
            ["#f8f8f2", "#f8f8f2"], # color 2 | fg
            ["#ff5555", "#ff5555"], # color 3 | red
            ["#50fa7b", "#50fa7b"], # color 4 | green
            ["#f1fa8c", "#f1fa8c"], # color 5 | yellow
            ["#bd93f9", "#bd93f9"], # color 6 | blue
            ["#ff79c6", "#ff79c6"], # color 7 | magenta
            ["#8be9fd", "#8be9fd"], # color 8 | cyan
            ["#bbbbbb", "#bbbbbb"]] # color 9 | white

def init_separator():
    return widget.Sep(
                size_percent = 60,
                margin = 5,
                linewidth = 2,
                background = colors[1],
                foreground = "#555555"
                )

def nerd_icon(nerdfont_icon, fg_color):
    return widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 16,
                padding=10,
                text = nerdfont_icon,
                foreground = fg_color,
                background = colors[1]
                )

def init_edge_spacer():
    return widget.Spacer(
                length = 5,
                background = colors[1]
                )


colors = init_colors()
sep = init_separator()
space = init_edge_spacer()

widget_defaults = dict(
    font='Source Code Pro Medium',
    fontsize=12,
    padding=5,
)
extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
            # Left Side of the bar

            space,
            #widget.Image(
            #    filename = "/usr/share/pixmaps/archlinux-logo.png",
            #    background = colors[1],
            #    margin = 3
            #),
            widget.Image(
                filename = "/usr/share/pixmaps/archlinux-logo.png",
                background = colors[1],
                margin = 3,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(
                        'j4-dmenu-desktop'
                    ),
                    'Button3': lambda : qtile.cmd_spawn(
                        f'{terminal} -e vim {home_dir}/.config/qtile/config.py'
                    )
                }
            ),
            widget.GroupBox(
                font = "Iosevka Nerd Font",
                fontsize = 14,
                foreground = colors[2],
                background = colors[1],
                borderwidth = 4,
                highlight_method = "text",
                this_current_screen_border = colors[6],
                active = colors[4],
                inactive = colors[2]
            ),
            sep,
            nerd_icon(
                " ???",
                colors[6]
            ),
            widget.Battery(
                foreground = colors[2],
                background = colors[1],
                format = "{percent:2.0%}"
            ),
            nerd_icon(
                "???",
                colors[3]
            ),
            widget.PulseVolume(
                foreground = colors[2],
                background = colors[1]
            ),
            widget.Spacer(
                length = bar.STRETCH,
                background = colors[1]
            ),

            # Center bar

            nerd_icon(
                "???",
                colors[7]
            ),
            widget.CurrentLayout(
                foreground = colors[2],
                background = colors[1]
            ),
            sep,
            nerd_icon(
                "???",
                colors[3]
            ),
            widget.CPU(
                format = "{load_percent}%",
                foreground = colors[2],
                background = colors[1],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                }
            ),
            nerd_icon(
                "???",
                colors[4]
            ),
            widget.Memory(
                format = "{MemUsed:.0f}{mm}",
                foreground = colors[2],
                background = colors[1],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                }
            ),
            nerd_icon(
                "???",
                colors[6]
            ),
            widget.GenPollText(
                foreground = colors[2],
                background = colors[1],
                update_interval = 5,
                func = lambda: storage.diskspace('FreeSpace'),
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                }
            ),
            sep,
            nerd_icon(
                "???",
                colors[4]
            ),
            widget.GenPollText(
                foreground = colors[2],
                background = colors[1],
                update_interval = 5,
                func = lambda: subprocess.check_output(f"{home_dir}/.config/qtile/scripts/num-installed-pkgs").decode("utf-8")
            ),
            sep,
            nerd_icon(
                "???",
                colors[7]
            ),   
            widget.KeyboardLayout(
                foreground = colors[2],
                background = colors[1],
                configured_keyboards=['us', 'az', 'ir', 'de' , 'fr']
            ),

            widget.Chord(
                foreground = colors[2],
                background = colors[1],
            ),


            # Left Side of the bar

            widget.Spacer(
                length = bar.STRETCH,
                background = colors[1]
            ),
            nerd_icon(
                "???",
                colors[4]
            ),
            widget.Net(
                format = "{down} ?????? {up}",
                foreground = colors[2],
                background = colors[1],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn("def-nmdmenu")
                }
            ),
            sep,
            nerd_icon(
                "???",
                colors[7]
            ),
            widget.Clock(
                format = '%b %d-%Y',
                foreground = colors[2],
                background = colors[1]
            ),
            nerd_icon(
                "???",
                colors[8]
            ),
            widget.Clock(
                format = '%I:%M %p',
                foreground = colors[2],
                background = colors[1]
            ),
            widget.Systray(
                background = colors[1]
            ),
            space
        ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[-2:]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

# screens/bar
def init_screens():
    return [
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.7, size=24, margin=[5,10,0,10])),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.7, size=24, margin=[5,10,0,10])),
            ]


# custom workspace names and initialization
class Groupings:

    def init_group_names(self):
        return [("???", {"layout": "monadtall"}),     # Terminals
                ("???", {"layout": "monadtall"}),     # Web Browser
                ("???", {"layout": "monadtall"}),     # File Manager
                ("???", {"layout": "monadtall"}),     # Text Editor
                ("???", {"layout": "monadtall"}),     # Media
                ("???", {"layout": "monadtall"}),     # Music/Audio
                ("???", {"layout": "monadtall"})]    # Settings

    def init_groups(self):
        return [Group(name, **kwargs) for name, kwargs in group_names]


if __name__ in ["config", "__main__"]:
    group_names = Groupings().init_group_names()
    groups = Groupings().init_groups()
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group



def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#
# assign apps to groups/workspace
#
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}

#     # assign deez apps
#     d[group_names[0][0]] = ['Alacritty', 'xfce4-terminal']
#     d[group_names[1][0]] = ['Navigator', 'discord', 'brave-browser', 'midori', 'qutebrowser']
#     d[group_names[2][0]] = ['pcmanfm', 'thunar']
#     d[group_names[3][0]] = ['code', 'geany']
#     d[group_names[4][0]] = ['vlc', 'obs', 'mpv', 'mplayer', 'lxmusic', 'gimp']
#     d[group_names[5][0]] = ['spotify']
#     d[group_names[6][0]] = ['lxappearance', 'gpartedbin', 'lxtask', 'lxrandr', 'arandr', 'pavucontrol', 'xfce4-settings-manager']

#     wm_class = client.window.get_wm_class()[0]
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)


main = None
@hook.subscribe.startup
def start_once():
    start_script = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    subprocess.call([start_script])

@hook.subscribe.startup_once
def start_always():
    # fixes the cursor
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(wm_class='Viewnior'),  # Photos/Viewnior 
    Match(wm_class='Alafloat'),  # Floating Alacritty Terminal 
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

## Setup MutableScratch
mutscr = MutableScratch()
groups.append(Group(''))

keys.extend( [
    EzKey('M-S-<minus>', mutscr.add_current_window()),
    EzKey('M-<minus>',   mutscr.toggle()),
    EzKey('M-C-<minus>', mutscr.remove()),
] )
