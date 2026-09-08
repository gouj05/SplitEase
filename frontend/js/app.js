// ============================================================
// SPLIT STATE
// ============================================================

let currentBillId = null;

let currentBillData = null;

let members = [];
let currentBill = null;
// ============================================================
// ELEMENTS
// ============================================================
const splitSection =
    document.getElementById(
        "splitSection"
    );


const memberName =
    document.getElementById(
        "memberName"
    );


const addMemberBtn =
    document.getElementById(
        "addMemberBtn"
    );


const membersList =
    document.getElementById(
        "membersList"
    );


const itemAssignmentList =
    document.getElementById(
        "itemAssignmentList"
    );


const calculateSplitBtn =
    document.getElementById(
        "calculateSplitBtn"
    );


const splitResult =
    document.getElementById(
        "splitResult"
    );
const uploadArea =
    document.getElementById(
        "uploadArea"
    );


const billFile =
    document.getElementById(
        "billFile"
    );


const browseBtn =
    document.getElementById(
        "browseBtn"
    );


const filePreview =
    document.getElementById(
        "filePreview"
    );


const previewImage =
    document.getElementById(
        "previewImage"
    );


const fileName =
    document.getElementById(
        "fileName"
    );


const removeFile =
    document.getElementById(
        "removeFile"
    );


const processBtn =
    document.getElementById(
        "processBtn"
    );


const loadingSection =
    document.getElementById(
        "loadingSection"
    );


const resultSection =
    document.getElementById(
        "resultSection"
    );


const billResult =
    document.getElementById(
        "billResult"
    );


// ============================================================
// SELECT FILE
// ============================================================

browseBtn.addEventListener(

    "click",

    function (event) {

        event.stopPropagation();

        billFile.click();

    }
);


// ============================================================
// CLICK UPLOAD AREA
// ============================================================

uploadArea.addEventListener(

    "click",

    function () {

        billFile.click();

    }
);


// ============================================================
// FILE CHANGE
// ============================================================

billFile.addEventListener(

    "change",

    function () {

        const file =
            billFile.files[0];


        if (!file) {

            return;

        }


        if (
            !file.type.startsWith(
                "image/"
            )
        ) {

            alert(
                "Please upload an image file"
            );

            billFile.value = "";

            return;

        }


        showPreview(
            file
        );

    }
);


// ============================================================
// SHOW PREVIEW
// ============================================================

function showPreview(file) {

    const reader =
        new FileReader();


    reader.onload =
        function (event) {

            previewImage.src =
                event.target.result;

        };


    reader.readAsDataURL(
        file
    );


    fileName.textContent =
        file.name;


    uploadArea.classList.add(
        "d-none"
    );


    filePreview.classList.remove(
        "d-none"
    );


    resultSection.classList.add(
        "d-none"
    );

}


// ============================================================
// REMOVE FILE
// ============================================================

removeFile.addEventListener(

    "click",

    function () {

        billFile.value =
            "";


        previewImage.src =
            "";


        fileName.textContent =
            "";


        filePreview.classList.add(
            "d-none"
        );


        uploadArea.classList.remove(
            "d-none"
        );


        resultSection.classList.add(
            "d-none"
        );

    }
);


// ============================================================
// DRAG OVER
// ============================================================

uploadArea.addEventListener(

    "dragover",

    function (event) {

        event.preventDefault();

        uploadArea.classList.add(
            "drag-active"
        );

    }
);


// ============================================================
// DRAG LEAVE
// ============================================================

uploadArea.addEventListener(

    "dragleave",

    function () {

        uploadArea.classList.remove(
            "drag-active"
        );

    }
);


// ============================================================
// DROP FILE
// ============================================================

uploadArea.addEventListener(

    "drop",

    function (event) {

        event.preventDefault();


        uploadArea.classList.remove(
            "drag-active"
        );


        const file =
            event.dataTransfer.files[0];


        if (!file) {

            return;

        }


        if (
            !file.type.startsWith(
                "image/"
            )
        ) {

            alert(
                "Please upload an image file"
            );

            return;

        }


        const dataTransfer =
            new DataTransfer();


        dataTransfer.items.add(
            file
        );


        billFile.files =
            dataTransfer.files;


        showPreview(
            file
        );

    }
);


