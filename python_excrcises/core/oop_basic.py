class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    
    def __init__(self, rank:str,value:int):
        self.rank = rank
        self.value = value
        self._internal =None  # Internal attribute, not part of the public interface
        self.__mangled = None  # Name-mangled attribute, not part of the public interface
        
    def __repr__(self) -> str:
        return f"Card(rank={self.rank!r}, value={self.value!r})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.value == other.value
    
    def __str__(self) -> str:
        return self.rank
    

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.value < other.value