
from abc import ABC, abstractmethod

class Solution(ABC):
    @abstractmethod
    def write(filename):
        """Write the solution out to a file."""