// ============================================================
// PROCESS BILL
// ============================================================

processBtn.addEventListener(

    "click",

    async function () {

        const file =
            billFile.files[0];


        // ====================================================
        // CHECK FILE
        // ====================================================

        if (!file) {

            alert(
                "Please select a bill image first"
            );

            return;

        }


        // ====================================================
        // CREATE FORM DATA
        // ====================================================

        const formData =
            new FormData();


        // IMPORTANT:
        // Backend parameter name is "file"

        formData.append(
            "file",
            file
        );


        // ====================================================
        // SHOW LOADING
        // ====================================================

        loadingSection.classList.remove(
            "d-none"
        );


        resultSection.classList.add(
            "d-none"
        );


        processBtn.disabled =
            true;


        processBtn.innerHTML =
            `
            <span
                class="spinner-border spinner-border-sm"
            ></span>

            Processing...
            `;


        try {


            // =================================================
            // CALL FASTAPI
            // =================================================

            const response =
                await fetch(

                    "/api/bills/upload",

                    {

                        method:
                            "POST",

                        body:
                            formData

                    }

                );


            // =================================================
            // PARSE RESPONSE
            // =================================================

            const data =
                await response.json();


            // =================================================
            // HANDLE ERROR
            // =================================================

            if (!response.ok) {

                throw new Error(

                    data.detail
                    ||
                    "Failed to process bill"

                );

            }


            // =================================================
            // DEBUG
            // =================================================

            console.log(
                "API RESPONSE:",
                data
            );


            // =================================================
            // DISPLAY RESULT
            // =================================================

            // ============================================================
// SAVE LATEST BILL DATA
// ============================================================

window.latestBillData =
    data;


// ============================================================
// SAVE CURRENT BILL
// ============================================================

currentBillData =
    data;


// ============================================================
// DISPLAY NORMAL RESULT
// ============================================================

displayBillResult(
    data
);


// ============================================================
// DISPLAY EDITABLE BILL
// ============================================================

displayEditableBill(

    data.bill,

    data.bill_id
);


// ============================================================
// UPDATE PROGRESS
// ============================================================

document
    .getElementById(
        "step1"
    )
    .classList
    .remove(
        "active"
    );


document
    .getElementById(
        "step2"
    )
    .classList
    .add(
        "active"
    );
        }


        catch (error) {


            console.error(
                "ERROR:",
                error
            );


            alert(

                "Error processing bill: "

                + error.message

            );

        }


        finally {


            // =================================================
            // HIDE LOADING
            // =================================================

            loadingSection.classList.add(
                "d-none"
            );


            // =================================================
            // ENABLE BUTTON
            // =================================================

            processBtn.disabled =
                false;


            processBtn.innerHTML =
                `
                <i
                    class="bi bi-cpu"
                ></i>

                Process Bill
                `;

        }

    }

);


// ============================================================
// DISPLAY BILL RESULT
// ============================================================

