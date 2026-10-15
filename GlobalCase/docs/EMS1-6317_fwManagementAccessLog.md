# EMS1-6317 fwManagementAccessLog

## Objective

Verify that uploading and then deleting a firmware file through Maintenance / Firmware File Management creates the correct Access Log entries with the actual uploaded filename.

## Test Data

- EMS URL/account: from `environment_parameter.json`
- Firmware directory: `AUTO_SITE.upload_path` (`ForUpload`)
- NeoX device upload file: `NXC`
- IES device upload file: `MSC`
- OLT140X device upload file: `Image`

## Steps

1. Go to `Maintenance / Firmware File Management`.
2. Immediately click the Add icon without searching the table or checking whether the firmware already exists.
3. Select `NXC`, `MSC`, or `Image` from `ForUpload`, according to the DUT type.
4. Record the upload time and submit the upload regardless of existing table contents. Wait up to 600 seconds for either the `Upload Success` alert or the upload window to close automatically, then return to the main window.
5. After confirmed upload completion, search the Firmware File Management table by its `time` column across the sorted pages. Select the newest row whose time is between upload start and one minute after confirmed completion, and record the `name` from that same row. If no row matches the upload time, stop immediately.
6. Go to `System / Security / Access Log` and open Filter.
7. Set Date From to one minute before the upload time and Date To to one minute after upload completion.
8. Click Query.
9. Use the filename already recorded from Firmware File Management to verify the complete upload success description:
    `[Maintenance - firmware file management] new success (filename [<uploaded filename>])`
10. Return to `Maintenance / Firmware File Management`.
11. Select the uploaded firmware row, record the delete time and filename, and click Delete.
12. Go directly to `System / Security / Access Log`; this page does not always display a `message_text` modal after Delete.
13. Open Filter and set Date From to one minute before the delete time and Date To to one minute after deletion.
14. Click Query.
15. Verify an entry exists with the exact description:
    `[Maintenance - firmware file management] delete success (filename [<uploaded filename>])`

## Expected Result

- The selected firmware file uploads successfully and appears in Firmware File Management.
- The Case does not close the upload popup while the large firmware transfer is running. It accepts either the `Upload Success` alert or EMS automatically closing the upload popup, then verifies the resulting table row and Access Log.
- The Add icon is clicked immediately; existing firmware table pages are not searched before upload.
- The Case does not assume the first table row is the upload because the table can be sorted.
- The expected filename comes from the Firmware File Management row matching the recorded upload time, never from parsing the Access Log.
- If no table row falls within the upload-time range, the Case stops before Access Log verification or deletion.
- The Access Log contains the firmware upload success entry within the recorded time range.
- The filename inside the Access Log exactly matches the filename displayed in Firmware File Management.
- The uploaded firmware matching the filename recorded from the Firmware File Management table can be selected and deleted successfully.
- The Access Log contains the firmware deletion success entry within the recorded delete-time range.
- The filename in the delete entry exactly matches the same filename recorded after upload.
