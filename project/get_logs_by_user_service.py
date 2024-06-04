from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AuditLogEntry(BaseModel):
    """
    A single audit log entry providing details of an action performed.
    """

    id: int
    action: str
    timestamp: datetime
    userId: int
    todoListId: Optional[int] = None
    taskId: Optional[int] = None


class GetUserAuditLogsResponse(BaseModel):
    """
    The response model containing the list of audit logs related to actions performed by the specified user.
    """

    audit_logs: List[AuditLogEntry]


async def get_logs_by_user(user_id: int) -> GetUserAuditLogsResponse:
    """
    Fetches all audit logs for a specific user by their user ID. The response is an array of log objects related to the actions performed by the specified user. This helps in monitoring user-specific activities.

    Args:
        user_id (int): The user ID for which to fetch the audit logs.

    Returns:
        GetUserAuditLogsResponse: The response model containing the list of audit logs related to actions performed by the specified user.

    Example:
        user_logs = await get_logs_by_user(1)
    """
    import prisma.models

    audit_log_entries = await prisma.models.AuditLog.prisma().find_many(
        where={"userId": user_id}
    )
    audit_logs = [
        AuditLogEntry(
            id=log.id,
            action=log.action,
            timestamp=log.timestamp,
            userId=log.userId,
            todoListId=log.todoListId,
            taskId=log.taskId,
        )
        for log in audit_log_entries
    ]
    return GetUserAuditLogsResponse(audit_logs=audit_logs)
