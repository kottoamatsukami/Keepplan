class PriorityQueueLeaf(object):
    def __init__(self, priority: float, value) -> None:
        self.priority = priority
        self.value    = value

    def __repr__(self):
        return f"Leaf {self.priority}"


class PriorityQueue(object):
    def __init__(self):
        self.queue : list = []
        self.n     : int  = 0
        self.t     : int  = 0

    def push(self, item: PriorityQueueLeaf) -> None:
        self.n += 1
        self.t += 1
        self.queue.append(item)
        self.__buble_up(self.n - 1)

    def peek(self) -> PriorityQueueLeaf:
        return self.queue[0]

    def pop(self) -> PriorityQueueLeaf:
        if self.n > 1:
            res = self.queue[0]
            self.queue[0] = self.queue.pop()
            self.n -= 1
            self.__bubble_down(0)
            return res
        elif self.n == 1:
            self.n -= 1
            return self.queue.pop()

    def __bubble_down(self, index: int):
        while 2*(index + 1) < self.n:
            left_child, right_child = self.queue[2*index + 1], self.queue[2*(index + 1)]
            if left_child.priority > self.queue[index].priority:
                self.queue[index], self.queue[2*index + 1] = self.queue[2*index + 1], self.queue[index]
                index = 2*index + 1
            else:
                self.queue[index], self.queue[2*(index + 1)] = self.queue[2*(index + 1)], self.queue[index]
                index = 2*(index + 1)

    def __buble_up(self, index: int):
        assert index < self.n
        while index > -1:
            if self.queue[index // 2].priority < self.queue[index].priority:
                self.queue[index], self.queue[index // 2] = self.queue[index // 2], self.queue[index]
                index //= 2
            else:
                break

    def __repr__(self) -> str:
        return self.queue.__repr__()

    def __getitem__(self, item):
        return self.queue[item]

    def __iter__(self):
        return iter(self.queue)

    def __len__(self) -> int:
        return self.n


if __name__ == '__main__':
    import random
    print("Running priority queue unit-testing...")
    queue = PriorityQueue()
    nums  = [random.randint(0, 10) for _ in range(5)]
    print(f"Appending next elements:")
    print(nums, f"Sorted: {sorted(nums, reverse=True)}")
    for num in nums:
        queue.push(PriorityQueueLeaf(num, "Some value"))
    print(queue)
    print(f"Popping elements")
    for _ in range(len(nums)):
        print(queue.pop())
