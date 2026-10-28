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