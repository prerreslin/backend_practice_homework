from main import app
from schemas import UserModel
from db import Session,User

@app.post("/register")
async def register_user(data: UserModel):
    with Session() as session:
        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=data.password,
            phone_number=data.phone_number,
            has_permission=data.has_permission
        )
        session.add(user)
        session.commit()
        return {"message": "User registered successfully"}