class Status:
        def __init__(self):
                self.checks = []
                self.index = 0

        def add(self, check):
                self.checks.append(check)
        
        def __iter__(self):
                return self

        def next(self):
                try:
                        result = self.checks[self.index]
                except IndexError:
                        raise StopIteration
                self.index += 1
                return result


