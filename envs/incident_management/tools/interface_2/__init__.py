from .fetch_subcategories import FetchSubcategories
from .add_incident_comment import AddIncidentComment
from .fetch_users import FetchUsers
from .create_category import CreateCategory
from .get_category_by_name import GetCategoryByName
from .create_incident import CreateIncident
from .get_company_by_name import GetCompanyByName
from .create_incident_task import CreateIncidentTask
from .get_incident_comments import GetIncidentComments
from .create_sla_policy import CreateSLAPolicy
from .get_incident_tasks import GetIncidentTasks
from .create_subcategory import CreateSubcategory
from .log_incident_change import LogIncidentChange
from .fetch_breached_incident_sla import FetchBreachedIncidentSLA
from .update_attached_incident_sla import UpdateAttachedIncidentSLA
from .fetch_departments import FetchDepartments
from .update_category import UpdateCategory
from .fetch_incident_slas import FetchIncidentSLAs
from .update_sla_policy import UpdateSLAPolicy
from .fetch_incidents import FetchIncidents
from .update_subcategory import UpdateSubcategory


ALL_TOOLS_INTERFACE_2 = [
    FetchSubcategories,
    AddIncidentComment,
    FetchUsers,
    CreateCategory,
    GetCategoryByName,
    CreateIncident,
    GetCompanyByName,
    CreateIncidentTask,
    GetIncidentComments,
    CreateSLAPolicy,
    GetIncidentTasks,
    CreateSubcategory,
    LogIncidentChange,
    FetchBreachedIncidentSLA,
    UpdateAttachedIncidentSLA,
    FetchDepartments,
    UpdateCategory,
    FetchIncidentSLAs,
    UpdateSLAPolicy,
    FetchIncidents,
    UpdateSubcategory
]
