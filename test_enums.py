import enum

class _Inside(enum.Enum):
    Downstairs = 'downstairs'
    Upstairs = 'upstairs'

class Location(enum.Enum):
    Outside = 'outside'
    Inside = _Inside 

print(Location.Inside.value.Downstairs.value)