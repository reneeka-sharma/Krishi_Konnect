#models.py
# it defines SQLite tables and fixed status value
from datetime import date, datetime
from enum import Enum  # used to create fixed choice
# column and data-type
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum as SqlEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
""" 
- mapped and mapped_column used to define the column of our database
- relationship tells how different tables are connected with each other 

"""
from .database import Base #from database.py

# 1. USER ROLE
class UserRole(str, Enum):
    FARMER = "FARMER"
    FAMILY_MEMBER = "FAMILY_MEMBER"
    CENTER_OPERATOR = "CENTER_OPERATOR"
    ADMIN = "ADMIN"

# 2. PROCUREMENT STATUS
class ProcurementStatus(str, Enum):
    REGISTERED = "REGISTERED"
    SLOT_ASSIGNED = "SLOT_ASSIGNED"
    ARRIVED = "ARRIVED"
    WAITING = "WAITING"
    VERIFICATION = "VERIFICATION"
    WEIGHING = "WEIGHING"
    PROCURED = "PROCURED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAYMENT_PROCESSING = "PAYMENT_PROCESSING"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"

# 3. PAYMENT STATUS
class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"

# 4. USER TABLE
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.FARMER)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    farmer_profile: Mapped["Farmer | None"] = relationship(back_populates="user", uselist=False)

# 5. FARMER TABLE
class Farmer(Base):
    __tablename__ = "farmers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    village: Mapped[str | None] = mapped_column(String(120), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    user: Mapped[User] = relationship(back_populates="farmer_profile")
    transactions: Mapped[list["ProcurementTransaction"]] = relationship(back_populates="farmer")

# 6. FAMILY TABLE
class Family(Base):
    __tablename__ = "families"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    primary_farmer_id: Mapped[int] = mapped_column(ForeignKey("farmers.id"))

# 7. FAMILY MEMBER TABLE
class FamilyMember(Base):
    __tablename__ = "family_members"
    id: Mapped[int] = mapped_column(primary_key=True)
    family_id: Mapped[int] = mapped_column(ForeignKey("families.id"))
    farmer_id: Mapped[int] = mapped_column(ForeignKey("farmers.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    relationship_name: Mapped[str] = mapped_column(String(50), default="Family member")

# 8. PROCUREMENT CENTER TABLE
class Center(Base):
    __tablename__ = "centers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    address: Mapped[str] = mapped_column(String(200))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    capacity: Mapped[int] = mapped_column(Integer)
    processing_rate: Mapped[int] = mapped_column(Integer, comment="Farmers processed per hour")
    active_counters: Mapped[int] = mapped_column(Integer, default=3)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

# 9. CROP TABLE
class Crop(Base):
    __tablename__ = "crops"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    support_price: Mapped[float] = mapped_column(Float)

# 10. PROCUREMENT TRANSACTION TABLE
class ProcurementTransaction(Base):
    __tablename__ = "procurement_transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    farmer_id: Mapped[int] = mapped_column(ForeignKey("farmers.id"))
    center_id: Mapped[int] = mapped_column(ForeignKey("centers.id"))
    crop_name: Mapped[str] = mapped_column(String(60))
    expected_quantity: Mapped[float] = mapped_column(Float)
    actual_quantity: Mapped[float | None] = mapped_column(Float, nullable=True)
    expected_price: Mapped[float] = mapped_column(Float)
    final_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    preferred_date: Mapped[date] = mapped_column(Date)
    slot_start: Mapped[str | None] = mapped_column(String(30), nullable=True)
    slot_end: Mapped[str | None] = mapped_column(String(30), nullable=True)
    status: Mapped[ProcurementStatus] = mapped_column(SqlEnum(ProcurementStatus), default=ProcurementStatus.REGISTERED)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    farmer: Mapped[Farmer] = relationship(back_populates="transactions")
    center: Mapped[Center] = relationship()
    payment: Mapped["Payment | None"] = relationship(back_populates="transaction", uselist=False)
    token: Mapped["Token | None"] = relationship(back_populates="transaction", uselist=False)

# 11. QUEUE RECORD TABLE
class QueueRecord(Base):
    __tablename__ = "queue_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    center_id: Mapped[int] = mapped_column(ForeignKey("centers.id"))
    queue_size: Mapped[int] = mapped_column(Integer)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# 12. PAYMENT TABLE
class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("procurement_transactions.id"), unique=True)
    estimated_amount: Mapped[float] = mapped_column(Float)
    final_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(SqlEnum(PaymentStatus), default=PaymentStatus.PENDING)
    expected_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    transaction: Mapped[ProcurementTransaction] = relationship(back_populates="payment")

# 13. NOTIFICATION TABLE
class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# 14. TOKEN / QUEUE TOKEN TABLE
class Token(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    token_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("procurement_transactions.id"), unique=True)
    center_id: Mapped[int] = mapped_column(ForeignKey("centers.id"))
    queue_position: Mapped[int] = mapped_column(Integer)
    counter_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_called: Mapped[bool] = mapped_column(Boolean, default=False)
    transaction: Mapped[ProcurementTransaction] = relationship(back_populates="token")


