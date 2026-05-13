"""Smart Guardian - Emergency Contact repository"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.emergency_contact import EmergencyContact


class EmergencyContactRepository:
    """Data access layer for EmergencyContact model"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, contact: EmergencyContact) -> EmergencyContact:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def get_by_id(self, contact_id: int) -> Optional[EmergencyContact]:
        return self.db.query(EmergencyContact).filter(EmergencyContact.id == contact_id).first()

    def get_by_user(self, user_id: int) -> List[EmergencyContact]:
        return self.db.query(EmergencyContact).filter(EmergencyContact.user_id == user_id).order_by(EmergencyContact.is_primary.desc(), EmergencyContact.created_at.asc()).all()

    def get_primary(self, user_id: int) -> Optional[EmergencyContact]:
        return self.db.query(EmergencyContact).filter(EmergencyContact.user_id == user_id, EmergencyContact.is_primary == True).first()

    def get_notifiable(self, user_id: int) -> List[EmergencyContact]:
        return self.db.query(EmergencyContact).filter(EmergencyContact.user_id == user_id, EmergencyContact.notify_on_alert == True).all()

    def update(self, contact: EmergencyContact) -> EmergencyContact:
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def delete(self, contact: EmergencyContact) -> None:
        self.db.delete(contact)
        self.db.commit()
