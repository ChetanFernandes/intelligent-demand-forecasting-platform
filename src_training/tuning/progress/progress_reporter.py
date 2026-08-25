from abc import ABC, abstractmethod

class ProgressReporter(ABC):
    def report(self,metric,step):
        """Report intermediate progress."""
        pass