'''
  ___  _   _ _         ____             __ _
 / _ \| |_(_) | ___   / ___|___  _ __  / _(_) __ _
| | | | __| | |/ _ \ | |   / _ \| '_ \| |_| |/ _` |
| |_| | |_| | |  __/ | |__| (_) | | | |  _| | (_| |
 \__\_\\__|_|_|\___|  \____\___/|_| |_|_| |_|\__, |
                                             |___/
'''
# By RPICoder
# Based of dt's config

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List

mod = "mod1"  # mod1 is the alt key and mod4 is the windows key
terminal = "xfce4-terminal"
browser = "chromium-browser"
spacing = 500  # Change this value if the time in your panel is not centered
gap = 10

'''
 _  __          ____  _           _ _
| |/ /___ _   _| __ )(_)_ __   __| (_)_ __   __ _ ___
| ' // _ \ | | |  _ \| | '_ \ / _` | | '_ \ / _` / __|
| . \  __/ |_| | |_) | | | | | (_| | | | | | (_| \__ \
|_|\_\___|\__, |____/|_|_| |_|\__,_|_|_| |_|\__, |___/
          |___/                             |___/
'''

keys = [
    # Changing focus between tiled windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    # Changing position of tiled windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Changing size of tiled windows
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),


    # For dual monitors - chaning focus between two screens
    Key([mod, "shift"], "m", lazy.to_screen(0)),
    Key([mod, "shift"], "n", lazy.to_screen(1)),


    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    # Functions Keys
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    Key([], "XF86Display", lazy.spawn("monitor_layout.sh")),

    # Power options for qtile
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "control"], 's', lazy.spawn("xset -display :0.0 dpms force off")),

    Key([mod, "control"], 'k', lazy.layout.increase_ratio()),
    Key([mod, "control"], 'j', lazy.layout.decrease_ratio()),

    # Applications
    Key([mod], "b", lazy.spawn(browser)),
    Key([mod], "f", lazy.spawn("nautilus")),
    Key([mod], "v", lazy.spawn("codium")),
    
    ## Flameshot
    Key([mod], "s", lazy.spawn("flameshot screen -p /home/rpicoder/Pictures")),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui")),  

]


# --- Workspaces ---

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7"]
#group_labels = ["", "", "", "", "", "", ""]
group_labels = [""] * 7
group_layouts = ["columns"] * 7
for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i]
        ))

