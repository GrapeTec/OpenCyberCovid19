
from numpy.random import gamma

class DelayModel :
    def __init__(self, depth = 1) :
        self.depth = depth
        self.buffer = []

    def push(self, input) :
        self.buffer.append(input)
        if len(self.buffer) > self.depth :
            output = self.buffer[0]
            self.buffer = self.buffer[1 : self.depth + 1]
            return output
        return 0

    def getSum(self) :
        sum = 0
        for value in self.buffer :
            sum += value
        return sum

# TO-DO
# class DampingModel :
#     def __init__(self, depth, value) -> None:
#         self.buffer = []
#         self.depth = depth
#         self.value = value
#         for i in range(0, depth + 1) :
#             self.buffer.append(value)

#     def push(self, value) :
#         if self.value == value :
#             return self.shift(value)
#         pass

#     def shift(self, value) :
#         self.buffer.append(value)
#         value = self.buffer[0]
#         self.buffer = self.buffer[1, self.depth + 1]
#         return value