from datetime import datetime
from typing import List, Optional

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


class GetTodoListResponse(BaseModel):
    """
    Response model for fetching a specific TODO list by its unique identifier. It includes details of the TODO list such as title, description, creation date, and associated tasks.
    """

    id: int
    name: str
    description: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    tasks: List[Task]


async def getTodoList(id: int) -> GetTodoListResponse:
    """
    Fetches a specific TODO list by its unique identifier. The response will include all the details of the TODO list such as title, description, creation date, and associated tasks.

    Args:
        id (int): The unique identifier of the TODO list to be fetched.

    Returns:
        GetTodoListResponse: Response model for fetching a specific TODO list by its unique identifier. It includes details of the TODO list such as title, description, creation date, and associated tasks.

    Example:
        todo_list = await getTodoList(1)
        print(todo_list)
        # Output: GetTodoListResponse(id=1, name='Groceries', description='Weekly groceries list', ...)
    """
    todo_list = await prisma.models.TodoList.prisma().find_unique(
        where={"id": id}, include={"tasks": True}
    )
    if not todo_list:
        raise ValueError(f"TODO list with id {id} not found")
    tasks_list = todo_list.tasks if todo_list.tasks is not None else []
    tasks = [
        Task(
            id=task.id,
            title=task.title,
            dueDate=task.dueDate,
            priority=task.priority,
            notes=task.notes,
            completed=task.completed,
            createdAt=task.createdAt,
            updatedAt=task.updatedAt,
        )
        for task in tasks_list
    ]
    response = GetTodoListResponse(
        id=todo_list.id,
        name=todo_list.name,
        description=todo_list.description,
        createdAt=todo_list.createdAt,
        updatedAt=todo_list.updatedAt,
        tasks=tasks,
    )
    return response
