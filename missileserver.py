#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
USB Missile Command Center
written by Chris Evans <cevans@delta-risk.net>

Mashed up from USB Missile Launcher Python Interface written by Pedram Amini <pamini@tippingpoint.com>
          and  Armageddon USB Missile Launcher by Piotr Maliński (aka riklaunim), http://www.rk.edu.pl

Installation Instructions:
  Grab the prerequisites:
    - apt-get install python-dev
    - apt-get install python-pip
    - sudo pip install --pre pyusb
  Get the necessry files (all in one directory):
    - missileserver.py
    - armageddon.py
    - armageddon.pyc
    - stopmissileserver.sh
  Run:
    python ./missileserver.py
      press 'w' when prompted to start webserver
      browse to http://IP:12345 to attempt to access the command center web page
      browse to http://IP:12345/pass=2492 to access the command center web page
  Only tested with the Dream Cheeky 908 Thunder Missile Launcher and Ubuntu 14.04.2 LTS Desktop 64bit
"""

import ctypes
import struct
import time
from armageddon import Armageddon

PASS = "2492"

########################################################################################################################
if __name__ == "__main__":
    while 1:
        mode = raw_input("[w]eb server or [s]ocket or [c]ommand line? ").lower()

        if mode[0] in ["w", "s", "c"]:
            break

#    m = missile(debug=False)
    m = Armageddon(debug=False)

    def command_processor(cmd):
        percent = None
        if " " in cmd:
            try:
                percent = int(cmd.split(" ", 1)[1])
            except:
                pass

        if cmd.startswith("l"):
            #m.send_cmd(m.LEFT)
            #m.send_cmd(m.STOP)
            m.send_move(m.LEFT, 100)
            return True
        elif cmd.startswith("r"):
            #m.send_cmd(m.RIGHT)
            #m.send_cmd(m.STOP)
            m.send_move(m.RIGHT, 100)
            return True
        elif cmd.startswith("u"):
            #m.send_cmd(m.UP)
            #m.send_cmd(m.STOP)
            m.send_move(m.UP, 100)
            return True
        elif cmd.startswith("d"):
            #m.send_cmd(m.DOWN)
            #m.send_cmd(m.STOP)
            m.send_move(m.DOWN, 100)
            return True
        elif cmd.startswith("f"):
            m.send_cmd(m.FIRE)
            return True
        elif cmd.startswith("s"):
            m.send_cmd(m.STOP)
            return True

        return False


    if mode.startswith("w"):
        import BaseHTTPServer
        import threading

        class web_interface_handler (BaseHTTPServer.BaseHTTPRequestHandler):
            def __init__(self, request, client_address, server):
                BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
#                self.missile = None

            def do_GET (self):
                self.do_everything()

            def do_HEAD (self):
                self.do_everything()

            def do_POST (self):
                self.do_everything()

            def do_everything (self):
                if "pass="+PASS not in self.path:
                    self.send_error(401, "Incorrect 'pass' paramter")
                    return
                if "up" in self.path:
                    #m.send_cmd(self, m.UP, 100)
                    #m.send_cmd(m.STOP)
                    m.send_move(m.UP, 100)
                if "down" in self.path:
                    #m.send_cmd(self, m.DOWN, 100)
                    #m.send_cmd(m.STOP)
                    m.send_move(m.DOWN, 100)
                if "left" in self.path:
                    #m.send_cmd(self, m.LEFT, 100)
                    #m.send_cmd(m.STOP)
                    m.send_move(m.LEFT, 100)
                if "right" in self.path:
                    #m.send_cmd(self, m.RIGHT, 100)
                    #m.send_cmd(m.STOP)
                    m.send_move(m.RIGHT, 100)
                if "fire" in self.path:
                    m.send_cmd(m.FIRE)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                response = """
                <title>Missile Command Center</title>
                <table border=0 cellpadding=20 cellspacing=0 style="font-size: 10em;">
                    <tr><td></td><td><a href="/up{0}">U</a></td><td></td></tr>
                    <tr><td><a href="/left{0}">L</a></td><td><a href="/fire{0}">F</a></td><td><a href="/right{0}">R</a></td></tr>
                    <tr><td></td><td><a href="/down{0}">D</a></td><td></td></tr>
                </table>
                """.format("&pass="+PASS)

                self.wfile.write(response)

        class web_interface_server (BaseHTTPServer.HTTPServer):
            def __init__(self, server_address, RequestHandlerClass, m):
                BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)
                self.RequestHandlerClass.m = m

        class web_interface_thread (threading.Thread):
            def __init__ (self, m):
                threading.Thread.__init__(self)
                self.m = m
                self.server  = None

            def run (self):
                self.server = web_interface_server(('', 12345), web_interface_handler, self.m)
                self.server.serve_forever()

        t = web_interface_thread(m)
        t.start()

    elif mode.startswith("c"):
        while 1:
            cmd = raw_input("cmd> ").lower()

            if cmd == "exit":
                break
            elif command_processor(cmd):
                pass
            elif cmd.startswith("e"):
                ret = eval(cmd.split(" ", 1)[1])
                print "eval returned: %02x" % ret
            else:
                print "valid commands [l]eft [r]ight [u]p [d]own [f]ire re[s]et [e]val <expression>"
    else:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", 12345))
        sock.listen(5)

        print "[*] missile control listening on 0.0.0.0:12345"

        while 1:
            client_sock, client_address = sock.accept()
            print "[*] client connection from %s to missile control" % client_address[0]
            client_sock.send("TSRT MISSILE COMMAND... READY\n")
            auth = False

            while 1:
                try:
                    msg = None
                    cmd = client_sock.recv(1024).lower().rstrip()

                    if not cmd:
                        raise Exception
                except:
                    print "[*] client disconnected"

                print "[*] missile received command: %s" % cmd

                if not auth:
                    if cmd == "password":
                        auth = True
                        msg  = "AUTHORIZATION ACCEPTED\n"
                    else:
                        msg  = "UNAUTHORIZED\n"

                elif cmd == "exit":
                    client_sock.close()
                    break
                elif command_processor(cmd):
                    pass
                else:
                    msg = "valid commands [l]eft [r]ight [u]p [d]own [f]ire re[s]et\n"

                if msg:
                    try:
                        client_sock.send(msg)
                    except:
                        print "[*] client disconnected"
                        break
