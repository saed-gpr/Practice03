from fastapi import FastAPI, Query, HTTPException, status, Path, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from core.schema import CostCreateSchema, CostUpdateSchema
from core.models import get_db, Expense
from core.database import engine
from sqlalchemy.orm import Session


app = FastAPI()



# Create
@app.post('/expenses')
def new_cost(payload: CostCreateSchema, db : Session = Depends(get_db)):
    new_expense = Expense(**payload.model_dump())

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    
    return JSONResponse(
        content={
            'id' : new_expense.id,
            'description' : new_expense.description,
            'amount' : new_expense.amount
        },
        status_code=status.HTTP_200_OK
    )

# Read
@app.get('/expenses')
def get_expenses(description: Optional[str] = None, db : Session = Depends(get_db)):
    if description:
        result = db.query(Expense).filter(Expense.description.ilike(f'%{description}%')).all()

    else :
        result = db.query(Expense).all()

    return JSONResponse(
        content=[
            {
                'id' : expense.id,
                'description' : expense.description,
                'amount' : expense.amount
            }

            for expense in result
        ],
        status_code=status.HTTP_200_OK
    )


# Read one expense
@app.get('/expenses/{expense_id}')
def get_expense(expense_id: int, db : Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).one_or_none()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Expense not found'
        )

    return JSONResponse(
        content={
            'id' : expense.id,
            'description' : expense.description,
            'amount' : expense.amount
        },
        status_code=status.HTTP_200_OK
    )

# Update
@app.put('/expenses/{expense_id}')
def update_expense(expense_id: int, payload : CostUpdateSchema, db : Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id==expense_id).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='there is no record like that'
        )
    
    expense.description = payload.description
    expense.amount = payload.amount
    
    db.commit()

    db.refresh(expense)
    return expense

# Delete
@app.delete('/expenses/{expense_id}')
def delete_expense(expense_id: int, db : Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id==expense_id).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='there is no record like that'
        )

    db.delete(expense)
    db.commit()

    return JSONResponse(
        content= {
            'message' : 'Expense deleted successfully'
        },
        status_code=status.HTTP_204_NO_CONTENT
    )