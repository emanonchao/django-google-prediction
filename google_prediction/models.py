import httplib2
from django.conf import settings
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient import discovery

class ModelManager:

	def get_model(self, model):
		if not hasattr(self, 'api'):
			self.authorize()
		return HostedModel(self.api, model)

	# TODO Change this function
	def get_model_tmp(self, project, model):
		if not hasattr(self, 'api'):
			self.authorize()
		return TrainedModel(self.api, project, model)

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
		# TODO check for lists in input
		body = {'input': {'csvInstance': [inputData]}}
		return ModelManager.api.hostedmodels().predict(
			project=self.HOSTED_PROJECT_ID,
			hostedModelName=self.model,
			body=body
		).execute()


class TrainedModel:

	PROJECT_ID = None

	# TODO Change function structure
	models = ModelManager().get_model_tmp

	def __init__(self, api, project, model):
		self.api, self.PROJECT_ID, self.model = api, project, model

	def analyze(self):
		return ModelManager.api.trainedmodels().analyze(
			project=self.PROJECT_ID,
			id=self.model,
		).execute()

	def get(self):
		return ModelManager.api.trainedmodels().get(
			project=self.PROJECT_ID,
			id=self.model,
		).execute()

	def insert(self, model_name, storage_data_location):
		body = {
			'storageDataLocation': storage_data_location,
			'id': model_name,
		}

		return ModelManager.api.trainedmodels().insert(
			project=self.PROJECT_ID,
			body=body
		).execute()

	# TODO This is clumsy - requires project
	def list(self):
		return ModelManager.api.trainedmodels().list(
			project=self.PROJECT_ID
		).execute()

	def predict(self, inputData):
		if not isinstance(inputData, (list, tuple)):
			inputData = [inputData]

		body = {'input': {'csvInstance': inputData}}
		return ModelManager.api.trainedmodels().predict(
			project=self.PROJECT_ID,
			id=self.model,
			body=body
		).execute()

