import uuid
from typing import Dict, Optional


class BillStore:

    def __init__(self):

        self.bills: Dict[str, Dict] = {}


    # ========================================================
    # SAVE BILL
    # ========================================================

    def save_bill(
        self,
        bill_data: Dict
    ) -> str:

        bill_id = str(
            uuid.uuid4()
        )


        self.bills[
            bill_id
        ] = bill_data


        return bill_id


    # ========================================================
    # GET BILL
    # ========================================================

    def get_bill(
        self,
        bill_id: str
    ) -> Optional[Dict]:

        return self.bills.get(
            bill_id
        )


    # ========================================================
    # UPDATE BILL
    # ========================================================

    def update_bill(
        self,
        bill_id: str,
        data: Dict
    ) -> bool:

        if bill_id not in self.bills:

            return False


        self.bills[
            bill_id
        ].update(
            data
        )


        return True


    # ========================================================
    # DELETE BILL
    # ========================================================

    def delete_bill(
        self,
        bill_id: str
    ) -> bool:

        if bill_id not in self.bills:

            return False


        del self.bills[
            bill_id
        ]


        return True


# ========================================================
# CREATE SINGLE STORE INSTANCE
# ========================================================

bill_store = BillStore()