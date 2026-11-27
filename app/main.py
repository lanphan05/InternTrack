from datetime import date
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI(title="InternTrack")

Status = Literal["wishlist", "applied", "interview", "offer", "rejected"]


class ApplicationCreate(BaseModel):
    """The fields a client sends to create an application (everything except id)."""

    company: str
    role: str
    link: str | None = None
    status: Status = "wishlist"
    date_applied: date | None = None
    notes: str = ""

    @field_validator("company", "role")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must contain non-whitespace characters")
        return value


class Application(ApplicationCreate):
    """A saved application: the client's fields plus the server-assigned id."""

    id: int


# In-memory storage. Data is lost when the server restarts; SQLite replaces this later.
applications: dict[int, Application] = {}
next_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/applications", status_code=201, response_model=Application)
def create_application(payload: ApplicationCreate) -> Application:
    global next_id
    application = Application(id=next_id, **payload.model_dump())
    applications[application.id] = application
    next_id += 1
    return application


@app.get("/applications", response_model=list[Application])
def list_applications(status: Status | None = None) -> list[Application]:
    if status is None:
        return list(applications.values())
    return [
        application
        for application in applications.values()
        if application.status == status
    ]


@app.get("/applications/{application_id}", response_model=Application)
def get_application(application_id: int) -> Application:
    application = applications.get(application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application
