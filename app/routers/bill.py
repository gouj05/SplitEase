from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from pathlib import Path

import shutil
import uuid


from app.schemas.bill import (
    Bill,
    SplitBillRequest
)


from app.services.vision_service import (
    extract_bill_from_image
)


from app.services.validation_service import (
    validate_bill
)


from app.services.review_service import (
    review_bill
)


from app.services.split_service import (
    split_bill
)
from app.storage.bill_store import (
    bill_store
)
# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/bills",
    tags=["Bills"]
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)


UPLOAD_DIR = BASE_DIR / "uploads"


UPLOAD_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# UPLOAD AND PROCESS BILL
# ============================================================

@router.post("/upload")
async def upload_bill(

    file: UploadFile = File(
        ...,
        description="Upload a bill image"
    )
):

    # ========================================================
    # VALIDATE FILE
    # ========================================================

    if not file.content_type:

        raise HTTPException(
            status_code=400,
            detail="File type could not be determined"
        )


    if not file.content_type.startswith("image/"):

        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed"
        )


    # ========================================================
    # GENERATE UNIQUE FILE NAME
    # ========================================================

    original_filename = (
        file.filename
        or "bill_image"
    )


    file_extension = Path(
        original_filename
    ).suffix


    unique_filename = (
        f"{uuid.uuid4()}"
        f"{file_extension}"
    )


    file_path = (
        UPLOAD_DIR
        / unique_filename
    )


    # ========================================================
    # SAVE FILE
    # ========================================================

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to save file: "
                f"{str(error)}"
            )
        )


    # ========================================================
    # PROCESS BILL
    # ========================================================

    try:

    # ====================================================
    # STEP 1: GEMINI VISION EXTRACTION
    # ====================================================

        bill = (
    
            extract_bill_from_image(
    
                str(file_path)
            )
        )
    
    
        # ====================================================
        # STEP 2: VALIDATION ENGINE
        # ====================================================
    
        validation = (
    
            validate_bill(
    
                bill["items"],
    
                bill["summary"]
            )
        )
    
    
        # ====================================================
        # STEP 3: REVIEW ENGINE
        # ====================================================
    
        review = (
    
            review_bill(
    
                bill,
    
                validation
            )
        )
    
    
        # ====================================================
        # STEP 4: SAVE BILL
        # ====================================================
    
        bill_id = (
    
            bill_store.save_bill({
    
                "bill":
                    bill,
    
                "validation":
                    validation,
    
                "review":
                    review,
    
                "reviewed":
                    False,
    
                "confirmed":
                    False,
    
                "file": {
    
                    "original_name":
                        original_filename,
    
                    "stored_name":
                        unique_filename,
    
                    "content_type":
                        file.content_type
                }
            })
        )
    
    
        # ====================================================
        # FINAL RESPONSE
        # ====================================================
    
        return {
    
            "success":
                True,
    
            "message":
                "Bill processed successfully",
    
            "bill_id":
                bill_id,
    
            "file": {
    
                "original_name":
                    original_filename,
    
                "stored_name":
                    unique_filename,
    
                "content_type":
                    file.content_type
            },
    
            "bill":
                bill,
    
            "validation":
                validation,
    
            "review":
                review
        }
    

    except Exception as error:
    
        raise HTTPException(
    
            status_code=500,
    
            detail=(
    
                "Bill processing failed: "
    
                f"{str(error)}"
            )
        )

@router.post("/test-schema")
async def test_schema(
    bill: Bill
):

    return {

        "success": True,

        "message":
            "Pydantic validation successful",

        "data":
            bill
    }
@router.get("/{bill_id}")
async def get_bill(
    bill_id: str
):

    stored_bill = (
        bill_store.get_bill(
            bill_id
        )
    )


    if not stored_bill:

        raise HTTPException(

            status_code=404,

            detail="Bill not found"
        )


    return {

        "success": True,

        "bill_id":
            bill_id,

        "data":
            stored_bill
    }
