class TACInterpreter:
    def run(self, tac_code: str):
        from collections import defaultdict
        self.memory = defaultdict(int)
        self._search_labels(tac_code)
        self._execution_loop(tac_code)
        return self.memory
    
    def _search_labels(self, tac_code: str):
        for i, line in enumerate(tac_code.splitlines()):
            instruction = line.split()
            if self._is_label(instruction):
                self.memory[instruction[0]] = i

    def _execution_loop(self, tac_code: str):
        self.memory["ip"] = ip = 0
        lines = tac_code.splitlines()
        while self.memory["ip"] < len(lines):
            instruction = lines[self.memory["ip"]].split()
            self.memory["ip"] += 1
            self._run_instruction(instruction)

    def _run_instruction(self, instruction: list[str]):
        if len(instruction) == 2:  # print a
            self._run_command(instruction)
        elif len(instruction) == 3:  # a = b
            self._run_assign(instruction)
        elif len(instruction) == 5:  # a = b + c
            self._run_op(instruction)
        elif len(instruction) == 6:
            self._run_conditional_jump(instruction)
    
    def _run_command(self, instruction: list[str]):
        '''
        command a
        '''
        command, a = instruction

        if command == "print":
            print(self._val(a))
        if command == "goto":
            self.memory["ip"] = self.memory[a]


    def _run_assign(self, instruction: list[str]):
        '''
        a = b
        '''
        a = instruction[0]
        b = instruction[2]

        if b.isnumeric():
            self.memory[a] = int(b)
        else:
            self.memory[a] = self.memory[b]

    def _run_op(self, instruction: list[str]):
        '''
        a = b op c
        '''
        a = instruction[0]
        b = instruction[2]
        op = instruction[3]
        c = instruction[4]

        if op == "+":
            self.memory[a] = self._val(b) + self._val(c)
        elif op == "-":
            self.memory[a] = self._val(b) - self._val(c)
        elif op == "*":
            self.memory[a] = self._val(b) * self._val(c)
        elif op == "/":
            self.memory[a] = self._val(b) // self._val(c)

    def _run_conditional_jump(self, instruction: list[str]):
        '''
        if a cmp b goto label
        '''
        a = instruction[1]
        cmp = instruction[2]
        b = instruction[3]
        label = instruction[5]
        
        if cmp == "==":
            condition = self._val(a) == self._val(b)
        elif cmp == "!=":
            condition = self._val(a) != self._val(b)
        elif cmp == ">":
            condition = self._val(a) > self._val(b)
        elif cmp == "<":
            condition = self._val(a) < self._val(b)
        elif cmp == ">=":
            condition = self._val(a) >= self._val(b)
        elif cmp == "<=":
            condition = self._val(a) <= self._val(b)

        if condition:
            self.memory["ip"] = self.memory[label]
        
    def _val(self, data: str):
        if data.isnumeric():
            return int(data)
        else:
            return self.memory[data]

    def _is_label(self, instruction: list[str]) -> bool:
        return len(instruction) == 1  # i guess it will be more complex
