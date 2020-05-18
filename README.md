# CurrencyXchange

**Images of project are present in images folder feel free to explore them.**

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

   
