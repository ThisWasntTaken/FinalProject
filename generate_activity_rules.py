"""
Generate the purpose to activity mapping.
"""
import pickle
import inspect
import enum
from utils import INVERSE_SERIALIZATION_HELPER, PurposeType

def enumerate_activities(e, l):
    for member in e:  
        if inspect.isclass(member.value) and issubclass(member.value, enum.Enum):
            enumerate_activities(member.value, l)
        else:
            l.append(INVERSE_SERIALIZATION_HELPER[member])
    
    return l

def generate_activity_rules():
    PURPOSE_ACTIVITY_MAP = dict()
    for purpose in PurposeType:
        PURPOSE_ACTIVITY_MAP[INVERSE_SERIALIZATION_HELPER[purpose]] = enumerate_activities(purpose.value, list()) if inspect.isclass(purpose.value) and issubclass(purpose.value, enum.Enum) else [INVERSE_SERIALIZATION_HELPER[purpose]]
    
    with open('activity_rules.txt', 'wb') as file:
     file.write(pickle.dumps(PURPOSE_ACTIVITY_MAP))

if __name__ == "__main__":
    generate_activity_rules()