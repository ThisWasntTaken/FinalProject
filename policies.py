import pickle
import inspect
from utils import *

try:
    with open('activity_rules.txt', 'rb') as file:
        PURPOSE_ACTIVITY_MAP = dict()
        activity_rules = pickle.loads(file.read())
        for key, value in activity_rules.items():
            PURPOSE_ACTIVITY_MAP[PURPOSE_MAP[key]] = [PURPOSE_MAP[x] for x in value]
except:
    print("Could not load activity rules, generate them first by running policies.py")

USERTYPE_RECORDTYPE_MAP = {
    UserType.DOCTOR : [RecordType.REGISTRATION, RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    UserType.ADMIN : [],
    UserType.NURSE : [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION],
    UserType.RECEPTIONIST : [RecordType.REGISTRATION],
    UserType.PHARMACIST : [RecordType.PRESCRIPTION]
}

USERTYPE_ACTIVITY_MAP = {
    UserType.ADMIN : [],
    UserType.DOCTOR : [PurposeType.SURGERY, PurposeType.DIAGNOSIS, PurposeType.ROUNDS],
    UserType.NURSE : [PurposeType.DIAGNOSIS, PurposeType.ROUNDS],
    UserType.RECEPTIONIST : [PurposeType.REGISTRATION],
    UserType.PHARMACIST : [PurposeType.PURCHASE]
}

ACTIVITY_RECORDTYPE_MAP = {
    PurposeType.SURGERY : [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    PurposeType.DIAGNOSIS : [RecordType.BLOOD_TEST, RecordType.MRI],
    PurposeType.REGISTRATION : [RecordType.REGISTRATION],
    PurposeType.PURCHASE : [RecordType.PRESCRIPTION],
    PurposeType.ROUNDS : [RecordType.BLOOD_TEST, RecordType.MRI]
}

def enumerate_activities(e, l):
    for member in e:  
        if inspect.isclass(member.value) and issubclass(member.value, enum.Enum):
            enumerate_activities(member.value, l)
        else:
            l.append(INVERSE_PURPOSE_MAP[member])
    
    return l

def generate_activity_rules():
    PURPOSE_ACTIVITY_MAP = dict()
    for purpose in PurposeType:
        PURPOSE_ACTIVITY_MAP[INVERSE_PURPOSE_MAP[purpose]] = enumerate_activities(purpose.value, list()) if inspect.isclass(purpose.value) and issubclass(purpose.value, enum.Enum) else [INVERSE_PURPOSE_MAP[purpose]]
    
    with open('activity_rules.txt', 'wb') as file:
     file.write(pickle.dumps(PURPOSE_ACTIVITY_MAP))

if __name__ == "__main__":
    generate_activity_rules()