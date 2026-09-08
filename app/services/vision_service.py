import os
import json
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)


if not GEMINI_API_KEY:

    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )


client = genai.Client(

    api_key=GEMINI_API_KEY
)


# ============================================================
# BILL EXTRACTION PROMPT
# ============================================================

BILL_EXTRACTION_PROMPT = """
You are an expert receipt and restaurant bill extraction system.

Your job is to carefully analyze the uploaded bill image and
extract the purchased items and bill summary.

Return ONLY valid JSON.

Do not return markdown.

Do not use ```json.

============================================================
ITEM EXTRACTION RULES
============================================================

1. Extract EVERY purchased item separately.

2. Each visual item row should normally be treated as a separate item.

3. NEVER merge two consecutive item rows into one item.

4. Only combine multiple lines when they clearly belong to the
   SAME item name.

5. Use table columns such as:
   - Item
   - Description
   - Quantity
   - Qty
   - Rate
   - Price
   - Amount

   to understand item boundaries.

6. An item should contain:

   - name
   - quantity
   - unit_price
   - line_total

7. If quantity is missing, assume:

   quantity = 1

   only when this is logically supported by the bill.

8. Do not invent items.

9. Do not merge item names just because they appear vertically close.

10. Preserve the item names exactly as reasonably visible.

============================================================
IMPORTANT ITEM EXAMPLES
============================================================

If the bill visually contains:

Shawarma Plate       1     140.00     140.00
Poratta Normal
Paratha              2      15.00      30.00

Then the correct extraction is:

Item 1:
name = "Shawarma Plate"
quantity = 1
unit_price = 140
line_total = 140

Item 2:
name = "Poratta Normal Paratha"
quantity = 2
unit_price = 15
line_total = 30

Do NOT return:

"Shawarma Plate Poratta Normal"

as one item.

============================================================
SUMMARY RULES
============================================================

Extract the following if present:

- subtotal
- packing_charges
- gst
- tax
- discount
- service_charge
- grand_total

Do NOT treat these values as purchased items.

If a field is not present, use 0.

============================================================
VALIDATION RULES
============================================================

Before returning JSON:

1. Check:

   quantity × unit_price ≈ line_total

2. Check that:

   sum(item line totals) ≈ subtotal

3. Check that:

   subtotal
   + packing charges
   + GST
   + tax
   + service charge
   - discount

   ≈ grand total

4. Do not modify clearly visible bill values merely to make
   calculations match.

============================================================
CONFIDENCE RULES
============================================================

confidence should be between 0 and 1.

Use:

0.95 - 1.0
for clearly visible values.

0.75 - 0.94
for slightly unclear values.

Below 0.75
for uncertain extraction.

Set needs_review = true when:

- item name is unclear
- numeric values are unclear
- item row structure is uncertain
- values appear inconsistent

============================================================
RETURN FORMAT
============================================================

Return exactly this JSON structure:

{
    "items": [
        {
            "name": "string",
            "quantity": 1,
            "unit_price": 0,
            "line_total": 0,
            "confidence": 0.95,
            "needs_review": false
        }
    ],
    "summary": {
        "subtotal": 0,
        "packing_charges": 0,
        "gst": 0,
        "tax": 0,
        "discount": 0,
        "service_charge": 0,
        "grand_total": 0
    }
}
"""


# ============================================================
# CLEAN GEMINI RESPONSE
# ============================================================

def clean_json_response(
    response_text: str
) -> str:

    text = response_text.strip()


    # Remove markdown JSON block

    text = re.sub(

        r"^```json",

        "",

        text,

        flags=re.IGNORECASE
    )


    # Remove normal markdown block

    text = re.sub(

        r"^```",

        "",

        text
    )


    text = re.sub(

        r"```$",

        "",

        text
    )


    text = text.strip()


    return text


# ============================================================
# NORMALIZE NUMERIC VALUES
# ============================================================

def to_float(
    value,
    default=0.0
):

    if value is None:

        return default


    if isinstance(
        value,
        (int, float)
    ):

        return float(value)


    try:

        value = str(value)


        value = value.replace(
            "₹",
            ""
        )


        value = value.replace(
            ",",
            ""
        )


        value = value.strip()


        return float(value)


    except Exception:

        return default


# ============================================================
# NORMALIZE ITEM
# ============================================================

def normalize_item(
    item: dict
) -> dict:

    return {

        "name":

            str(

                item.get(
                    "name",
                    "Unknown Item"
                )

            ).strip(),


        "quantity":

            to_float(

                item.get(
                    "quantity",
                    1
                ),

                1
            ),


        "unit_price":

            to_float(

                item.get(
                    "unit_price",
                    0
                )
            ),


        "line_total":

            to_float(

                item.get(
                    "line_total",
                    0
                )
            ),


        "confidence":

            min(

                max(

                    to_float(

                        item.get(
                            "confidence",
                            0.8
                        ),

                        0.8
                    ),

                    0
                ),

                1
            ),


        "needs_review":

            bool(

                item.get(
                    "needs_review",
                    False
                )
            )
    }


