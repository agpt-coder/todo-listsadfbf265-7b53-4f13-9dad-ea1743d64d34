import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class DeleteTodoListResponse(BaseModel):
    """
    Response model confirming the deletion of the TODO list.
    """

    message: str


async def deleteTodoList(id: int) -> DeleteTodoListResponse:
    """
    Deletes a specific TODO list by its unique identifier. The response will confirm the deletion. Note: This will also trigger interactions with the TaskModule to delete all associated tasks and with AuditLogModule to log the deletion action.

    Args:
    id (int): The unique identifier of the TODO list to be deleted.

    Returns:
    DeleteTodoListResponse: Response model confirming the deletion of the TODO list.

    Example:
    deleteTodoList(1)
    > DeleteTodoListResponse(message="TODO list with ID 1 has been deleted successfully.")
    """
    todo_list = await prisma.models.TodoList.prisma().find_unique(where={"id": id})
    if not todo_list:
        raise HTTPException(
            status_code=404, detail=f"TODO list with ID {id} not found."
        )
    await prisma.models.Task.prisma().delete_many(where={"todoListId": id})
    await prisma.models.TodoList.prisma().delete(where={"id": id})
    await prisma.models.AuditLog.prisma().create(
        data={
            "action": "Deleted TODO list",
            "userId": todo_list.userId,
            "todoListId": id,
        }
    )
    return DeleteTodoListResponse(
        message=f"TODO list with ID {id} has been deleted successfully."
    )
