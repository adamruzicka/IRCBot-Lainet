import socket
import re

class Bot:
    def __init__(self, host, channels, nick):
        self.__channels = []
        self.__nick = nick
        self.__connect(host)
        self.__login(nick)
        for channel in channels:
            self.join(channel)
        self.__users = []

    def __connect(self, host):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, 6667))

    def __login(self, username):
        self.__send('USER {0} {0} {0} : {0} {0}'.format(username))
        self.__send('NICK {0}'.format(username))

    def __send(self, msg):
        print("Sending |"+msg+"|")
        self.__socket.send(msg + '\r\n')

    def join(self, channel):
        self.__send('JOIN {0}'.format(channel))
        self.__channels.append(channel)

    def sendm(self, channel, msg):
        if isinstance(msg, list):
            for m in msg:
                self.sendm(channel, m)
        else:
            self.__send('PRIVMSG ' + channel + ' :' + str(msg))

    def say(self, args):
        self.sendm(args)

    def motd(self, args):
        self.sendm('Hello! I am LainBot! To find out what I can do type !help')

    def ping(self, text):
        self.__send("PONG {0}".format(text.split()[1]))

    def handle_command(self, message):
        raise NotImplementedError("This method should be redefined")

    def handle_message(self, message):
        raise NotImplementedError("This method should be redefined")

    def run(self):
        while 1:
            text = self.__socket.recv(2040)
            print text.strip()
            
            if re.search('^PING', text):
                self.ping(text)
                continue
            
            regex = re.search(r'^:([^!]+)!([^ ]+) (\w+) ([a-zA-Z\#\&]+) :(.*)$', text)
            if not regex:
                continue

            message = {
                'sender': regex.group(1),
                'sender_addr': regex.group(2),
                'msg_type': regex.group(3),
                'channel': regex.group(4),
                'text': regex.group(5).strip()
            }

            if message['channel'] == self.__nick:
                message['channel'] = message['sender']

            regex = re.search('!(\w+)(.+)?', message['text'])
            if not regex:
                self.handle_message(message)
            else:
                message['command'] = regex.group(1)
                message['args'] = regex.group(2)
                self.handle_command(message)