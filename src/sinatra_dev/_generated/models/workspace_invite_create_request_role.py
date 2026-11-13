from enum import StrEnum


class WorkspaceInviteCreateRequestRole(StrEnum):
    ADMIN = "admin"
    MEMBER = "member"

    def __str__(self) -> str:
        return str(self.value)
