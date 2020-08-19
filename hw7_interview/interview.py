from collections import deque

BRACKETS = ['()', '{}', '[]']


class Stack:
    def __init__(self, string):
        self.string = string

    def is_empty(self):
        if not self.string:
            return True
        else:
            return False

    def push(self, element):
        return list(self.string).append(element)

    def pop(self, element):
        return list(self.string).pop(element)

    def peek(self):
        return list(self.string)[-1]

    def size(self):
        return len(self.string)

    def is_balanced(self):
        dq = deque(self.string)
        length = self.size()
        if self.is_empty():
            return f'string {self.string} is not balanced'
        elif length % 2 != 0:
            return f'string {self.string} is not balanced'
        else:
            for i in range(int(length / 2)):
                first = dq.popleft()
                last = dq.pop()
                if f'{first}{last}' not in BRACKETS:
                    return f'string {self.string} is not balanced'
                elif not dq:
                    return f'string {self.string} is balanced'


if __name__ == '__main__':
    strings = ['(((([{}]))))', '[([])((([[[]]])))]{()}', '{{[()]}}', '}{}', '{{[(])]}}', '[[{())}]']
    objects = [Stack(string) for string in strings]
    for obj in objects:
        print(obj.is_balanced())