function displayBillResult(data) {


    // ========================================================
    // GET DATA
    // ========================================================

    const bill =
        data.bill;


    const validation =
        data.validation;


    const review =
        data.review;


    const items =
        bill.items
        ||
        [];


    const summary =
        bill.summary
        ||
        {};


    // ========================================================
    // BUILD HTML
    // ========================================================

    let html =
        `
        <div
            class="row"
        >
        `;


    // ========================================================
    // ITEMS CARD
    // ========================================================

    html +=
        `
        <div
            class="col-lg-8"
        >

            <div
                class="card shadow-sm border-0 mb-4"
            >

                <div
                    class="card-body"
                >

                    <h4
                        class="fw-bold mb-4"
                    >

                        <i
                            class="bi bi-receipt"
                        ></i>

                        Extracted Items

                    </h4>
        `;


    // ========================================================
    // ITEMS
    // ========================================================

    if (
        items.length === 0
    ) {

        html +=
            `
            <div
                class="alert alert-warning"
            >

                No items found.

            </div>
            `;

    }


    items.forEach(

        function (item, index) {


            const reviewBadge =
                item.needs_review

                ?

                `
                <span
                    class="badge bg-warning text-dark"
                >

                    Review

                </span>
                `

                :

                `
                <span
                    class="badge bg-success"
                >

                    Verified

                </span>
                `;


            html +=
                `

                <div
                    class="bill-item"
                >

                    <div
                        class="d-flex justify-content-between"
                    >

                        <div>

                            <h5
                                class="mb-1"
                            >

                                ${index + 1}.
                                ${item.name}

                            </h5>


                            <small
                                class="text-muted"
                            >

                                Quantity:

                                ${item.quantity}

                                ×

                                ₹${item.unit_price}

                            </small>

                        </div>


                        <div
                            class="text-end"
                        >

                            <h5>

                                ₹${item.line_total}

                            </h5>

                            ${reviewBadge}

                        </div>

                    </div>

                </div>

                `;

        }

    );


    html +=
        `

                </div>

            </div>

        </div>
        `;


    // ========================================================
    // SUMMARY CARD
    // ========================================================

    html +=
        `

        <div
            class="col-lg-4"
        >

            <div
                class="card shadow-sm border-0"
            >

                <div
                    class="card-body"
                >

                    <h4
                        class="fw-bold mb-4"
                    >

                        Bill Summary

                    </h4>


                    <div
                        class="summary-row"
                    >

                        <span>

                            Subtotal

                        </span>


                        <strong>

                            ₹${summary.subtotal || 0}

                        </strong>

                    </div>


                    <div
                        class="summary-row"
                    >

                        <span>

                            Packing

                        </span>


                        <strong>

                            ₹${summary.packing_charges || 0}

                        </strong>

                    </div>


                    <hr>


                    <div
                        class="d-flex justify-content-between fs-5"
                    >

                        <strong>

                            Grand Total

                        </strong>


                        <strong
                            class="text-success"
                        >

                            ₹${summary.grand_total || 0}

                        </strong>

                    </div>


                </div>

            </div>

        </div>


        </div>
        `;


    // ========================================================
    // ADD SPLIT BUTTON
    // ========================================================

    html +=
        `

        <div
            class="text-center mt-4"
        >

            <button

                class="btn btn-primary btn-lg px-5"

                onclick="
                    startSplit(
                        '${data.bill_id}'
                    )
                "

            >

                <i
                    class="bi bi-people"
                ></i>

                Split This Bill

            </button>

        </div>

        `;


    // ========================================================
    // SHOW RESULT
    // ========================================================

    billResult.innerHTML =
        html;


    resultSection.classList.remove(
        "d-none"
    );


    // ========================================================
    // SCROLL TO RESULT
    // ========================================================

    resultSection.scrollIntoView(

        {

            behavior:
                "smooth"

        }

    );

}


// ============================================================
// START SPLIT
// ============================================================

// ============================================================
// START SPLIT
// ============================================================

function startSplit(
    billId
) {


    // ========================================================
    // SAVE BILL ID
    // ========================================================

    currentBillId =
        billId;


    // ========================================================
    // MAKE SURE EDITED DATA IS USED
    // ========================================================

    if (
        currentBillData
    ) {

        currentBillData.bill =
            getEditedBill();

    }


    // ========================================================
    // SAVE CURRENT DATA
    // ========================================================

    window.latestBillData =
        currentBillData;


    // ========================================================
    // RESET MEMBERS
    // ========================================================

    members =
        [];


    membersList.innerHTML =
        "";


    itemAssignmentList.innerHTML =
        "";


    splitResult.innerHTML =
        "";


    // ========================================================
    // SHOW SPLIT SECTION
    // ========================================================

    splitSection
        .classList
        .remove(
            "d-none"
        );


    // ========================================================
    // UPDATE PROGRESS
    // ========================================================

    document
        .getElementById(
            "step2"
        )
        .classList
        .remove(
            "active"
        );


    document
        .getElementById(
            "step3"
        )
        .classList
        .add(
            "active"
        );


    // ========================================================
    // SCROLL
    // ========================================================

    splitSection.scrollIntoView(

        {

            behavior:
                "smooth"

        }

    );


    // ========================================================
    // RENDER
    // ========================================================

    renderMembers();

    renderItemAssignments();

}
// ============================================================
// ENTER KEY
// ============================================================

