# django-google-prediction

## Introduction

*django-google-prediction* is a Django application that wraps the [Google Prediction API](https://developers.google.com/prediction/) to make it easier to build web applications with machine learning and data analysis functionality.

## Instructions

- Add private key to base directory

- Add the following to settings.py:
'''python
GOOGLE_PREDICTION_PRIVATE_KEY = os.path.join(BASE_DIR, 'private-key.p12') # REPLACE WITH YOUR KEY
GOOGLE_PREDICTION_PROJECT_EMAIL = '_________' # REPLACE WITH YOUR PROJECT EMAIL

'''