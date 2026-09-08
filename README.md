# SplitEase

> AI-powered bill extraction, validation, review, editing, and expense splitting application.

SmartSplit AI allows users to upload restaurant bills, automatically extract structured bill information using a Vision LLM, validate the extracted data, review uncertain values, manually edit incorrect values, and split expenses among multiple people.

---

## Features

### Bill Image Upload
- Upload bill images through the web interface or API
- Supports image files such as JPG, JPEG, PNG, and WEBP
- Generates unique filenames before storing uploaded files

### Vision LLM Bill Extraction
- Uses a Vision Language Model to understand bill images
- Extracts:
  - Item names
  - Quantities
  - Unit prices
  - Line totals
  - Subtotal
  - Packing charges
  - GST
  - Tax
  - Discount
  - Service charges
  - Grand total

### Structured Bill Output
The extracted bill is normalized into a structured JSON format.

```json
{
  "items": [
    {
      "name": "Paneer Butter Masala",
      "quantity": 1,
      "unit_price": 180,
      "line_total": 180,
      "confidence": 0.99,
      "needs_review": false
    }
  ],
  "summary": {
    "subtotal": 180,
    "packing_charges": 0,
    "gst": 9,
    "tax": 0,
    "discount": 0,
    "service_charge": 0,
    "grand_total": 189
  }
}
```

### Validation Engine
The application validates:

- Item quantity × unit price
- Item line totals
- Calculated subtotal
- Extracted subtotal
- Calculated grand total
- Extracted grand total

### Review Engine
The review system detects:

- Low-confidence extractions
- OCR or Vision LLM repair requirements
- Invalid calculations
- Suspicious numeric values

### Manual Bill Editing
Users can manually correct extracted values if the Vision LLM reads a bill incorrectly.

Editable values include:

- Item name
- Quantity
- Unit price
- Line total
- Subtotal
- GST
- Tax
- Discount
- Packing charges
- Service charges
- Grand total

### Bill Splitting
Users can split bill items among multiple members.

The application supports:

- Individual item assignment
- Shared items
- Multiple members per item
- Proportional charge distribution
- Packing charge distribution
- GST distribution
- Tax distribution
- Service charge distribution
- Discount distribution

### Dark Theme Frontend
The frontend includes:

- Modern dark theme
- Bill upload section
- Extracted bill display
- Editable bill values
- Validation results
- Review results
- Member management
- Item assignment
- Final split summary

---

# Project Architecture

```text
                    ┌─────────────────┐
                    │     User        │
                    │   Web Browser   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Frontend     │
                    │ HTML / CSS / JS │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │    Backend      │
                    └────────┬────────┘
                             │
           ┌─────────────────┼──────────────────┐
           ▼                 ▼                  ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Vision LLM   │  │ Validation   │  │ Split Engine │
    │ Extraction   │  │ Service      │  │              │
    └──────────────┘  └──────────────┘  └──────────────┘
           │                 │                  │
           └─────────────────┼──────────────────┘
                             ▼
                    ┌─────────────────┐
                    │   Bill Store    │
                    └─────────────────┘
```

---

# Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

## AI

- Google Gemini Vision LLM
- Google GenAI SDK

## Frontend

- HTML
- CSS
- JavaScript

## Other Tools

- Git
- GitHub
- Python Virtual Environment

---

# Project Structure

```text
ITGeeksVibecodingProject/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── routers/
│   │   └── bill.py
│   │
│   ├── schemas/
│   │   ├── bill.py
│   │   └── split.py
│   │
│   ├── services/
│   │   ├── vision_service.py
│   │   ├── validation_service.py
│   │   ├── review_service.py
│   │   └── split_service.py
│   │
│   ├── storage/
│   │   └── bill_store.py
│   │
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
│
├── uploads/
│
├── requirements.txt
│
├── .env
│
├── .gitignore
│
└── README.md
```

---

# Application Workflow

## Step 1: Upload Bill

The user uploads a restaurant bill image.

```text
User
  ↓
Upload Bill Image
  ↓
FastAPI
```

## Step 2: Vision LLM Extraction

The uploaded image is sent to the Vision LLM.

```text
Bill Image
   ↓
Vision LLM
   ↓
Structured JSON
```

Example extracted information:

```text
Item Name
Quantity
Unit Price
Line Total
Subtotal
GST
Grand Total
```

## Step 3: Normalization

The Vision LLM response is normalized into a consistent bill structure.

```text
Vision Response
      ↓
Normalization
      ↓
Standard Bill Schema
```

## Step 4: Validation

The extracted bill is mathematically validated.

Example:

```text
Quantity × Unit Price

3 × ₹20

= ₹60
```

The application compares the expected value with the extracted line total.

## Step 5: Review

The review engine checks:

```text
Confidence
Validation
Extraction Repairs
Suspicious Values
```

If problems are found:

```text
review_required = true
```

## Step 6: Manual Editing

The user can edit incorrect values directly from the frontend.

Example:

```text
Original:

Veg Biryani
Quantity: 1
Price: ₹150

User Correction:

Quantity: 2
Price: ₹150
```

## Step 7: Bill Splitting

Users enter members and assign items.

