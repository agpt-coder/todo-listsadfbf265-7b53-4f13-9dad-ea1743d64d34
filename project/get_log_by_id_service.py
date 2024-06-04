from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    """
    Response model for the audit log containing details such as timestamp, user ID, action performed, and associated TODO list or task ID.
    """

    id: int
    action: str
    timestamp: datetime
    userId: int
    todoListId: Optional[int] = None
    taskId: Optional[int] = None


async def get_log_by_id(log_id: int) -> AuditLogResponse:
    """
    Fetches a specific audit log by its ID. The expected response is a log object, providing details such as timestamp, user ID, action performed, and associated TODO list or task ID. This allows an admin to review specific changes.

    Args:
    log_id (int): The ID of the audit log to be fetched.

    Returns:
    AuditLogResponse: Response model for the audit log containing details such as timestamp, user ID, action performed, and associated TODO list or task ID.

    Example:
    log = await get_log_by_id(123)
    print(log)
    """
    log = await prisma.models.AuditLog.prisma().find_unique(where={"id": log_id})
    if not log:
        raise ValueError(f"Audit log with ID {log_id} not found.")
    return AuditLogResponse(
        id=log.id,
        action=log.action,
        timestamp=log.timestamp,
        userId=log.userId,
        todoListId=log.todoListId,
        taskId=log.taskId,
    )