memberName.addEventListener(

    "keypress",

    function (event) {

        if (

            event.key ===
            "Enter"

        ) {

            addMember();

        }

    }

);


// ============================================================
// ADD MEMBER FUNCTION
// ============================================================

function addMember() {


    const name =
        memberName.value.trim();


    // ========================================================
    // VALIDATE
    // ========================================================

    if (!name) {

        alert(
            "Please enter a member name"
        );

        return;

    }


    // ========================================================
    // DUPLICATE CHECK
    // ========================================================

    if (

        members.includes(
            name
        )

    ) {

        alert(
            "Member already exists"
        );

        return;

    }


    // ========================================================
    // ADD
    // ========================================================

    members.push(
        name
    );


    // ========================================================
    // CLEAR INPUT
    // ========================================================

    memberName.value =
        "";


    // ========================================================
    // RENDER
    // ========================================================

    renderMembers();


    renderItemAssignments();

}
// ============================================================
// RENDER MEMBERS
// ============================================================

function renderMembers() {


    membersList.innerHTML =
        "";


    // ========================================================
    // EMPTY
    // ========================================================

    if (

        members.length ===
        0

    ) {

        membersList.innerHTML =
            `
            <p
                class="text-muted small"
            >

                No members added yet

            </p>
            `;

        return;

    }


    // ========================================================
    // SHOW MEMBERS
    // ========================================================

    members.forEach(

        function (
            member,
            index
        ) {


            membersList.innerHTML +=
                `

                <div
                    class="member-card"
                >

                    <div>

                        <i
                            class="bi bi-person-circle"
                        ></i>

                        ${member}

                    </div>


                    <button

                        class="btn btn-sm btn-outline-danger"

                        onclick="
                            removeMember(
                                ${index}
                            )
                        "

                    >

                        <i
                            class="bi bi-x"
                        ></i>

                    </button>


                </div>

                `;

        }

    );

}
// ============================================================
// REMOVE MEMBER
// ============================================================

function removeMember(index) {


    members.splice(

        index,

        1

    );


    renderMembers();


    renderItemAssignments();

}
// ============================================================
// RENDER ITEM ASSIGNMENTS
// ============================================================

function renderItemAssignments() {


    itemAssignmentList.innerHTML =
        "";


    // ========================================================
    // CHECK BILL
    // ========================================================

    if (

        !currentBillData

    ) {

        return;

    }


    const items =
        currentBillData
        .bill
        .items;


    // ========================================================
    // CHECK MEMBERS
    // ========================================================

    if (

        members.length ===
        0

    ) {

        itemAssignmentList.innerHTML =
            `

            <div
                class="alert alert-info"
            >

                Add members first.

            </div>

            `;

        return;

    }


    // ========================================================
    // SHOW ITEMS
    // ========================================================

    items.forEach(

        function (
            item,
            itemIndex
        ) {


            let memberCheckboxes =
                "";


            members.forEach(

                function (
                    member
                ) {


                    memberCheckboxes +=
                        `

                        <div
                            class="form-check"
                        >

                            <input

                                class="
                                    form-check-input
                                    item-member
                                    item-${itemIndex}
                                "

                                type="checkbox"

                                value="${member}"

                                id="
                                    item-${itemIndex}-${member}
                                "

                            >


                            <label

                                class="form-check-label"

                                for="
                                    item-${itemIndex}-${member}
                                "

                            >

                                ${member}

                            </label>

                        </div>

                        `;

                }

            );


            itemAssignmentList.innerHTML +=
                `

                <div
                    class="assignment-card"
                >


                    <div
                        class="
                            d-flex
                            justify-content-between
                            mb-3
                        "
                    >

                        <strong>

                            ${item.name}

                        </strong>


                        <strong
                            class="text-success"
                        >

                            ₹${item.line_total}

                        </strong>


                    </div>


                    <p
                        class="text-muted small"
                    >

                        Assign to:

                    </p>


                    ${memberCheckboxes}


                </div>

                `;

        }

    );

}
// ============================================================
// CALCULATE SPLIT
// ============================================================

