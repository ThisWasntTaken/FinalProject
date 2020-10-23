import enum

class UserType(enum.Enum):
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    NURSE = "Nurse"
    RECEPTIONIST = "Receptionist"
    PHARMACIST = "Pharmacist"

class PurposeType(enum.Enum):
    DIAGNOSIS = "Diagnosis"
    PRESCRIPTION = "Prescription"

PURPOSE_MAP = {"Diagnosis" : PurposeType.DIAGNOSIS, "Prescription" : PurposeType.PRESCRIPTION}
INVERSE_PURPOSE_MAP = {val : key for key, val in PURPOSE_MAP.items()}
USER_TYPE_MAP = {"Admin" : UserType.ADMIN, "Doctor" : UserType.DOCTOR, "Nurse" : UserType.NURSE, "Receptionist" : UserType.RECEPTIONIST, "Pharmacist" : UserType.PHARMACIST}
INVERSE_USER_TYPE_MAP = {val : key for key, val in USER_TYPE_MAP.items()}