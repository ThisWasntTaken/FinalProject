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

class StatusType(enum.Enum):
    ACTIVE = "Active"
    ACCEPTED = "Accepted"
    DENIED = "Denied"
    REVOKED = "Revoked"

PURPOSE_MAP = {"Diagnosis" : PurposeType.DIAGNOSIS, "Surgery" : PurposeType.SURGERY}
INVERSE_PURPOSE_MAP = {val : key for key, val in PURPOSE_MAP.items()}
USER_TYPE_MAP = {"Admin" : UserType.ADMIN, "Doctor" : UserType.DOCTOR, "Nurse" : UserType.NURSE, "Receptionist" : UserType.RECEPTIONIST, "Pharmacist" : UserType.PHARMACIST}
INVERSE_USER_TYPE_MAP = {val : key for key, val in USER_TYPE_MAP.items()}