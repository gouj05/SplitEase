from typing import Dict, List


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
# VALIDATE SINGLE ITEM
# ============================================================

def validate_item(
    item: Dict
) -> Dict:

    item_name = str(

        item.get(
            "name",
            "Unknown Item"
        )

    )


    quantity = to_float(

        item.get(
            "quantity",
            1
        ),

        1
    )


    unit_price = to_float(

        item.get(
            "unit_price",
            0
        )
    )


    actual_total = to_float(

        item.get(
            "line_total",
            0
        )
    )


    # ========================================================
    # CALCULATE EXPECTED TOTAL
    # ========================================================

    expected_total = round(

        quantity
        *
        unit_price,

        2
    )


    difference = round(

        actual_total
        -
        expected_total,

        2
    )


    # ========================================================
    # VALIDATION
    # ========================================================

    tolerance = 0.01


    is_valid = (

        abs(
            difference
        )

        <=

        tolerance
    )


    return {

        "item_name":
            item_name,

        "quantity":
            quantity,

        "unit_price":
            unit_price,

        "expected_total":
            expected_total,

        "actual_total":
            actual_total,

        "difference":
            difference,

        "is_valid":
            is_valid
    }


# ============================================================
# VALIDATE SUBTOTAL
# ============================================================

def validate_subtotal(
    items: List[Dict],
    summary: Dict
) -> Dict:

    calculated_subtotal = round(

        sum(

            to_float(

                item.get(
                    "line_total",
                    0
                )
            )

            for item
            in items
        ),

        2
    )


    actual_subtotal = to_float(

        summary.get(
            "subtotal",
            0
        )
    )


    difference = round(

        actual_subtotal
        -
        calculated_subtotal,

        2
    )


    tolerance = 0.01


    is_valid = (

        abs(
            difference
        )

        <=

        tolerance
    )


    return {

        "calculated_subtotal":
            calculated_subtotal,

        "actual_subtotal":
            actual_subtotal,

        "difference":
            difference,

        "is_valid":
            is_valid
    }


# ============================================================
# VALIDATE GRAND TOTAL
# ============================================================

def validate_grand_total(
    summary: Dict
) -> Dict:

    subtotal = to_float(

        summary.get(
            "subtotal",
            0
        )
    )


    packing_charges = to_float(

        summary.get(
            "packing_charges",
            0
        )
    )


    gst = to_float(

        summary.get(
            "gst",
            0
        )
    )


    tax = to_float(

        summary.get(
            "tax",
            0
        )
    )


    service_charge = to_float(

        summary.get(
            "service_charge",
            0
        )
    )


    discount = to_float(

        summary.get(
            "discount",
            0
        )
    )


    actual_total = to_float(

        summary.get(
            "grand_total",
            0
        )
    )


    # ========================================================
    # CALCULATE TOTAL
    # ========================================================

    calculated_total = round(

        subtotal

        +

        packing_charges

        +

        gst

        +

        tax

        +

        service_charge

        -

        discount,

        2
    )


    difference = round(

        actual_total
        -
        calculated_total,

        2
    )


    tolerance = 0.01


    is_valid = (

        abs(
            difference
        )

        <=

        tolerance
    )


    return {

        "calculated_total":
            calculated_total,

        "actual_total":
            actual_total,

        "difference":
            difference,

        "is_valid":
            is_valid
    }


# ============================================================
# MAIN VALIDATION FUNCTION
# ============================================================

def validate_bill(
    items: List[Dict],
    summary: Dict
) -> Dict:

    # ========================================================
    # VALIDATE ITEMS
    # ========================================================

    item_validations = [

        validate_item(
            item
        )

        for item
        in items
    ]


    # ========================================================
    # VALIDATE SUBTOTAL
    # ========================================================

    subtotal_validation = (

        validate_subtotal(

            items,

            summary
        )
    )


    # ========================================================
    # VALIDATE GRAND TOTAL
    # ========================================================

    grand_total_validation = (

        validate_grand_total(
            summary
        )
    )


    # ========================================================
    # CHECK ITEMS
    # ========================================================

    all_items_valid = all(

        item[
            "is_valid"
        ]

        for item
        in item_validations
    )


    # ========================================================
    # OVERALL VALIDATION
    # ========================================================

    overall_valid = (

        all_items_valid

        and

        subtotal_validation[
            "is_valid"
        ]

        and

        grand_total_validation[
            "is_valid"
        ]
    )


    return {

        "item_validations":
            item_validations,

        "subtotal_validation":
            subtotal_validation,

        "grand_total_validation":
            grand_total_validation,

        "overall_valid":
            overall_valid
    }