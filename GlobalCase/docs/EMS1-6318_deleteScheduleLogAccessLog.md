# EMS1-6318 Delete Schedule Log Access Log

## Purpose

Verify that deleting a Maintenance Result Log creates the corresponding System Access Log with the deleted schedule Log ID.

## Marker

`@pytest.mark.Unicase`

## Steps

1. Open **Maintenance / Result Log** (or **Result**, depending on the EMS label).
2. Read and record the Log ID from the first row.
3. Select the first row and record the deletion time.
4. Click the **Delete** icon.
5. Verify the message is `Delete success.` and click **OK**.
6. Open **System / Security / Access Log**.
7. Open **Filter** and reset existing conditions.
8. Set Date From to one minute before the deletion and Date To to one minute after opening Access Log.
9. Click **Query** and wait up to 60 seconds, refreshing while necessary.

## Expected result

The filtered Access Log contains this exact Description, using the Log ID recorded before deletion:

```text
[Maintenance - result log] delete success (schedule log ID : <Log ID>)
```
