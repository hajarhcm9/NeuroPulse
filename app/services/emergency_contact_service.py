"""Smart Guardian - Emergency Contact Service"""

import logging
from typing import List
from fastapi import HTTPException, status
from app.models.emergency_contact import EmergencyContact
from app.repositories.emergency_contact_repository import EmergencyContactRepository
from app.schemas.emergency_contact import EmergencyContactCreate, EmergencyContactUpdate, EmergencyContactResponse

logger = logging.getLogger("smart-guardian")


class EmergencyContactService:
    """Business logic for emergency contacts"""

    def __init__(self, db):
        self.contact_repo = EmergencyContactRepository(db)

    def create_contact(self, user_id: int, data: EmergencyContactCreate) -> EmergencyContactResponse:
        if data.is_primary:
            existing_primary = self.contact_repo.get_primary(user_id)
            if existing_primary:
                existing_primary.is_primary = False
                self.contact_repo.update(existing_primary)

        contact = EmergencyContact(
            user_id=user_id,
            full_name=data.full_name,
            phone=data.phone,
            email=data.email,
            relationship=data.relationship,
            is_primary=data.is_primary,
            notify_on_alert=data.notify_on_alert,
        )
        contact = self.contact_repo.create(contact)
        logger.info("Emergency contact created: user=%d contact=%s", user_id, data.full_name)
        return EmergencyContactResponse.model_validate(contact)

    def get_user_contacts(self, user_id: int) -> List[EmergencyContactResponse]:
        contacts = self.contact_repo.get_by_user(user_id)
        return [EmergencyContactResponse.model_validate(c) for c in contacts]

    def update_contact(self, contact_id: int, user_id: int, data: EmergencyContactUpdate) -> EmergencyContactResponse:
        contact = self.contact_repo.get_by_id(contact_id)
        if not contact or contact.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emergency contact not found")

        if data.is_primary and not contact.is_primary:
            existing_primary = self.contact_repo.get_primary(user_id)
            if existing_primary:
                existing_primary.is_primary = False
                self.contact_repo.update(existing_primary)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(contact, field, value)

        contact = self.contact_repo.update(contact)
        return EmergencyContactResponse.model_validate(contact)

    def delete_contact(self, contact_id: int, user_id: int) -> dict:
        contact = self.contact_repo.get_by_id(contact_id)
        if not contact or contact.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emergency contact not found")
        self.contact_repo.delete(contact)
        return {"message": "Emergency contact deleted"}

    def get_notifiable_contacts(self, user_id: int) -> List[EmergencyContactResponse]:
        contacts = self.contact_repo.get_notifiable(user_id)
        return [EmergencyContactResponse.model_validate(c) for c in contacts]
