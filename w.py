#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' fethes data weather data from wttr.in and transforms it into a
    i3blocks frindly string '''
import re
import sys
import requests
import fontawesome as fa
import colortrans

def get_data(location):
    '''fetches json weather data from wttr.in'''
    # get data from wttr.in
    url = "http://wttr.in/~"+location
    headers={'Accept-Language':'en'}

    resp = requests.get(url,headers=headers)
    data =resp.content.decode("utf-8")
    data = data.split("\n")

    bolt = fa.icons['bolt']
    if len(sys.argv) > 45:
        if "We were unable to find your location" in data[46]:
            print(bolt+" location not found")
            sys.exit(0)

    #indication that they are out of queries
    if "Follow" in data[0]:
        print(bolt+" out of queries")
        sys.exit(0)
    return data

def parse_data(data):
    ''' process the data to get something of the form
    ['Light rain', ('49', '+3'), ('51', '-3'), '°C', '↑', ('196', '39')] or
    ['Sunny', ('154', '16'), '', '↑', ('208', '24')]
     this function is messy and should be imporved.'''

    data = data[1:6] #strip away some stuff
    output = []

    for line in data: # go through every line in data
        entry = line.split('\x1b[') #split line wrt ctrl chars
        if 'km/h' in line: #pick out [-3] do some magic & append
            arrow = entry[-5]
            arrow = re.sub('.*m', '', entry[-5])
            output.append(arrow)
            color = re.findall('38;5;(.*)m', entry[-3])[0]
            value = re.sub('.*m', '', entry[-3])
            wind = (color,value)
            output.append(wind)
            break
        for thing in entry:
            if "38;5;2" not in thing:
                if ("0m" in thing or "1m" in thing) and "38;5;" not in thing:
                    thing = re.sub('[1|0]m', '', thing).strip()
                thing = thing.strip()
                if thing not in ['','(',]:
                    if "38;5;" in thing:
                        color = re.findall('38;5;(.*)m', thing)[0]
                        if color[0] == '0':
                            color = color[1:]
                        value = re.sub('.*m', '', thing)
                        thing = (color,value)
                    output.append(thing)
    return output

def gen_temp(data):
    ''' generate temperature string'''
    color = data[1][0]
    temp = data[1][1]
    if len(data) == 6: #if temp in range calc mean
        color2 = data[2][0]
        temp2 = data[2][1]
        temp = round((int(temp)+int(temp2))/2)
        color = str(int((int(color)+int(color2))/2))

    color_rgb = colortrans.short2rgb(color)
    if isinstance(temp, str):
        if temp[0] == '+':
            temp = temp[1:]
    if int(temp) >= 15 or int(temp) <= -10:
        temp  = "<b>"+str(temp)+"</b>"
    temp = str(temp)
    deg_c = "°C"

    output = ' <span foreground="#'+color_rgb+'">'+temp+'</span>'+deg_c
    return output

def gen_wind(data):
    ''' generate wind speed string'''
    color = data[-1][0]
    color_rgb = colortrans.short2rgb(color)
    wind = data[-1][1]
    wind = str(round(int(wind)/(3.6),1)) #kh/h -> m/s

    if str(wind)[-1] == '0':
        wind = str(wind)[:-2]
    if str(wind) == '0':
        output = ""
    else:
        arrow = data[-2]
        arrow = "<b>"+arrow+"</b>"
        output = ' '+arrow+'<span foreground="#'+color_rgb+'">'+wind+'</span>m/s'
    return output

def get_icon(data):
    ''' replace string "cloud" with cute cloud icon '''
    weather_string = data[0].lower()
    icon = ""
    if "cloudy" in weather_string:
        icon = fa.icons['cloud']
    elif "overcast" in weather_string:
        icon = fa.icons['cloud-rain']
    elif "sunny" in weather_string:
        icon = fa.icons['sun']
    elif "rain" in weather_string:
        icon = fa.icons['umbrella']
    elif "drizzle" in weather_string:
        icon = fa.icons['umbrella']
    elif "snow" in weather_string:
        icon = fa.icons['snowflake']
    elif "clear" in weather_string:
        icon= ""
    else:
        icon = data[0]
    return icon

def main():
    ''' where all the magick happens'''
    if len(sys.argv) < 2:
        bolt = fa.icons['bolt']
        print(bolt+"must provide a location")
        sys.exit(0)

    location = sys.argv[1]
    data = get_data(location)
    data = parse_data(data)

    temp = gen_temp(data)
    wind = gen_wind(data)
    icon = get_icon(data)

    var = data[0].lower()+"\n"  #this is temporary
    with open("WEATHER.txt", "a") as file:
        file.write(var)

    output = icon+temp+wind
    print(output)

if __name__ == "__main__":
    main()