# Adding workspaces related keyboard shortcuts
for i in groups:
    keys.extend([
        # Change Workspaces
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        # Move window to workspace and don't follow moved window
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        # Move window to workspace and to the workspace of the window
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

layout_defaults = {
    "border_width": 4,  # Width of border around focused window
    "margin": 6,  # Gap between tiled windows
    "border_focus": "BF616A",  # Colour of the border across focused windows
    "border_normal": "1D2330"
}

layouts = [
    layout.Columns(**layout_defaults),
    layout.MonadTall(**layout_defaults),
    layout.Max(**layout_defaults),
    layout.Floating(**layout_defaults),
    # layout.Bsp(**layout_defaults),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

colors = [["#2d333f"],  # Panel Colour 1
          ["#2d333f"],  # Panel Colour 2
          ["#ffffff"],  # Text Colour
          ["#2d333f"],
          ["#D08770"]]  # Nord Orange


'''
 ____                  _  __        ___     _            _       
|  _ \ __ _ _ __   ___| | \ \      / (_) __| | __ _  ___| |_ ___ 
| |_) / _` | '_ \ / _ \ |  \ \ /\ / /| |/ _` |/ _` |/ _ \ __/ __|
|  __/ (_| | | | |  __/ |   \ V  V / | | (_| | (_| |  __/ |_\__ \
|_|   \__,_|_| |_|\___|_|    \_/\_/  |_|\__,_|\__, |\___|\__|___/
                                              |___/              
'''

widget_defaults = dict(
    font="FantasqueSansMono Nerd Font Mono",
    fontsize=20,
    padding=2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth=0,
            padding=10,
            background=colors[0]
        ),
        widget.Image(
            filename="/home/pi/.config/qtile/icons/QPI.png",
            scale="True",
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal)},
            margin=-1,
            background=colors[0]
        ),     
        widget.Sep(
            linewidth=0,
            padding=1,
            background=colors[0]
        ),
        widget.GroupBox(
            fontsize=27,
            margin_y=3,
            margin_x=1,
            padding_y=5,
            padding_x=1,
            borderwidth=3,
            active=colors[4],
            inactive=colors[4],
            foreground=colors[2],
            background=colors[3],
            rounded=True,
            highlight_method="text",
            this_current_screen_border=colors[2],
            this_screen_border=colors[2],
            disable_drag=True,
            spacing=-3,
            margin=2
        ),

        widget.Spacer(
            bar.STRETCH,
            background=colors[0]
        ),
        widget.TextBox(
            text='',
            background=colors[3],
            foreground=colors[4],
            padding=0,
            fontsize=30
        ),
        widget.Sep(
            linewidth=0,
            padding=gap,
            background=colors[0]
        ),
        widget.WindowName(
            background=colors[3],
            foreground=colors[2],
            empty_group_string='Qtile Pi ',
            max_chars=100,
            format='{name}'
        ),
        widget.Sep(
            linewidth=0,
            padding=spacing,
            background=colors[0]
        ),

        widget.Spacer(
            bar.STRETCH,
            background=colors[0]
        ),
        widget.TextBox(
            text='',
            background=colors[3],
            foreground=colors[4],
            padding=0,
            fontsize=30,
        ),
        widget.Clock(
            foreground=colors[2],
            background=colors[3],
            format=" %I:%M %p "
        ),
        widget.Sep(
            linewidth=0,
            padding=5,
            background=colors[0]
        ),
        widget.TextBox(
            text='',
            background=colors[3],
            foreground=colors[4],
            padding=0,
            fontsize=30,
        ),
        widget.Clock(
            foreground=colors[2],
            background=colors[3],
            format=" %a %b %d",
        ),
        widget.Sep(
            linewidth=0,
            padding=gap,
            background=colors[0]
        ),
        widget.TextBox(
            text='',
            background=colors[3],
            foreground=colors[4],
            padding=0,
            fontsize=20
        ),
        widget.Sep(
            linewidth=0,
            padding=3,
            background=colors[0]
        ),
        widget.ThermalSensor(
            foreground=colors[2],
            background=colors[3],
            threshold=90,
            padding=5
        ),
        widget.Sep(
            linewidth=0,
            padding=5,
            background=colors[0]
        ),
        widget.TextBox(
            text='力',
            background=colors[3],
            foreground=colors[4],
            padding=0,
            fontsize=25
        ),
        widget.Memory(
            background=colors[3],
            foreground=colors[2],
            format='{MemUsed: .0f}{mm}',
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                terminal + ' -e htop')},
        ),
        widget.Sep(
            linewidth=0,
            padding=gap,
            background=colors[0]
        ),

        widget.TextBox(
            text='',
            background=colors[3],
            foreground=colors[4],
            padding=0,
            fontsize=35
        ),
        widget.Sep(
            linewidth=0,
            padding=5,
            background=colors[0]
        ),
        widget.CPU(
            background=colors[3],
            foreground=colors[2],
            format='{load_percent}%',
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                terminal + ' -e htop')},
        ),
        widget.Sep(
            linewidth=0,
            padding=gap,
            background=colors[0]
        ),
        widget.TextBox(
            text='蓼',
            background=colors[3],
            foreground=colors[4],
            padding=0,
            fontsize=22
        ),
        widget.Sep(
            linewidth=0,
            padding=4,
            background=colors[0]
        ),
        widget.Volume(
            foreground=colors[2],
            background=colors[3],
            padding=3,
        ),
        widget.Sep(
            linewidth=0,
            padding=4,
            background=colors[0]
        ),
        widget.CurrentLayoutIcon(
                custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                foreground = colors[3],
                background = colors[1],
                padding = 0,
                scale = 0.6
        ),     
        widget.CurrentLayout(
                foreground = colors[2],
                background = colors[3],
                padding = 0,
        ),                
      widget.Systray(
               background = colors[0],
               padding = 2,
               icon_size=20
        ), 
        widget.Sep(
            linewidth=0,
            padding=4,
            background=colors[0]
        ),        

    ]
    return widgets_list


screens = [
    Screen(top=bar.Bar(widgets=init_widgets_list(), size=30,
           margin=5,  background=colors[4],  wallpaper_mode='fill'))
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
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
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


wmname = "Qtile"
