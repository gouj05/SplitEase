from pydantic import BaseModel, Field
from typing import Optional, List


# ==========================================
# GENERIC FIELD WITH CONFIDENCE
# ==========================================

class MoneyField(BaseModel):

    value: Optional[float] = Field(
        default=None,
        description="Extracted monetary value"
    )

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )


# ==========================================
# TEXT FIELD WITH CONFIDENCE
# ==========================================

class TextField(BaseModel):

    value: Optional[str] = Field(
        default=None,
        description="Extracted text value"
    )

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )


# ==========================================
# QUANTITY FIELD
# ==========================================

class QuantityField(BaseModel):

    value: Optional[float] = Field(
        default=None
    )

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )


# ==========================================
# BILL ITEM
# ==========================================

class BillItem(BaseModel):

    name: TextField

    quantity: QuantityField

    unit_price: MoneyField

    line_total: MoneyField


# ==========================================
# COMPLETE BILL
# ==========================================

class Bill(BaseModel):

    restaurant_name: Optional[TextField] = None

    items: List[BillItem] = []

    subtotal: MoneyField

    gst: MoneyField

    service_charge: MoneyField

    discount: MoneyField

    printed_total: MoneyField


# ========================================================
# MEMBER
# ========================================================

class Member(BaseModel):

    name: str


# ========================================================
# ITEM ASSIGNMENT
# ========================================================

class ItemAssignment(BaseModel):

    item_index: int

    members: List[str]


# ========================================================
# SPLIT BILL REQUEST
# ========================================================

class SplitBillRequest(BaseModel):

    members: List[Member]

    assignments: List[ItemAssignment]