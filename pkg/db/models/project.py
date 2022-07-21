from pydantic import BaseModel


class Project(BaseModel):
    project_id: int = 0
    project_name: str = ''
    team_lead: str = ''


def new_project(project_id=0, project_name='', team_lead=''):
    res = Project()
    res.project_id = project_id
    res.project_name = project_name
    res.team_lead = team_lead
    return res