# ============================================================
# NORMALIZE SUMMARY
# ============================================================

def normalize_summary(
    summary: dict
) -> dict:

    return {

        "subtotal":

            to_float(

                summary.get(
                    "subtotal",
                    0
                )
            ),


        "packing_charges":

            to_float(

                summary.get(
                    "packing_charges",
                    0
                )
            ),


        "gst":

            to_float(

                summary.get(
                    "gst",
                    0
                )
            ),


        "tax":

            to_float(

                summary.get(
                    "tax",
                    0
                )
            ),


        "discount":

            to_float(

                summary.get(
                    "discount",
                    0
                )
            ),


        "service_charge":

            to_float(

                summary.get(
                    "service_charge",
                    0
                )
            ),


        "grand_total":

            to_float(

                summary.get(
                    "grand_total",
                    0
                )
            )
    }


# ============================================================
# NORMALIZE FULL BILL
# ============================================================

def normalize_bill(
    bill: dict
) -> dict:

    items = bill.get(
        "items",
        []
    )


    summary = bill.get(
        "summary",
        {}
    )


    normalized_items = []


    for item in items:

        if not isinstance(
            item,
            dict
        ):

            continue


        normalized_item = (

            normalize_item(
                item
            )
        )


        # Skip completely empty items

        if (

            not normalized_item["name"]

            or

            normalized_item["name"]
            == "Unknown Item"
        ):

            continue


        normalized_items.append(

            normalized_item
        )


    return {

        "items":

            normalized_items,


        "summary":

            normalize_summary(
                summary
            )
    }


# ============================================================
# EXTRACT BILL USING GEMINI VISION
# ============================================================

def extract_bill_from_image(
    image_path: str
) -> dict:

    print(
        "\n"
        "=" * 60
    )

    print(
        "VISION BILL EXTRACTION"
    )

    print(
        "=" * 60
    )


    # ========================================================
    # READ IMAGE
    # ========================================================

    with open(

        image_path,

        "rb"

    ) as image_file:

        image_bytes = (

            image_file.read()
        )


    # ========================================================
    # DETERMINE MIME TYPE
    # ========================================================

    extension = (

        os.path.splitext(
            image_path
        )[1]

        .lower()
    )


    mime_map = {

        ".jpg":
            "image/jpeg",

        ".jpeg":
            "image/jpeg",

        ".png":
            "image/png",

        ".webp":
            "image/webp"
    }


    mime_type = (

        mime_map.get(
            extension,
            "image/jpeg"
        )
    )


    # ========================================================
    # CREATE IMAGE PART
    # ========================================================

    image_part = (

        types.Part.from_bytes(

            data=image_bytes,

            mime_type=mime_type
        )
    )


    # ========================================================
    # CALL GEMINI
    # ========================================================

    try:

        response = (

            client.models.generate_content(

                model=GEMINI_MODEL,

                contents=[

                    image_part,

                    BILL_EXTRACTION_PROMPT
                ],

                config=types.GenerateContentConfig(

                    temperature=0.1,

                    response_mime_type=
                        "application/json"
                )
            )
        )


    except Exception as error:

        raise RuntimeError(

            "Gemini Vision API failed: "

            f"{str(error)}"
        )


    # ========================================================
    # GET RESPONSE TEXT
    # ========================================================

    if not response.text:

        raise RuntimeError(

            "Gemini returned an empty response"
        )


    print(
        "\nRAW GEMINI RESPONSE:\n"
    )

    print(
        response.text
    )


    # ========================================================
    # CLEAN RESPONSE
    # ========================================================

    cleaned_response = (

        clean_json_response(
            response.text
        )
    )


    # ========================================================
    # PARSE JSON
    # ========================================================

    try:

        bill_data = (

            json.loads(
                cleaned_response
            )
        )


    except json.JSONDecodeError as error:

        raise RuntimeError(

            "Gemini returned invalid JSON: "

            f"{str(error)}"
        )


    # ========================================================
    # NORMALIZE BILL
    # ========================================================

    normalized_bill = (

        normalize_bill(
            bill_data
        )
    )


    print(
        "\n"
        "=" * 60
    )

    print(
        "FINAL NORMALIZED BILL"
    )

    print(
        "=" * 60
    )

    print(

        json.dumps(

            normalized_bill,

            indent=4
        )
    )


    return normalized_bill