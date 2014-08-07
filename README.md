gbstatus
--------

Drop-in replacement for i3status, for use with i3bar / [i3wm](http://i3wm.org/).

To enable, chuck this or similar in your i3 config file:

    bar {
        status_command /path/to/gbstatus
    }

Very much at a "works for me" stage. Displays:

 - all IPv4 addresses by interface
 - wifi SSID(s) connected
 - speed of wired ethernet connections
 - whether wifi is enabled
 - whether wifi hardware switch is turned on
 - list of running LXC containers (via libvirt)
 - battery charge level
 - load average
 - current date / time


