#!/usr/bin/env python

import socket
import time
import re
from modules import weather, tinyUrlConverter

host = 'IRC_IP'
channel = '#CHANNEL'
password = ''
nicks = 'LainBot'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((host, 6667))
irc.send('USER LainBot LainBot LainBot : Lain Bot\r\n')
irc.send('NICK ' + str(nicks) + '\r\n')
irc.send('JOIN ' + channel + '\r\n')


def sendm(msg):
    irc.send('PRIVMSG ' + channel + ' :' + str(msg) + '\r\n')


def say(args):
    sendm(args)


def motd(args):
    sendm('Hello! I am LainBot! To find out what I can do type !help')


def ping(text):
    irc.send('PONG ' + text.split() [1] + '\r\n')
    print 'PONG ' + text.split()[1] + '\r\n'


def help_command(args):
    sendm('Here is the list of all that I can do ! ')
    sendm('- !time makes me tell you the current time (in montreal for now)')
    sendm('- !date makes me tell you the current date')
    sendm('- !weather followed by the name of a town makes me tell you it\'s temperature in Celsius')
    sendm('- !tinyurl followed by a web adress generate a tinyUrl link of it')


def date(args):
    sendm('Today is ' + time.strftime("%a, %b %d, %y", time.localtime()) + ' !')


def time_command(args):
    sendm('The current time is ' + time.strftime("%H:%M:%S", time.localtime()) + ' !')


def source(args):
    sendm('My source is hosted at : https://github.com/Lacsap-/Lainbot ! Feel free to contribute.')


def tinyurl(args):
    #Convert an URL to a tinyUrl
    url = args.strip()
    short_url = tinyUrlConverter.tiny_url(url)
    sendm(str(short_url))


def kick(args):
    irc.send('JOIN ' + channel + '\r\n')


def join(args):
    das = args.strip()
    irc.send('JOIN ' + str(das) + '\r\n')


def weather_command(args):
    town = args
    #ask the temperature from the weather.py module
    temp = weather.temperature(town)

    #Reply depending of temperature() output
    if temp == "Not Found":
        sendm("Sorry, I don't know what town you are talking about!")
    elif temp == "Error":
        sendm("It seems like there was an error finding your temperature!")
    else:
        sendm("The current temperature in " + town + " is: " + temp + " C!")


def main():
    motd('')
    
    commands = {
        'say': say,
        'motd': motd,
        'help': help_command,
        'date': date,
        'time': time_command,
        'source': source,
        'tinyurl': tinyurl,
        'kick': kick,
        'join': join,
        'weather': weather_command
    }

    while 1:
        text = irc.recv(2040)
        print text.strip()
        
        if re.search('^PING', text):
            ping(text)
        
        regex = re.search(r'!(\w+)', text)
        if not regex:
            continue

        command = regex.group(1)
        args = re.search(r'!(\w+)(.+)', text).group(2).strip()

        if command in commands.keys():
            commands[command](args)


if __name__ == '__main__':
  main()
