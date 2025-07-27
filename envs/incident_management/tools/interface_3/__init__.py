from .query_change_requests import QueryChangeRequests
from .add_incident_attachment import AddIncidentAttachment
from .query_departments import QueryDepartments
from .add_incident_comment import AddIncidentComment
from .query_incident_slas import QueryIncidentSLAs
from .attach_incident_sla import AttachIncidentSLA
from .query_incidents import QueryIncidents
from .create_incident import CreateIncident
from .query_kb_articles import QueryKBArticles
from .create_incident_task import CreateIncidentTask
from .query_sla_policies import QuerySLAPolicies
from .get_category_by_name import GetCategoryByName
from .query_subcategories import QuerySubcategories
from .get_company_by_name import GetCompanyByName
from .query_users import QueryUsers
from .get_incident_attachments import GetIncidentAttachments
from .register_change_request import RegisterChangeRequest
from .get_incident_comments import GetIncidentComments
from .unlink_incident_from_kb import UnlinkIncidentFromKB
from .get_incident_history import GetIncidentHistory
from .update_incident import UpdateIncident
from .get_incident_tasks import GetIncidentTasks
from .update_incident_comment import UpdateIncidentComment
from .link_incident_to_kb import LinkIncidentToKB
from .update_task import UpdateTask
from .log_incident_change import LogIncidentChange


ALL_TOOLS_INTERFACE_3 = [
    QueryChangeRequests,
    AddIncidentAttachment,
    QueryDepartments,
    AddIncidentComment,
    QueryIncidentSLAs,
    AttachIncidentSLA,
    QueryIncidents,
    CreateIncident,
    QueryKBArticles,
    CreateIncidentTask,
    QuerySLAPolicies,
    GetCategoryByName,
    QuerySubcategories,
    GetCompanyByName,
    QueryUsers,
    GetIncidentAttachments,
    RegisterChangeRequest,
    GetIncidentComments,
    UnlinkIncidentFromKB,
    GetIncidentHistory,
    UpdateIncident,
    GetIncidentTasks,
    UpdateIncidentComment,
    LinkIncidentToKB,
    UpdateTask,
    LogIncidentChange
]
