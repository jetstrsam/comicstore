from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Buy, BuyCreate, BuyItem, Buys, BuysIssueLink, Customer, Issue


router = APIRouter(prefix="/buys", tags=["Buys"])

@router.post("/", response_model=Buy, status_code=status.HTTP_201_CREATED)
def create_buy(tx_data: BuyCreate, session: SessionDep):
    customer = session.get(Customer, tx_data.customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    if not tx_data.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The buy must contain at least one iten you bonehead.")

    new_buy = Buys(customer_id=tx_data.customer_id, total=0.0)
    session.add(new_buy)
    session.flush()

    calculated_total = 0.0

    for item in tx_data.items:
        issue = session.get(Issue, item.issue_id)
        if not issue or not issue.esta_activo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Issue with ID {item.issue_id} not found",
            )

        if issue.stock < item.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for issue ID {item.issue_id}. Available: {issue.stock}",
            )

        issue.stock -= item.cantidad
        calculated_total += issue.precio * item.cantidad
        session.add(issue)

        existing_link = session.get(BuysIssueLink, (new_buy.id, issue.id))
        if existing_link:
            existing_link.cantidad += item.cantidad
            session.add(existing_link)
        else:
            link = BuysIssueLink(
                buys_id=new_buy.id,
                issue_id=issue.id,
                cantidad=item.cantidad,
            )
            session.add(link)

    new_buy.total = calculated_total
    session.add(new_buy)
    session.commit()
    session.refresh(new_buy)

    links = session.exec(
        select(BuysIssueLink).where(BuysIssueLink.buys_id == new_buy.id)
    ).all()

    processed_items = [
        BuyItem(issue_id=link.issue_id, cantidad=link.cantidad) for link in links
    ]

    return Buy(
        id=new_buy.id,
        customer_id=new_buy.customer_id,
        fecha=new_buy.fecha,
        total=new_buy.total,
        items=processed_items,
    )

    
@router.get("/", response_model=list[Buy])
def get_all_buys(session: SessionDep):
    buys_list = session.exec(select(Buys)).all()
    result: list[Buy] = []

    for buy in buys_list:
        links = session.exec(
            select(BuysIssueLink).where(BuysIssueLink.buys_id == buy.id)
        ).all()

        items = [
            BuyItem(issue_id=link.issue_id, cantidad=link.cantidad) for link in links
        ]

        result.append(
            Buy(
                id=buy.id,
                customer_id=buy.customer_id,
                fecha=buy.fecha,
                total=buy.total,
                items=items,
            )
        )

    return result

@router.get("/{buy_id}", response_model=Buy)
def get_one_buy(buy_id: int, session: SessionDep):
    buy = session.get(Buys, buy_id)
    if not buy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buy not found")

    links = session.exec(
        select(BuysIssueLink).where(BuysIssueLink.buys_id == buy.id)
    ).all()

    items = [
        BuyItem(issue_id=link.issue_id, cantidad=link.cantidad) for link in links
    ]

    return Buy(
        id=buy.id,
        customer_id=buy.customer_id,
        fecha=buy.fecha,
        total=buy.total,
        items=items,
    )

@router.delete("/{buy_id}")
def delete_buy(buy_id: int, session: SessionDep):
    statement = select(Buys).where(Buys.id == buy_id)
    buy = session.exec(statement).first()
    if not buy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buy not found")

    links = session.exec(
        select(BuysIssueLink).where(BuysIssueLink.buys_id == buy.id)
    ).all()

    for link in links:
        issue = session.get(Issue, link.issue_id)
        if issue:
            issue.stock += link.cantidad
            session.add(issue)
        session.delete(link)

        session.delete(buy)
        session.commit()
        return {"detail": "Buy has been deleted and stock restored. now everything is back to normal."}