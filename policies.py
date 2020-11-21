import pickle
from utils import SERIALIZATION_HELPER, UserType, RecordType, PurposeType

try:
    with open('activity_rules.txt', 'rb') as file:
        PURPOSE_ACTIVITY_MAP = dict()
        activity_rules = pickle.loads(file.read())
        for key, value in activity_rules.items():
            PURPOSE_ACTIVITY_MAP[SERIALIZATION_HELPER[key]] = [SERIALIZATION_HELPER[x] for x in value]
except:
    print("Could not load activity rules, generate them first by running generate_activity_rules.py")

USERTYPE_RECORDTYPE_MAP = {
    UserType.DOCTOR :                                           [RecordType.REGISTRATION, RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    # UserType.ADMIN :                                          [],
    UserType.NURSE :                                            [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION],
    UserType.RECEPTIONIST :                                     [RecordType.REGISTRATION],
    UserType.PHARMACIST :                                       [RecordType.PRESCRIPTION]
}

USERTYPE_ACTIVITY_MAP = {
    # UserType.ADMIN :                                          [],
    UserType.DOCTOR :                                           PURPOSE_ACTIVITY_MAP[PurposeType.SURGERY] + PURPOSE_ACTIVITY_MAP[PurposeType.DIAGNOSIS] + PURPOSE_ACTIVITY_MAP[PurposeType.ROUNDS],
    UserType.NURSE :                                            PURPOSE_ACTIVITY_MAP[PurposeType.DIAGNOSIS] + PURPOSE_ACTIVITY_MAP[PurposeType.ROUNDS],
    UserType.RECEPTIONIST :                                     PURPOSE_ACTIVITY_MAP[PurposeType.REGISTRATION],
    UserType.PHARMACIST :                                       PURPOSE_ACTIVITY_MAP[PurposeType.PURCHASE]
}

ACTIVITY_RECORDTYPE_MAP = {
    PurposeType.REGISTRATION :                                  [RecordType.REGISTRATION],
    PurposeType.PURCHASE :                                      [RecordType.PRESCRIPTION],
    PurposeType.ROUNDS.value.ENTER_VITAL_PARAMETER :            [RecordType.BLOOD_TEST, RecordType.MRI],
    PurposeType.ROUNDS.value.ROUNDS1 :                          [RecordType.BLOOD_TEST, RecordType.MRI],
    PurposeType.DIAGNOSIS.value.DIAGNOSIS1 :                    [RecordType.BLOOD_TEST, RecordType.MRI],
    PurposeType.DIAGNOSIS.value.DIAGNOSIS2 :                    [RecordType.BLOOD_TEST, RecordType.MRI],
    PurposeType.SURGERY.value.SURGERY1 :                        [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    PurposeType.SURGERY.value.SURGERY2 :                        [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    PurposeType.SURGERY.value.SURGERY3.value.INNERSURGERY1 :    [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    PurposeType.SURGERY.value.SURGERY3.value.INNERSURGERY2 :    [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI]
}