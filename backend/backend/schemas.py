# schemas define the fromat of data that enters and leave API also validate data before backend process it 
from datetime import date, datetime
from typing import Optional # means the field can be provided or can be empty 
from pydantic import BaseModel, ConfigDict, Field # for creating and vaildating schemas
from .models import PaymentStatus, ProcurementStatus, UserRole # import fixed choices/enums from our database models

# 1. REGISTER REQUEST
class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=10, max_length=30)
    village: Optional[str] = None

# 2. LOGIN REQUEST
class LoginRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=10, max_length=30)

# 3. LOGIN RESPONSE
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    name: str

# 4. FARMER UPDATE
class FarmerUpdate(BaseModel):
    phone: Optional[str] = Field(default=None, max_length=30)
    village: Optional[str] = Field(default=None, max_length=120)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# 5. FARMER RESPONSE
class FarmerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    phone: Optional[str]
    village: Optional[str]
    role: UserRole

# 6. CENTER RESPONSE
class CenterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    capacity: int
    processing_rate: int
    active_counters: int
    is_active: bool

# 7. CREATE PROCUREMENT REQUEST
class ProcurementCreate(BaseModel):
    farmer_id: Optional[int] = None  # operators may create on behalf of a farmer
    center_id: int
    crop_name: str = Field(min_length=2, max_length=60)
    expected_quantity: float = Field(gt=0, le=10000)
    expected_price: float = Field(gt=0, le=100000)
    preferred_date: date
    slot_start: Optional[str] = None
    slot_end: Optional[str] = None

# 8. UPDATE PROCUREMENT STATUS
class ProcurementStatusUpdate(BaseModel):
    status: ProcurementStatus
    actual_quantity: Optional[float] = Field(default=None, gt=0, le=10000)
    final_price: Optional[float] = Field(default=None, gt=0, le=100000)

# 9. PROCUREMENT RESPONSE
class ProcurementResponse(BaseModel):
    id: int
    farmer_id: int
    center_id: int
    center_name: str
    crop_name: str
    expected_quantity: float
    actual_quantity: Optional[float]
    expected_price: float
    final_price: Optional[float]
    estimated_value: float
    final_value: Optional[float]
    preferred_date: date
    slot_start: Optional[str]
    slot_end: Optional[str]
    status: ProcurementStatus
    token_number: Optional[str]

# 10. CREATE PAYMENT
class PaymentCreate(BaseModel):
    transaction_id: int
    expected_date: Optional[date] = None

# 11. UPDATE PAYMENT STATUS
class PaymentStatusUpdate(BaseModel):
    status: PaymentStatus

# 12. PAYMENT RESPONSE
class PaymentResponse(BaseModel):
    id: int
    transaction_id: int
    estimated_amount: float
    final_amount: Optional[float]
    status: PaymentStatus
    expected_date: Optional[date]
    paid_at: Optional[datetime]

# 13. QUEUE WAIT-TIME PREDICTION REQUEST
class WaitPredictionRequest(BaseModel):
    queue_size: int = Field(ge=0, le=1000)
    center_capacity: int = Field(gt=0, le=10000)
    processing_rate: int = Field(gt=0, le=1000)
    quantity: float = Field(gt=0, le=10000)
    crop: str = Field(min_length=2, max_length=60)
    hour: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6)
    active_counters: int = Field(gt=0, le=20)

# 14. SMART SCHEDULE REQUEST
class ScheduleRequest(BaseModel):
    crop: str = Field(min_length=2, max_length=60)
    quantity: float = Field(gt=0, le=10000)
    location: str = Field(min_length=2, max_length=120)
    preferred_date: date

# 15. BOOK A SCHEDULE
class ScheduleBookRequest(BaseModel):
    center_id: int
    crop: str = Field(min_length=2, max_length=60)
    quantity: float = Field(gt=0, le=10000)
    preferred_date: date
    slot_start: str
    slot_end: str

# 16. CREATE FAMILY MEMBER
class FamilyMemberCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=10, max_length=30)
    relationship_name: str = Field(default="Family member", max_length=50)

# 17. STATUS ACTION REQUEST
class StatusActionRequest(BaseModel):
    transaction_id: int
    counter_number: Optional[int] = Field(default=None, ge=1, le=20)

# 18. TOKEN CALL REQUEST
class TokenCallRequest(BaseModel):
    counter_number: Optional[int] = Field(default=None, ge=1, le=20)

# 19. ASSISTED REGISTRATION REQUEST
class AssistedRegistrationRequest(BaseModel):
    farmer_name: str = Field(min_length=2, max_length=100)
    crop: str = Field(min_length=2, max_length=60)
    quantity: float = Field(gt=0, le=10000)
    location: str = Field(min_length=2, max_length=120)
    preferred_date: date
    center_id: int = 2

# 20. CHAT REQUEST
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
