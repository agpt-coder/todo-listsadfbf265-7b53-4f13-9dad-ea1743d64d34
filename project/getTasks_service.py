from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class TaskDetails(BaseModel):
    """
    Model representing the details of a task.
    """

    title: str
    id: int
    description: Optional[str] = None
    completed: bool
    due_date: Optional[datetime] = None


class GetTasksResponse(BaseModel):
    """
    Response model containing the list of tasks associated with the specified TODO list. Each task includes details such as task ID, title, description, status, and due date.
    """

    tasks: List[TaskDetails]


async def getTasks(todo_list_id: int) -> GetTasksResponse:
    """
    This endpoint fetches all tasks associated with a specific TODO list. Users need to provide the TODO list ID.
    The response will include a list of all tasks with their details (e.g., task ID, title, description, status, due date).
    This is primarily used to display tasks belonging to a TODO list, leveraging interaction with the TodoListModule.

    Args:
    todo_list_id (int): The ID of the TODO list whose tasks are to be fetched.

    Returns:
    GetTasksResponse: Response model containing the list of tasks associated with the specified TODO list. Each task includes details such as task ID, title, description, status, and due date.

    Example:
    todo_list_id = 1
    response = await getTasks(todo_list_id)
    print(response)
    > GetTasksResponse(tasks=[TaskDetails(id=1, title="Task1", description="Desc1", completed=False, due_date="2023-12-31T00:00:00"), ...])
    """
    todo_list = await prisma.models.TodoList.prisma().find_unique(
        where={"id": todo_list_id}, include={"tasks": True}
    )
    if not todo_list or not todo_list.tasks:
        return GetTasksResponse(tasks=[])
    task_details_list = [
        TaskDetails(
            id=task.id,
            title=task.title,
            description=task.notes or "",
            completed=task.completed,
            due_date=task.dueDate,
        )
        for task in todo_list.tasks
    ]
    response = GetTasksResponse(tasks=task_details_list)
    return response
