BRACKETS = {'(': ')', '{': '}', '[': ']'}


class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        length = self.size()
        return length == 0

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        length = self.size()
        if length:
            return self.stack[-1]
        else:
            return None

    def size(self):
        return len(self.stack)

    def is_balanced(self, string):
        for i in string:
            if i in BRACKETS.keys():
                self.push(i)
            elif i in BRACKETS.values():
                if BRACKETS.get(self.peek()) == i:
                    self.pop()
                else:
                    return f'string {string} is not balanced'

            if self.is_empty():
                return f'string {string} is balanced'


if __name__ == '__main__':
    strings = ['(((([{}]))))', '[([])((([[[]]])))]{()}', '{{[()]}}', '}{}', '{{[(])]}}', '[[{())}]']
    obj = Stack()
    for s in strings:
        print(obj.is_balanced(s))
