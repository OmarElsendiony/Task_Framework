from .add_incident_attachment import AddIncidentAttachment
from .add_incident_comment import AddIncidentComment
from .create_incident_task import CreateIncidentTask
from .create_kb_article import CreateKBArticle
from .filter_change_requests import FilterChangeRequests
from .filter_departments import FilterDepartments
from .filter_kb_articles import FilterKBArticles
from .filter_overdue_tasks import FilterOverdueTasks
from .filter_subcategories import FilterSubcategories
from .filter_users import FilterUsers
from .get_category_by_name import GetCategoryByName
from .get_company_by_name import GetCompanyByName
from .get_incident_comments import GetIncidentComments
from .get_incident_tasks import GetIncidentTasks
from .get_overdue_change_requests import GetOverdueChangeRequests
from .link_incident_to_kb import LinkIncidentToKB
from .log_incident_change import LogIncidentChange
from .query_incidents import QueryIncidents
from .register_change_request import RegisterChangeRequest
from .update_change_request import UpdateChangeRequest
from .update_incident import UpdateIncident
from .update_task import UpdateTask


ALL_TOOLS_INTERFACE_4 = [
    AddIncidentAttachment,
    AddIncidentComment,
    CreateIncidentTask,
    CreateKBArticle,
    FilterChangeRequests,
    FilterDepartments,
    FilterKBArticles,
    FilterOverdueTasks,
    FilterSubcategories,
    FilterUsers,
    GetCategoryByName,
    GetCompanyByName,
    GetIncidentComments,
    GetIncidentTasks,
    GetOverdueChangeRequests,
    LinkIncidentToKB,
    LogIncidentChange,
    QueryIncidents,
    RegisterChangeRequest,
    UpdateChangeRequest,
    UpdateIncident,
    UpdateTask
]