@router.post("/{bill_id}/split")
async def split_bill_between_members(

    bill_id: str,

    request: SplitBillRequest
):

    # ========================================================
    # GET BILL
    # ========================================================

    stored_bill = bill_store.get_bill(
        bill_id
    )


    if not stored_bill:

        raise HTTPException(

            status_code=404,

            detail="Bill not found"
        )


    # ========================================================
    # DEBUG STORED BILL
    # ========================================================

    print("\n")
    print("=" * 60)
    print("SPLIT DEBUG")
    print("=" * 60)

    print("BILL ID:")
    print(bill_id)

    print("\nSTORED BILL:")
    print(stored_bill)

    print("\nSTORED ITEMS:")

    print(
        stored_bill.get(
            "bill",
            {}
        ).get(
            "items",
            []
        )
    )

    print("\nNUMBER OF STORED ITEMS:")

    print(
        len(
            stored_bill.get(
                "bill",
                {}
            ).get(
                "items",
                []
            )
        )
    )

    print("\nREQUEST ASSIGNMENTS:")

    print(
        request.assignments
    )

    print("=" * 60)
    print("\n")


    # ========================================================
    # EXTRACT MEMBER NAMES
    # ========================================================

    member_names = [

        member.name.strip()

        for member
        in request.members
    ]


    # ========================================================
    # CONVERT ASSIGNMENTS
    # ========================================================

    assignments = [

        assignment.model_dump()

        for assignment
        in request.assignments
    ]


    # ========================================================
    # SPLIT BILL
    # ========================================================

    try:

        split_result = split_bill(

            bill=stored_bill[
                "bill"
            ],

            assignments=assignments,

            all_members=member_names
        )


    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)
        )


    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(
                "Bill splitting failed: "
                f"{str(error)}"
            )
        )


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "success": True,

        "message":
            "Bill split successfully",

        "bill_id":
            bill_id,

        "split":
            split_result
    }
@router.post("/{bill_id}/review")
async def review_stored_bill(

    bill_id: str

):

    # ========================================================
    # GET BILL
    # ========================================================

    stored_bill = bill_store.get_bill(

        bill_id
    )


    if not stored_bill:

        raise HTTPException(

            status_code=404,

            detail="Bill not found"
        )


    # ========================================================
    # GET ORIGINAL DATA
    # ========================================================

    bill = stored_bill.get(
        "bill"
    )


    validation = stored_bill.get(
        "validation"
    )


    # ========================================================
    # RUN REVIEW
    # ========================================================

    review = review_bill(

        bill,

        validation
    )


    # ========================================================
    # UPDATE ONLY REVIEW
    # ========================================================

    stored_bill[
        "review"
    ] = review


    stored_bill[
        "reviewed"
    ] = True


    # ========================================================
    # SAVE
    # ========================================================

    bill_store.update_bill(

        bill_id,

        stored_bill
    )


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "success": True,

        "message":
            "Bill reviewed successfully",

        "bill_id":
            bill_id,

        "review":
            review
    }
@router.post("/{bill_id}/confirm")
async def confirm_bill(

    bill_id: str

):

    # ========================================================
    # GET STORED BILL
    # ========================================================

    stored_bill = bill_store.get_bill(

        bill_id
    )


    if not stored_bill:

        raise HTTPException(

            status_code=404,

            detail="Bill not found"
        )


    # ========================================================
    # DEBUG
    # ========================================================

    print("\n")
    print("=" * 60)
    print("CONFIRM BILL DEBUG")
    print("=" * 60)

    print("BEFORE CONFIRM:")
    print(
        stored_bill.get(
            "bill"
        )
    )

    print("=" * 60)


    # ========================================================
    # CONFIRM BILL
    # ========================================================

    stored_bill[
        "confirmed"
    ] = True


    # ========================================================
    # SAVE UPDATED BILL
    # ========================================================

    bill_store.update_bill(

        bill_id,

        stored_bill
    )


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "success": True,

        "message":
            "Bill confirmed successfully",

        "bill_id":
            bill_id,

        "bill":
            stored_bill[
                "bill"
            ],

        "confirmed":
            True
    }