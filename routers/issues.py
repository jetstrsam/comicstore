from fastapi import APIRouter, HTTPException, status
from models.issue import Issue, IssueCreate, IssueUpdate
from localdata.csv import read_csv, write_csv, get_next_id

router = APIRouter(prefix="/issues", tags=["Issues"])
FILENAME = "issues.csv"
FIELDNAMES = ["id", "titulo", "editorial", "precio", "stock", "esta_activo"]

@router.post("/", response_model=Issue, status_code=status.HTTP_201_CREATED)
def create_issue(issue: IssueCreate):
    rows = read_csv(FILENAME)
    new_id = get_next_id(FILENAME)

    new_issue = {
        "id": new_id,
        "titulo": issue.titulo,
        "editorial": issue.editorial,
        "precio": issue.precio,
        "stock": issue.stock,
        "esta_activo": str(issue.esta_activo)
    }
    rows.append(new_issue)
    write_csv(FILENAME, rows, FIELDNAMES)

    response_issue = new_issue.copy()
    response_issue["esta_activo"] = issue.esta_activo

    return response_issue

@router.get("/", response_model=list[Issue])
def get_all_issues(include_inactive:bool = False):
    rows = read_csv(FILENAME)
    issues_list=[]

    for row in rows:
        is_active = row.get("esta_activo", "True") == "True"
        if not include_inactive and not is_active:
            continue

    issues_list.append({
        "id": int(row["id"]),
        "titulo": row["titulo"],
        "editorial": row["editorial"],
        "precio": float(row["precio"]),
        "stock": int(row["stock"]),
        "esta_activo": is_active
    })    

@router.get("/{issue_id}", response_model=Issue)
def get_one_issue(issue_id: int):
    rows = read_csv(FILENAME)
    for row in rows:
        if int(row["id"]) == issue_id:
            return {
                "id": int(row["id"]),
                "titulo": row["titulo"],
                "editorial": row["editorial"],
                "precio": float(row["precio"]),
                "stock": int(row["stock"])
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.patch("/{issue_id}", response_model=Issue)
def update_issue(issue_id: int, issue: IssueUpdate):
    rows = read_csv(FILENAME)
    found = False
    updated_issue = None

    for row in rows:
        if int(row["id"]) == issue_id:
            found = True
            update_localdata = issue.model_dump(exclude_unset=True)
            for key, value in update_localdata.items():
                row[key] = value
            updated_issue = {
                "id": issue_id,
                "titulo": row["titulo"],
                "editorial": row["editorial"],
                "precio": float(row["precio"]),
                "stock": int(row["stock"]),
                "esta_activo": row.get("esta_activo", "True") == "True"
            }
            break
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

    write_csv(FILENAME, rows, FIELDNAMES)
    return updated_issue

@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: int):
    rows = read_csv(FILENAME)
    found = False

    for row in rows:
        if int(row["id"]) == issue_id:
            row["esta_activo"] = "False"
            found = True
            break
    
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")



    write_csv(FILENAME, rows, FIELDNAMES)
    return {"message": "The Issue has gone to heck... or not?"}