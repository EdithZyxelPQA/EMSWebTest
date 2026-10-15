# EMS1-6699 devXontInfoInventoryAllOnt

## Unregistered ONT 空值比對

Inventory / ONT 顯示 Unregistered ONT 時，下列沒有資料的欄位允許使用空字串或 `--` 表示：

- Model
- Version A
- Version B
- Description
- Template Name

其餘狀態、識別資料與 Restful devinfo 的驗證邏輯維持不變。
