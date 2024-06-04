from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateTodoListResponse(BaseModel):
    """
    The response model for creating a TODO list. It returns the created TODO list with its unique identifier, title, and optional description.
    """

    id: int
    title: str
    description: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime


async def createTodoList(
    title: str, description: Optional[str], userId: int
) -> CreateTodoListResponse:
    """
    Creates a new TODO list for the user. The request should contain the title of the TODO list and, optionally, a description.
    The response will return the created TODO list with its unique identifier.

    Args:
        title (str): The title of the TODO list.
        description (Optional[str]): An optional description of the TODO list.
        userId (int): The ID of the user creating the TODO list.

    Returns:
        CreateTodoListResponse: The response model for creating a TODO list. It returns the created TODO list with its unique identifier, title, and optional description.

    Example:
        createTodoList("Groceries", "List of grocery items to buy", 1)
        > CreateTodoListResponse(id=1, title="Groceries", description="List of grocery items to buy", createdAt=datetime(...), updatedAt=datetime(...))
    """
    new_todo_list = await prisma.models.TodoList.prisma().create(
        data={"name": title, "description": description, "userId": userId}
    )
    response = CreateTodoListResponse(
        id=new_todo_list.id,
        title=new_todo_list.name,
        description=new_todo_list.description,
        createdAt=new_todo_list.createdAt,
        updatedAt=new_todo_list.updatedAt,
    )
    return response
