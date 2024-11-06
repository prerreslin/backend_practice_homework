from main import app
from schemas import EventModel,UserModel,DateModel
from fastapi import HTTPException
from db import Event,Session,User
from sqlalchemy import select
from datetime import date

@app.post("/add_event", response_model=EventModel, status_code=201)
async def create_event(event: EventModel,user_id : int):
    with Session() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.has_permission:
            raise HTTPException(status_code=403, detail="Forbidden")

        curr_event = session.scalar(select(Event).where(Event.title == event.title))
        if curr_event:
            raise HTTPException(status_code=400, detail="Bad Request: Event already exists")

        new_event = Event(
            title=event.title,
            description=event.description,
            date=event.date,
            is_public=event.is_public,
            owner_id=user_id
        )
        session.add(new_event)
        session.commit()
        session.refresh(new_event)
        return new_event


@app.get("/get_events")
async def get_all_events():
    with Session() as session:
        events = session.query(Event).all()
        if events == []:
            raise HTTPException(status_code=204,detail="No Content")
        return events
    
@app.get("/get_event/{event_id}")
async def get_event(event_id:int):
    with Session() as session:
        event = session.scalar(select(Event).where(Event.id == event_id))
        if not event:
            raise HTTPException(status_code=404,detail="Not found")
        return event
    
@app.put("/edit_event/{event_id}")
async def edit_event(event_id:int,data:EventModel,user_id:int):
    with Session() as session:
        event = session.scalar(select(Event).where(Event.id == event_id))
        user = session.scalar(select(User).where(User.id == user_id))
        if not event:
            raise HTTPException(status_code=404,detail="Event not found")
        if not user:
            raise HTTPException(status_code=404,detail="User not found")
        if event.date < data.date:
            raise HTTPException(status_code=422,detail="Unprocessable Entity")
        if event.owner_id != user_id:
            raise HTTPException(status_code=403,detail="Forbidden")
        
        event = Event(
            title=data.title,
            description=data.description,
            date=event.date,
            is_public=data.is_public,
            owner_id=event.owner_id,
            executors=event.executors
        )
        session.commit()
        return event

@app.delete("/delete_event/{event_id}")
def delete_event(event_id:int,user_id:int):
    with Session() as session:
        event = session.scalar(select(Event).where(Event.id == event_id))
        user = session.scalar(select(User).where(User.id == user_id))
        if not event:
            raise HTTPException(status_code=404,detail="Event not found")
        if not user:
            raise HTTPException(status_code=404,detail="User not found")
        if event.owner_id != user.id or not user.has_permission:
            raise HTTPException(status_code=403,detail="Forbidden")
        
        session.delete(event)
        session.commit()
        return {"Event":"Deleted"}
    
@app.patch("/events/{event_id}/reschedule")
def reschedule_event(event_id: int, data: DateModel, user_id: int):
    with Session() as session:
        event = session.scalar(select(Event).where(Event.id == event_id))
        user = session.scalar(select(User).where(User.id == user_id))
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if data.data is None:
            raise HTTPException(status_code=400, detail="Bad Request")
        if event.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        event.date = data.data
        session.commit()
        return {"Message":"Changed"}

@app.post("/events/{id}/rsvp")
def event_registration(event_id:int,user_id:int):
    with Session() as session:
        event = session.scalar(select(Event).where(Event.id == event_id))
        user = session.scalar(select(User).where(User.id == user_id))
        if not event:
            raise HTTPException(status_code=404,detail="Event not found")
        if not user:
            raise HTTPException(status_code=404,detail="User not found")
        if event.owner_id == user_id or user_id in event.get_executor_ids():
            raise HTTPException(status_code=409,detail="Conflict")
        event.add_executor(user)
        session.commit()
        return {"Message":"User added to executors"}
        

        
        
        