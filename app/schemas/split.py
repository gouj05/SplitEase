from pydantic import (
    BaseModel,
    Field,
    field_validator
)

from typing import List


# ============================================================
# MEMBER
# ============================================================

class Member(BaseModel):

    name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )


# ============================================================
# ITEM ASSIGNMENT
# ============================================================

class ItemAssignment(BaseModel):

    item_index: int = Field(
        ...,
        ge=0
    )


    members: List[str] = Field(
        ...,
        min_length=1
    )


    @field_validator("members")
    @classmethod
    def validate_members(
        cls,
        members
    ):

        cleaned_members = []


        for member in members:

            member = member.strip()


            if member:

                cleaned_members.append(
                    member
                )


        if not cleaned_members:

            raise ValueError(
                "At least one member must be assigned"
            )


        # Remove duplicates

        return list(
            dict.fromkeys(
                cleaned_members
            )
        )


# ============================================================
# SPLIT REQUEST
# ============================================================

class SplitBillRequest(BaseModel):

    members: List[Member] = Field(
        ...,
        min_length=1,
        max_length=20
    )


    assignments: List[
        ItemAssignment
    ] = Field(
        ...,
        min_length=1
    )


    @field_validator("members")
    @classmethod
    def validate_unique_members(
        cls,
        members
    ):

        names = [

            member.name.strip()

            for member in members
        ]


        if len(names) != len(set(names)):

            raise ValueError(
                "Member names must be unique"
            )


        return members