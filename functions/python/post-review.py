import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1


def main(params):
  with open('../.creds.json') as f:
    creds = json.load(f)

  authenticator = IAMAuthenticator(creds['IAM_API_KEY'])
  service = CloudantV1(authenticator=authenticator)
  service.set_service_url(creds['COUCH_URL'])

  try:
    response = service.post_document(
      db='reviews',
      document={'dealership': params['review']},
    ).get_result()

    return {'statusCode': 201, 'body': response}

  except Exception as e:
    return {'statusCode': 500, 'body': 'Something went wrong on the server', 'error': str(e)}


if __name__ == '__main__':
  print(main({
    "review":
      {
        "id": 1114,
        "name": "Upkar Lidder",
        "dealership": 15,
        "review": "Great service!",
        "purchase": False,
        "another": "field",
        "purchase_date": "02/16/2021",
        "car_make": "Audi",
        "car_model": "Car",
        "car_year": 2021
      }
  }))
