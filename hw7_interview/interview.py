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
        string_length = len(string)
        for number, element in enumerate(string, start=1):

            # если текущий элемент является открывающим - пишем в стек
            if element in BRACKETS.keys():
                self.push(element)
            # если текущий элемент закрывающий, проверяем, соответствует ли он последнему открывающему в стеке
            elif element in BRACKETS.values():
                # если соответствует - снимаем открывающий элемент
                if BRACKETS.get(self.peek()) == element:
                    self.pop()
                else:
                    return f'string {string} is not balanced'
            # если дошли до конца строки и стек пустой: строка сбалансирована
            if self.is_empty() and number == string_length:
                return f'string {string} is balanced'
            else:
                return f'string {string} is not balanced'


if __name__ == '__main__':
    strings = ['(((([{}]))))', '[([])((([[[]]])))]{()}', '{{[()]}}', '}{}', '{{[(])]}}', '[[{())}]']
    obj = Stack()
    for s in strings:
        print(obj.is_balanced(s))
