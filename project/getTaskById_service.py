from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GetTaskResponseModel(BaseModel):
    """
    Model for the response containing the details of the specified task. It includes fields such as title, description, status, and due date.
    """

    id: int
    title: str
    description: Optional[str] = None
    dueDate: Optional[datetime] = None
    priority: Optional[int] = None
    notes: Optional[str] = None
    completed: bool
    createdAt: datetime
    updatedAt: datetime


async def getTaskById(taskId: int) -> GetTaskResponseModel:
    """
    This endpoint retrieves the details of a specific task using its ID. Users need to provide the task ID as a URL parameter. The response will include task details such as title, description, status, and due date. It helps users to view individual task details.

    Args:
    taskId (int): The ID of the task to retrieve.

    Returns:
    GetTaskResponseModel: Model for the response containing the details of the specified task. It includes fields such as title, description, status, and due date.

    Example:
        task = await getTaskById(1)
        print(task)
    """
    task = await prisma.models.Task.prisma().find_unique(where={"id": taskId})
    if not task:
        raise ValueError(f"Task with ID {taskId} not found")
    return GetTaskResponseModel(
        id=task.id,
        title=task.title,
        dueDate=task.dueDate,
        priority=task.priority,
        notes=task.notes,
        completed=task.completed,
        createdAt=task.createdAt,
        updatedAt=task.updatedAt,
    )
