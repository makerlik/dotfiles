#!/bin/env bash

# sets wallpaper using feh
bash $HOME/.config/i3/.fehbg

# start arandr
~/.screenlayout/duali3.sh

# polybar
#$HOME/.config/i3/bin/launchbar.sh
~/.config/polybar/launch.sh


# Fix cursor
xsetroot -cursor_name left_ptr

# kill if already running
killall -9 picom xfce4-power-manager ksuperkey dunst sxhkd conky eww

# Launch conky

# sets superkey
ksuperkey -e 'Super_L=Alt_L|F1' &
ksuperkey -e 'Super_R=Alt_L|F1' &

# Launch notification daemon
dunst -config $HOME/.config/i3/dunstrc &

# start compositor and power manager
xfce4-power-manager &

while pgrep -u $UID -x picom >/dev/null; do sleep 1; done
picom --config $HOME/.config/i3/picom.conf &

# start polkit
if [[ ! `pidof xfce-polkit` ]]; then
    /usr/lib/xfce-polkit/xfce-polkit &
fi

/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# start udiskie
udiskie &

# start copyq
copyq &

# start numlockx
numlockx on &

# start unclutter
unclutter &

# start nm-applet
nm-applet &

# set keymap
setxkbmap -model pc105 -layout us,az,tr,ir -option grp:alt_shift_toggle &
