#!/usr/bin/env python

from modules.lainBot import LainBot

if __name__ == '__main__':
    bot = LainBot('irc.freenode.net', ['#testochanneru'], 'LainBot')
    bot.run()
