#!/usr/bin/env python3

from heapq import heapify, heappush, heappop
from dataclasses import dataclass, field
from typing import Any
class PriorityQueue:
    @dataclass(order=True)
    class __PrioritizedItem:
        __priority: Any
        __item: Any=field(compare=False)
        __valid:bool=field(default=True,compare=False)
        
        def __contains__(self, key):
            return key == self.__item

        def setValid(self, value: bool = False):
            self.__valid = value

        def setItem(self, value: Any):
            self.__item = value

        def isValid(self):
            return self.__valid

        def getData(self):
            return self.__item

    __queue: list
    __reverse: bool = False
    __priorityType: Any = int
    __duplicatesAllowed: bool = False
    __invalidItems: int
    def __init__(self, priorityType: Any = int, reverse: bool = False, duplicatesAllowed:bool = False):
        if priorityType != int and priorityType != tuple:
            raise TypeError("priorityType must be int or tuple. Current type: {0}".format(priorityType))

        self.__queue = []
        self.__reverse = reverse
        self.__priorityType = priorityType
        self.__duplicatesAllowed = duplicatesAllowed
        self.__invalidItems = 0

    def isEmpty(self):
        return len(self.__queue) == 0

    def refactor(self):
        print("Refactoring. This may take a while.")
        heap = []

        for item in self.__queue:
            if item.isValid():
                heappush(heap, item)

        self.__invalidItems = 0
        self.__queue = heap

    def update(self, key, priority):
        if not isinstance(priority, self.__priorityType):
            raise TypeError("priorityType mismatch. Expected {0} got {1}".format(self.__priorityType, type(priority)))
        if self.__duplicatesAllowed:
            print("Update requested when duplicates are allowed. invalidating duplicate data in queue")
        itemExists = False
        for item in self.__queue:
            if key in item and item.isValid():
                itemExists = True
                item.setValid(False)
                self.__invalidItems += 1
        if itemExists:
            heappush(self.__queue, self.__PrioritizedItem(priority, key))
        else:
            print("key not found. No new data added. Use enQueue function to add new data")

    def enQueue(self, priority, data):
        if not isinstance(priority, self.__priorityType):
            raise TypeError("priorityType mismatch. Expected {0} got {1}".format(self.__priorityType, type(priority)))
        if not self.__duplicatesAllowed:
            for item in self.__queue:
                if data in item and item.isValid():
                    print("duplicate data entered when duplicates not allowed. Invalidating old data. Use update function to update data")
                    item.setValid(False)
                    self.__invalidItems += 1
        #print(data)
        heappush(self.__queue, self.__PrioritizedItem(priority, data))
        #print(self.__queue[0].getData())

    def deQueue(self):
        if self.isEmpty():
            raise IndexError("attempted to deQueue from an empty queue")
        
        item = heappop(self.__queue)
        while not item.isValid():
            self.__invalidItems -= 1
            if not self.isEmpty():
                item = heappop(self.__queue)
            else:
                print("no valid data in queue")
                return None
        if len(self.__queue) > 0:
            if self.__invalidItems / len(self.__queue) > 0.2:
                print("invalid items beyond the threshold of acceptability")
                self.refactor()
    
        return item.getData()

    def getQueue(self):
        return self.__queue
"""
class PriorityQueue:
    __queue = []
    __reverse = False
    __priority = None
    __type = int
    __duplicatesAllowed = False
    def __init__(self, reverse = False, priority = None, type = int, duplicatesAllowed = False):
        if not isinstance(reverse, bool):
            raise TypeError("reverseOrder must be bool. Current type: {0}".format(type(reverse)))
        
        if priority is not None and not callable(priority):
            raise TypeError("priority must be None(default sorting) or a function. Current type: {0}".format(type(priority)))

        if not isinstance(duplicatesAllowed, bool):
            raise TypeError("duplicatesAllowed must be bool. Current type: {0}".format(type(duplicatesAllowed)))
        
        self.__queue = []
        self.__reverse = reverse
        self.__priority = priority
        self.__type = type
        self.__duplicatesAllowed = duplicatesAllowed

    def empty(self):
        return len(self.__queue) == 0

    def enQueue(self, data):
        if not isinstance(data, self.__type):
            raise TypeError("data must be type {0}. Current type: {1}".format(self.__type, type(data)))
        if not self.__duplicatesAllowed:
            if data in self.__queue:
                return
        self.__queue.append(data)

    def deQueue(self):
        if self.empty():
            raise IndexError("Attempted to deQueue from an empty queue")
        self.__queue.sort(reverse = self.__reverse, key = self.__priority)
        return self.__queue.pop(0)

    def clear(self):
        self.__queue.clear()

    def size(self):
        return len(self.__queue)
"""
