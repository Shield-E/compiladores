class TACInterpreter:
    def run(self, string: str):
        from collections import defaultdict
        memory = defaultdict(int)
        for line in string.splitlines():
            self._decode_instruction(line.split(), memory)
        print(memory)
    
    def _decode_instruction(self, instruction, memory):
        if len(instruction) == 3:  # a = b
            self._decode_assign(instruction, memory)
        elif len(instruction) == 5:  # a = b + c
            self._decode_op(instruction, memory) 
        else:
            pass
    
    def _decode_assign(self, instruction: list[str], memory: dict):
        '''
        a = b
        '''
        a = instruction[0]
        b = instruction[2]

        if b.isnumeric():
            memory[a] = int(b)
        else:
            memory[a] = memory[b]

    def _decode_op(self, instruction: list[str], memory: dict):
        '''
        a = b op c
        '''
        a = instruction[0]
        b = instruction[2]
        op = instruction[3]
        c = instruction[4]

        if op == "+":
            memory[a] = memory[b] + memory[c]
        elif op == "-":
            memory[a] = memory[b] - memory[c]
        elif op == "*":
            memory[a] = memory[b] * memory[c]
        elif op == "/":
            memory[a] = memory[b] // memory[c]
        else:
            pass
