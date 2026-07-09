# Power Query Templates

Use these in Power BI Desktop after importing each CSV with **Transform Data**. They are meant as starter templates, so adjust the `Source` step if your import step name differs.

## sales

```powerquery
let
    Source = Csv.Document(File.Contents(DataFolder & "\sales.csv"), [Delimiter=",", Columns=14, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    RenamedColumns = Table.RenameColumns(PromotedHeaders, {{"VendorNo", "VendorNumber"}}),
    CleanText = Table.TransformColumns(
        RenamedColumns,
        {
            {"VendorName", each Text.Trim(Text.Clean(_)), type text},
            {"Description", each Text.Trim(Text.Clean(_)), type text},
            {"Size", each Text.Trim(Text.Clean(_)), type text}
        }
    ),
    ChangedTypes = Table.TransformColumnTypes(
        CleanText,
        {
            {"InventoryId", type text},
            {"Store", Int64.Type},
            {"Brand", Int64.Type},
            {"Description", type text},
            {"Size", type text},
            {"SalesQuantity", Int64.Type},
            {"SalesDollars", type number},
            {"SalesPrice", type number},
            {"SalesDate", type date},
            {"Volume", Int64.Type},
            {"Classification", Int64.Type},
            {"ExciseTax", type number},
            {"VendorNumber", Int64.Type},
            {"VendorName", type text}
        }
    ),
    RemovedDuplicates = Table.Distinct(ChangedTypes)
in
    RemovedDuplicates
```

## purchases

```powerquery
let
    Source = Csv.Document(File.Contents(DataFolder & "\purchases.csv"), [Delimiter=",", Columns=16, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    CleanText = Table.TransformColumns(
        PromotedHeaders,
        {
            {"VendorName", each Text.Trim(Text.Clean(_)), type text},
            {"Description", each Text.Trim(Text.Clean(_)), type text},
            {"Size", each Text.Trim(Text.Clean(_)), type text}
        }
    ),
    ChangedTypes = Table.TransformColumnTypes(
        CleanText,
        {
            {"InventoryId", type text},
            {"Store", Int64.Type},
            {"Brand", Int64.Type},
            {"Description", type text},
            {"Size", type text},
            {"VendorNumber", Int64.Type},
            {"VendorName", type text},
            {"PONumber", Int64.Type},
            {"PODate", type date},
            {"ReceivingDate", type date},
            {"InvoiceDate", type date},
            {"PayDate", type date},
            {"PurchasePrice", type number},
            {"Quantity", Int64.Type},
            {"Dollars", type number},
            {"Classification", Int64.Type}
        }
    ),
    RemovedDuplicates = Table.Distinct(ChangedTypes)
in
    RemovedDuplicates
```

## vendor_invoice

```powerquery
let
    Source = Csv.Document(File.Contents(DataFolder & "\vendor_invoice.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    CleanText = Table.TransformColumns(
        PromotedHeaders,
        {
            {"VendorName", each Text.Trim(Text.Clean(_)), type text},
            {"Approval", each if _ = null or Text.Trim(_) = "" then "Unknown" else Text.Trim(Text.Clean(_)), type text}
        }
    ),
    ChangedTypes = Table.TransformColumnTypes(
        CleanText,
        {
            {"VendorNumber", Int64.Type},
            {"VendorName", type text},
            {"InvoiceDate", type date},
            {"PONumber", Int64.Type},
            {"PODate", type date},
            {"PayDate", type date},
            {"Quantity", Int64.Type},
            {"Dollars", type number},
            {"Freight", type number},
            {"Approval", type text}
        }
    ),
    RemovedDuplicates = Table.Distinct(ChangedTypes)
in
    RemovedDuplicates
```

## begin_inventory

