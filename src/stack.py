class Stack(list):
    def push(self, a):
        return self.append(a)
    
    def pop(self):
        if len(self) == 0:
            raise RuntimeError('Tried popping from empty stack!')
        return super().pop()