calculateSplitBtn.addEventListener(

    "click",

    async function () {


        // ====================================================
        // VALIDATE MEMBERS
        // ====================================================

        if (

            members.length ===
            0

        ) {

            alert(
                "Please add members"
            );

            return;

        }


        // ====================================================
        // GET ITEMS
        // ====================================================

        const items =
            currentBillData
            .bill
            .items;


        const assignments =
            [];


        // ====================================================
        // LOOP ITEMS
        // ====================================================

        for (

            let index = 0;

            index < items.length;

            index++

        ) {


            const checkboxes =
                document.querySelectorAll(

                    `.item-${index}:checked`

                );


            const assignedMembers =
                Array.from(
                    checkboxes
                ).map(

                    function (
                        checkbox
                    ) {

                        return (
                            checkbox.value
                        );

                    }

                );


            // =================================================
            // VALIDATE ASSIGNMENT
            // =================================================

            if (

                assignedMembers.length ===
                0

            ) {

                alert(

                    `Please assign "${items[index].name}"`

                );

                return;

            }


            assignments.push({

                item_index:
                    index,

                members:
                    assignedMembers

            });

        }


        // ====================================================
        // REQUEST BODY
        // ====================================================

        const requestData =
            {

                members:

                    members.map(

                        function (
                            member
                        ) {

                            return {

                                name:
                                    member

                            };

                        }

                    ),


                assignments:
                    assignments

            };


        // ====================================================
        // DEBUG
        // ====================================================

        console.log(

            "SPLIT REQUEST:",

            requestData

        );


        // ====================================================
        // BUTTON LOADING
        // ====================================================

        calculateSplitBtn.disabled =
            true;


        calculateSplitBtn.innerHTML =
            `
            <span
                class="
                    spinner-border
                    spinner-border-sm
                "
            ></span>

            Calculating...
            `;


        try {


            // =================================================
            // API CALL
            // =================================================

            const response =
                await fetch(

                    `/api/bills/${currentBillId}/split`,

                    {

                        method:
                            "POST",


                        headers: {

                            "Content-Type":
                                "application/json"

                        },


                        body:

                            JSON.stringify(

                                requestData

                            )

                    }

                );


            const data =
                await response.json();


            // =================================================
            // ERROR
            // =================================================

            if (

                !response.ok

            ) {

                throw new Error(

                    data.detail
                    ||
                    "Failed to split bill"

                );

            }


            // =================================================
            // DEBUG
            // =================================================

            console.log(

                "SPLIT RESPONSE:",

                data

            );


            // =================================================
            // DISPLAY
            // =================================================

            displaySplitResult(

                data.split

            );


        }


        catch (
            error
        ) {


            console.error(

                error

            );


            alert(

                error.message

            );

        }


        finally {


            calculateSplitBtn.disabled =
                false;


            calculateSplitBtn.innerHTML =
                `
                <i
                    class="
                        bi bi-calculator
                    "
                ></i>

                Calculate Split
                `;

        }

    }

);
// ============================================================
// DISPLAY SPLIT RESULT
// ============================================================

