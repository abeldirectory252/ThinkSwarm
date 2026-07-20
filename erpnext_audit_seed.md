# ERPNext Financial Audit - Reality Seed Materials

## 1. Context & Scope
* **Company Name**: Apex Global Technologies Ltd.
* **Fiscal Year**: 2025 - 2026
* **Reporting Currency**: USD (with secondary multi-currency support in EUR, CAD)
* **Accounting Standards**: IFRS Compliant

## 2. ERPNext DocTypes Schema Mapping
The audit agent will simulate scanning the following core ERPNext DocTypes for transaction verification:

### DocType: General Ledger (GL Entry)
Represents all postings made to accounts.
* `account`: The ledger account modified.
* `debit`: Debit amount in company currency.
* `credit`: Credit amount in company currency.
* `voucher_type`: Document type triggering the entry (e.g., Sales Invoice, Journal Entry).
* `voucher_no`: Reference ID of the source document.
* `posting_date`: The official transaction date.
* `is_cancelled`: Boolean indicator of voided transactions.

### DocType: Sales Invoice
Represents invoices sent to customers.
* `name`: Invoice ID.
* `customer`: Customer profile ID.
* `grand_total`: Total billable amount.
* `outstanding_amount`: Unpaid balance.
* `status`: Current state (Paid, Unpaid, Overdue, Cancelled).
* `update_stock`: Indicator if inventory stock ledger was directly impacted.

### DocType: Purchase Invoice
Represents invoices received from suppliers.
* `name`: Invoice ID.
* `supplier`: Supplier profile ID.
* `grand_total`: Total payable amount.
* `outstanding_amount`: Unpaid balance.
* `status`: Current state (Paid, Unpaid, Overdue, Cancelled).

### DocType: Journal Entry
Manual adjustive entries made by accounting personnel.
* `voucher_type`: E.g., Debit Note, Credit Note, Journal Entry.
* `user_remark`: Narrative explanations for manual postings.
* `accounts`: List of account debits/credits mapping.

## 3. Financial Auditor Inspection & Risk Classification Rules
To detect anomalies, the auditor agent must analyze transactions against the following risk guidelines:

| Risk Category | Rule Description | Detection Threshold | Action required |
|---|---|---|---|
| **Stock Ledger Discrepancy** | Sales Invoice has `update_stock` checked but no corresponding Stock Ledger entry exists. | Discrepancy > 0 | Flag for inventory audit. |
| **Manual Adjustments** | Large Journal Entries posted directly to Cash or Revenue accounts without a reference Purchase/Sales Invoice. | Transaction > $10,000 USD | Flag for authorization review. |
| **Three-Way Match Failure** | Difference between Purchase Order amount, Purchase Receipt quantities, and Purchase Invoice total. | Variance > 1% | Flag for supply chain audit. |
| **Duplicate Vouchers** | Invoices from the same Supplier with matching amounts and dates posted within 24 hours. | Identical match | Flag for potential double payment. |
| **Out-of-Hours Postings** | Transactions posted outside standard operating business hours (e.g., weekends, midnight). | 10 PM - 6 AM / Weekends | Flag for security review. |

## 4. Accounts Reference List
* **Asset L01**: Bank & Cash Accounts (`1110.01` - `1110.99`)
* **Revenue L02**: Direct Product Sales (`4110.01`), Service Contracts (`4120.01`)
* **Liability L03**: Accounts Payable (`2110.01`)
* **Expense L04**: Cost of Goods Sold (`5110.01`), Operations (`5120.01`)