```powerquery
let
    Source = Csv.Document(File.Contents(DataFolder & "\begin_inventory.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    CleanText = Table.TransformColumns(
        PromotedHeaders,
        {
            {"City", each Text.Trim(Text.Clean(_)), type text},
            {"Description", each Text.Trim(Text.Clean(_)), type text},
            {"Size", each Text.Trim(Text.Clean(_)), type text}
        }
    ),
    ChangedTypes = Table.TransformColumnTypes(
        CleanText,
        {
            {"InventoryId", type text},
            {"Store", Int64.Type},
            {"City", type text},
            {"Brand", Int64.Type},
            {"Description", type text},
            {"Size", type text},
            {"onHand", Int64.Type},
            {"Price", type number},
            {"startDate", type date}
        }
    ),
    AddedInventoryValue = Table.AddColumn(ChangedTypes, "InventoryValue", each [onHand] * [Price], type number),
    RemovedDuplicates = Table.Distinct(AddedInventoryValue)
in
    RemovedDuplicates
```

## end_inventory

```powerquery
let
    Source = Csv.Document(File.Contents(DataFolder & "\end_inventory.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    CleanText = Table.TransformColumns(
        PromotedHeaders,
        {
            {"City", each Text.Trim(Text.Clean(_)), type text},
            {"Description", each Text.Trim(Text.Clean(_)), type text},
            {"Size", each Text.Trim(Text.Clean(_)), type text}
        }
    ),
    ChangedTypes = Table.TransformColumnTypes(
        CleanText,
        {
            {"InventoryId", type text},
            {"Store", Int64.Type},
            {"City", type text},
            {"Brand", Int64.Type},
            {"Description", type text},
            {"Size", type text},
            {"onHand", Int64.Type},
            {"Price", type number},
            {"endDate", type date}
        }
    ),
    AddedInventoryValue = Table.AddColumn(ChangedTypes, "InventoryValue", each [onHand] * [Price], type number),
    RemovedDuplicates = Table.Distinct(AddedInventoryValue)
in
    RemovedDuplicates
```

## purchase_prices

```powerquery
let
    Source = Csv.Document(File.Contents(DataFolder & "\purchase_prices.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    CleanText = Table.TransformColumns(
        PromotedHeaders,
        {
            {"VendorName", each Text.Trim(Text.Clean(_)), type text},
            {"Description", each Text.Trim(Text.Clean(_)), type text},
            {"Size", each Text.Trim(Text.Clean(_)), type text}
        }
    ),
    ChangedTypes = Table.TransformColumnTypes(
        CleanText,
        {
            {"Brand", Int64.Type},
            {"Description", type text},
            {"Price", type number},
            {"Size", type text},
            {"Volume", Int64.Type},
            {"Classification", Int64.Type},
            {"PurchasePrice", type number},
            {"VendorNumber", Int64.Type},
            {"VendorName", type text}
        }
    ),
    RemovedDuplicates = Table.Distinct(ChangedTypes)
in
    RemovedDuplicates
```

## DimVendor

Create this as a **Reference** query from `purchase_prices`.

```powerquery
let
    Source = purchase_prices,
    KeepColumns = Table.SelectColumns(Source, {"VendorNumber", "VendorName"}),
    RemovedDuplicates = Table.Distinct(KeepColumns)
in
    RemovedDuplicates
```

## DimProduct

Create this as a **Reference** query from `purchase_prices`.

```powerquery
let
    Source = purchase_prices,
    KeepColumns = Table.SelectColumns(Source, {"Brand", "Description", "Size", "Volume", "Classification"}),
    RemovedDuplicates = Table.Distinct(KeepColumns)
in
    RemovedDuplicates
```

## DimStore

Create this by appending references from both inventory tables.

```powerquery
let
    BeginStore = Table.SelectColumns(begin_inventory, {"Store", "City"}),
    EndStore = Table.SelectColumns(end_inventory, {"Store", "City"}),
    Combined = Table.Combine({BeginStore, EndStore}),
    RemovedDuplicates = Table.Distinct(Combined)
in
    RemovedDuplicates
```
