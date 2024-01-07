'''
  ___ _____ ___ _     _____    ____             __ _       
 / _ \_   _|_ _| |   | ____|  / ___|___  _ __  / _(_) __ _ 
| | | || |  | || |   |  _|   | |   / _ \| '_ \| |_| |/ _` |
| |_| || |  | || |___| |___  | |__| (_) | | | |  _| | (_| |
 \__\_\|_| |___|_____|_____|  \____\___/|_| |_|_| |_|\__, |
                                                     |___/ 
'''


from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
import subprocess
from qtile_extras.widget.decorations import PowerLineDecoration

##############
#Startup Apps#
##############

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["/usr/lib/xfce-polkit/xfce-polkit"])
    subprocess.Popen(["picom"])
    subprocess.Popen(["/home/linus/.screenlayout/Perfect.sh"])
    subprocess.Popen(["nitrogen", "--restore"])
    subprocess.Popen(["dunst"])
    subprocess.Popen(["polybar"])

mod = "mod4"
terminal = guess_terminal()

####################
#Keyboard Shortcuts#
####################

keys = [
    Key([mod], "a", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "d", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "s", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "w", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "a", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "d", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "s", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "w", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "a", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "d", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "s", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "w", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod, "shift"],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun")),
    Key([mod], "x", lazy.spawn("betterlockscreen -l dim")),
    Key([mod], "f", lazy.spawn("firefox")),
    Key([mod], "e", lazy.spawn("thunar")),
    Key([mod], "v", lazy.spawn("codium")),
    Key([mod], "p", lazy.spawn("pavucontrol")),
    Key([mod, "shift"], "r", lazy.spawn("rofi -show run")),


]

####################
#Groups(Workspaces)#
####################

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

#########
#Layouts#
#########

layouts = [
    layout.MonadTall(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=0, margin = 19),
    layout.Max(),
    layout.Floating(),
]

#########
#Widgets#
#########

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)

widget.Clock(
    
    
    font='comfortaa', 
    mouse_callbacks = {'Button1': lambda qtile : qtile.cmd_spawn('peaclock')}
)

extension_defaults = widget_defaults.copy()

#################
#Mouse Callbacks#
#################

def open_peaclock(qtile):
    qtile.cmd_spawn('peaclock')

######
#Bars#
######

screens = [
    Screen(
#        top=bar.Bar(
#            [
#                widget.GroupBox(highlight_color='5c4cb200', hide_unused=True, foreground='ffffff', font='comfortaa', highlight_method='line'),
#                widget.Spacer(),
#                widget.Clock(format="%I:%M %a %Y-%m-%d %p", foreground='ffffff', ),
#            ],
#            34,
#            background="00000045",
#        ),
    ),
]

###############
#Floating Mode#
###############

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# IDK Seems stupid
wmname = "LG3D"