function displaySplitResult(

    split

) {


    let html =
        `

        <h2
            class="
                fw-bold
                text-center
                mb-4
            "
        >

            Split Result

        </h2>


        <div
            class="row"
        >

        `;


    // ========================================================
    // MEMBERS
    // ========================================================

    Object.entries(

        split.members

    ).forEach(

        function (

            [
                memberName,
                memberData
            ]

        ) {


            html +=
                `

                <div
                    class="
                        col-lg-6
                        mb-4
                    "
                >

                    <div
                        class="
                            card
                            shadow-sm
                            border-0
                            split-card
                        "
                    >

                        <div
                            class="card-body"
                        >


                            <h4
                                class="
                                    fw-bold
                                    mb-4
                                "
                            >

                                <i
                                    class="
                                        bi bi-person-circle
                                    "
                                ></i>

                                ${memberName}

                            </h4>


                            <h6>

                                Items

                            </h6>

                `;


            // =================================================
            // ITEM BREAKDOWN
            // =================================================

            memberData
                .item_breakdown
                .forEach(

                    function (
                        item
                    ) {


                        html +=
                            `

                            <div
                                class="
                                    d-flex
                                    justify-content-between
                                    mb-2
                                "
                            >

                                <span>

                                    ${item.item}

                                </span>


                                <strong>

                                    ₹${item.amount}

                                </strong>

                            </div>

                            `;

                    }

                );


            // =================================================
            // CHARGES
            // =================================================

            html +=
                `

                <hr>


                <h6>

                    Charges

                </h6>


                <div
                    class="
                        d-flex
                        justify-content-between
                    "
                >

                    <span>

                        Packing

                    </span>


                    <span>

                        ₹${memberData.charges.packing_charges}

                    </span>

                </div>


                <div
                    class="
                        d-flex
                        justify-content-between
                    "
                >

                    <span>

                        GST

                    </span>


                    <span>

                        ₹${memberData.charges.gst}

                    </span>

                </div>


                <hr>


                <div
                    class="
                        d-flex
                        justify-content-between
                        fs-4
                    "
                >

                    <strong>

                        Total

                    </strong>


                    <strong
                        class="
                            text-success
                        "
                    >

                        ₹${memberData.final_amount}

                    </strong>

                </div>


                        </div>

                    </div>

                </div>

                `;

        }

    );


    html +=
        `

        </div>

        `;


    // ========================================================
    // SUMMARY
    // ========================================================

    html +=
        `

        <div
            class="
                card
                shadow-sm
                border-0
                mt-3
            "
        >

            <div
                class="card-body"
            >

                <h4
                    class="fw-bold"
                >

                    Final Summary

                </h4>


                <div
                    class="
                        d-flex
                        justify-content-between
                    "
                >

                    <span>

                        Calculated Total

                    </span>


                    <strong>

                        ₹${split.summary.calculated_total}

                    </strong>

                </div>


                <div
                    class="
                        d-flex
                        justify-content-between
                    "
                >

                    <span>

                        Actual Bill Total

                    </span>


                    <strong>

                        ₹${split.summary.actual_grand_total}

                    </strong>

                </div>


            </div>

        </div>

        `;


    // ========================================================
    // DISPLAY
    // ========================================================

    splitResult.innerHTML =
        html;


    splitResult.scrollIntoView(

        {

            behavior:
                "smooth"

        }

    );

}
function displayEditableBill(
    billData,
    billId
) {

    currentBill = billData;

    currentBillId = billId;


    const billSection =
        document.getElementById(
            "billSection"
        );


    const billItemsBody =
        document.getElementById(
            "billItemsBody"
        );


    billSection.style.display =
        "block";


    billItemsBody.innerHTML =
        "";


    billData.items.forEach(

        (
            item,
            index
        ) => {

            const row =
                document.createElement(
                    "tr"
                );


            row.dataset.index =
                index;


            row.innerHTML = `

                <td>

                    <input
                        type="text"
                        class="item-name"
                        value="${item.name || ""}"
                    >

                </td>


                <td>

                    <input
                        type="number"
                        class="item-quantity"
                        value="${item.quantity || 1}"
                        min="1"
                        step="1"
                    >

                </td>


                <td>

                    <input
                        type="number"
                        class="item-price"
                        value="${item.unit_price || 0}"
                        min="0"
                        step="0.01"
                    >

                </td>


                <td>

                    <input
                        type="number"
                        class="item-total"
                        value="${item.line_total || 0}"
                        min="0"
                        step="0.01"
                    >

                </td>


                <td>

                    <button
                        class="delete-item-btn"
                        type="button"
                    >

                        🗑

                    </button>

                </td>

            `;


            billItemsBody.appendChild(
                row
            );

        }

    );


    populateSummary(
        billData.summary
    );

}
function populateSummary(
    summary
) {

    document.getElementById(
        "subtotalInput"
    ).value =
        summary.subtotal || 0;


    document.getElementById(
        "packingChargesInput"
    ).value =
        summary.packing_charges || 0;


    document.getElementById(
        "gstInput"
    ).value =
        summary.gst || 0;


    document.getElementById(
        "taxInput"
    ).value =
        summary.tax || 0;


    document.getElementById(
        "discountInput"
    ).value =
        summary.discount || 0;


    document.getElementById(
        "serviceChargeInput"
    ).value =
        summary.service_charge || 0;


    document.getElementById(
        "grandTotalInput"
    ).value =
        summary.grand_total || 0;

}
document
    .getElementById(
        "addItemBtn"
    )
    .addEventListener(

        "click",

        function () {

            const body =
                document.getElementById(
                    "billItemsBody"
                );


            const row =
                document.createElement(
                    "tr"
                );


            row.innerHTML = `

                <td>

                    <input
                        type="text"
                        class="item-name"
                        placeholder="Item name"
                    >

                </td>


                <td>

                    <input
                        type="number"
                        class="item-quantity"
                        value="1"
                        min="1"
                    >

                </td>


                <td>

                    <input
                        type="number"
                        class="item-price"
                        value="0"
                        min="0"
                        step="0.01"
                    >

                </td>


                <td>

                    <input
                        type="number"
                        class="item-total"
                        value="0"
                        min="0"
                        step="0.01"
                    >

                </td>


                <td>

                    <button
                        class="delete-item-btn"
                        type="button"
                    >

                        🗑

                    </button>

                </td>

            `;


            body.appendChild(
                row
            );

        }

    );
    document
    .getElementById(
        "billItemsBody"
    )
    .addEventListener(

        "click",

        function (
            event
        ) {

            if (

                event.target.classList.contains(
                    "delete-item-btn"
                )

            ) {

                event.target
                    .closest(
                        "tr"
                    )
                    .remove();

            }

        }

    );
    function recalculateBill() {

    const rows =
        document.querySelectorAll(
            "#billItemsBody tr"
        );


    let subtotal =
        0;


    rows.forEach(

        (
            row
        ) => {

            const quantity =
                parseFloat(

                    row.querySelector(
                        ".item-quantity"
                    ).value

                ) || 0;


            const price =
                parseFloat(

                    row.querySelector(
                        ".item-price"
                    ).value

                ) || 0;


            const total =
                quantity * price;


            row.querySelector(
                ".item-total"
            ).value =
                total.toFixed(
                    2
                );


            subtotal +=
                total;

        }

    );


    document.getElementById(
        "subtotalInput"
    ).value =
        subtotal.toFixed(
            2
        );


    const packing =
        parseFloat(

            document.getElementById(
                "packingChargesInput"
            ).value

        ) || 0;


    const gst =
        parseFloat(

            document.getElementById(
                "gstInput"
            ).value

        ) || 0;


    const tax =
        parseFloat(

            document.getElementById(
                "taxInput"
            ).value

        ) || 0;


    const serviceCharge =
        parseFloat(

            document.getElementById(
                "serviceChargeInput"
            ).value

        ) || 0;


    const discount =
        parseFloat(

            document.getElementById(
                "discountInput"
            ).value

        ) || 0;


    const grandTotal =

        subtotal

        + packing

        + gst

        + tax

        + serviceCharge

        - discount;


    document.getElementById(
        "grandTotalInput"
    ).value =
        grandTotal.toFixed(
            2
        );

}
function getEditedBill() {

    const rows =
        document.querySelectorAll(
            "#billItemsBody tr"
        );


    const items =
        [];


    rows.forEach(

        (
            row
        ) => {

            const item = {

                name:

                    row.querySelector(
                        ".item-name"
                    ).value.trim(),


                quantity:

                    parseFloat(

                        row.querySelector(
                            ".item-quantity"
                        ).value

                    ) || 0,


                unit_price:

                    parseFloat(

                        row.querySelector(
                            ".item-price"
                        ).value

                    ) || 0,


                line_total:

                    parseFloat(

                        row.querySelector(
                            ".item-total"
                        ).value

                    ) || 0,


                confidence:

                    1.0,


                needs_review:

                    false

            };


            items.push(
                item
            );

        }

    );


    const summary = {

        subtotal:

            parseFloat(

                document.getElementById(
                    "subtotalInput"
                ).value

            ) || 0,


        packing_charges:

            parseFloat(

                document.getElementById(
                    "packingChargesInput"
                ).value

            ) || 0,


        gst:

            parseFloat(

                document.getElementById(
                    "gstInput"
                ).value

            ) || 0,


        tax:

            parseFloat(

                document.getElementById(
                    "taxInput"
                ).value

            ) || 0,


        discount:

            parseFloat(

                document.getElementById(
                    "discountInput"
                ).value

            ) || 0,


        service_charge:

            parseFloat(

                document.getElementById(
                    "serviceChargeInput"
                ).value

            ) || 0,


        grand_total:

            parseFloat(

                document.getElementById(
                    "grandTotalInput"
                ).value

            ) || 0

    };


    return {

        items:

            items,

        summary:

            summary

    };

}
// ============================================================
// RECALCULATE BUTTON
// ============================================================

