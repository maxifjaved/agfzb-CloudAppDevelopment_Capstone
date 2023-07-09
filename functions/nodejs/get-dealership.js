const creds = require('../.creds.json');
const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

async function main(params) {
  const authenticator = new IamAuthenticator({apikey: creds.IAM_API_KEY})
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator
  });
  cloudant.setServiceUrl(creds.COUCH_URL);

  try {
    let selector = {};
    if (params.state) {
      selector = { state: params.state };
    }

    const response = await cloudant.postFind({
      db: 'dealerships',
      selector: selector,
    });
    if (!response.result.docs || response.result.docs.length === 0) {
      return {statusCode: 404, body: 'The database is empty'};
    }

    return {statusCode: 200, body: response.result.docs};
  } catch (error) {
    return {statusCode: 500, body: 'Something went wrong on the server', error: error.message || error.description};
  }
}

// main({}).then(console.log).catch(console.error)
// main({state: 'NY'}).then(console.log).catch(console.error)
