# weatheri3blocks
Weather for i3blocks written in python parsing wttr.in


This is a small python script to parse some weather information from
https://wttr.in/ and output the information in pretty colors +
fontawesome icons to a pango formated sting in a i3blocks


Example
 <span foreground="#00ffff">-3</span>°C <b>↘</b><span foreground="#afff00">2.5</span>m/s



example picture

block:

    [weather]
    markup=pango
    separator=true
    command=python3 ~/code/python/w.py pripyat
    interval=300



requierments

pip3 install fontawesome

cred for color translation
