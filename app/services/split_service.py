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
# PREPARE ASSIGNMENTS
# ============================================================

def prepare_assignments(
    bill: Dict,
    assignments: List[Dict],
    all_members: List[str]
) -> List[Dict]:

    items = bill.get(
        "items",
        []
    )


    prepared_assignments = []


    assigned_indexes = set()


    for assignment in assignments:

        item_index = assignment.get(
            "item_index"
        )


        members = assignment.get(
            "members",
            []
        )


        # ====================================================
        # VALIDATE ITEM INDEX
        # ====================================================

        if item_index is None:

            raise ValueError(

                "Item index is required"
            )


        try:

            item_index = int(
                item_index
            )


        except (
            ValueError,
            TypeError
        ):

            raise ValueError(

                f"Invalid item index: "
                f"{item_index}"
            )


        if (

            item_index
            <
            0

            or

            item_index
            >=
            len(items)
        ):

            max_index = (

                len(items)
                -
                1
            )


            raise ValueError(

                f"Invalid item index: "
                f"{item_index}. "

                f"Valid indexes are "

                f"0 to {max_index}"
            )


        # ====================================================
        # DUPLICATE ASSIGNMENT
        # ====================================================

        if (

            item_index
            in
            assigned_indexes
        ):

            raise ValueError(

                f"Item index "
                f"{item_index} "
                f"is assigned multiple times"
            )


        assigned_indexes.add(
            item_index
        )


        # ====================================================
        # VALIDATE MEMBERS
        # ====================================================

        if not members:

            raise ValueError(

                f"Item index "
                f"{item_index} "
                f"has no members"
            )


        cleaned_members = []


        for member in members:

            member_name = str(
                member
            ).strip()


            if not member_name:

                continue


            if (

                member_name
                not in
                all_members
            ):

                raise ValueError(

                    f"Unknown member: "
                    f"{member_name}"
                )


            if (

                member_name
                not in
                cleaned_members
            ):

                cleaned_members.append(
                    member_name
                )


        if not cleaned_members:

            raise ValueError(

                f"No valid members found "
                f"for item index "
                f"{item_index}"
            )


        # ====================================================
        # GET ITEM
        # ====================================================

        item = items[
            item_index
        ]


        item_name = str(

            item.get(
                "name",
                f"Item {item_index}"
            )
        )


        line_total = to_float(

            item.get(
                "line_total",
                0
            )
        )


        prepared_assignments.append({

            "item_index":
                item_index,

            "item_name":
                item_name,

            "line_total":
                line_total,

            "members":
                cleaned_members
        })


    return prepared_assignments


# ============================================================
# VALIDATE ALL ITEMS ASSIGNED
# ============================================================

def validate_all_items_assigned(
    bill: Dict,
    prepared_assignments: List[Dict]
):

    items = bill.get(
        "items",
        []
    )


    assigned_indexes = {

        assignment[
            "item_index"
        ]

        for assignment
        in prepared_assignments
    }


    missing_indexes = []


    for index in range(
        len(items)
    ):

        if (

            index
            not in
            assigned_indexes
        ):

            missing_indexes.append(
                index
            )


    if missing_indexes:

        raise ValueError(

            "All items must be assigned. "

            f"Missing item indexes: "
            f"{missing_indexes}"
        )


# ============================================================
# SPLIT ITEM COST
# ============================================================

def split_item_cost(
    item_total: float,
    members: List[str]
) -> Dict:

    if not members:

        raise ValueError(

            "Cannot split item "
            "without members"
        )


    member_count = len(
        members
    )


    equal_share = round(

        item_total
        /
        member_count,

        2
    )


    result = {

        member:
            equal_share

        for member
        in members
    }


    # ========================================================
    # FIX ROUNDING DIFFERENCE
    # ========================================================

    current_total = round(

        sum(
            result.values()
        ),

        2
    )


    difference = round(

        item_total
        -
        current_total,

        2
    )


    if difference != 0:

        first_member = members[0]


        result[
            first_member
        ] = round(

            result[
                first_member
            ]

            +

            difference,

            2
        )


    return result


# ============================================================
# DISTRIBUTE CHARGE PROPORTIONALLY
# ============================================================

def distribute_charge(
    total_charge: float,
    member_totals: Dict[str, float]
) -> Dict:

    total_charge = round(
        total_charge,
        2
    )


    if total_charge == 0:

        return {

            member:
                0.0

            for member
            in member_totals
        }


    total_items = round(

        sum(
            member_totals.values()
        ),

        2
    )


    # ========================================================
    # EQUAL DISTRIBUTION IF ITEM TOTAL IS ZERO
    # ========================================================

    if total_items <= 0:

        member_names = list(
            member_totals.keys()
        )


        if not member_names:

            return {}


        equal_share = round(

            total_charge
            /
            len(member_names),

            2
        )


        result = {

            member:
                equal_share

            for member
            in member_names
        }


    # ========================================================
    # PROPORTIONAL DISTRIBUTION
    # ========================================================

    else:

        result = {}


        for member, amount in member_totals.items():

            proportion = (

                amount
                /
                total_items
            )


            member_charge = round(

                total_charge
                *
                proportion,

                2
            )


            result[
                member
            ] = member_charge


    # ========================================================
    # FIX ROUNDING
    # ========================================================

    distributed_total = round(

        sum(
            result.values()
        ),

        2
    )


    difference = round(

        total_charge
        -
        distributed_total,

        2
    )


    if difference != 0:

        first_member = next(
            iter(result)
        )


        result[
            first_member
        ] = round(

            result[
                first_member
            ]

            +

            difference,

            2
        )


    return result


