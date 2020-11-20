import enum
import inspect

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

print(_InnerSurgery.INNERSURGERY1 == PurposeType.SURGERY.value.SURGERY3.value.INNERSURGERY1)