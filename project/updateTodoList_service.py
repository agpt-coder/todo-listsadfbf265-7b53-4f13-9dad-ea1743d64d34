from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class TodoListOutputObject(BaseModel):
    """
    Will return the updated TODO list object.
    """

    id: int
    title: str
    description: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    userId: int


async def updateTodoList(
    id: int, title: str, description: Optional[str]
) -> TodoListOutputObject:
    """
    Updates the details of an existing TODO list identified by its unique identifier. The request should provide the updated title and description. The response will return the updated TODO list.

    Args:
        id (int): The unique identifier of the TODO list to update.
        title (str): The updated title of the TODO list.
        description (Optional[str]): The updated description of the TODO list.

    Returns:
        TodoListOutputObject: Will return the updated TODO list object.

    Example:
        updated_todo = await updateTodoList(1, 'New Title', 'Updated Description')
    """
    existing_todo = await prisma.models.TodoList.prisma().find_unique(where={"id": id})
    if not existing_todo:
        raise ValueError("TodoList not found")
    updated_todo = await prisma.models.TodoList.prisma().update(
        where={"id": id}, data={"name": title, "description": description}
    )
    output = TodoListOutputObject(
        id=updated_todo.id,
        title=updated_todo.name,
        description=updated_todo.description,
        createdAt=updated_todo.createdAt,
        updatedAt=updated_todo.updatedAt,
        userId=updated_todo.userId,
    )
    return output
