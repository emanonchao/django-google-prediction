# django-google-prediction

## Introduction

*django-google-prediction* is a Django application that wraps the [Google Prediction API](https://developers.google.com/prediction/) to make it easier to build web applications with machine learning and data analysis functionality.

## Instructions

### Creating a new project

- Go to the [Google Developers Console](https://console.developers.google.com/), click *Create Project* and fill in the project name and id.
- Go to your project, select *APIs & auth > APIs* and turn the *Prediction API* on.

### Uploading a dataset (.csv)
- In your project dashboard, select *Cloud Storage > Storage browser*.
- You might be requested to enable billing for this feature.
- Click *New Bucket*, fill in as desired and upload your dataset.

### Configuring your Django application
- In your project dashboard, select *APIs & auth > Credentials*.
- Click *Create New Client ID*, select the *Service account* option and save your private key as *private-key.p12* in your project's base directory.
- Still in that page, note the *Email address* provided for that key (e.g. 1234567890-abcdefghijklmnopqrstuvwxyz1234567890@developer.gserviceaccount.com).
- Add the following to *settings.py*:

```python
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
GOOGLE_PREDICTION_PRIVATE_KEY = os.path.join(BASE_DIR, 'private-key.p12')
GOOGLE_PREDICTION_PROJECT_EMAIL = '_________' # REPLACE WITH YOUR PROJECT EMAIL
```

- Add the *google_prediction* folder to your project's base directory.
- Install all the modules in *requirements.txt* (use *pip install -r requirements.txt*).

## Examples

- Using Hosted Models
```python
HostedModel('sample.languageid').predict('Me llamo Gabriel. Como te llamas?')
# {u'kind': u'prediction#output', u'outputLabel': u'Spanish', u'id': u'sample.languageid', u'selfLink': u'https://www.googleapis.com/prediction/v1.6/projects/414649711441/hostedmodels/sample.languageid/predict', u'outputMulti': [{u'score': u'0.032187', u'label': u'English'}, {u'score': u'0.512064', u'label': u'Spanish'}, {u'score': u'0.455749', u'label': u'French'}]}

m = HostedModel('sample.languageid')
m.predict('My name is Gabriel - nice to meet you!')['outputLabel']
# u'English'
m.predict("Je m'appelle Gabriel. J'aime la France!")['outputLabel']
# u'French'
```

- Using Trained Models
```python
# Listing all your models
TrainedModel.list("YOUR_PROJECT_ID")

# Creating a new model 
# (DATASET_LOCATION must be in a Google Storage bucket; leave blank for empty model)
TrainedModel("YOUR_PROJECT_ID", "YOUR_MODEL_NAME").insert("DATASET_LOCATION")

# Inserting data into your model
TrainedModel("YOUR_PROJECT_ID", "YOUR_MODEL_NAME").update(OUTPUT, INPUT_DATA)

# Getting information about your model
TrainedModel("YOUR_PROJECT_ID", "YOUR_MODEL_NAME").get()

# Analyzing your model
TrainedModel("YOUR_PROJECT_ID", "YOUR_MODEL_NAME").analyze()

# Predicting based on your model
TrainedModel("YOUR_PROJECT_ID", "YOUR_MODEL_NAME").predict(INPUT_DATA)

# Deleting your model
TrainedModel("YOUR_PROJECT_ID", "YOUR_MODEL_NAME").delete()

# Multiple calls
m = TrainedModel("YOUR_PROJECT_ID", "YOUR_MODEL_NAME")
m.predict(INPUT_DATA)
m.predict(SOME_OTHER_DATA)
m.predict(MORE_STUFF_HERE)
```