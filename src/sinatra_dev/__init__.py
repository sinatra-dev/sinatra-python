"""A Python client for the Sinatra API.

    from sinatra_dev import Sinatra

    with Sinatra() as sinatra:  # reads SINATRA_TOKEN
        me = sinatra.me.get()

Reference: https://docs.sinatra.dev/docs/api-reference
"""

from ._client import (
    DEFAULT,
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    MeApi,
    MessagesApi,
    Sinatra,
    TasksApi,
    TicketsApi,
    Timeout,
)
from ._errors import SinatraError
from ._generated.models import (
    CreateMessageResponse,
    CreateTaskResponse,
    DelegateTicketResponse,
    Me,
    Message,
    MessageList,
    MeUser,
    PullRequest,
    StopTaskResponse,
    Task,
    TaskList,
    Ticket,
    TicketSearchResult,
    TicketSearchResultGithub,
    TicketSearchResultLinear,
    Workspace,
)
from ._generated.models import Error as ErrorBody

__all__ = [
    "DEFAULT",
    "DEFAULT_BASE_URL",
    "DEFAULT_TIMEOUT",
    "CreateMessageResponse",
    "CreateTaskResponse",
    "DelegateTicketResponse",
    "ErrorBody",
    "Me",
    "MeApi",
    "MeUser",
    "Message",
    "MessageList",
    "MessagesApi",
    "PullRequest",
    "Sinatra",
    "SinatraError",
    "StopTaskResponse",
    "Task",
    "TaskList",
    "TasksApi",
    "Ticket",
    "TicketSearchResult",
    "TicketSearchResultGithub",
    "TicketSearchResultLinear",
    "TicketsApi",
    "Timeout",
    "Workspace",
]
