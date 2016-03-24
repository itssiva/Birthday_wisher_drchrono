This is a third party web application for drchrono website, useful for doctors to send birthday wishes to their parents, either by using e-mail or SMS automatically.

The service automatically sends the greeting to the doctors' patients daily at 07:30 AM PST, either by email or SMS as per the doctor's preference.


**Once the user (doctor) logs in using drchrono :**
  - the user can customize the default greeting, for both SMS and email
  - the user can activate or deactivate ate ant time to the service
  - the user can change the greeting type instantly between SMS and email

**Planning to include:**
 -  e-cards in greeting
 - Multiple custom messages
 - Timezone support
 - National Holidays and Regional Festivals



**The apps in the project are**
--------------------------------
**drchronoAPI**
- This app contains the functions related to get the data from the drchrono API (api.py)
- get_user_data, to get the details of the user
- get_doctor_details, to get the info of doctor
- get_patients_for_doctor, gets the patients data for a doctor-id, access_token 

**Greeting**
- This app contains the models for the Greeting, the model used to store the data regarding the user's custom_message.
- Also contains utilities necessary for formatting the greeting.

**UserAuth**
- authorizes the user, gets the access tokens and other data
- using the access-token call the API to get data of user, doctor, patients
- Refresh the token incase of expired tokens
- When user first logs in, creates a default greeting.
- Handles the user logout

### The production_settings.py contains

- BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
- STATIC_ROOT = os.path.join(BASE_DIR, 'static')

**Database Settings in Production (DEBUG = False)**

- 'ENGINE': ENGINE_NAME,
- 'NAME': DATABASE_NAME,
- 'USER': DATABASE_USER_USERNAME,
- 'PASSWORD': DATABASE_USER_PASSWORD,
- 'HOST': IPADDRESS(localhost),
- 'PORT': PORT,

**Email Settings**

- EMAIL_USE_TLS = True
- EMAIL_HOST = 'smtp.gmail.com'
- EMAIL_PORT = 587
- EMAIL_HOST_USER = EMAIL
- EMAIL_HOST_PASSWORD = PASSWORD
- DEFAULT_FROM_EMAIL = FROM_EMAIL
- DEFAULT_TO_EMAIL = TO_EMAIL
- EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

**Keys for DRCHRONO Auth**
- SOCIAL_AUTH_DRCHRONO_KEY = YOUR_APP_KEY
- SOCIAL_AUTH_DRCHRONO_SECRET = YOUR_APP_SECRET
- SOCIAL_AUTH_DRCHRONO_SCOPE = [permissions]

**Celery settings**

**Redis server address**
- BROKER_URL = REDIS_BROKER_URL

**Store task results in redis**
- CELERY_RESULT_BACKEND = CELRY_RESULT_BACKEND

**Twilio Settings**
- ACCOUNT_SID = TWILIO_ACCOUNT_SID
- AUTH_TOKEN = TWILIO_AUTH_TOKEN
- TWILIO_NUMBER = TWILIO_NUMBER