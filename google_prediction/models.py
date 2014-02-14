import httplib2
from django.conf import settings
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient import discovery

class ModelManager:

	def get_model(self, model):
		if not hasattr(self, 'api'):
			self.authorize()
		return HostedModel(self.api, model)

	@classmethod
	def authorize(self):
		# TODO Validate credentials
		private_key = open(settings.GOOGLE_PREDICTION_PRIVATE_KEY).read()
		http = httplib2.Http()

		credentials = SignedJwtAssertionCredentials(
			 	settings.GOOGLE_PREDICTION_PROJECT_EMAIL,
			 	private_key,
			 	[
			      'https://www.googleapis.com/auth/devstorage.full_control',
			      'https://www.googleapis.com/auth/devstorage.read_only',
			      'https://www.googleapis.com/auth/devstorage.read_write',
			      'https://www.googleapis.com/auth/prediction',
			    ]
			)

		credentials.authorize(http)
		ModelManager.api = discovery.build('prediction', 'v1.6', http=http)

class HostedModel:
	HOSTED_PROJECT_ID = 414649711441

	models = ModelManager().get_model

	def __init__(self, api, model):
		self.api = api
		self.model = model

	def predict(self, inputData):
		body = {'input': {'csvInstance': [inputData]}}
		return ModelManager.api.hostedmodels().predict(
			project=self.HOSTED_PROJECT_ID,
			hostedModelName=self.model,
			body=body
		).execute()