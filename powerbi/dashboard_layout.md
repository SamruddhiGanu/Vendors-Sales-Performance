# Dashboard Layout Based On Your Reference

Yes, your Power BI page can look very close to the screenshot. Use this as the layout recipe for the first report page.

## Page setup

- Canvas: 16:9
- Background: very light blue-gray
- Page title: `Vendor Performance Dashboard`
- Top-right slicers: Date, Vendor, City, Classification

## Row 1: KPI cards

Place 5 cards across the top:

1. `Net Sales`
2. `Purchase Spend`
3. `Gross Profit Proxy`
4. `Profit Margin Proxy`
5. `Closing Inventory Value`

Formatting:

- Rounded corners
- White background
- Soft shadow
- Accent border
- Large value text
- Small subtitle text

## Row 2 left: donut chart

- Visual: Donut
- Title: `Purchase Contribution %`
- Legend: top 5 vendors by purchase spend
- Value: `Purchase Spend`
- Detail: `VendorName`
- Center card value: `Top 10 Vendor Purchase Share`

This is where your notebook insight `65.69%` should appear.

## Row 2 center: top vendors

- Visual: Clustered bar chart
- Title: `Top Vendors By Sales`
- Axis: `DimVendor[VendorName]`
- Value: `Net Sales`
- Visual filter: Top N = 10 by `Net Sales`

## Row 2 right: top brands

- Visual: Clustered bar chart
- Title: `Top Brands By Sales`
- Axis: `DimProduct[Description]`
- Value: `Net Sales`
- Visual filter: Top N = 10 by `Net Sales`

## Row 3 left: low performing vendors

- Visual: Bar chart or table with data bars
- Title: `Low Performing Vendors`
- Fields:
  - `DimVendor[VendorName]`
  - `Gross Profit Proxy`
  - `Profit Margin Proxy`
- Filter: show bottom 5 or bottom 10 by `Gross Profit Proxy`

Use red conditional formatting for negative values.

## Row 3 right: vendor performance scatter

- Visual: Scatter chart
- Title: `Vendor Performance`
- X-axis: `Purchase Spend`
- Y-axis: `Net Sales`
- Size: `Sales Units`
- Legend or color saturation: `Profit Margin Proxy`
- Details: `DimVendor[VendorName]`

This is a better business version of the scatter in your screenshot because it compares spend vs return directly.

## Design notes

- Keep card labels short and consistent.
- Use `Gross Profit Proxy` instead of `Gross Profit` to avoid overstating accounting accuracy.
- Turn on data labels only where they stay readable.
- Sort all Top N visuals descending.
- Add report-page tooltips for vendor name, sales, purchase spend, margin, freight, and payment days.

## Best visual order for your project

If you want the report to feel polished, build pages in this order:

1. Executive Overview
2. Vendor Performance
3. Inventory
4. Procurement and Invoices
5. Product and Sales
