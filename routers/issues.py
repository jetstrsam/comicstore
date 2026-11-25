from fastapi import APIRouter, HTTPException, status
from requests import session
from sqlmodel import select
from db import SessionDep
from models import Issue, IssueCreate, IssueUpdate

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/", response_model=Issue, status_code=status.HTTP_201_CREATED)
def create_issue(issue: IssueCreate, session: SessionDep):
    new_issue = Issue.model_validate(issue)
    session.add(new_issue)
    session.commit()
    session.refresh(new_issue)
    return new_issue

@router.get("/", response_model=list[Issue])
def get_all_issues(include_inactive: bool = False):
    statement = select(Issue)
    if not include_inactive:
        statement = statement.where(Issue.esta_activo == True)
    return session.exec(statement).all()

@router.get("/{issue_id}", response_model=Issue)
def get_one_issue(issue_id: int, session: SessionDep):
    statement = select(Issue).where(Issue.id == issue_id)
    issue = session.exec(statement).first()
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    return issue
 
@router.patch("/{issue_id}", response_model=Issue)
def update_issue(issue_id: int, issue: IssueUpdate, session: SessionDep):
    statement = select(Issue).where(Issue.id == issue_id)
    db_issue = session.exec(statement).first()
    if not db_issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

    issue_data = issue.model_dump(exclude_unset=True)
    for key, value in issue_data.items():
        setattr(db_issue, key, value)

    session.add(db_issue)
    session.commit()
    session.refresh(db_issue)
    return db_issue

@router.delete("/{issue_id}")
def delete_issue(issue_id: int, session: SessionDep):
    statement = select(Issue).where(Issue.id == issue_id)
    db_issue = session.exec(statement).first()
    if not db_issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

    session.add(db_issue)
    session.commit()

    return {"detail": "Issue has been sent to heck... or not?"}
