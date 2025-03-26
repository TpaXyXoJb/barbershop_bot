from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from bot.models.base import Base


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service = Column(String, nullable=False)
    master_id = Column(Integer, nullable=False)
    date_time = Column(DateTime, nullable=False)
    status = Column(String, default="active")  # active, canceled, completed