document
    .getElementById(
        "recalculateBtn"
    )
    .addEventListener(

        "click",

        function () {

            recalculateBill();

            alert(
                "Bill recalculated successfully"
            );

        }

    );
    // ============================================================
// SAVE EDITED BILL
// ============================================================

function saveEditedBill() {


    // ========================================================
    // CHECK BILL
    // ========================================================

    if (
        !currentBillData
    ) {

        alert(
            "No bill available to save"
        );

        return;

    }


    // ========================================================
    // GET EDITED DATA
    // ========================================================

    const editedBill =
        getEditedBill();


    // ========================================================
    // UPDATE CURRENT BILL
    // ========================================================

    currentBillData.bill =
        editedBill;


    // ========================================================
    // UPDATE WINDOW DATA
    // ========================================================

    window.latestBillData =
        currentBillData;


    // ========================================================
    // UPDATE CURRENT BILL
    // ========================================================

    currentBill =
        editedBill;


    // ========================================================
    // RENDER RESULT AGAIN
    // ========================================================

    displayBillResult(
        currentBillData
    );


    // ========================================================
    // RENDER EDITABLE BILL AGAIN
    // ========================================================

    displayEditableBill(

        editedBill,

        currentBillId
    );


    // ========================================================
    // UPDATE PROGRESS
    // ========================================================

    document
        .getElementById(
            "step2"
        )
        .classList
        .add(
            "active"
        );


    alert(
        "Bill changes saved successfully!"
    );


    console.log(
        "UPDATED BILL:",
        currentBillData
    );

}
// ============================================================
// TOP SAVE BUTTON
// ============================================================

