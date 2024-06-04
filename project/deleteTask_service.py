import prisma
import prisma.models
from pydantic import BaseModel


class DeleteTaskResponseModel(BaseModel):
    """
    Response model for the DELETE /tasks/{taskId} endpoint. Returns a confirmation message indicating the task was successfully deleted.
    """

    confirmation_message: str


async def log_audit_event(taskId: int, userId: int):
    """
    Logs the deletion event of a task in the `AuditLog` table.

    Args:
        taskId (int): The ID of the task being deleted.
        userId (int): The ID of the user who is performing the deletion.

    Returns:
        None

    Example:
        await log_audit_event(123, 1)
    """
    await prisma.models.AuditLog.prisma().create(
        data={"action": "DELETED_TASK", "taskId": taskId, "userId": userId}
    )


async def deleteTask(taskId: int) -> DeleteTaskResponseModel:
    """
    This endpoint handles the deletion of a specific task in a TODO list.
    The user must provide the task ID as a parameter.
    Upon successful deletion, a confirmation message is returned.
    This action verifies the task’s existence within the user's TODO list
    and logs the deletion event using the audit logging mechanism.

    Args:
    taskId (int): The ID of the task to be deleted.

    Returns:
    DeleteTaskResponseModel: Response model for the DELETE /tasks/{taskId} endpoint.
    Returns a confirmation message indicating the task was successfully deleted.

    Example:
        await deleteTask(123)
        > DeleteTaskResponseModel(confirmation_message="Task successfully deleted.")
    """
    task = await prisma.models.Task.prisma().find_unique(where={"id": taskId})
    if not task:
        raise ValueError(f"Task with ID {taskId} does not exist.")
    todoList = await prisma.models.TodoList.prisma().find_unique(
        where={"id": task.todoListId}, include={"user": True}
    )
    if not todoList:
        raise ValueError(f"TodoList with ID {task.todoListId} does not exist.")
    userId = todoList.userId
    await prisma.models.Task.prisma().delete(where={"id": taskId})
    await log_audit_event(taskId, userId)
    return DeleteTaskResponseModel(confirmation_message="Task successfully deleted.")
