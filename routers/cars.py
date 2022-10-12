from datetime import datetime

from db import engine, get_session, Session
from sqlmodel import select

from routers.auth import get_current_user
from schemas import Car, Trip, TripInput, CarOutput, CarInput, User
from fastapi import APIRouter, HTTPException, Depends


router = APIRouter(prefix="/api/cars")


@router.get("/")
def get_cars(size: str|None = None, doors: int|None =None, session: Session = Depends(get_session)) -> list:
        query = select(Car)
        if size:
            query = query.where(Car.size == size)
        if doors:
            query = query.where(Car.doors == doors)

        return session.exec(query).all()


@router.post("/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, trip_input: TripInput, session: Session = Depends(get_session)) -> Trip:
    #matches = [car for car in db if car.id == id]
    car = session.get(Car, car_id)
    if car:
        if trip_input is not None:
            new_trip = Trip.from_orm(trip_input, update={'car_id': car_id})
            car.trips.append(new_trip)
            session.commit()
            session.refresh(new_trip)
            return new_trip
        else:
            raise HTTPException(status_code=400, detail="No trip information found")
    else:
        raise HTTPException(status_code=404, detail=f"No car with {id} found")


@router.get("/{id}", response_model=CarOutput)
def car_by_id(id: int, session: Session = Depends(get_session)) -> Car:
    #result = [car for car in db if car.id == id]
    car = session.get(Car, id)
    if car:
        return car
    raise HTTPException(status_code=404, detail=f"No car with {id} not found")


@router.post("/", response_model=Car)
def add_car(car_input: CarInput,
            session: Session = Depends(get_session),
            user: User =  Depends(get_current_user)) -> Car:

    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car

    #new_car = CarOutput( size=car.size, doors=car.doors, fuel=car.fuel, transmission=car.transmission, id=len(db)+1)
    #db.append(new_car)
    #save_db(db)
    #return new_car


@router.put("/{id}", response_model=Car)
def change_car(id: int, new_data: CarInput, session: Session = Depends(get_session)):
    car = session.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        session.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id} found")


@router.delete("/{id}", status_code=204)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    #matches= [car for car in db if car.id == id]
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id} found")


@router.get('/')
def welcome(name="Chakri"):
    """Return a friendly welcome message"""
    return {"message":f"Welcome {name} to car sharing service"}


@router.get('/date')
def date():
    return {"date":datetime.now()}
