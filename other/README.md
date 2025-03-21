run 'pip install -r requirements.txt' in terminal to install all requirements
run db_setup.py once to intialise the database, this does not have to be done again
run main.py to use the system
admin login:
user: admin
password: 123

## Setup Instructions
This project requires an API key for ExchangeRate API.
1. Sign up at [ExchangeRate Host](https://exchangerate.host/) and get your API key.
2. Create a `config.json` file in the project root.
3. Add the following content:

   {
       "EXCHANGE_RATE_API_KEY": "your_api_key_here"
   }
