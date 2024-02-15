from .priority_queue import PriorityQueue, PriorityQueueLeaf
from datetime import date

import colorama
import datetime
import pickle
import os

colorama.init(autoreset=True)


class Task(object):
    def __init__(self, task_id: str, deadline: date, task_desc: str, priority: int):
        self.id       = task_id
        self.deadline = deadline
        self.desc     = task_desc
        self.priority = priority

    def __repr__(self):
        return f"[{self.id}][{self.deadline}][{self.priority}]: {self.desc}"


class TaskTree(object):
    def __init__(self, tree_path: os.PathLike or str) -> None:
        self.tree_path = tree_path
        if os.path.exists(tree_path):
            print(f"Loading task tree from {tree_path}")
            with open(tree_path, 'rb') as file:
                self.tree = pickle.load(file)
        else:
            print(f"Couldn't find task tree at {tree_path}")
            print(f"Creating new tree")
            self.tree = PriorityQueue()
        self.checkpoint()

    def checkpoint(self) -> None:
        with open(self.tree_path, 'wb') as file:
            pickle.dump(self.tree, file)

    def push_task(self, task: Task) -> None:
        leaf = PriorityQueueLeaf(
            priority = self.__get_priority(task.priority, task.deadline),
            value    = task,
        )
        self.tree.push(leaf)
        self.checkpoint()

    def complete(self):
        with open("./all", 'a+', encoding="utf-8") as file:
            res = self.tree.pop()
            if res is not None:
                s = res.value.__repr__() + "\n"
                file.write(s)
        self.checkpoint()

    def __get_priority(self, priority: int, deadline: datetime.datetime) -> float:
        ded = (int(datetime.datetime.today().timestamp()) - int(deadline.timestamp()))
        return ded + priority

    def update(self):
        new_tree = PriorityQueue()
        for task in self.tree:
            new_tree.push(
                PriorityQueueLeaf(
                    priority = self.__get_priority(
                        priority = task.value.priority,
                        deadline = task.value.deadline,
                    ),
                    value = task.value
                )
            )
        new_tree.n = self.tree.n
        new_tree.t = self.tree.t
        self.tree  = new_tree

    @staticmethod
    def __get_date_timestamp(data: date) -> float:
        return datetime.datetime.strptime(data.strftime("%d/%m/%Y"), "%d/%m/%Y").timestamp()

    def __repr__(self) -> str:
        # get longest vars
        longest_id       = 0
        longest_deadline = 0
        longest_desc     = 0
        longest_priority = 0
        for node in self.tree:
            longest_id       = max(longest_id, len(str(node.value.id)))
            longest_deadline = max(longest_deadline, len(str(node.value.deadline)))
            longest_desc     = max(longest_desc, len(str(node.value.desc)))
            longest_priority = max(longest_priority, len(str(node.value.priority)))

        if len(self.tree) != 0:
            res =  "╔" + "═"*longest_id + "╦" + "═"*longest_deadline + "╦" + "═"*longest_desc + "╦" + "═"*longest_priority + "╗"+'\n'
            for i, leaf in enumerate(self.tree):
                if leaf.value.deadline < datetime.datetime.today():
                    color = colorama.Fore.RED
                else:
                    if i == 0:
                        color = colorama.Fore.GREEN
                    else:
                        color = colorama.Fore.WHITE

                res += f"║{color}{str(leaf.value.id      ):^{longest_id}}"       + colorama.Fore.WHITE
                res += f"║{color}{str(leaf.value.deadline):^{longest_deadline}}" + colorama.Fore.WHITE
                res += f"║{color}{str(leaf.value.desc    ):^{longest_desc}}"     + colorama.Fore.WHITE
                res += f"║{color}{str(leaf.value.priority):^{longest_priority}}" + colorama.Fore.WHITE
                res += f"║\n"
                if i == len(self.tree) - 1:
                    res += "╚" + "═"*longest_id + "╩" + "═"*longest_deadline + "╩" + "═"*longest_desc + "╩" + "═"*longest_priority + "╝"+'\n'
                else:
                    res += "╠" + "═"*longest_id + "╬" + "═"*longest_deadline + "╬" + "═"*longest_desc + "╬" + "═"*longest_priority + "╣"+'\n'
            return res
        return ""
