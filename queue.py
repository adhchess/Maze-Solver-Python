#!/usr/bin/env python3


class Queue:
    queue = []

    def __init__(self, data=[]):
        if isinstance(data, list):
            self.queue = data
        else:
            self.queue.append(data)
    
    def isEmpty(self):
        return len(self.queue) == 0
    
    def enQueue(self, data):
        self.queue.append(data)
    
    def deQueue(self):
        if self.isEmpty() == False:
            return self.queue.pop(0)
        else:
            return False


