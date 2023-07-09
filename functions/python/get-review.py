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
    response = service.post_find(
      db='reviews',
      selector={'dealership': int(params['dealerId'])},
    ).get_result()

    if not response['docs']:
      return {'statusCode': 404, 'body': 'dealerId does not exist'}

    return {'statusCode': 201, 'body': response['docs']}

  except Exception as e:
    return {'statusCode': 500, 'body': 'Something went wrong on the server', 'error': str(e)}

if __name__ == '__main__':
  print(main({'dealerId': 15}))
