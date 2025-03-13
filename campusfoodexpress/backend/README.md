# Backend

## Installation of Code Style Checker
The following commands will install the pre-commit hook that runs the code style checker before each commit.
Your commit will be rejected if the code style checker fails.
```bash
pip install pre-commit
pre-commit install
```

## 订单状态 order.state
- 订单已创建: Created
- 订单已接单: Shipped
- 订单已完成: Completed
- 订单已取消: Deleted

### 系统消息状态 SystemNotification.state
- 用户被禁: User Ban
- 实名认证: Real-Name Authentication
- 举报处理: Report Handling
- 系统广播: System Broadcast
- 其他: Others

### 订单通知 OrderNotification.state
- 订单创建：Order Created
- 订单配送：Order Shipped
- 订单完成：Order Completed
- 订单取消：Order Cancelled
- 订单删除：Order Deleted