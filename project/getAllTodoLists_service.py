from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GetTodoListsRequest(BaseModel):
    """
    Request model for retrieving all TODO lists for the authenticated user. The request should include the user's identifier to fetch their TODO lists.
    """

    pass


class TodoListResponse(BaseModel):
    """
    The response model for a TODO list, including its unique identifier, title, and description.
    """

    id: int
    name: str
    description: Optional[str] = None
    userId: int


class GetTodoListsResponse(BaseModel):
    """
    Response model returning a list of TODO lists belonging to the authenticated user. Each TODO list includes its unique identifier, title, and description.
    """

    todolists: List[TodoListResponse]


async def getAllTodoLists(request: GetTodoListsRequest) -> GetTodoListsResponse:
    """
    Retrieves all the TODO lists for the authenticated user. The response will be a list of objects, each representing a TODO list, including its unique identifier, title, and description.

    Args:
    request (GetTodoListsRequest): Request model for retrieving all TODO lists for the authenticated user. The request should include the user's identifier to fetch their TODO lists.

    Returns:
    GetTodoListsResponse: Response model returning a list of TODO lists belonging to the authenticated user. Each TODO list includes its unique identifier, title, and description.

    Example:
        request = GetTodoListsRequest(userId=1)
        response = await getAllTodoLists(request)
        print(response)
    """
    todo_lists = await prisma.models.TodoList.prisma().find_many(
        where={"userId": request.userId}
    )  # TODO(autogpt): Cannot access attribute "userId" for class "GetTodoListsRequest"
    #     Attribute "userId" is unknown. reportAttributeAccessIssue
    todo_list_responses = [
        TodoListResponse(
            id=todo_list.id,
            name=todo_list.name,
            description=todo_list.description,
            userId=todo_list.userId,
        )
        for todo_list in todo_lists
    ]
    return GetTodoListsResponse(todolists=todo_list_responses)
