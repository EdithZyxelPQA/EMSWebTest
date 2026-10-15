# EMS1-4507_4510 ontInfo

## Export 資料比對

- Inventory / ONT 畫面資料必須能在匯出檔中找到對應資料。
- 匯出內容中的零寬字元會先移除，再進行比對。
- `null`、`--` 與空白視為相同內容。
- Slot、Port、ONT ID 的空白與 `0` 視為相同內容。
- Tx Power、Rx Power、Optical Power 為即時光功率，畫面擷取到匯出完成期間允許 `0.3 dB` 的數值差異。
- 其他固定欄位仍須完全相符。
