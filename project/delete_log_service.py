import prisma
import prisma.models
from pydantic import BaseModel


class DeleteAuditLogResponse(BaseModel):
    """
    Response model providing the status of the audit log deletion operation.
    """

    status: str


async def delete_log(log_id: int) -> DeleteAuditLogResponse:
    """
    Deletes an audit log entry by its ID. This action is typically reserved for maintenance purposes.
    The expected response is a confirmation message with the status of the deletion.

    Args:
        log_id (int): The unique identifier of the audit log entry to be deleted.

    Returns:
        DeleteAuditLogResponse: A response model providing the status of the audit log deletion operation.

    Example:
        log_id = 123
        response = await delete_log(log_id)
        > DeleteAuditLogResponse(status='Audit log entry successfully deleted.')
    """
    audit_log = await prisma.models.AuditLog.prisma().find_unique(where={"id": log_id})
    if audit_log is None:
        return DeleteAuditLogResponse(status="Audit log entry not found.")
    await prisma.models.AuditLog.prisma().delete(where={"id": log_id})
    return DeleteAuditLogResponse(status="Audit log entry successfully deleted.")
