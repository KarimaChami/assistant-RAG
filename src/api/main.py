# src/api/main.py
from fastapi import FastAPI, Depends, HTTPException
# from jose import JWTError, jwt
# from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.utils.auth import verify_password, create_access_token, hash_password, get_current_user
from src.utils.rag_service import ask_rag
from src.api.schemas import QuestionRequest
from src.api.db import  engine,get_db
from src.api.models import Base,User, Query
from src.api.schemas import UserCreate, Token
from datetime import timedelta
Base.metadata.create_all(bind=engine)
print("Tables crees")
app = FastAPI()




@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email,hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/login",response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401,detail="Incorrect email or password")

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/query")
async def query_rag(payload:QuestionRequest,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):

    # Appeler la fonction RAG
    answer, latency = ask_rag(payload.question)

    # Sauvegarder dans la DB
    q = Query(
        user_id=current_user.id,
        question=payload.question,
        answer=answer,
        latency_ms=latency
    )
    db.add(q)
    db.commit()
    db.refresh(q)

    return {
        "question": payload.question,
        "answer": answer,
        "latency_ms": latency
    }

@app.get("/history")
def get_history(db:Session = Depends(get_db),current_user: str =Depends(get_current_user)):
    queries = (
        db.query(Query)
        .filter(Query.user_id == current_user.id)
        .order_by(Query.created_at.desc())
        .all()
    )

    return [
        {
            "question": q.question,
            "answer": q.answer,
            "latency_ms": q.latency_ms,
            "cluster": q.cluster,
            "created_at": q.created_at
        }
        for q in queries
    ]
   
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "rag-it-assistant"
    }