import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import project.create_log_service
import project.createTask_service
import project.createTodoList_service
import project.delete_log_service
import project.deleteTask_service
import project.deleteTodoList_service
import project.deleteUser_service
import project.generate_token_service
import project.get_all_logs_service
import project.get_log_by_id_service
import project.get_logs_by_user_service
import project.getAllTodoLists_service
import project.getTaskById_service
import project.getTasks_service
import project.getTodoList_service
import project.getUserProfile_service
import project.invalidate_token_service
import project.loginUser_service
import project.partialUpdateTask_service
import project.refresh_token_service
import project.registerUser_service
import project.updateTask_service
import project.updateTodoList_service
import project.updateUserProfile_service
import project.validate_token_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="TODO lists",
    lifespan=lifespan,
    description="This should be an API that receives peoples TODO lists and store them for the users, they should be able to retreive them from the database",
)


@app.get(
    "/api/token/validate",
    response_model=project.validate_token_service.TokenValidationResponse,
)
async def api_get_validate_token(
    token: str,
) -> project.validate_token_service.TokenValidationResponse | Response:
    """
    Validates the provided JWT token. It ensures the token is not expired and has been issued by the server. It utilizes the UserManagementModule to cross-check user permissions and roles embedded within the token.
    """
    try:
        res = project.validate_token_service.validate_token(token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/users/register",
    response_model=project.registerUser_service.RegisterUserOutput,
)
async def api_post_registerUser(
    username: str, password: str, email: str
) -> project.registerUser_service.RegisterUserOutput | Response:
    """
    Registers a new user in the system. It accepts user details like username, password, and email. Upon successful registration, it returns a success message and the user ID.
    """
    try:
        res = project.registerUser_service.registerUser(username, password, email)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/users/delete", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    auth_token: str,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Deletes the authenticated user account from the system. This action removes all associated data, including TODO lists. Requires a valid token.
    """
    try:
        res = await project.deleteUser_service.deleteUser(auth_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/token/invalidate",
    response_model=project.invalidate_token_service.InvalidateTokenResponse,
)
async def api_delete_invalidate_token(
    token: str,
) -> project.invalidate_token_service.InvalidateTokenResponse | Response:
    """
    Invalidates an existing JWT token, effectively logging the user out. It marks the token as unusable in the token store. This endpoint ensures that the user can log out securely, and their token cannot be reused.
    """
    try:
        res = await project.invalidate_token_service.invalidate_token(token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/audit/logs", response_model=project.get_all_logs_service.AuditLogsResponse)
async def api_get_get_all_logs(
    request: project.get_all_logs_service.GetAuditLogsRequest,
) -> project.get_all_logs_service.AuditLogsResponse | Response:
    """
    Fetches all audit logs. The expected response is an array of log objects, containing details such as timestamp, user ID, action performed, and associated TODO list or task ID. This endpoint allows administrators to review all changes made in the system.
    """
    try:
        res = project.get_all_logs_service.get_all_logs(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/token/refresh", response_model=project.refresh_token_service.TokenResponse
)
async def api_post_refresh_token(
    refresh_token: str,
) -> project.refresh_token_service.TokenResponse | Response:
    """
    Refreshes an existing JWT token. It accepts a valid refresh token, verifies its authenticity, and returns a new JWT token with updated expiration. This ensures continuous access without requiring the user to re-authenticate.
    """
    try:
        res = await project.refresh_token_service.refresh_token(refresh_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/tasks", response_model=project.createTask_service.CreateTaskResponse)
async def api_post_createTask(
    todo_list_id: int,
    title: str,
    description: Optional[str],
    due_date: Optional[datetime],
    priority: Optional[int],
    notes: Optional[str],
) -> project.createTask_service.CreateTaskResponse | Response:
    """
    This endpoint allows users to create a new task within a specific TODO list. The user needs to provide the TODO list ID and the task details (e.g., title, description, due date). Upon successful creation, the response will include the new task's ID and details. This operation will interact with TodoListModule to ensure the TODO list exists and with AuditLogModule to log the task creation event.
    """
    try:
        res = await project.createTask_service.createTask(
            todo_list_id, title, description, due_date, priority, notes
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/tasks/{taskId}",
    response_model=project.partialUpdateTask_service.PatchTaskResponse,
)
async def api_patch_partialUpdateTask(
    taskId: int,
    title: Optional[str],
    dueDate: Optional[datetime],
    priority: Optional[int],
    notes: Optional[str],
    completed: Optional[bool],
) -> project.partialUpdateTask_service.PatchTaskResponse | Response:
    """
    This endpoint allows users to partially update fields of an existing task without providing the complete task details. Users need to provide the task ID as a URL parameter and the fields to update in the request body. Upon success, the response includes the updated task details. Interaction with AuditLogModule is required to log this change.
    """
    try:
        res = project.partialUpdateTask_service.partialUpdateTask(
            taskId, title, dueDate, priority, notes, completed
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/todolists", response_model=project.getAllTodoLists_service.GetTodoListsResponse
)
async def api_get_getAllTodoLists(
    request: project.getAllTodoLists_service.GetTodoListsRequest,
) -> project.getAllTodoLists_service.GetTodoListsResponse | Response:
    """
    Retrieves all the TODO lists for the authenticated user. The response will be a list of objects, each representing a TODO list, including its unique identifier, title, and description.
    """
    try:
        res = await project.getAllTodoLists_service.getAllTodoLists(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/users/login", response_model=project.loginUser_service.UserLoginResponse
)
async def api_post_loginUser(
    username: str, password: str
) -> project.loginUser_service.UserLoginResponse | Response:
    """
    Authenticates a user by checking provided credentials (username and password). Upon successful authentication, it generates a token using the TokenModule and returns the token to the user.
    """
    try:
        res = project.loginUser_service.loginUser(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/audit/logs/user/{user_id}",
    response_model=project.get_logs_by_user_service.GetUserAuditLogsResponse,
)
async def api_get_get_logs_by_user(
    user_id: int,
) -> project.get_logs_by_user_service.GetUserAuditLogsResponse | Response:
    """
    Fetches all audit logs for a specific user by their user ID. The response is an array of log objects related to the actions performed by the specified user. This helps in monitoring user-specific activities.
    """
    try:
        res = await project.get_logs_by_user_service.get_logs_by_user(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/tasks/{taskId}", response_model=project.deleteTask_service.DeleteTaskResponseModel
)
async def api_delete_deleteTask(
    taskId: int,
) -> project.deleteTask_service.DeleteTaskResponseModel | Response:
    """
    This endpoint handles the deletion of a specific task in a TODO list. The user must provide the task ID as a URL parameter. Upon successful deletion, a confirmation message is returned. This action verifies the task’s existence within the user's TODO list and logs the deletion event using AuditLogModule.
    """
    try:
        res = await project.deleteTask_service.deleteTask(taskId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/todolists", response_model=project.createTodoList_service.CreateTodoListResponse
)
async def api_post_createTodoList(
    title: str, description: Optional[str], userId: int
) -> project.createTodoList_service.CreateTodoListResponse | Response:
    """
    Creates a new TODO list for the user. The request should contain the title of the TODO list and, optionally, a description. The response will return the created TODO list with its unique identifier.
    """
    try:
        res = await project.createTodoList_service.createTodoList(
            title, description, userId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/todolists/{id}",
    response_model=project.deleteTodoList_service.DeleteTodoListResponse,
)
async def api_delete_deleteTodoList(
    id: int,
) -> project.deleteTodoList_service.DeleteTodoListResponse | Response:
    """
    Deletes a specific TODO list by its unique identifier. The response will confirm the deletion. Note: This will also trigger interactions with the TaskModule to delete all associated tasks and with AuditLogModule to log the deletion action.
    """
    try:
        res = await project.deleteTodoList_service.deleteTodoList(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/audit/logs", response_model=project.create_log_service.AuditLogResponse)
async def api_post_create_log(
    user_id: int, action: str, todo_list_id: Optional[int], task_id: Optional[int]
) -> project.create_log_service.AuditLogResponse | Response:
    """
    Creates a new audit log entry. This endpoint is used internally by the TodoListModule and TaskModule to log changes. It expects a JSON payload containing details such as user ID, action performed, and associated TODO list or task ID. The response is the created log object.
    """
    try:
        res = await project.create_log_service.create_log(
            user_id, action, todo_list_id, task_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/token", response_model=project.generate_token_service.TokenResponseModel
)
async def api_post_generate_token(
    username: str, password: str
) -> project.generate_token_service.TokenResponseModel | Response:
    """
    Generates a new JWT token for authenticated users. It accepts a username and password, verifies these credentials using the UserManagementModule, and returns a JWT token if the credentials are valid. The token contains user information and expiration details.
    """
    try:
        res = await project.generate_token_service.generate_token(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/tasks/{taskId}", response_model=project.getTaskById_service.GetTaskResponseModel
)
async def api_get_getTaskById(
    taskId: int,
) -> project.getTaskById_service.GetTaskResponseModel | Response:
    """
    This endpoint retrieves the details of a specific task using its ID. Users need to provide the task ID as a URL parameter. The response will include task details such as title, description, status, and due date. It helps users to view individual task details.
    """
    try:
        res = await project.getTaskById_service.getTaskById(taskId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/tasks", response_model=project.getTasks_service.GetTasksResponse)
async def api_get_getTasks(
    todo_list_id: int,
) -> project.getTasks_service.GetTasksResponse | Response:
    """
    This endpoint fetches all tasks associated with a specific TODO list. Users need to provide the TODO list ID. The response will include a list of all tasks with their details (e.g., task ID, title, description, status, due date). This is primarily used to display tasks belonging to a TODO list, leveraging interaction with the TodoListModule.
    """
    try:
        res = await project.getTasks_service.getTasks(todo_list_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/todolists/{id}", response_model=project.getTodoList_service.GetTodoListResponse
)
async def api_get_getTodoList(
    id: int,
) -> project.getTodoList_service.GetTodoListResponse | Response:
    """
    Fetches a specific TODO list by its unique identifier. The response will include all the details of the TODO list such as title, description, creation date, and associated tasks.
    """
    try:
        res = await project.getTodoList_service.getTodoList(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/users/profile",
    response_model=project.getUserProfile_service.UserProfileResponse,
)
async def api_get_getUserProfile(
    Authorization: str,
) -> project.getUserProfile_service.UserProfileResponse | Response:
    """
    Retrieves the profile details of the authenticated user. This includes personal information like username, email, and other profile-related data. Requires a valid token.
    """
    try:
        res = await project.getUserProfile_service.getUserProfile(Authorization)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/users/profile",
    response_model=project.updateUserProfile_service.UpdateUserProfileResponse,
)
async def api_put_updateUserProfile(
    email: Optional[str], password: Optional[str], role: Optional[str]
) -> project.updateUserProfile_service.UpdateUserProfileResponse | Response:
    """
    Updates the profile information of the authenticated user. It accepts data fields that need updating and returns the updated profile details. Requires a valid token.
    """
    try:
        res = await project.updateUserProfile_service.updateUserProfile(
            email, password, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/audit/logs/{log_id}",
    response_model=project.get_log_by_id_service.AuditLogResponse,
)
async def api_get_get_log_by_id(
    log_id: int,
) -> project.get_log_by_id_service.AuditLogResponse | Response:
    """
    Fetches a specific audit log by its ID. The expected response is a log object, providing details such as timestamp, user ID, action performed, and associated TODO list or task ID. This allows an admin to review specific changes.
    """
    try:
        res = await project.get_log_by_id_service.get_log_by_id(log_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/audit/logs/{log_id}",
    response_model=project.delete_log_service.DeleteAuditLogResponse,
)
async def api_delete_delete_log(
    log_id: int,
) -> project.delete_log_service.DeleteAuditLogResponse | Response:
    """
    Deletes an audit log entry by its ID. This action is typically reserved for maintenance purposes. The expected response is a confirmation message with the status of the deletion.
    """
    try:
        res = await project.delete_log_service.delete_log(log_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/todolists/{id}",
    response_model=project.updateTodoList_service.TodoListOutputObject,
)
async def api_put_updateTodoList(
    id: int, title: str, description: Optional[str]
) -> project.updateTodoList_service.TodoListOutputObject | Response:
    """
    Updates the details of an existing TODO list identified by its unique identifier. The request should provide the updated title and description. The response will return the updated TODO list.
    """
    try:
        res = await project.updateTodoList_service.updateTodoList(
            id, title, description
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/tasks/{taskId}", response_model=project.updateTask_service.UpdateTaskResponse
)
async def api_put_updateTask(
    taskId: int,
    title: Optional[str],
    dueDate: Optional[datetime],
    priority: Optional[int],
    notes: Optional[str],
    completed: Optional[bool],
) -> project.updateTask_service.UpdateTaskResponse | Response:
    """
    This endpoint allows users to update the details of an existing task. Users must provide the task ID as a URL parameter and the updated task details in the request body. On successful update, a confirmation message along with the updated task details is returned. This route ensures the task belongs to the user's TODO list before updating and logs the operation via AuditLogModule.
    """
    try:
        res = await project.updateTask_service.updateTask(
            taskId, title, dueDate, priority, notes, completed
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
