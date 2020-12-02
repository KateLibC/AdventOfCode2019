import itertools
from time import time

code = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,2,9,19,23,1,9,23,27,2,27,9,31,1,31,5,35,2,35,9,39,1,39,10,43,2,43,13,47,1,47,6,51,2,51,10,55,1,9,55,59,2,6,59,63,1,63,6,67,1,67,10,71,1,71,10,75,2,9,75,79,1,5,79,83,2,9,83,87,1,87,9,91,2,91,13,95,1,95,9,99,1,99,6,103,2,103,6,107,1,107,5,111,1,13,111,115,2,115,6,119,1,119,5,123,1,2,123,127,1,6,127,0,99,2,14,0,0]
debug = True

class intmachine(object):
    def __init__(self, intcode):
        self.intcode = intcode
        self.opcodes = {
            1: {'f': self.op_01, 'i': 3, 'p': False},
            2: {'f': self.op_02, 'i': 3, 'p': False},
            99: {'f': None, 'i': None, 'p': True}
        }
        self.pc = 0
        self.opstate = True
        self.op_func = None
        self.op_data = []
        self.debug = False

    def debugMsg(self, message):
        if self.debug:
            out = ''
            if message is not None:
                out = f'[DEBUG] [PC: {self.pc}] {message}'
            print(out)

    def iterate(self):
        if len(self.intcode) < self.pc:
            self.debugMsg(message='EOL')
            return
        elif self.intcode[self.pc] is 99 and self.opstate:
            self.debugMsg(message='HALT')
            self.debugMsg(message=None)
            return
        else:
            v = self.intcode[self.pc]
            if self.opstate:
                self.op_func = self.opcodes[v]
                self.debugMsg(message=f'(OPC) Set opcode: {v}')
                self.opstate = False
            else:
                if 'i' in self.op_func.keys():
                    self.op_data.append(v)
                    if len(self.op_data) == self.op_func['i']:
                        self.op_func['f'](self.op_data)
                        self.op_data = []
                        self.op_func = None
                        self.opstate = True
            self.pc += 1
            self.iterate()

    def setIntcode(self, position, value):
        ov = self.intcode[position]
        self.debugMsg(message=f'(STA) Pos: {position} - Now: {ov} New: {value}')
        self.intcode[position] = value

    def readIntcode(self, position):
        ov = self.intcode[position]
        self.debugMsg(message=f'(LDA) Pos: {position} - Value: {ov}')
        return ov

    def op_01(self, values):
        noun, verb, out = values
        self.debugMsg(message=f'(ADD) Noun Pos: {noun} - Verb Pos: {verb} - Out pos: {out}')
        noun = self.readIntcode(noun)
        verb = self.readIntcode(verb)
        self.debugMsg(message=f'(ADD) Noun Val: {noun} - Verb Val: {verb}')
        self.setIntcode(position=out, value=noun + verb)

    def op_02(self, values):
        noun, verb, out = values
        self.debugMsg(message=f'(MUL) Noun Pos: {noun} - Verb Pos: {verb} - Out pos: {out}')
        noun = self.readIntcode(noun)
        verb = self.readIntcode(verb)
        self.debugMsg(message=f'(MUL) Noun Val: {noun} - Verb Val: {verb}')
        self.setIntcode(position=out, value=noun * verb)

def printCode(ic):
    ic = [str(x) for x in ic]
    ic = ','.join(ic)
    print(ic)

def runMachine(ic, n, v, debug=False):
    m = intmachine(intcode=ic)
    m.debug = debug
    m.setIntcode(position=1, value=n)
    m.setIntcode(position=2, value=v)
    m.iterate()
    return m.intcode

if __name__ == '__main__':
    ts = time()
    p = True
    i = []
    for x in range(100):
        for y in range(100):
            i.append([x, y])
    for x,y in i:
        d = runMachine(ic=[1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,2,9,19,23,1,9,23,27,2,27,9,31,1,31,5,35,2,35,9,39,1,39,10,43,2,43,13,47,1,47,6,51,2,51,10,55,1,9,55,59,2,6,59,63,1,63,6,67,1,67,10,71,1,71,10,75,2,9,75,79,1,5,79,83,2,9,83,87,1,87,9,91,2,91,13,95,1,95,9,99,1,99,6,103,2,103,6,107,1,107,5,111,1,13,111,115,2,115,6,119,1,119,5,123,1,2,123,127,1,6,127,0,99,2,14,0,0], n=x, v=y, debug=debug)
        if d[0] == 19690720:
            print(d)
            print(x, y)
            print(100 * x + y)
            print(time() - ts)
            quit()