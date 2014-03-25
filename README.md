# django-google-prediction

## Introduction

*django-google-prediction* is a Django application that wraps the [Google Prediction API](https://developers.google.com/prediction/) to make it easier to build web applications with machine learning and data analysis functionality.

## Instructions

- Add private key to base directory

- Add the following to settings.py:

```python
GOOGLE_PREDICTION_PRIVATE_KEY = os.path.join(BASE_DIR, 'private-key.p12') # REPLACE WITH YOUR KEY
GOOGLE_PREDICTION_PROJECT_EMAIL = '_________' # REPLACE WITH YOUR PROJECT EMAIL
```

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
TrainedModel("YOUR_PROJECT_ID", "YOUR_MODEL_NAME").predict(INPUT_DATA)

m = TrainedModel("YOUR_PROJECT_ID", "YOUR_MODEL_NAME")
m.predict(INPUT_DATA)
m.predict(SOME_OTHER_DATA)
m.predict(MORE_STUFF_HERE)
```