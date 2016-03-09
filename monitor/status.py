class Status:
        def __init__(self):
                self.checks = []
                self.index = 0

        def add(self, check):
                self.checks.append(check)

        def flush(self):
                self.checks = []
