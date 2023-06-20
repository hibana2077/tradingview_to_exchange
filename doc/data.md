# Database Design for Auto-Trading Bot

## Data Sheets

1. Orders
2. Users
3. Profile
4. Account
5. Logs
6. Assets

## Data Sheet Columns and API Functions

### Orders

- [X] Done

#### Columns

- Order ID
- User ID
- Order Time
- Order Status
- Order Details

#### API Functions

- `recordFailedOrder`: Record a failed trading order.
- `recordSuccessOrder`: Record a successful trading order.
- `getOrder`: Get the details of a specific order.
- `getUserOrders`: Get all orders of a specific user.

### Users

- [X] Done

#### Columns

- User ID
- User Name
- User Email
- User Password
- User Details
    - JWT token
    - Token Expiry Time

#### API Functions

- `createUser`: Create a new user.
- `getUser`: Get the details of a specific user.
- `updateUser`: Update the details of a user.
- `deleteUser`: Delete a user.

### Profile

- [X] Done

#### Columns

- User ID
- Profile Details

#### API Functions

- `getProfile`: Get the profile of a specific user.
- `updateProfile`: Update the profile of a user.
- `createProfile`: Create a profile for a user.
- `deleteProfile`: Delete the profile of a user.

### Account (API Settings)

- [X] Done

#### Columns

- User ID
- Account Details

#### API Functions

- `getAccountDetails`: Get the API settings of a user.
- `updateAccountDetails`: Update the API settings of a user.
- `createAccountDetails`: Create the API settings of a user.
- `deleteAccountDetails`: Delete the API settings of a user.

### Logs

- [X] Done

#### Columns

- Log ID
- User ID
- Log Time
- Log Details

#### API Functions

- `createLog`: Record a specific event.
- `getLog`: Get the details of a specific log.
- `getUserLogs`: Get all logs of a specific user.

### Assets

- [X] Done

#### Columns

- User ID
- Asset Details

#### API Functions

- `getAssets`: Get the asset details of a user.
- `updateAssets`: Update the assets of a user.
- `createAssets`: Create the assets of a user.
- `deleteAssets`: Delete the assets of a user.

