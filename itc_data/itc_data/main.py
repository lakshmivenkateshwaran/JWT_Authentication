from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from database import SessionLocal, engine
from models import Base, User, Token
from schemas import UserCreate, TokenData
from dependencies import get_db, authenticate_user, create_access_token, oauth2_scheme

# Initialize the database
Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret and algorithm
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Token expiration
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.post("/create_user/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully", "user": db_user.username}


@app.post("/token/")
def login_for_access_token(user: UserCreate, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})
    db_token = Token(token=access_token, user_id=db_user.id)
    db.add(db_token)
    db.commit()
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/scrape/")
def scrape(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Call Scrapy spider
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl('quarterly_results')
    process.start()
    return {"message": "Scraping started successfully"}
