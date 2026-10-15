# EMS1-5487 node

## 測試前置清理

進入 System / Security / Map Management 後，先檢查是否存在下列前次測試可能殘留的 node：

- `255.255.255.255`
- `1.2.3.4`

若存在，先選取該 node，進入 Edit 並執行 Delete。確認顯示 `Operation Success`，且訊息視窗完全關閉後，才繼續原本的 Add／Modify／Delete node 測試流程。
