#!/usr/bin/python3
# -*- coding: latin-1 -*-
#import commands, re, sys
import re, sys
import subprocess
import string
import fontawesome as fa
import colortrans

#todo
# colortrans to module
# fix variable names
# process describtion and add awesome font icons
# or for example remove "clear" completely
# write reasonable comments
# clean up code
# check that there is an argument
# write sdout
# write sder
# stdin?
#decypher preparsing and make readable comments
# deal with m = 0 returned somehow from genTemp comes from range thingy
#change name to
#fix range problem


#eg hexString = "#5fff00
#hex to arg
def hexCalc(hexString1, hexString2):

    r1 = int("0x"+hexString1[1:3],16)
    g1 = int("0x"+hexString1[3:5],16)
    b1 = int("0x"+hexString1[5:],16)

    r2 = int("0x"+hexString2[1:3],16)
    g2 = int("0x"+hexString2[3:5],16)
    b2 = int("0x"+hexString2[5:],16)

    r = hex((r1+r2)/2)[2:]
    if r == "0":
        r = "00"
    g = hex((g1+g2)/2)[2:]
    if g == "0":
        g = "00"
    b = hex((b1+b2)/2)[2:]
    if b == "0":
        b = "00"

    return "#"+r+g+b

def getData(location):
    cmd = "curl -H 'Accept-Language: en' -s wttr.in/~"+location
    data = subprocess.getoutput(cmd)
    data = data.split("\n")

    bolt = fa.icons['bolt']
    if len(sys.argv) > 45:
        if "We were unable to find your location" in data[46]:
            print(bolt+" location not found")
            sys.exit(0)

    if "Follow" in data[0]:
        print(bolt+" out of queries")
        sys.exit(0)

    data = data[1:6] #strip away some stuff

    wow = data

    #some ugly parsing
    wow2 = []
    #print wow
    check = 0
    for x in wow:
        apa = x.split('\x1b[')
        for y in apa:
            if "38;5;2" not in y:
                if "0m" in y:
                    if "38;5;" not in y:
                        y = re.sub('0m', '', y).strip()
    #            if "1m" in y:
    #                y = re.sub('1m', '', y).strip()
                y = y.strip()
                if y:
                    wow2.append(y)
            else:
                if apa.index(y) < len(apa) and check == 0:
                    if "km" in apa[apa.index(y)+1]:
                        wow2.append(y.strip())
                        check = 1
                        break
                    else:
                        z = y.strip()
                        if z[-1].isdigit() == True and check == 0:
                            wow2.append(z)
    wow2 = wow2[:-1]
    data = wow2
    return data

def genTemp(data):
    wow2 = data
    m = 0

    # if temp = n-m i.e range calc mean
    if wow2[2] == '..':
        m = 2
        tmpColor1 = re.findall('38;5;(.*)m', wow2[1])[0]
        if tmpColor1[0] == '0': #why?
            tmpColor1 = tmpColor1[1:]

        print(tmpColor1)

        tmpRGB1 = colortrans.short2rgb(tmpColor1)

        tmpColor2 = re.findall('38;5;(.*)m', wow2[3])[0]
        if tmpColor2[0] == '0': #why?
            tmpColor2 = tmpColor2[1:]

        tmpRGB2 = colortrans.short2rgb(tmpColor2)

        tmpRGB = hexCalc("#"+tmpRGB1,"#"+tmpRGB2)[1:]

        tmp1 = re.sub('.*m', '', wow2[1])
        tmp2 = re.sub('.*m', '', wow2[3])

        tmp = str((int(tmp1) + int(tmp2))/2)

        if int(tmp) >= 15 or int(tmp) <= -10:
            tmp = "<b>"+tmp+"</b>"
        tmpSubString = ' <span foreground="#'+tmpRGB+'">'+tmp+'</span>'+wow2[2+m]

    else:
        # tmperature Section
        print(wow2)
        tempColor = re.findall('38;5;(.*)m', wow2[1])[0]
        if tempColor[0] == '0': #why?
            tempColor = tempColor[1:]
        tempRGB = colortrans.short2rgb(tempColor)

        temp = re.sub('.*m', '', wow2[1])

        tempSubString = ' <span foreground="#'+tempRGB+'">'+temp+'</span>'+wow2[4][2:]
    if m > 0:
        print(m)
    return tempSubString

def genWind(data):
    m = 0
    wow2 = data
    # Wind speed Section:
    #['Clear', '38;5;033m-10', '(', '38;5;171m-15', ') °C', '1m↗', '38;5;154m9', 'km/h']
    windSpeedColor = re.findall('38;5;(.*)m', wow2[6+m])[0]

    if windSpeedColor[0] == '0': #why?
        windSpeedColor = windSpeedColor[1:]
    windRGB = colortrans.short2rgb(windSpeedColor)

    windSpeed = re.sub('.*m', '', wow2[6+m])

    windSpeed = str(round(int(windSpeed)/(3.6),1)) #kh/h -> m/s
    if str(windSpeed)[-1] == '0':
        windSpeed = str(windSpeed)[:-2]

    if str(windSpeed) == '0':
        windSubString = ""
    else:
        arrow = wow2[5+m]
        arrow = re.sub('1m', '',arrow).strip()
        arrow = "<b>"+arrow+"</b>"
        windSubString = ' '+arrow+'<span foreground="#'+windRGB+'">'+windSpeed+'</span>m/s'
    return windSubString

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
    wow2 = data

    temp = genTemp(data)
    wind = genWind(data)
    icon = getIcon(data)

    #document all possible strings
    var = data[0].lower()+"\n"
    with open("/home/nstr/WEATHER.txt", "a") as myfile:
        myfile.write(var)

    finalString = icon+temp+wind
    print(finalString)

if __name__ == "__main__":
    main()
