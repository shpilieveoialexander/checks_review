from enum import Enum


class JWTType(str, Enum):
    """JWT token types"""

    ACCESS = "access"
    REFRESH = "refresh"


class UserRole(str, Enum):
    """User roles"""

    ADMIN = "Admin"
    USER = "User"


class GroupRole(str, Enum):
    """User roles"""

    ADMIN = "Group Admin"
    USER = "User"


class PageName(str, Enum):
    """Pages names"""

    CORE = "core"
    ADS = "ads"
    DAYPART = "daypart"
    VOICE = "voice"
    PPC_AUTO = "ppc_auto"
    PPC_AUDIT = "pps_audit"
    ALERTS = "alerts"


class PermsType(int, Enum):
    """Permission type"""

    NONE = (0, "None")
    VIEW = (1, "View")
    VIEW_EDIT = (2, "View & Edit")

    def __new__(cls, value, label="..."):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj
