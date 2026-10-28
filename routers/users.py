from fastapi import APIRouter, HTTPException, status
from models.user import Customer, CustomerCreate, CustomerUpdate
from localdata.csv import read_csv, write_csv, get_next_id

router = APIRouter(prefix="/customers", tags=["customers"])
FILENAME = "customers.csv"
FIELDNAMES = ["id", "nombres", "apellidos", "cc", "telefono", "email", "direccion", "membresia"]

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate):
    rows = read_csv(FILENAME)
    new_id = get_next_id(FILENAME)

    new_customer = {
        "id": new_id,
        "nombres": customer.nombres,
        "apellidos": customer.apellidos,
        "cc": customer.cc,
        "telefono": customer.telefono,
        "email": customer.email,
        "direccion": customer.direccion,
        "membresia": customer.membresia
    }
    rows.append(new_customer)
    write_csv(FILENAME, rows, FIELDNAMES)
    return new_customer

router.get("/", response_model=list[Customer])
def get_all_customers():
    return read_csv(FILENAME)

@router.get("/{customer_id}", response_model=Customer)
def get_one_customer(customer_id: int):
    rows = read_csv(FILENAME)
    for row in rows:
        if int(row["id"]) == customer_id:
            return {
                "id": int(row["id"]),
                "nombres": row["nombres"],
                "apellidos": row["apellidos"],
                "cc": row["cc"],
                "telefono": row["telefono"],
                "email": row["email"],
                "direccion": row["direccion"],
                "membresia": row["membresia"]
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

@router.patch("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerUpdate):
    rows = read_csv(FILENAME)
    found = False
    updated_customer = None

    for row in rows:
        if int(row["id"]) == customer_id:
            found = True
            update_localdata = customer.model_dump(exclude_unset=True)
            for key, value in update_localdata.items():
                row[key] = value
            updated_customer = {
                "id": int(row["id"]),
                "nombres": row["nombres"],
                "apellidos": row["apellidos"],
                "cc": row["cc"],
                "telefono": row["telefono"],
                "email": row["email"],
                "direccion": row["direccion"],
                "membresia": row["membresia"]
            }
            break

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    write_csv(FILENAME, rows, FIELDNAMES)
    return updated_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int):
    rows = read_csv(FILENAME)
    new_rows = [row for row in rows if int(row["id"]) != customer_id]

    if len(rows) == len(new_rows):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    write_csv(FILENAME, new_rows, FIELDNAMES)
    return {"detail": "Customer has been send to heck"}