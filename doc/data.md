<!--
 * @Author: hibana2077 hibana2077@gmaill.com
 * @Date: 2023-04-19 10:25:11
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-04-24 20:13:20
 * @FilePath: /tradingview_to_exchange/doc/data.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# PPT

## data sheet

- [ ] Orders
- [ ] Users
- [ ] Account

## data sheet columns

### Orders

- [ ] Order Owner
- [ ] Order ID
- [ ] Order Time
- [ ] Order Status
- [ ] Order Details

### Users

- [ ] User ID
- [ ] User Name
- [ ] User Email
- [ ] User Password
- [ ] User Details

### Account

- [ ] Account User_ID
- [ ] Account Details

## data sheet relations

- Orders.Owner = Users.ID = Account.User_ID
