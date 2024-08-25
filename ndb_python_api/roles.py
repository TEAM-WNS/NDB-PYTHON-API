from enum import Enum
class Roles(Enum):
    ADMIN = "admin"
    MEMBER = "member"

    @property
    def role(self):
        return self.value
    