Example:

```text
Paneer Butter Masala
→ Gourang

Veg Biryani
→ Rahul

Tandoori Roti
→ Gourang + Rahul
```

## Step 8: Charge Distribution

Additional charges are distributed proportionally.

```text
Items Total
     ↓
Calculate Member Share
     ↓
Distribute GST
Distribute Packing Charges
Distribute Tax
     ↓
Final Amount
```

---

# API Endpoints

## Upload and Process Bill

### Endpoint

```text
POST /api/bills/upload
```

### Input

```text
multipart/form-data
```

Field:

```text
file
```

### Response

```json
{
  "success": true,
  "message": "Bill processed successfully",
  "bill_id": "generated-bill-id",
  "bill": {},
  "validation": {},
  "review": {}
}
```

---

## Get Bill

### Endpoint

```text
GET /api/bills/{bill_id}
```

Returns the stored bill details.

---

## Update Bill

### Endpoint

```text
PUT /api/bills/{bill_id}
```

Allows users to update incorrect extracted bill values.

---

## Split Bill

### Endpoint

```text
POST /api/bills/{bill_id}/split
```

### Example Request

```json
{
  "members": [
    {
      "name": "Gourang"
    },
    {
      "name": "Rahul"
    }
  ],
  "assignments": [
    {
      "item_index": 0,
      "members": [
        "Gourang"
      ]
    },
    {
      "item_index": 1,
      "members": [
        "Rahul"
      ]
    }
  ]
}
```

---

# Example Split Response

```json
{
  "success": true,
  "split": {
    "members": {
      "Gourang": {
        "items_total": 140,
        "final_amount": 148.24
      },
      "Rahul": {
        "items_total": 30,
        "final_amount": 31.76
      }
    }
  }
}
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd ITGeeksVibecodingProject
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv myvenv
```

Activate it:

```bash
myvenv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your `.env` file to GitHub.

---

# Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The server will run at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Example Vision Extraction

Input:

```text
Restaurant Bill Image
```

Output:

```json
{
  "items": [
    {
      "name": "Paneer Butter Masala",
      "quantity": 1,
      "unit_price": 180,
      "line_total": 180
    },
    {
      "name": "Veg Biryani",
      "quantity": 1,
      "unit_price": 150,
      "line_total": 150
    }
  ],
  "summary": {
    "subtotal": 330,
    "gst": 16.5,
    "grand_total": 346.5
  }
}
```

---

# Validation Logic

Each item is validated using:

```text
Expected Total

=

Quantity × Unit Price
```

Example:

```text
Quantity = 3

Unit Price = ₹20

Expected Total = ₹60

Actual Total = ₹60

Result = Valid
```

---

# Review Logic

The application calculates extraction confidence.

Example:

```text
Confidence = 0.99

Review Required = False
```

Low confidence example:

```text
Confidence = 0.60

Review Required = True
```

---

# Bill Splitting Logic

## Individual Item

```text
Item Total = ₹140

Assigned To:

Gourang

Final Share:

Gourang = ₹140
```

## Shared Item

```text
Item Total = ₹100

Assigned To:

Gourang
Rahul

Final Share:

Gourang = ₹50

Rahul = ₹50
```

---

# Additional Charge Distribution

Charges such as:

- GST
- Packing Charges
- Tax
- Service Charges

are distributed proportionally based on each member's item total.

Example:

```text
Gourang Items = ₹140

Rahul Items = ₹30

Total = ₹170
```

Packing Charge:

```text
₹10
```

Distribution:

```text
Gourang = ₹8.24

Rahul = ₹1.76
```

---

# Why Vision LLM Instead of Traditional OCR?

Traditional OCR can struggle with:

- Different bill layouts
- Merged text
- Different fonts
- Poor image quality
- Misaligned columns
- Complex restaurant invoices

The Vision LLM approach understands the bill as a document and directly produces structured information.

```text
Traditional Approach

Image
 ↓
OCR
 ↓
Text
 ↓
Layout Reconstruction
 ↓
Rule-Based Parsing


Vision LLM Approach

Image
 ↓
Vision LLM
 ↓
Structured Bill JSON
```

---

# Future Improvements

- PDF bill support
- Multi-page invoice support
- User authentication
- Persistent database storage
- Bill history
- User accounts
- Group expense history
- Payment integration
- Receipt analytics
- Monthly expense reports
- Multiple currencies
- Export split results as PDF
- Share bills through links
- WhatsApp sharing
- Mobile application

---

# Security

Sensitive files should be included in `.gitignore`.

Example:

```gitignore
myvenv/
.env
__pycache__/
*.pyc
uploads/
.vscode/
.idea/
```

---

# Project Status

Current features:

- [x] Bill image upload
- [x] Vision LLM bill extraction
- [x] Structured bill generation
- [x] Validation engine
- [x] Review engine
- [x] Manual bill editing
- [x] Member management
- [x] Item assignment
- [x] Bill splitting
- [x] Additional charge distribution
- [x] Dark theme frontend
- [x] FastAPI API documentation

---

# Author

**Gourang Joshi**

Computer Science Engineering Student

---

# License

This project is created for educational and academic purposes.
