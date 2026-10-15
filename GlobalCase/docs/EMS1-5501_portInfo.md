# EMS1-5501 portInfo

## Objective

Verify that the Inventory / Port export file is non-empty, newly downloaded, and consistent with the table displayed by EMS.

## Comparison Rules

- Compare matching columns and rows between the Inventory Port table and the exported file.
- Treat `null`, `--`, and an empty value as equivalent.
- Remove invisible zero-width formatting characters (`U+200B`, `U+200C`, `U+200D`, and `U+FEFF`) before comparison. For example, an exported `U+200B + null` is equivalent to an empty value displayed by EMS.
- Preserve the existing Slot/Port zero equivalence and live optical-value tolerance rules provided by the shared export comparison helper.

## Expected Result

The export is accepted when its only difference is an invisible formatting character before an otherwise equivalent empty value. Actual non-empty data differences still fail the Case.
