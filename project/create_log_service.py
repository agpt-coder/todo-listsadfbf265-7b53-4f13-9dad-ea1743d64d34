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


async def create_log(
    user_id: int, action: str, todo_list_id: Optional[int], task_id: Optional[int]
) -> AuditLogResponse:
    """
    Creates a new audit log entry. This endpoint is used internally by the TodoListModule and TaskModule to log changes. It expects a JSON payload containing details such as user ID, action performed, and associated TODO list or task ID. The response is the created log object.

    Args:
        user_id (int): The ID of the user performing the action.
        action (str): The action performed by the user (e.g., 'created', 'updated', 'deleted').
        todo_list_id (Optional[int]): The ID of the TODO list associated with the action. Null if the action is associated with a task.
        task_id (Optional[int]): The ID of the task associated with the action. Null if the action is associated with a TODO list.

    Returns:
        AuditLogResponse: Response model for the audit log containing details such as timestamp, user ID, action performed, and associated TODO list or task ID.

    Example:
        create_log(1, 'created', 2, None)
        > AuditLogResponse(id=1, action='created', timestamp=datetime.now(), userId=1, todoListId=2, taskId=None)
    """
    log_data = {
        "action": action,
        "userId": user_id,
        "todoListId": todo_list_id,
        "taskId": task_id,
    }
    created_log = await prisma.models.AuditLog.prisma().create(data=log_data)
    return AuditLogResponse(
        id=created_log.id,
        action=created_log.action,
        timestamp=created_log.timestamp,
        userId=created_log.userId,
        todoListId=created_log.todoListId,
        taskId=created_log.taskId,
    )
