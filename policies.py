"""
Global policies for constraints.
"""

import pickle
from utils import SERIALIZATION_HELPER, UserType, RecordType, PurposeType, State

try:
    with open('activity_rules.txt', 'rb') as file:
        PURPOSE_ACTIVITY_MAP = dict()
        activity_rules = pickle.loads(file.read())
        for key, value in activity_rules.items():
            PURPOSE_ACTIVITY_MAP[SERIALIZATION_HELPER[key]] = [SERIALIZATION_HELPER[x] for x in value]
except:
    print("Could not load activity rules, generate them first by running generate_activity_rules.py")

USERTYPE_RECORDTYPE_MAP = {
    # UserType.ADMIN :                                                          [],
    UserType.DOCTOR :                                                           [RecordType.REGISTRATION, RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    UserType.NURSE :                                                            [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION],
    UserType.RECEPTIONIST :                                                     [RecordType.REGISTRATION],
    UserType.PHARMACIST :                                                       [RecordType.PRESCRIPTION]
}

USERTYPE_ACTIVITY_MAP = {
    # UserType.ADMIN :                                                          [],
    UserType.DOCTOR :                                                           PURPOSE_ACTIVITY_MAP[PurposeType.SURGERY] + PURPOSE_ACTIVITY_MAP[PurposeType.DIAGNOSIS] + PURPOSE_ACTIVITY_MAP[PurposeType.TREATMENT],
    UserType.NURSE :                                                            PURPOSE_ACTIVITY_MAP[PurposeType.DIAGNOSIS] + PURPOSE_ACTIVITY_MAP[PurposeType.TREATMENT],
    UserType.RECEPTIONIST :                                                     PURPOSE_ACTIVITY_MAP[PurposeType.REGISTRATION],
    UserType.PHARMACIST :                                                       PURPOSE_ACTIVITY_MAP[PurposeType.PURCHASE]
}

ACTIVITY_RECORDTYPE_MAP = {
    PurposeType.REGISTRATION :                                                  [RecordType.REGISTRATION],
    PurposeType.PURCHASE :                                                      [RecordType.PRESCRIPTION],
    PurposeType.DIAGNOSIS.value.DIAGNOSIS1 :                                    [RecordType.BLOOD_TEST, RecordType.MRI],
    PurposeType.DIAGNOSIS.value.DIAGNOSIS2 :                                    [RecordType.BLOOD_TEST, RecordType.MRI],
    PurposeType.SURGERY.value.SURGERY1 :                                        [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    PurposeType.SURGERY.value.SURGERY2 :                                        [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    PurposeType.SURGERY.value.SURGERY3.value.ENTER_VITAL_PARAMETER :            [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    PurposeType.SURGERY.value.SURGERY3.value.ROUNDS1 :                          [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    PurposeType.TREATMENT.value.TREATMENT1 :                                    [RecordType.BLOOD_TEST, RecordType.MRI],
    PurposeType.TREATMENT.value.TREATMENT2 :                                    [RecordType.BLOOD_TEST, RecordType.MRI]
}

PURPOSE_STATE_MAP = {
    PurposeType.SURGERY :                                                       [State.ADMISSION, State.OBSERVATION, State.SURGERY, State.DISCHARGE],
    PurposeType.DIAGNOSIS :                                                     [State.ADMISSION, State.OBSERVATION, State.DISCHARGE],
    PurposeType.TREATMENT :                                                     [State.ADMISSION, State.TREATMENT, State.DISCHARGE],
    PurposeType.REGISTRATION :                                                  [State.ADMISSION, State.DISCHARGE],
    PurposeType.PURCHASE :                                                      [State.ADMISSION, State.DISCHARGE]
}

USERTYPE_STATE_MAP = {
    UserType.RECEPTIONIST :                                                     [State.ADMISSION, State.DISCHARGE],
    UserType.DOCTOR :                                                           [State.OBSERVATION, State.TREATMENT, State.SURGERY],
    UserType.NURSE :                                                            [State.OBSERVATION, State.TREATMENT, State.SURGERY],
    UserType.PHARMACIST :                                                       [State.DISCHARGE]
}