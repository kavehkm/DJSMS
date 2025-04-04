# dj
from django.db import models


class Message(models.Model):
    """Message"""

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    STATUSES = (
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
    )

    task_id = models.UUIDField(null=True)
    status = models.CharField(max_length=7, choices=STATUSES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"Message(id={self.id})"
