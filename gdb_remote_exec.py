# MIT License
# 
# Copyright (c) 2024 campmccl
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gdb
import socket

port = 12354

class ExecRemote(gdb.Command):
    def __init__(self):
        super(ExecRemote, self).__init__("exec_remote", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', port))
        client.send(arg.encode())
        client.close()

class ExecRemoteLocal(gdb.Command):
    def __init__(self):
        super(ExecRemoteLocal, self).__init__("exec_remote_local", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', port))
        client.send(arg.encode())
        client.close()
        try:
            gdb.execute(arg, from_tty=from_tty)
        except gdb.error as err:
            print(err)

class ExecServer(gdb.Command):
    def __init__(self):
        super(ExecServer, self).__init__("start_server", gdb.COMMAND_USER, completer_class=gdb.COMPLETE_NONE)

    def start_server(self, from_tty):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(1)
        server.bind(('localhost', port))
        server.listen(1)

        try:
            while True:
                client = None
                try:
                    client, addr = server.accept()
                except socket.timeout:
                    pass
                if client == None:
                    continue
                request = client.recv(1024)
                try:
                    gdb.execute(request.decode(), from_tty=from_tty)
                except gdb.error as err:
                    print(err)
                client.close()
        except KeyboardInterrupt:
            print("Terminating server")
            server.close()
        
    
    def invoke(self, arg, from_tty):
        self.start_server(from_tty)

ExecServer()
ExecRemote()
ExecRemoteLocal()
