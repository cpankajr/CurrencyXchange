# CurrencyXchange

**Images of project are present in images folder feel free to explore them.**

**Assumptions:**
   - User have to create wallet first before sending or recieving money
   - User will have his wallet in single currency and recieve and send money in that currrency only
   - Profit/Loss Calculation
      - example: 
         - user X(wallet($)) sends money $2 to user Y(wallet(INR)); user Y will recieve INR 100 (given 1 USD= 50 INR )
         - when you check for order analytics on next day (when 1 USD = 100 INR ) then for user X it will be loss of 1 USD
      

Instructions Tested on Ubuntu 18.04 and python3.7

- Make virtual environment with requirement.txt and activate that
   - Learn making virtual env (https://gist.github.com/frfahim/73c0fad6350332cef7a653bcd762f08d)
   - Then install package using requirement.txt in that
      - ```pip install -r requirement.txt```
   - Activate virtual env: ```source path-to-virtual-environment/bin/activate```
   
- migrate model migration in django
   - ```python manage.py makemigrations```
   - ```python manage.py migrate```

- Run Project: ```python manage.py runserver```

- To run test case: ```python manage.py test CurrencyExngApp/tests/```
- Pages:
  - Login Page
  - Signup Page
  - Home Page (Currency conversion, Send & Add Money, Create Wallet, Recent Transaction and Download Reciept)
  - Profile Page (Profile Pic and other details)

   
