from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Task(BaseModel):
    """
    Task object associated with the TODO list.
    """

    id: int
    title: str
    dueDate: Optional[datetime] = None
    priority: Optional[int] = None
    notes: Optional[str] = None
    completed: bool
    createdAt: datetime
    updatedAt: datetime


class UpdateTaskResponse(BaseModel):
    """
    The response model for task updates. It includes a confirmation message and the details of the updated task.
    """

    message: str
    updatedTask: Task


async def updateTask(
    taskId: int,
    title: Optional[str],
    dueDate: Optional[datetime],
    priority: Optional[int],
    notes: Optional[str],
    completed: Optional[bool],
) -> UpdateTaskResponse:
    """
    This endpoint allows users to update the details of an existing task. Users must provide the task ID as a URL parameter and the updated task details in the request body. On successful update, a confirmation message along with the updated task details is returned. This route ensures the task belongs to the user's TODO list before updating and logs the operation via AuditLogModule.

    Args:
    taskId (int): The ID of the task to be updated.
    title (Optional[str]): The updated title of the task.
    dueDate (Optional[datetime]): The updated due date of the task, if any.
    priority (Optional[int]): The updated priority of the task, if any.
    notes (Optional[str]): The updated notes for the task, if any.
    completed (Optional[bool]): The updated completion status of the task.

    Returns:
    UpdateTaskResponse: The response model for task updates. It includes a confirmation message and the details of the updated task.

    Example:
        await updateTask(1, "New Title", None, 3, "Some notes", True)
        > UpdateTaskResponse(message='Task updated successfully', updatedTask=Task(id=1, title='New Title', dueDate=None, priority=3, notes='Some notes', completed=True, createdAt=datetime.datetime(...), updatedAt=datetime.datetime(...)))
    """
    task = await prisma.models.Task.prisma().find_unique(
        where={"id": taskId}, include={"todoList": {"include": {"user": True}}}
    )
    if not task:
        raise ValueError("Task not found")
    if not task.todoList or not task.todoList.user:
        raise ValueError("Task does not belong to any user's TODO list")
    updated_data = {}
    if title is not None:
        updated_data["title"] = title
    if dueDate is not None:
        updated_data["dueDate"] = dueDate
    if priority is not None:
        updated_data["priority"] = priority
    if notes is not None:
        updated_data["notes"] = notes
    if completed is not None:
        updated_data["completed"] = completed
    updated_task = await prisma.models.Task.prisma().update(
        where={"id": taskId}, data=updated_data
    )
    await prisma.models.AuditLog.prisma().create(
        data={"action": "updateTask", "userId": task.todoList.userId, "taskId": taskId}
    )
    updated_task_model = Task(
        id=updated_task.id,
        title=updated_task.title,
        dueDate=updated_task.dueDate,
        priority=updated_task.priority,
        notes=updated_task.notes,
        completed=updated_task.completed,
        createdAt=updated_task.createdAt,
        updatedAt=updated_task.updatedAt,
    )
    response = UpdateTaskResponse(
        message="Task updated successfully", updatedTask=updated_task_model
    )
    return response
