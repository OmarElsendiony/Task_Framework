from .add_incident_comment import AddIncidentComment
from .create_incident import CreateIncident
from .create_incident_task import CreateIncidentTask
from .create_user import CreateUser
from .get_category_by_name import GetCategoryByName
from .get_company_by_name import GetCompanyByName
from .get_incident import GetIncident
from .get_incident_comments import GetIncidentComments
from .get_incident_tasks import GetIncidentTasks
from .link_incident_to_kb import LinkIncidentToKB
from .log_incident_change import LogIncidentChange
from .register_change_request import RegisterChangeRequest
from .search_change_requests import SearchChangeRequests
from .search_departments import SearchDepartments
from .search_incidents import SearchIncidents
from .search_kb_articles import SearchKBArticles
from .search_subcategories import SearchSubcategories
from .search_surveys import SearchSurveys
from .search_users import SearchUsers
from .update_change_request import UpdateChangeRequest
from .update_incident import UpdateIncident
from .update_kb_articles import UpdateKBArticles
from .update_task import UpdateTask
from .update_user_profile import UpdateUserProfile


ALL_TOOLS_INTERFACE_1 = [
    AddIncidentComment,
    CreateIncident,
    CreateIncidentTask,
    CreateUser,
    GetCategoryByName,
    GetCompanyByName,
    GetIncident,
    GetIncidentComments,
    GetIncidentTasks,
    LinkIncidentToKB,
    LogIncidentChange,
    RegisterChangeRequest,
    SearchChangeRequests,
    SearchDepartments,
    SearchIncidents,
    SearchKBArticles,
    SearchSubcategories,
    SearchSurveys,
    SearchUsers,
    UpdateChangeRequest,
    UpdateIncident,
    UpdateKBArticles,
    UpdateTask,
    UpdateUserProfile
]
