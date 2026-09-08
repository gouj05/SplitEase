from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from typing import (
    List,
    Optional
)


# ============================================================
# ITEM
# ============================================================

class ReviewItem(BaseModel):

    name: str = Field(
        ...,
        min_length=1
    )

    quantity: float = Field(
        ...,
        gt=0
    )

    unit_price: float = Field(
        ...,
        ge=0
    )

    line_total: float = Field(
        ...,
        ge=0
    )

    confidence: Optional[float] = Field(
        default=1.0,
        ge=0,
        le=1
    )

    needs_review: bool = False


# ============================================================
# BILL SUMMARY
# ============================================================

class ReviewSummary(BaseModel):

    subtotal: Optional[float] = Field(
        default=None,
        ge=0
    )

    packing_charges: Optional[float] = Field(
        default=None,
        ge=0
    )

    gst: Optional[float] = Field(
        default=None,
        ge=0
    )

    tax: Optional[float] = Field(
        default=None,
        ge=0
    )

    discount: Optional[float] = Field(
        default=None,
        ge=0
    )

    service_charge: Optional[float] = Field(
        default=None,
        ge=0
    )

    grand_total: Optional[float] = Field(
        default=None,
        ge=0
    )


# ============================================================
# REVIEW REQUEST
# ============================================================

class ReviewBillRequest(BaseModel):

    items: List[ReviewItem] = Field(
        ...,
        min_length=1
    )

    summary: ReviewSummary


# ============================================================
# CONFIRM REQUEST
# ============================================================

class ConfirmBillRequest(BaseModel):

    confirmed: bool