import enum

class UserType(enum.Enum):
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    NURSE = "Nurse"
    RECEPTIONIST = "Receptionist"
    PHARMACIST = "Pharmacist"

class PurposeType(enum.Enum):
    SURGERY = "Surgery"
    DIAGNOSIS = "Diagnosis"
    REGISTRATION = "Registration"
    PURCHASE = "Purchase"
    ROUNDS = "Rounds"

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

PURPOSE_MAP = {"Diagnosis" : PurposeType.DIAGNOSIS, "Surgery" : PurposeType.SURGERY, "Registration" : PurposeType.REGISTRATION, "Purchase" : PurposeType.PURCHASE, "Rounds" : PurposeType.ROUNDS}
INVERSE_PURPOSE_MAP = {val : key for key, val in PURPOSE_MAP.items()}
USER_TYPE_MAP = {"Admin" : UserType.ADMIN, "Doctor" : UserType.DOCTOR, "Nurse" : UserType.NURSE, "Receptionist" : UserType.RECEPTIONIST, "Pharmacist" : UserType.PHARMACIST}
INVERSE_USER_TYPE_MAP = {val : key for key, val in USER_TYPE_MAP.items()}
RECORD_TYPE_MAP = {"Registration" : RecordType.REGISTRATION, "BloodTest" : RecordType.BLOOD_TEST, "Prescription" : RecordType.PRESCRIPTION, "MRI" : RecordType.MRI}
INVERSE_RECORD_TYPE_MAP = {val : key for key, val in RECORD_TYPE_MAP.items()}

USERTYPE_RECORDTYPE_MAP = {
    UserType.DOCTOR : [RecordType.REGISTRATION, RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    UserType.ADMIN : [],
    UserType.NURSE : [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION],
    UserType.RECEPTIONIST : [RecordType.REGISTRATION],
    UserType.PHARMACIST : [RecordType.PRESCRIPTION]
}

USERTYPE_PURPOSETYPE_MAP = {
    UserType.ADMIN : [],
    UserType.DOCTOR : [PurposeType.SURGERY, PurposeType.DIAGNOSIS, PurposeType.ROUNDS],
    UserType.NURSE : [PurposeType.DIAGNOSIS, PurposeType.ROUNDS],
    UserType.RECEPTIONIST : [PurposeType.REGISTRATION],
    UserType.PHARMACIST : [PurposeType.PURCHASE]
}

PURPOSETYPE_RECORDTYPE_MAP = {
    PurposeType.SURGERY : [RecordType.BLOOD_TEST, RecordType.PRESCRIPTION, RecordType.MRI],
    PurposeType.DIAGNOSIS : [RecordType.BLOOD_TEST, RecordType.MRI],
    PurposeType.REGISTRATION : [RecordType.REGISTRATION],
    PurposeType.PURCHASE : [RecordType.PRESCRIPTION],
    PurposeType.ROUNDS : [RecordType.BLOOD_TEST, RecordType.MRI]
}