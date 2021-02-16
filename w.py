#!/usr/bin/python3
# -*- coding: latin-1 -*-
#import commands, re, sys
import re, sys
import subprocess
import string

#todo
# colortrans to module
# fix variable names
# process describtion and add awesome font icons
# or for example remove "clear" completely



def get_status_output(*args, **kwargs):
    p = subprocess.Popen(*args, **kwargs)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr

def hexCalc(hexString1, hexString2):
    #eg hexString = "#5fff00

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

def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())


city = sys.argv[1]
cmd = "curl -H 'Accept-Language: en' -s wttr.in/~"+city
#wow = commands.getstatusoutput(cmd)[1]
wow = subprocess.getoutput(cmd)
#wow = commands.getstatusoutput(cmd)[1]
wow = wow.split("\n")[1:6] # strip away some stuff
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
#
#print wow2
wow2 = wow2[:-1]
#print wow2
m = 0
# if temp = n-m i.e range calc mean
if wow2[2] == '..':
    m = 2
    tempColor1 = re.findall('38;5;(.*)m', wow2[1])[0]
    if tempColor1[0] == '0': #why?
        tempColor1 = tempColor1[1:]

    cmd = "python3 /home/nstr/kod/python/colortrans.py %s" % tempColor1
#    tempRGB1 =  commands.getstatusoutput(cmd)[1]
    tmpRGB1 = subprocess.getoutput(cmd)


    tempColor2 = re.findall('38;5;(.*)m', wow2[3])[0]
    if tempColor2[0] == '0': #why?
        tempColor2 = tempColor2[1:]

    cmd = "python3 /home/nstr/kod/python/colortrans.py %s" % tempColor2
#    tempRGB2 =  commands.getstatusoutput(cmd)[1]
    tmpRGB2 = subprocess.getoutput(cmd)

    tempRGB = hexCalc("#"+tempRGB1,"#"+tempRGB2)[1:]

    temp1 = re.sub('.*m', '', wow2[1])
    temp2 = re.sub('.*m', '', wow2[3])

    temp = str((int(temp1) + int(temp2))/2)

    if int(temp) >= 15 or int(temp) <= -10:
        temp = "<b>"+temp+"</b>"
    tempSubString = ' <span foreground="#'+tempRGB+'">'+temp+'</span>'+wow2[2+m]

else:
    # Temperature Section
    tempColor = re.findall('38;5;(.*)m', wow2[1])[0]
    if tempColor[0] == '0': #why?
        tempColor = tempColor[1:]
    cmd = "python3 /home/nstr/kod/python/colortrans.py %s" % tempColor
#    tempRGB =  commands.getstatusoutput(cmd)[1]
    tempRGB = subprocess.getoutput(cmd)

    temp = re.sub('.*m', '', wow2[1])

    tempSubString = ' <span foreground="#'+tempRGB+'">'+temp+'</span>'+wow2[4][2:]

# Wind speed Section:

#['Clear', '38;5;033m-10', '(', '38;5;171m-15', ') °C', '1m↗', '38;5;154m9', 'km/h']
#windSpeedColor = re.findall('38;5;(.*)m', wow2[5+m])[0]
windSpeedColor = re.findall('38;5;(.*)m', wow2[6+m])[0]

if windSpeedColor[0] == '0': #why?
    windSpeedColor = windSpeedColor[1:]
cmd = "python3 /home/nstr/kod/python/colortrans.py %s" % windSpeedColor
#windRGB = commands.getstatusoutput(cmd)[1]
windRGB= subprocess.getoutput(cmd)

windSpeed = re.sub('.*m', '', wow2[6+m])

windSpeed = str(round(int(windSpeed)/(3.6),1))
if str(windSpeed)[-1] == '0':
    windSpeed = str(windSpeed)[:-2]

if str(windSpeed) == '0':
    windSubString = ""
else:
    arrow = wow2[5+m]
    arrow = re.sub('1m', '',arrow).strip()
    arrow = "<b>"+arrow+"</b>"
    windSubString = ' '+arrow+'<span foreground="#'+windRGB+'">'+windSpeed+'</span>m/s'

#weather=$(echo $weather | sed -e 's/Partly cloudy//g')
#weather=$(echo $weather | sed -e 's/Sunny//g')
#weather=$(echo $weather | sed -e 's/Rain Shower//g')
#weather=$(echo $weather | sed -e 's/Light Drizzle//g')
#weather=$(echo $weather | sed -e 's/Drizzle//g')
#weather=$(echo $weather | sed -e 's/Clear//g')
#
#
import fontawesome as fa

var = wow2[0].lower()+"\n"

with open("/home/nstr/WEATHER.txt", "a") as myfile:
    myfile.write(var)


if "cloudy" in wow2[0].lower():
    wow2[0]= ""
    wow2[0] = fa.icons['cloud']
elif "overcast" in wow2[0].lower():
    wow2[0]= ""
    wow2[0] = fa.icons['cloud-rain']
elif "sunny" in wow2[0].lower():
    wow2[0] = fa.icons['sun']
elif "rain" in wow2[0].lower():
    wow2[0] = fa.icons['umberella']
elif "drizzle" in wow2[0].lower():
    wow2[0] = fa.icons['umberella']
elif "snow" in wow2[0].lower():
    wow2[0] = fa.icons['snowflake']
elif "clear" in wow2[0].lower():
    wow2[0]= ""
elif wow2[0] == "":
    tempSubString = tempSubString.lstrip(' ')


#mystery = wow2[0]
#if isascii(mystery):
#    finalString = wow2[0]+tempSubString+windSubString
#else:
#    finalString = tempSubString+windSubString

finalString = wow2[0]+tempSubString+windSubString
print(finalString)



