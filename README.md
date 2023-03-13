# Pipewire Controller

A small GUI app made for use of Pipewire with Reaper DAW. Reaper has some issues with pipewire, for example, It can't be set to ASLA mode because Pipewire won't let Reaper take control of ALSA and in Jack mode it doesn't have any settings for buffer size of sample rate in Reaper itself.

So what this program is intended to do is simply giving a small GUI for adjusting the most common settings aswell as having the option suspending pipewire to allow Reaper to be run with ALSA.

## Dependencies

It should work without installing anything on most common distrobutions since it really only needs pipewire and python3, if anything your distrobution of choice might not run pipewire but in that case you probably don't care about this program to begin with!

### Confirmed working right after a fresh install on the following distrobutions
* Fedora 37
* Manjaro 22.0.0 (KDE & Gnome)
* Pop_OS! 22.04
* Ubuntu 22.04

### If not working right away, try:

Debian-based systems:
```
sudo apt install pipewire python3
```
Fedora-based systems:
```
sudo dnf install pipewire python3
```
Arch-based systems... Well you guys will figure it out but maybe something like this? :D
```
pacman -SdaHsfiJwW98rnewhiofw! pipewire python3
```

## Potential future improvements

* Add 2046 buffer size option
* Put buffer size options in drop-down menu instead of radio buttons
* Make radio buttons positions reflect current settings when starting program, rather than my preferred settings being pre-selected
* When reactivating pipewire after having it suspending the program freezes until pipewire service is running again. On slower systems this time will be long enough to flag the program as unrespnsive and give option to wait or force quit. Instead there should probably be some kind of loading message to let the user know it might take some time.

## Final words

Please note that there are probably much better ways of solving the problems I have attemped to solve with this program and there might even be pre-existing solutions aswell but this was specifically made to work for me and my workflow and to be a real world useful project for gettings into some programming
