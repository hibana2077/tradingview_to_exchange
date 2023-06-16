<!--
 * @Author: hibana2077 hibana2077@gmaill.com
 * @Date: 2023-04-19 10:25:11
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-04-24 20:13:20
 * @FilePath: /tradingview_to_exchange/doc/data.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->

這是一個自動交易機器人的資料庫設計

## data sheet

- [ ] Orders
- [ ] Users
- [ ] Account

## data sheet columns

### Orders

- [ ] Order ID
- [ ] User ID
- [ ] Order Time
- [ ] Order Status
- [ ] Order Details

### Users

- [ ] User ID
- [ ] User Name
- [ ] User Email
- [ ] User Password
- [ ] User Details

### Profile

- [ ] User ID
- [ ] Profile Details

### Account (api settings)

- [ ] User ID
- [ ] Account Details

### Logs

- [ ] Log ID
- [ ] User ID
- [ ] Log Time
- [ ] Log Details

### Trade

- [ ] Trade ID
- [ ] User ID
- [ ] Trade Time
- [ ] Trade Symbol
- [ ] Trade Details

### Assets

- [ ] User ID
- [ ] Asset Details

```py
my_col = my_db["orders"]
my_col.create_index("order_id", unique=True)
my_col = my_db["profiles"]
my_col.create_index("user_id", unique=True)
my_col = my_db["api_setting"]
my_col.create_index("user_id", unique=True)
```
根據以上的設計,把python code補完