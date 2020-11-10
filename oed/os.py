#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

from queue import Queue, Empty

from random import choice

from string import ascii_uppercase, digits
from subprocess import Popen, PIPE

from threading import Thread, Event

from time import sleep



class Reader(Thread):

    def __init__(self, source, destination, marker="OED"):
        super().__init__()
        self._source = source
        self._destination = destination
        self._marker = marker
        self._stopped = Event()
 
    def run(self):
        while not self._stopped.is_set():
            response = []
            line = ""
            for any_character in iter(lambda: self._source.read(1), None):
                line += any_character
                if line.startswith(self._marker):
                    self._destination.put("".join(response))
                    response.clear()
                if any_character == "\n":
                    response.append(line)
                    line = ""
        self._destination.put("".join(response))
        self._source.close()
    
    def stop(self):
        self._stopped.set()
        self.join()



class Shell:

    SESSION_ID_LENGTH = 10

    @staticmethod
    def generated_random_ID(length):
        return ''.join(choice(ascii_uppercase + digits) for _ in range(length))
    
    def __init__(self):
        self._shell = None
        self._queue = Queue()

    def start(self):
        self._session_ID = Shell.generated_random_ID(7)
        self._shell = Popen("cmd.exe", stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        self._stdout = Reader(self._shell.stdout, self._queue, self._prompt)
        self._stdout.daemon = True
        self._stdout.start()
        self._set_prompt()
        
    def _set_prompt(self):
        escaped_prompt = self._prompt.replace(">", "$g")
        self.execute("prompt {}".format(escaped_prompt))

    @property
    def _prompt(self):
        return "OeD-{}>".format(self._session_ID)

    def close(self):
        self.execute("exit")
        self._stdout.stop()
        self._shell.terminate()
        
    def execute(self, command):
        print("Sending command: ",  command)
        self._shell.stdin.write(command + "\n")
        self._shell.stdin.flush()
        try:
            return self._queue.get(timeout=10)
        except Empty:
            print("Nothing in the queue after 10 sec.")
            return None

        
        
if __name__ == "__main__":
    shell = Shell()
    shell.start()
    output = shell.execute("dir")
    print(output)
    print("------")
    output = shell.execute("date /t")
    print(output)
    print("------")
    output = shell.execute("hostname")
    print(output)
    print("------")
    shell.close()
    