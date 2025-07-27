from .list_kb_articles_by_filters import ListKBArticlesByFilters
from .add_incident_comment import AddIncidentComment
from .create_incident_task import CreateIncidentTask
from .create_kb_article import CreateKBArticle
from .create_survey import CreateSurvey
from .get_average_csat import GetAverageCSAT
from .get_incident_tasks import GetIncidentTasks
from .link_incident_to_kb import LinkIncidentToKB
from .list_categories_by_filters import ListCategoriesByFilters
from .list_companies_by_filters import ListCompaniesByFilters
from .list_departments_by_filters import ListDepartmentsByFilters
from .list_incident_comments import ListIncidentComments
from .list_incidents_by_filters import ListIncidentsByFilters
from .list_incidents_by_kb import ListIncidentsByKB
from .list_low_rated_incidents import ListLowRatedIncidents
from .list_subcategories_by_filters import ListSubcategoriesByFilters
from .list_surveys_by_filters import ListSurveysByFilters
from .list_users_by_filters import ListUsersByFilters
from .log_incident_change import LogIncidentChange
from .update_incident import UpdateIncident
from .update_kb_article import UpdateKBArticle
from .update_survey import UpdateSurvey
from .update_task import UpdateTask
from .update_user_profile import UpdateUserProfile


ALL_TOOLS_INTERFACE_5 = [
    ListKBArticlesByFilters,
    AddIncidentComment,
    CreateIncidentTask,
    CreateKBArticle,
    CreateSurvey,
    GetAverageCSAT,
    GetIncidentTasks,
    LinkIncidentToKB,
    ListCategoriesByFilters,
    ListCompaniesByFilters,
    ListDepartmentsByFilters,
    ListIncidentComments,
    ListIncidentsByFilters,
    ListIncidentsByKB,
    ListLowRatedIncidents,
    ListSubcategoriesByFilters,
    ListSurveysByFilters,
    ListUsersByFilters,
    LogIncidentChange,
    UpdateIncident,
    UpdateKBArticle,
    UpdateSurvey,
    UpdateTask,
    UpdateUserProfile
]
