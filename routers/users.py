from fastapi import APIRouter, HTTPException, status
from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDep 
from sqlmodel import select


router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, session: SessionDep):
    new_customer = Customer.model_validate(customer)
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer

@router.get("/", response_model=list[Customer])
def get_all_customers(session: SessionDep):
    statement = select(Customer)
    return session.exec(statement).all()

@router.get("/{customer_id}", response_model=Customer)
def get_one_customer(customer_id: int, session: SessionDep):
    statement = select(Customer).where(Customer.id == customer_id)
    customer = session.exec(statement).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer
        
@router.patch("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerUpdate, session: SessionDep):
    statement = select(Customer).where(Customer.id == customer_id)
    db_customer = session.exec(statement).first()
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    customer_data = customer.model_dump(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(db_customer, key, value)

    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, session: SessionDep):
    statement = select(Customer).where(Customer.id == customer_id)
    db_customer = session.exec(statement).first()
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    session.delete(db_customer)
    session.commit()

    return {"detail": "Customer has been sent to heck"}