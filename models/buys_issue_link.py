from sqlmodel import Field, SQLModel

class BuysIssueLink(SQLModel, table=True):
    buys_id: int | None=Field(default=None, foreign_key="buys.id", primary_key=True)
    issue_id:int | None=Field(default=None, foreign_key="issue.id", primary_key=True)
    quantity: int | Field(default = 1, gt=0)
 