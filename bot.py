# -*- coding: utf-8 -*-
import driver
import json
import os
import re
import socket
import traceback

msg_format = re.compile("^(?::(\S+) )?(\S+)( (?!:)(?:.+?))?(?: :(.+))?$")

def main():
    with open('config.json') as fd:
        irc = Ircbot(**json.load(fd))
    irc.connect()
    irc.mainloop()

class Ircbot(object):
    def __init__(self, server, port, nick, channel):
        self.server   = server
        self.port     = 6667
        self.username = nick
        self.realname = 'a bot by Cheery'
        self.nick     = nick
        self.driver_mt = os.path.getmtime(driver.__file__)
        # kanava jolle botti halutaan
        self.channel = channel
        # luodaan socket
        self.socket = socket.socket()
        # päälooppia toistettan kunnes done = 1
        self.done = 0

    def send( self, string ):
        self.socket.send( string + '\r\n' )

    def connect( self ):
        self.socket.connect( ( self.server, self.port ) )
        self.send( 'NICK %s' % self.nick )
        self.send( 'USER %s a a :%s' % ( self.username, self.realname ) )
        # liitytään kanavalle
        self.send( 'JOIN %s' % self.channel )

    def check( self, line ):
        match = msg_format.match(line)
        if not match:
            print line
            return
        prefix, command, params, trailing = match.groups()
        if params is not None:
            params = params.strip()
        print (prefix, command, params, trailing)
        if command == 'PING':
            self.send( 'PONG :abc' )
        else:
            try:
                self.refresh_driver()
                driver.response(self, prefix, command, params, trailing)
            except Exception as e:
                traceback.print_exc()

    def refresh_driver(self):
        mt = os.path.getmtime(driver.__file__)
        if self.driver_mt < mt:
            reload(driver)
            self.driver_mt = mt


    def mainloop( self ):
        buffer = ''
        while not self.done:
            # vastaanotetaan dataa
            buffer += self.socket.recv( 4096 )
            buffer = buffer.split( '\r\n' )
            for line in buffer[0:-1]:
                self.check( line )
            buffer = buffer[-1]

if __name__ == '__main__': main()
