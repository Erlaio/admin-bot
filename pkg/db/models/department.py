from pydantic import BaseModel


class Department(BaseModel):
    department_id: int = 0
    department: str = ''
    team_lead: str = ''


def new_department(department_id=0, department='', team_lead=''):
    res = Department()
    res.department_id = department_id
    res.department = department
    res.team_lead = team_lead
    return res
