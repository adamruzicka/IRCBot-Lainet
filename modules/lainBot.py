from bot import Bot
import weather, tinyUrlConverter
import time

class LainBot(Bot):

    def handle_command(self, cmd):
        print "Command {0}".format(cmd)
        com = cmd['command']+'_command'
        if com == 'handle_command':
            return
        if hasattr(self, com):
            exec 'method = self.'+com
            if callable(method):
                out = method(cmd['args'])
                self.sendm(cmd['channel'], out)

    def handle_message(self, msg):
        print "Message from '{0}' on '{1}': '{2}'".format(msg['sender'], msg['channel'], msg['text'])

    def date_command(self, args):
        return 'Today is ' + time.strftime("%a, %b %d, %y", time.localtime()) + '!'

    def time_command(self, args):
        return 'The current time is ' + time.strftime("%H:%M:%S", time.localtime()) + '!'

    def source_command(self, args):
        return 'My source is hosted at: https://github.com/Lacsap-/Lainbot ! Feel free to contribute.'

    def tinyurl_command(self, args):
        #Convert an URL to a tinyUrl
        url = args.strip()
        short_url = tinyUrlConverter.tiny_url(url)
        return str(short_url)

    def weather_command(self, args):
        town = args
        #ask the temperature from the weather.py module
        temp = weather.temperature(town)

        #Reply depending of temperature() output
        if temp == "Not Found":
            return "Sorry, I don't know what town you are talking about!"
        elif temp == "Error":
            return "It seems like there was an error finding your temperature!"
        else:
            return "The current temperature in " + town + " is: " + temp + " C!"

    def help_command(self, args):
        return [
            'Here is the list of all that I can do ! ',
            '- !time makes me tell you the current time (in montreal for now)',
            '- !date makes me tell you the current date',
            '- !weather followed by the name of a town makes me tell you it\'s temperature in Celsius',
            '- !tinyurl followed by a web adress generate a tinyUrl link of it',
            '- !source makes me tell where my source is hosted'
        ]

