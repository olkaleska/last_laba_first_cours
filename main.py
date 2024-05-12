"""Create my_graph.dot, depending if it's weekday or weekend"""
import random
from collections import deque
from graphviz import Source

def create_str_file(edes_list, linking_list):
    """Функція, що створює відповідний до автомата словник, і записує його до файлу"""
    dot_code = """digraph G {
    graph [rankdir=LR labelfontcolor=red fontname="monospace" nodesep=1.0 size="7.75,10.25"]
    node [fontname="monospace" fontsize=11]
    edge [fontname="monospace" color="grey" fontsize=11]

"""
    for i, el in enumerate(edes_list):
        if i == len(edes_list)-1:
            dot_code += f'\t{el} [label="{el}" shape="doublecircle"]\n'
        else:
            dot_code += f'\t{el} [label="{el}" shape="circle"]\n'
    dot_code += '\n'
    for first in linking_list:
        dot_code += f'\t{first[0]} -> {first[1]} [label="{first[2]}"]\n'
    dot_code += '}'
    with open('automate.dot', 'w', encoding='utf-8') as new_file:
        new_file.write(dot_code)

class State:
    """Перелік усіх можливих станів"""
    def __init__(self):
        self.SLEEP = 'SLEEP'
        self.EAT = "EAT"
        self.GO_HICKING = "GO_HICKING"
        self.GO_CYCLING = "GO_CYCLING"
        self.UNIVERSITY = "UNIVERSITY"
        self.STUDING = "STUDING"
        self.CYCLING = "CYCLING"
        self.MEATING_FRIENDS = "MEATING_FRIENDS"
        self.UNEXPECTED_EVENT = 'UNEXPECTED_EVENT'

State = State()

class Automat:
    """
    Наш автоматик, який перевіряє який тип дня
    І відповідно до нього, створюємо дані, щоб передати у створення файлу
    """
    def __init__(self, day_of_week, hours_to_display):
        self.state = "start"
        if day_of_week in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
            self.day_of_week = ('weekend' if day_of_week in ['Saturday', 'Sunday'] else 'weekday')
        else:
            raise NameError
        self.edes_list = []
        self.linking_list = []
        hours_to_display = sorted(hours_to_display)
        self.queue = deque(hours_to_display)

    def change_state_weekday(self):
        """Змінюємо стани"""
        while self.queue:
            curr = self.queue.popleft()
            timed = self.state
            if curr <= 8 or curr == 21 or curr >= 23:
                self.state, lable = State.SLEEP, 'Just sleeping'
            # Якщо поганий настрій, треба йти поїсти
            elif random.randint(0, 10) == 3 and curr > 12:
                self.state, lable = State.EAT, 'I need some sweets'
            # Або хоч з друзями погомоніти
            elif random.randint(0, 10) == 2 and curr > 12 and curr < 21:
                self.state, lable = State.MEATING_FRIENDS,'Friends can also help'
            elif 8 < curr <= 12:
                self.state, lable = State.UNIVERSITY, 'My UNI is also important'
            elif curr == 13 or curr == 19 or curr == 22:
                self.state, lable = State.EAT, 'Food. Finally!'
            elif 13 < curr < 21:
                self.state, lable = State.STUDING, "Homework won't do itself"
            else:
                self.state, lable = State.CYCLING, "I need somehow get home"

            if self.state in self.edes_list:
                self.edes_list.remove(self.state)
            self.edes_list.append(self.state)
            if [timed, self.state, lable] not in self.linking_list:
                self.linking_list.append([timed, self.state, lable])

    def change_state_weekend(self):
        """Змінюємо стани"""
        while self.queue:
            curr = self.queue.popleft()
            timed = self.state
            if curr < 9 or curr >= 23:
                self.state, lable = State.SLEEP, 'Just sleeping'
            elif curr == 9 or curr == 22:
                self.state, lable = State.EAT, 'Food. Finally!'
            elif random.randint(0, 10) == 7 and curr < 11:
                print('Time for fun')
                self.state, lable = State.UNEXPECTED_EVENT, 'Going somewhere cool'
                while any([self.queue.count(el) for el in list(self.queue) if el <= 21]):
                    self.queue.popleft()
            elif random.randint(0, 100) % 2 == 0:
                self.state, lable = State.GO_HICKING, 'Love Mountains'
                while any([self.queue.count(el) for el in list(self.queue) if el <= 21]):
                    self.queue.popleft()
            else:
                self.state, lable = State.GO_CYCLING, 'I want to ride my bicycle, I want to ride my bike'
                while any([self.queue.count(el) for el in list(self.queue) if el <= 21]):
                    self.queue.popleft()

            if self.state in self.edes_list:
                self.edes_list.remove(self.state)
            self.edes_list.append(self.state)
            if [timed, self.state, lable] not in self.linking_list:
                self.linking_list.append([timed, self.state, lable])

def main():
    """Our main"""
    auto = Automat('Saturday', [el for el in range(1, 25)])
    if auto.day_of_week == 'weekday':
        auto.change_state_weekday()
    else:
        auto.change_state_weekend()
    create_str_file(auto.edes_list, auto.linking_list)
    with open("automate.dot", "r", encoding='utf-8') as f:
        gr = Source(f.read())

if __name__ == "__main__":
    main()
