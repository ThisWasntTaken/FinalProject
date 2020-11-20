import enum

class UserType(enum.Enum):
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    NURSE = "Nurse"
    RECEPTIONIST = "Receptionist"
    PHARMACIST = "Pharmacist"

class _InnerSurgery(enum.Enum):
    INNERSURGERY1 = "InnerSurgery1"
    INNERSURGERY2 = "InnerSurgery2"

class _Surgery(enum.Enum):
    SURGERY1 = "Surgery1"
    SURGERY2 = "Surgery2"
    SURGERY3 = _InnerSurgery

class _Diagnosis(enum.Enum):
    DIAGNOSIS1 = "Diagnosis1"
    DIAGNOSIS2 = "Diagnosis2"

class _Rounds(enum.Enum):
    ENTER_VITAL_PARAMETER = "Enter_Vital_Parameter"
    ROUNDS1 = "Rounds1"

class PurposeType(enum.Enum):
    SURGERY = _Surgery
    DIAGNOSIS = _Diagnosis
    REGISTRATION = "Registration"
    PURCHASE = "Purchase"
    ROUNDS = _Rounds

class StatusType(enum.Enum):
    ACTIVE = "Active"
    ACCEPTED = "Accepted"
    DENIED = "Denied"
    REVOKED = "Revoked"
    CACHED = "Cached"

class RecordType(enum.Enum):
    REGISTRATION = "Registration"
    BLOOD_TEST = "BloodTest"
    PRESCRIPTION = "Prescription"
    MRI = "MRI"

PURPOSE_MAP = {
    "Diagnosis" : PurposeType.DIAGNOSIS,
    "Surgery" : PurposeType.SURGERY,
    "Registration" : PurposeType.REGISTRATION,
    "Purchase" : PurposeType.PURCHASE,
    "Rounds" : PurposeType.ROUNDS,
    "Enter_Vital_Parameter" : PurposeType.ROUNDS.value.ENTER_VITAL_PARAMETER,
    "Rounds1" : PurposeType.ROUNDS.value.ROUNDS1,
    "Diagnosis1" : PurposeType.DIAGNOSIS.value.DIAGNOSIS1,
    "Diagnosis2" : PurposeType.DIAGNOSIS.value.DIAGNOSIS2,
    "Surgery1" : PurposeType.SURGERY.value.SURGERY1,
    "Surgery2" : PurposeType.SURGERY.value.SURGERY2,
    "InnerSurgery1" : PurposeType.SURGERY.value.SURGERY3.value.INNERSURGERY1,
    "InnerSurgery2" : PurposeType.SURGERY.value.SURGERY3.value.INNERSURGERY2
}
INVERSE_PURPOSE_MAP = {val : key for key, val in PURPOSE_MAP.items()}

USER_TYPE_MAP = {
    "Admin" : UserType.ADMIN,
    "Doctor" : UserType.DOCTOR,
    "Nurse" : UserType.NURSE,
    "Receptionist" : UserType.RECEPTIONIST,
    "Pharmacist" : UserType.PHARMACIST
}
INVERSE_USER_TYPE_MAP = {val : key for key, val in USER_TYPE_MAP.items()}

RECORD_TYPE_MAP = {
    "Registration" : RecordType.REGISTRATION,
    "BloodTest" : RecordType.BLOOD_TEST,
    "Prescription" : RecordType.PRESCRIPTION,
    "MRI" : RecordType.MRI
}
INVERSE_RECORD_TYPE_MAP = {val : key for key, val in RECORD_TYPE_MAP.items()}