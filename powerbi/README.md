# Vendor Performance Dashboard

## Goal

Build an executive Power BI report for sales, procurement, inventory, and vendor performance using the CSV files in `data/`.

The source contains about 12.8M sales rows and 2.37M purchase rows. Use 64-bit Power BI Desktop and load the CSVs with Power Query. Disable load for staging queries and prefer a star schema over one large merged table.

## Data preparation

Create a text parameter named `DataFolder` that points to the project's `data` folder. Import each CSV, then apply these rules:

- Trim and clean `VendorName`, `Description`, `City`, and `Size`.
- Set IDs (`InventoryId`, `Brand`, `VendorNumber`, `VendorNo`, `PONumber`, `Store`) to consistent types.
- Rename `sales[VendorNo]` to `VendorNumber`.
- Parse all date fields as Date using locale `English (United States)`.
- Set quantities to Whole Number and money/tax/freight/price fields to Decimal Number.
- Remove exact duplicate rows, but do not deduplicate legitimate daily sales.
- Replace blank `Approval` with `"Unknown"`.
- Add `InventoryValue = onHand * Price` to both inventory tables.

For performance, keep only necessary columns, turn off Auto date/time, and use incremental refresh on `sales[SalesDate]` if the report will be published to a supported Power BI capacity.

## Model

Create these dimensions:

- `DimDate`: one row per day from the minimum transactional date to the maximum date.
- `DimVendor`: distinct `VendorNumber` and trimmed `VendorName`, preferably sourced from `purchase_prices`.
- `DimProduct`: distinct `Brand`, `Description`, `Size`, `Volume`, and `Classification`, sourced from `purchase_prices`.
- `DimStore`: distinct `Store` and `City`, sourced from the union of opening and closing inventory.

Use single-direction, one-to-many relationships:

| Dimension | Key | Fact table | Foreign key |
|---|---|---|---|
| DimDate | Date | sales | SalesDate |
| DimDate | Date | purchases | ReceivingDate |
| DimDate | Date | vendor_invoice | InvoiceDate |
| DimVendor | VendorNumber | sales | VendorNumber |
| DimVendor | VendorNumber | purchases | VendorNumber |
| DimVendor | VendorNumber | vendor_invoice | VendorNumber |
| DimProduct | Brand | sales | Brand |
| DimProduct | Brand | purchases | Brand |
| DimProduct | Brand | begin_inventory | Brand |
| DimProduct | Brand | end_inventory | Brand |
| DimStore | Store | sales | Store |
| DimStore | Store | purchases | Store |
| DimStore | Store | begin_inventory | Store |
| DimStore | Store | end_inventory | Store |

Do not relate facts directly to one another. Mark `DimDate` as the date table. If `Brand` is not unique in `purchase_prices`, build `DimProduct` by grouping on `Brand` and investigate conflicting descriptions rather than creating a many-to-many relationship.

## Report pages

### 1. Executive overview

- KPI cards: Net Sales, Gross Profit Proxy, Profit Margin Proxy, Sales Units, Closing Inventory Value, Vendor Count.
- Combo chart: Net Sales and Gross Profit Proxy by month.
- Bar chart: Top 10 vendors by Net Sales.
- Waterfall: Sales → Purchase Spend → Freight → Excise Tax → Gross Profit Proxy.
- Slicers: Date, Vendor, Store/City, Classification.

### 2. Vendor performance

- Scatter chart: Purchase Spend vs Net Sales; bubble size = Sales Units; color = Profit Margin Proxy.
- Matrix: Vendor, Net Sales, Purchase Spend, Gross Profit Proxy, Margin, Stock Turnover Proxy, Freight Rate, Payment Days.
- Pareto chart: Purchase Contribution % and cumulative contribution by vendor.
- Conditional formatting for negative gross profit, low turnover, and high freight rate.

The notebook found that the top 10 vendors represent **65.69% of purchasing**, so procurement concentration should be a prominent callout.

### 3. Product and sales

- Sales trend by month.
- Top/bottom products by Net Sales and Gross Profit Proxy.
- Decomposition tree: Net Sales → Classification → Vendor → Brand → Store.
- Matrix with Brand, Description, Sales Units, Net Sales, Average Selling Price, and Margin.

### 4. Inventory

- KPI cards: Opening Inventory Value, Closing Inventory Value, Inventory Value Change, Sell-through Proxy.
- Bar chart: Closing inventory value by store/city.
- Table: slow-moving brands where Stock Turnover Proxy < 1.
- Scatter: Closing Units vs Sales Units by brand.

### 5. Procurement and invoices

- KPI cards: Purchase Spend, Freight Cost, Freight Rate, Average Payment Days, PO Count.
- Trend: purchases and freight by month.
- Vendor matrix: PO Count, Purchase Units, Purchase Spend, Freight, Freight Rate, Payment Days.
- Table of unusually high freight-rate invoices.

## Important interpretation note

`Gross Profit Proxy` follows the notebook definition: sales minus purchases, freight, excise tax. Purchases are not accounting COGS, so this is a management proxy—not audited gross profit. The same applies to `Stock Turnover Proxy`, which uses purchased units as the denominator. Rename these measures only if a reliable COGS or average-inventory method is introduced.

## Build order

1. Load and clean the six CSV queries.
2. Create the four dimensions and relationships.
3. Add the measures from `measures.dax`.
4. Validate totals against the notebooks.
5. Build the five pages and apply slicer synchronization.
6. Check that selecting a vendor filters sales, purchases, and invoices consistently.

