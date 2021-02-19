#!/usr/bin/python3
# -*- coding: latin-1 -*-
import re, sys
import requests
import fontawesome as fa
import colortrans

#todo
# fix variable names
# example remove "clear" completely?
# write reasonable comments
# clean up code
# write sdout
# write sder
# stdin?
# decypher preparsing and make readable comments

def getData(location):
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

    if "Follow" in data[0]:
        print(bolt+" out of queries")
        sys.exit(0)
    return data

def parseData(data):
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
        for x in entry:
            if "38;5;2" not in x:
                if ("0m" in x or "1m" in x) and "38;5;" not in x:
                        x = re.sub('[1|0]m', '', x).strip()
                x = x.strip()
                if x not in ['','(',') °C']:
                    if "38;5;" in x:
                        color = re.findall('38;5;(.*)m', x)[0]
                        if color[0] == '0':
                            color = color[1:]
                        value = re.sub('.*m', '', x)
                        x = (color,value)
                    output.append(x)

    output[-3] = output[-3][2:] #fulhax to fix deg C
    return output

def genTemp(data):
    color = data[1][0]
    temp = data[1][1]
    if len(data) == 5:
        color2 = data[2][0]
        temp2 = data[2][1]
        temp = round((int(temp)+int(temp2))/2)
        color = str(int((int(color)+int(color2))/2))

    colorRGB = colortrans.short2rgb(color)
    if int(temp) >= 15 or int(temp) <= -10:
        temp  = "<b>"+str(temp)+"</b>"
    tempStr = ' <span foreground="#'+colorRGB+'">'+temp+'</span>'+data[-3]
    return tempStr

def genWind(data):
    color = data[-1][0]
    colorRGB = colortrans.short2rgb(color)
    wind = data[-1][1]
    wind = str(round(int(wind)/(3.6),1)) #kh/h -> m/s

    if str(wind)[-1] == '0':
        wind = str(wind)[:-2]
    if str(wind) == '0':
        output = ""
    else:
        arrow = data[-2]
        arrow = "<b>"+arrow+"</b>"
        output = ' '+arrow+'<span foreground="#'+colorRGB+'">'+wind+'</span>m/s'
    return output

def getIcon(data):
    s = data[0].lower()
    icon = ""
    if "cloudy" in s:
        icon = fa.icons['cloud']
    elif "overcast" in s:
        icon = fa.icons['cloud-rain']
    elif "sunny" in s:
        icon = fa.icons['sun']
    elif "rain" in s:
        icon = fa.icons['umberella']
    elif "drizzle" in s:
        icon = fa.icons['umberella']
    elif "snow" in s:
        icon = fa.icons['snowflake']
    elif "clear" in s:
        icon= ""
    return icon

def main():
    if len(sys.argv) < 2:
        bolt = fa.icons['bolt']
        print(bolt+"must provide a location")
        sys.exit(0)

    location = sys.argv[1]
    data = getData(location)
    data = parseData(data)

    temp = genTemp(data)
    wind = genWind(data)
    icon = getIcon(data)

    var = data[0].lower()+"\n"
    with open("/home/nstr/WEATHER.txt", "a") as myfile:
        myfile.write(var)

    finalString = icon+temp+wind
    print(finalString)

if __name__ == "__main__":
    main()