# ============================================================
# MAIN SPLIT BILL FUNCTION
# ============================================================

def split_bill(
    bill: Dict,
    assignments: List[Dict],
    all_members: List[str]
) -> Dict:

    # ========================================================
    # VALIDATE BILL
    # ========================================================

    if not bill:

        raise ValueError(
            "Bill data is missing"
        )


    items = bill.get(
        "items",
        []
    )


    if not items:

        raise ValueError(
            "Bill contains no items"
        )


    # ========================================================
    # VALIDATE MEMBERS
    # ========================================================

    cleaned_members = []


    for member in all_members:

        member_name = str(
            member
        ).strip()


        if (

            member_name

            and

            member_name
            not in
            cleaned_members
        ):

            cleaned_members.append(
                member_name
            )


    if not cleaned_members:

        raise ValueError(

            "At least one member "
            "is required"
        )


    all_members = cleaned_members


    # ========================================================
    # PREPARE ASSIGNMENTS
    # ========================================================

    prepared_assignments = (

        prepare_assignments(

            bill=bill,

            assignments=assignments,

            all_members=all_members
        )
    )


    # ========================================================
    # CHECK ALL ITEMS ASSIGNED
    # ========================================================

    validate_all_items_assigned(

        bill,

        prepared_assignments
    )


    # ========================================================
    # INITIALIZE MEMBER TOTALS
    # ========================================================

    member_totals = {

        member:
            0.0

        for member
        in all_members
    }


    # ========================================================
    # ITEM BREAKDOWN
    # ========================================================

    item_breakdown = {

        member:
            []

        for member
        in all_members
    }


    # ========================================================
    # SPLIT ITEMS
    # ========================================================

    for assignment in prepared_assignments:

        item_name = assignment[
            "item_name"
        ]


        item_total = assignment[
            "line_total"
        ]


        assigned_members = assignment[
            "members"
        ]


        split_result = (

            split_item_cost(

                item_total,

                assigned_members
            )
        )


        for member, amount in split_result.items():

            member_totals[
                member
            ] += amount


            item_breakdown[
                member
            ].append({

                "item":
                    item_name,

                "amount":
                    round(
                        amount,
                        2
                    ),

                "shared_with":
                    assigned_members
            })


    # ========================================================
    # BILL SUMMARY
    # ========================================================

    summary = bill.get(
        "summary",
        {}
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


    # ========================================================
    # DISTRIBUTE CHARGES
    # ========================================================

    packing_distribution = (

        distribute_charge(

            packing_charges,

            member_totals
        )
    )


    gst_distribution = (

        distribute_charge(

            gst,

            member_totals
        )
    )


    tax_distribution = (

        distribute_charge(

            tax,

            member_totals
        )
    )


    service_distribution = (

        distribute_charge(

            service_charge,

            member_totals
        )
    )


    discount_distribution = (

        distribute_charge(

            discount,

            member_totals
        )
    )


    # ========================================================
    # FINAL MEMBER DATA
    # ========================================================

    final_members = {}


    for member in all_members:

        items_total = round(

            member_totals[
                member
            ],

            2
        )


        member_packing = round(

            packing_distribution.get(
                member,
                0
            ),

            2
        )


        member_gst = round(

            gst_distribution.get(
                member,
                0
            ),

            2
        )


        member_tax = round(

            tax_distribution.get(
                member,
                0
            ),

            2
        )


        member_service = round(

            service_distribution.get(
                member,
                0
            ),

            2
        )


        member_discount = round(

            discount_distribution.get(
                member,
                0
            ),

            2
        )


        # ====================================================
        # EXTRA CHARGES
        # ====================================================

        extra_charges = round(

            member_packing

            +

            member_gst

            +

            member_tax

            +

            member_service,

            2
        )


        # ====================================================
        # FINAL AMOUNT
        # ====================================================

        final_amount = round(

            items_total

            +

            extra_charges

            -

            member_discount,

            2
        )


        final_members[
            member
        ] = {

            "items_total":
                items_total,

            "item_breakdown":
                item_breakdown[
                    member
                ],

            "charges": {

                "packing_charges":
                    member_packing,

                "gst":
                    member_gst,

                "tax":
                    member_tax,

                "service_charge":
                    member_service
            },

            "discount":
                member_discount,

            "final_amount":
                final_amount
        }


    # ========================================================
    # FINAL RECONCILIATION
    # ========================================================

    calculated_total = round(

        sum(

            member[
                "final_amount"
            ]

            for member
            in final_members.values()
        ),

        2
    )


    actual_total = to_float(

        summary.get(
            "grand_total",
            0
        )
    )


    difference = round(

        calculated_total
        -
        actual_total,

        2
    )


    # ========================================================
    # TOTAL EXTRA CHARGES
    # ========================================================

    total_extra_charges = round(

        packing_charges

        +

        gst

        +

        tax

        +

        service_charge,

        2
    )


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "members":
            final_members,

        "summary": {

            "items_total":

                round(

                    sum(
                        member_totals.values()
                    ),

                    2
                ),

            "extra_charges":
                total_extra_charges,

            "discount":
                round(
                    discount,
                    2
                ),

            "calculated_total":
                calculated_total,

            "actual_grand_total":
                actual_total,

            "difference":
                difference
        }
    }