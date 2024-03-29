Nwokorobia Ugochukwu Franklin 
Uhexos@gmail.com 

Technology: Django and Django rest framework(python) 
Sqlite for testing and postgres in prod for database tasks. 

# decagon

Setup
--------------------------------------------------------
CD to top level directory and in the console enter 
```
sudo docker-compose up
```
This will install the application. The application uses a preseeded sqlite db for easy testing in a dev environment. Each account contains the appropriate wallet and profile aalready attached. New user may be created with the register endpoint. However access will be restricted till they create a profile and pick a main currency. Default 
role is a NOOB account.
The ideal choice for a db would be postgres

To fund or withdraw from a wallet visit the appropriate endpoint. Using the id for the transaction visit the aapproporiate approval endpoint. the transaction must be approved before the values are subtracted from the wallet.

Available Users
---------------------------------
role | username|password
------|--------|-------|
super-user| super | password|
admin   |    admin |01234Admin
noob|   noob| 01234Noob
elite|elite| 01234Elite

All wallets are funded in NGN but can recieve all currencies.
To view all available currencies consult the currency list endpoint

**All endpoints exccept register require a token to access.
Signup using the REGISTER endpoint**

Get token form LOGIN endpoint 
attach to header an Authorization field with value Token token_number
eg 
```
Authorization: Token 96fb778e3a9b6db04740fa36a7894bf28ef364ab
```
Available EndPoints
--------------------------------------- 
1)
Post auth/users/ register 

Required data
---------------
- username
- email
- password
- re_password

2)
Post /auth/token/login/  login
Required data and example input
-------------------------------
- username: admin
- password: password

3)
Post /auth/token/logout/ logout

4)
Get /currency/  currency-list

5)
Post /profile/  profile-create
- Required data and example input
-------------------------------
currency:NGN
role:EL

6)
Put/Patch /profile/\<id\>/  profile-update
Required data and example input
-------------------------------
- currency:EUR
- role:NB
- id:9

7)
Post /wallet/   wallet-create
Required data and example input
-------------------------------
- currency:AED

8)
Post /wallet/fund/ wallet-fund
Required data and example input
-------------------------------
- currency:USD
- amount: 100
- to_wallet: 1

9)
Post /wallet/approve_funding    wallet-approve-funding
Required data and example input
-------------------------------
- fund_id:2

10)
Post /wallet/withdrawal/   wallet-withdrawal
Required data and example input
-------------------------------
- currency:ALL #can be any 3 character currency code
- amount: 450000
- from_wallet: 1
- user: 2

11)
POST /wallet/approve_withdrawal/    wallet-approve-withdrawal
Required data and example input
-------------------------------
- withdrawal_id:4