document
    .getElementById(
        "saveBillBtn"
    )
    .addEventListener(

        "click",

        function () {

            saveEditedBill();

        }

    );



// ============================================================
// BOTTOM SAVE BUTTON
// ============================================================

document
    .getElementById(
        "saveBillBtnBottom"
    )
    .addEventListener(

        "click",

        function () {

            saveEditedBill();

        }

    );
// ============================================================
// AUTO RECALCULATE ITEM TOTAL
// ============================================================

document
    .getElementById(
        "billItemsBody"
    )
    .addEventListener(

        "input",

        function (
            event
        ) {

            if (

                event.target.classList.contains(
                    "item-quantity"
                )

                ||

                event.target.classList.contains(
                    "item-price"
                )

            ) {

                const row =
                    event.target.closest(
                        "tr"
                    );


                const quantity =

                    parseFloat(

                        row
                        .querySelector(
                            ".item-quantity"
                        )
                        .value

                    )

                    ||

                    0;


                const price =

                    parseFloat(

                        row
                        .querySelector(
                            ".item-price"
                        )
                        .value

                    )

                    ||

                    0;


                const total =

                    quantity
                    *
                    price;


                row
                    .querySelector(
                        ".item-total"
                    )
                    .value =

                    total.toFixed(
                        2
                    );

            }

        }

    );