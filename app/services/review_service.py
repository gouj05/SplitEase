from typing import Dict, List


# ============================================================
# CONFIGURATION
# ============================================================

LOW_CONFIDENCE_THRESHOLD = 0.75

MEDIUM_CONFIDENCE_THRESHOLD = 0.90


# ============================================================
# HELPER
# ============================================================

def to_float(
    value,
    default: float = 0.0
) -> float:

    if value is None:

        return default


    try:

        return float(value)


    except (
        ValueError,
        TypeError
    ):

        return default


# ============================================================
# REVIEW SINGLE ITEM
# ============================================================

def review_item(
    item: Dict,
    validation: Dict
) -> Dict:

    review_reasons = []


    item_name = str(

        item.get(
            "name",
            "Unknown Item"
        )
    )


    confidence = to_float(

        item.get(
            "confidence",
            0.8
        ),

        0.8
    )


    needs_review = bool(

        item.get(
            "needs_review",
            False
        )
    )


    # ========================================================
    # LOW CONFIDENCE
    # ========================================================

    if (

        confidence
        <
        LOW_CONFIDENCE_THRESHOLD
    ):

        review_reasons.append(

            "Low extraction confidence"
        )


    # ========================================================
    # MEDIUM CONFIDENCE
    # ========================================================

    elif (

        confidence
        <
        MEDIUM_CONFIDENCE_THRESHOLD
    ):

        review_reasons.append(

            "Moderate extraction confidence"
        )


    # ========================================================
    # MODEL FLAGGED REVIEW
    # ========================================================

    if needs_review:

        review_reasons.append(

            "Vision model flagged item for review"
        )


    # ========================================================
    # VALIDATION FAILED
    # ========================================================

    if not validation.get(

        "is_valid",
        True
    ):

        review_reasons.append(

            "Item calculation mismatch"
        )


    # ========================================================
    # EMPTY ITEM NAME
    # ========================================================

    if (

        not item_name.strip()

        or

        item_name.lower()
        ==
        "unknown item"
    ):

        review_reasons.append(

            "Item name missing or unclear"
        )


    # ========================================================
    # REVIEW REQUIRED
    # ========================================================

    review_required = (

        len(
            review_reasons
        )
        >
        0
    )


    return {

        "name":
            item_name,

        "confidence":
            round(
                confidence,
                4
            ),

        "review_required":
            review_required,

        "review_reasons":
            review_reasons
    }


# ============================================================
# REVIEW BILL
# ============================================================

def review_bill(
    bill: Dict,
    validation: Dict
) -> Dict:

    items = bill.get(

        "items",
        []
    )


    item_validations = validation.get(

        "item_validations",
        []
    )


    reviewed_items = []


    overall_reasons = []


    # ========================================================
    # REVIEW EACH ITEM
    # ========================================================

    for index, item in enumerate(items):

        item_validation = {}


        if (

            index
            <
            len(
                item_validations
            )
        ):

            item_validation = (

                item_validations[
                    index
                ]
            )


        item_review = (

            review_item(

                item,

                item_validation
            )
        )


        reviewed_items.append(

            item_review
        )


    # ========================================================
    # CHECK ITEM REVIEWS
    # ========================================================

    item_review_required = any(

        item[
            "review_required"
        ]

        for item
        in reviewed_items
    )


    # ========================================================
    # SUBTOTAL VALIDATION
    # ========================================================

    subtotal_validation = validation.get(

        "subtotal_validation",
        {}
    )


    if not subtotal_validation.get(

        "is_valid",
        True
    ):

        overall_reasons.append(

            "Subtotal calculation mismatch"
        )


    # ========================================================
    # GRAND TOTAL VALIDATION
    # ========================================================

    grand_total_validation = validation.get(

        "grand_total_validation",
        {}
    )


    if not grand_total_validation.get(

        "is_valid",
        True
    ):

        overall_reasons.append(

            "Grand total calculation mismatch"
        )


    # ========================================================
    # NO ITEMS
    # ========================================================

    if not items:

        overall_reasons.append(

            "No bill items extracted"
        )


    # ========================================================
    # COPY ITEM REVIEW REASONS
    # ========================================================

    for item in reviewed_items:

        for reason in item[

            "review_reasons"
        ]:

            if reason not in overall_reasons:

                overall_reasons.append(
                    reason
                )


    # ========================================================
    # CALCULATE OVERALL CONFIDENCE
    # ========================================================

    if items:

        confidence_values = [

            to_float(

                item.get(
                    "confidence",
                    0.8
                ),

                0.8
            )

            for item
            in items
        ]


        overall_confidence = round(

            sum(
                confidence_values
            )

            /

            len(
                confidence_values
            ),

            4
        )


    else:

        overall_confidence = 0.0


    # ========================================================
    # FINAL REVIEW STATUS
    # ========================================================

    review_required = (

        item_review_required

        or

        len(
            overall_reasons
        )
        >
        0

        or

        not validation.get(
            "overall_valid",
            False
        )
    )


    return {

        "overall_confidence":
            overall_confidence,

        "review_required":
            review_required,

        "review_reasons":
            overall_reasons,

        "items":
            reviewed_items
    }