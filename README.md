# surakcha

Steps to create the project
## install postgres
## install redis
## git clone
## cd surakcha
## create virtualenv and activate it
## pip install -r requirement.txt
## create suraksha db in postgres with user you can change in settings
## python manage.py migrate
## python manage.py runserver

### voila!!!!

API to care about

## login api POST
POST
http://{YOUR_IP}/api/authn/login/

{
	"mobile": 8441000947,
	"name": "Aman"
}


repsonse: 
{'success': "OTP has been sent", 'existing_user': false}


## Resend otp api POST
POST
http://{YOUR_IP}/api/authn/resend_otp/

{
	"mobile": 8441000947,
	"name": "Aman"
}

repsonse: 
{'success': "OTP has been sent", 'existing_user': false}


## verify otp POST
POST
http://{YOUR_IP}/api/authn/verify_otp/

{
	"mobile": 8441000947,
	"otp": 413033,
}

reponse 
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtb2JpbGUiOjg0NDEwMDA5NDcsImV4cCI6MTU5MTgwNzExMn0.2jnpiYeRGhbA20pWK3RS4X90noJJdRHsLKfXZHuqVoU",
    "id": 2
}


## token exchange POST
POST
http://{YOUR_IP}/api/banking/token_exchange/

header: {"Authorization": "JWT 'token'"} // token you get from login api

{
	"public_token": "public-sandbox-ebf36bf1-5fea-4cdc-8135-e8fc9955f3a0"
}

reponse
{
    "success": true,
    "item_id": "zvVV1RN6oMfB3Jp1Rb57UJadlM9wZJfo13rxg"
}

## api for fetching accounts and transactions GET
GET
http://{YOUR_IP}/api/banking/account_statement/?account_id=

header: {"Authorization": "JWT 'token'"} // token you get from login api

where if you want details of specific account you can pass account_id as param

[
    {
        "available_balance": 200,
        "transactions": [
            {
                "amount": 25,
                "pending": false,
                "pending_transaction_id": null,
                "currency": "USD",
                "name": "CREDIT CARD 3333 PAYMENT *//",
                "transaction_type": "special",
                "authorized_date": null,
                "date": "2020-03-16",
                "transaction_id": "LBZpLbKpxyILAM5yBp1pivKXdamEkVCPGXLWa",
                "categories": [
                    "Payment",
                    "Credit Card"
                ]
            },
            {
                "amount": -4.22,
                "pending": false,
                "pending_transaction_id": null,
                "currency": "USD",
                "name": "INTRST PYMNT",
                "transaction_type": "special",
                "authorized_date": null,
                "date": "2020-03-11",
                "transaction_id": "1kp6bwN673FQVXqrLjDjHKW8rAPaXqU5l8QPe",
                "categories": [
                    "Transfer",
                    "Credit"
                ]
            },
            {
                "amount": 25,
                "pending": false,
                "pending_transaction_id": null,
                "currency": "USD",
                "name": "CREDIT CARD 3333 PAYMENT *//",
                "transaction_type": "special",
                "authorized_date": null,
                "date": "2020-02-15",
                "transaction_id": "M3MgpZrgdGhpKN573gLgTnpLay5mwBi9VJDRV",
                "categories": [
                    "Payment",
                    "Credit Card"
                ]
            },
            {
                "amount": -4.22,
                "pending": false,
                "pending_transaction_id": null,
                "currency": "USD",
                "name": "INTRST PYMNT",
                "transaction_type": "special",
                "authorized_date": null,
                "date": "2020-02-10",
                "transaction_id": "Z1VEvjQEzDIngAKzvxbxhqz3gdEWRQfgV681D",
                "categories": [
                    "Transfer",
                    "Credit"
                ]
            }
        ],
        "subtype": "savings",
        "account_id": "gyVM4JnMlZswm4eBAD9DHrnrzbMM9mcgQrvK1",
        "official_name": "Plaid Silver Standard 0.1% Interest Saving",
        "currency": "USD",
        "updated": "True",
        "item_id": "Z1VEvjQEzDIngAKzvxbxhqzqp6z7RMCgm3W38",
        "type": "depository",
        "current_balance": 210
    }
]


## webhook for Plaid trnscation update
POST
http://{YOUR_IP}/api/banking/transactions/update

{
"error": null,
"webhook_code": "data",
"webhook_type": "data",
"item_id": "item_id",
"new_transaction": 105
}

response:
{'message': 'Recieved', 'code': 'TRANSACTION_UPDATE'}



