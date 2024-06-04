from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateTaskResponse(BaseModel):
    """
    The response model for the newly created task. This includes the task ID, title, description, due date, priority, notes, and related todo list ID.
    """

    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    notes: Optional[str] = None
    todo_list_id: int


async def createTask(
    todo_list_id: int,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    priority: Optional[int] = None,
    notes: Optional[str] = None,
) -> CreateTaskResponse:
    """
    This endpoint allows users to create a new task within a specific TODO list. The user needs to provide the TODO list ID and the task details (e.g., title, description, due date). Upon successful creation, the response will include the new task's ID and details. This operation will interact with TodoListModule to ensure the TODO list exists and with AuditLogModule to log the task creation event.

    Args:
        todo_list_id (int): The ID of the TODO list where the task will be created.
        title (str): The title of the new task.
        description (Optional[str]): The detailed description of the new task.
        due_date (Optional[datetime]): The due date of the new task.
        priority (Optional[int]): The priority level of the new task.
        notes (Optional[str]): Additional notes for the new task.

    Returns:
        CreateTaskResponse: The response model for the newly created task. This includes the task ID, title, description, due date, priority, notes, and related todo list ID.

    Example:
        response = createTask(1, 'Buy groceries', 'Buy milk and eggs', datetime.now(), 2, 'Remember to check for discounts')
    """
    todo_list = await prisma.models.TodoList.prisma().find_unique(
        where={"id": todo_list_id}
    )
    if not todo_list:
        raise ValueError(f"TODO list with ID {todo_list_id} does not exist")
    task = await prisma.models.Task.prisma().create(
        data={
            "title": title,
            "dueDate": due_date,
            "priority": priority,
            "notes": notes,
            "todoListId": todo_list_id,
        }
    )
    await prisma.models.AuditLog.prisma().create(
        data={
            "action": "Task Created",
            "timestamp": datetime.now(),
            "userId": todo_list.userId,
            "todoListId": todo_list_id,
            "taskId": task.id,
        }
    )
    response = CreateTaskResponse(
        id=task.id,
        title=task.title,
        description=description,
        due_date=task.dueDate,
        priority=task.priority,
        notes=task.notes,
        todo_list_id=task.todoListId,
    )
    return response
