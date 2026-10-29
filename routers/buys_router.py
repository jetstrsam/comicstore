
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import json
from models.buys import Buy, BuyCreate, BuyItem
from localdata.csv import read_csv, write_csv, get_next_id

router = APIRouter(prefix="/buys", tags=["Buys"])
FILENAME = "buys.csv"
FIELDNAMES = ["id", "customer_id", "fecha", "total", "items"]

ISSUES_FILENAME = "issues.csv"
CUSTOMERS_FILENAME = "customers.csv"  #

@router.post("/", response_model=Buy, status_code=status.HTTP_201_CREATED)
def create_buy(tx_data: BuyCreate):
    buys = read_csv(FILENAME)
    issues = read_csv(ISSUES_FILENAME)
    
    new_id = get_next_id(FILENAME)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    calculated_total = 0.0
    processed_items = []
    
    issues_dict = {int(i["id"]): i for i in issues}
    
    for item in tx_data.items:
        if item.issue_id not in issues_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Issue with ID {item.issue_id} not found"
            )
            
        issue_row = issues_dict[item.issue_id]
        stock_actual = int(issue_row["stock"])
        
        if stock_actual < item.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Not enough stock for issue ID {item.issue_id}. Available: {stock_actual}"
            )
            
        precio = float(issue_row["precio"])
        calculated_total += precio * item.cantidad
        
        issue_row["stock"] = str(stock_actual - item.cantidad)
        
        processed_items.append({
            "issue_id": item.issue_id,
            "cantidad": item.cantidad,
            "precio_unitario": precio
        })
    issues_fieldnames = ["id", "titulo", "editorial", "precio", "stock", "esta_activo"]
    write_csv(ISSUES_FILENAME, list(issues_dict.values()), issues_fieldnames)

    new_transaction = {
        "id": new_id,
        "customer_id": tx_data.customer_id,
        "fecha": current_date,
        "total": calculated_total,
        "items": json.dumps(processed_items)  
    }
    
    buys.append(new_transaction)
    write_csv(FILENAME, buys, FIELDNAMES)

    return {
        "id": new_id,
        "customer_id": tx_data.customer_id,
        "fecha": current_date,
        "total": calculated_total,
        "items": processed_items
    }

@router.get("/", response_model=list[Buy])
def get_all_buys():
    rows = read_csv(FILENAME)
    if not rows:
        return []
        
    result = []
    for row in rows:
        result.append({
            "id": int(row["id"]),
            "customer_id": int(row["customer_id"]),
            "fecha": row["fecha"],
            "total": float(row["total"]),
            "items": json.loads(row["items"]) if isinstance(row["items"], str) else row["items"]
        })
    return result

@router.get("/{buy_id}", response_model=Buy)
def get_one_buy(buy_id: int):
    rows = read_csv(FILENAME)
    for row in rows:
        if int(row["id"]) == buy_id:
            return {
                "id": int(row["id"]),
                "customer_id": int(row["customer_id"]),
                "fecha": row["fecha"],
                "total": float(row["total"]),
                "items": json.loads(row["items"]) if isinstance(row["items"], str) else row["items"]
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buy not found")