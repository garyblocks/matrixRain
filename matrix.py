#!/usr/bin/python
# author: Gary Wang

import subprocess
import sys
import time
import fcntl
import struct
import termios
import random as rand

class matrix(object):

    def __init__(self):
        # constants
        self.height, self.width = struct.unpack('hh', fcntl.ioctl(1, termios.TIOCGWINSZ, '1234'))
        self.half = int(self.width / 2)
        self.green  = '\033[92m'
        self.yellow = '\033[93m'
        self.red    = '\033[91m'
        self.dark   = '\033[90m'
        self.bold   = '\033[1m' + self.green
        self.end    = '\033[0m' + self.green
        self.colors = [self.green, self.yellow, self.red, self.dark, self.bold]
        # variables
        self.matrix = [[' ' for col in range(self.width)] for row in range(self.height)]
        self.mat    = [['  ' for col in range(self.half)] for row in range(self.height)]
        self.status = [['' for col in range(self.width)] for row in range(self.height)]
        self.cnt    = 0
        print(self.green + ''.join(sum(self.matrix, [])))

    def get_char(self):
        r = rand.random()
        if r > 0.5:
            return unichr(rand.randrange(0x0021, 0x007E))
        elif r > 0.2:
            return unichr(rand.randrange(0x0180, 0x024F))
        else:
            return unichr(rand.randrange(0x16A0, 0x16F0))

    def get_jp(self):
        r = rand.random()
        if r > 0.5:
            return unichr(rand.randrange(0x0021, 0x007E)) + ' '
        else:
            return unichr(rand.randrange(0x3041, 0x3097))

    def run(self, colorful=False, jp=True):
        matrix = self.mat if jp else self.matrix
        width  = self.half if jp else self.width
        self.cnt += 1
        # keep most of the matrix
        for i in range(self.height - 1, 0, -1):
            for j in range(width - 1, -1, -1):
                # create flow effect
                if j % 7 == 0 and self.cnt % 2 != 0:
                    continue
                elif j % 3 == 0 and self.cnt % 3 != 0:
                    continue
                elif j % 2 == 0 and self.cnt % 3 != 0:
                    continue
                # move one step
                if matrix[i][j].isspace() != matrix[i - 1][j].isspace():
                    if matrix[i - 1][j] == ' ':
                        matrix[i][j] = ' '
                    elif matrix[i - 1][j] == '  ':
                        matrix[i][j] = '  '
                    elif colorful:
                        self.status[i][j] = self.status[i - 1][j]
                        char = self.get_jp() if jp else self.get_char()
                        matrix[i][j] = self.status[i][j] + char
                    else:
                        char = self.get_jp() if jp else self.get_char()
                        matrix[i][j] = char
        # generate rain
        for k in range(width):
            r = rand.random()
            if matrix[1][k] == ' ' or matrix[1][k] == '  ':
                if r > 0.05:
                    self.matrix[0][k] = '  ' if jp else ' '
                elif colorful:
                    char = self.get_jp() if jp else self.get_char()
                    self.status[0][k] = rand.sample(self.colors, 1)[0]
                    matrix[0][k] = self.status[0][k] + char
                else:
                    char = self.get_jp() if jp else self.get_char()
                    matrix[0][k] = char
            else:
                char = self.get_jp() if jp else self.get_char()
                if r > 0.1:
                    matrix[0][k] = char
                else:
                    matrix[0][k] = '  ' if jp else ' '
        # control speed
        time.sleep(0.08)
        # generate output
        self.matrix = matrix
        output = []
        for i in matrix:
            line = ''.join(i)
            if self.width % 2 == 1:
                line += ' '
            output.append(line)
        print(self.green + ''.join(output))

if __name__ == '__main__':
    color = True if 'color' in sys.argv else False
    jp    = False if 'no-jp' in sys.argv else True
    rain = matrix()
    while True:
        try:
            rain.run(color, jp)
        except KeyboardInterrupt:
            subprocess.call(["clear"])
            sys.exit()
