# weatheri3blocks
Weather for i3blocks written in python parsing wttr.in


This is a small python script to parse some weather information from
https://wttr.in/ and output the data with pretty colors and fontawesome
icons. for i3blocks



Example
     <span foreground="#00ffff">-3</span>°C <b>↘</b><span foreground="#afff00">2.5</span>m/s


block:

    [weather]
    markup=pango
    separator=true
    command=python3 ~/code/python/w.py kiev
    interval=300

example picture

![image](block.jpg)



# requierments, configuration and installation
just download w.py add a block in your i3blocks config and use the place
you're in as an argument. Set the interval to something reasonable not
to make wtr.in angry. 

pip3 install fontawesome

cred for color translation thingy
