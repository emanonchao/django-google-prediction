import httplib2
from django.conf import settings
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient import discovery

class APIManager:

	@staticmethod
	def get_api():
		if not hasattr(APIManager, '__api'):
			APIManager.__auth()
		return APIManager.__api

	@staticmethod
	def __auth():
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
		APIManager.__api = discovery.build('prediction', 'v1.6', http=http)


class HostedModel:

	HOSTED_PROJECT_ID = 414649711441

	def __init__(self, model_name):
		self.model_name = model_name

	def predict(self, input_data):
		if not isinstance(input_data, (list, tuple)):
			input_data = [input_data]

		body = {'input': {'csvInstance': input_data}}
		return APIManager.get_api().hostedmodels().predict(
			project=self.HOSTED_PROJECT_ID,
			hostedModelName=self.model_name,
			body=body
		).execute()


class TrainedModel:

	def __init__(self, project_id, model_name):
		self.project_id, self.model_name = project_id, model_name

	def analyze(self):
		return APIManager.get_api().trainedmodels().analyze(
			project=self.project_id,
			id=self.model_name,
		).execute()

	def delete(self):
		APIManager.get_api().trainedmodels().delete(
			project=self.project_id,
			id=self.model_name,
		).execute()

	def get(self):
		return APIManager.get_api().trainedmodels().get(
			project=self.project_id,
			id=self.model_name,
		).execute()

	def insert(self, storage_data_location):
		body = {
			'storageDataLocation': storage_data_location,
			'id': self.model_name,
		}

		return APIManager.get_api().trainedmodels().insert(
			project=self.project_id,
			body=body
		).execute()

	def predict(self, input_data):
		if not isinstance(input_data, (list, tuple)):
			input_data = [input_data]

		body = {'input': {'csvInstance': input_data}}
		return APIManager.get_api().trainedmodels().predict(
			project=self.project_id,
			id=self.model_name,
			body=body
		).execute()

	def update(self, output, input_data):
		if not isinstance(input_data, (list, tuple)):
			input_data = [input_data]

		body = {'csvInstance': input_data, 'output': output}
		
		return APIManager.get_api().trainedmodels().update(
			project=self.project_id,
			id=self.model_name,
			body=body
		).execute()

	@staticmethod
	def list(project_id):
		return APIManager.get_api().trainedmodels().list(
			project=project_id
		).execute()