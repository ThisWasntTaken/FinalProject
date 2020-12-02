"""
Useful (and required) utilities like Enumerations and Serialization Maps.
"""

import enum

class UserType(enum.Enum):
    # ADMIN = "Admin"
    DOCTOR = "Doctor"
    NURSE = "Nurse"
    RECEPTIONIST = "Receptionist"
    PHARMACIST = "Pharmacist"

class _Treatment(enum.Enum):
    TREATMENT1 = "Treatment1"
    TREATMENT2 = "Treatment2"

class _Rounds(enum.Enum):
    ENTER_VITAL_PARAMETER = "Enter Vital Parameter"
    ROUNDS1 = "Rounds1"

class _Surgery(enum.Enum):
    SURGERY1 = "Surgery1"
    SURGERY2 = "Surgery2"
    SURGERY3 = _Rounds

class _Diagnosis(enum.Enum):
    DIAGNOSIS1 = "Diagnosis1"
    DIAGNOSIS2 = "Diagnosis2"

class PurposeType(enum.Enum):
    SURGERY = _Surgery
    DIAGNOSIS = _Diagnosis
    REGISTRATION = "Registration"
    PURCHASE = "Purchase"
    TREATMENT = _Treatment

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

class State(enum.Enum):
    ADMISSION = "Admission"
    OBSERVATION = "Observation"
    SURGERY = "Surgery"
    TREATMENT = "Treatment"
    DISCHARGE = "Discharge"

PURPOSE_MAP = {
    "Diagnosis" : PurposeType.DIAGNOSIS,
    "Surgery" : PurposeType.SURGERY,
    "Registration" : PurposeType.REGISTRATION,
    "Purchase" : PurposeType.PURCHASE,
    "Treatment" : PurposeType.TREATMENT
}
INVERSE_PURPOSE_MAP = {val : key for key, val in PURPOSE_MAP.items()}

ACTIVITY_MAP = {
    "Diagnosis1" : PurposeType.DIAGNOSIS.value.DIAGNOSIS1,
    "Diagnosis2" : PurposeType.DIAGNOSIS.value.DIAGNOSIS2,
    "Surgery1" : PurposeType.SURGERY.value.SURGERY1,
    "Surgery2" : PurposeType.SURGERY.value.SURGERY2,
    "Enter Vital Parameter" : PurposeType.SURGERY.value.SURGERY3.value.ENTER_VITAL_PARAMETER,
    "Rounds1" : PurposeType.SURGERY.value.SURGERY3.value.ROUNDS1,
    "Treatment1" : PurposeType.TREATMENT.value.TREATMENT1,
    "Treatment2" : PurposeType.TREATMENT.value.TREATMENT2,
    "Registration" : PurposeType.REGISTRATION,
    "Purchase" : PurposeType.PURCHASE
}
INVERSE_ACTIVITY_MAP = {val : key for key, val in ACTIVITY_MAP.items()}

SERIALIZATION_HELPER = {**PURPOSE_MAP, **ACTIVITY_MAP}
INVERSE_SERIALIZATION_HELPER = {val : key for key, val in SERIALIZATION_HELPER.items()}

USER_TYPE_MAP = {i.value : i for i in UserType}
INVERSE_USER_TYPE_MAP = {val : key for key, val in USER_TYPE_MAP.items()}

RECORD_TYPE_MAP = {i.value : i for i in RecordType}
INVERSE_RECORD_TYPE_MAP = {val : key for key, val in RECORD_TYPE_MAP.items()}

STATE_MAP = {i.value : i for i in State}
INVERSE_STATE_MAP = {val : key for key, val in STATE_MAP.items()}