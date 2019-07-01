const request = require('request')
const crypto = require('crypto')
var fs = require('fs')

const apiKey = '605ccfa99ccd3ff8ccfe9bf25a9a9e05'
const apiSecret = '$2a$10$s2PAs2i3TC4PhpwpouPawOtdnSc2E/U/fd9U2Q.rZ4HEZEcFJEgxW'
const baseUrl = 'https://api.bitopro.com/v2'


const url = '/accounts/balance'
const nonce = Date.now()
const completeURL = baseUrl + url
var body = {}

for (let j = 0; j < process.argv.length; j++) {  
   if( j == 2){
      if(process.argv[j]){
         body = process.argv[j+1]
         body = JSON.parse(body)
         if(body['identity']){
            body.nonce = parseInt(body.nonce)
         }
         else if (body['timestamp']){
            body.timestamp = parseInt(body.timestamp)
         }
      }
   }

}

const payload = new Buffer(JSON.stringify(body)).toString('base64')

const signature = crypto
   .createHmac('sha384', apiSecret)
   .update(payload)
   .digest('hex')

fs.writeFile('payload.txt',payload , function (err) {
   if (err) throw err;
});
fs.writeFile('signature.txt',signature , function (err) {
   if (err) throw err;
});

console.log(payload)
console.log(signature)
console.log(JSON.stringify(body) )
const options = {
   url: completeURL,
   headers: {
     'X-BITOPRO-APIKEY': apiKey,
     'X-BITOPRO-PAYLOAD': payload,    // For the authenticated APIs using DELETE method, you don't need the payload field.
     'X-BITOPRO-SIGNATURE': signature
   },
   body: JSON.stringify(body)    // For the authenticated APIs using GET method, you don't need the body field.
}

// console.log(body.timestamp)
// if(body['timestamp']){
//    options.url = baseUrl + '/orders/btc_twd'
//    const result = request.post(
//       options,
//       function(error, response, body) {
//       console.log('post response:', JSON.stringify(body, 0, 2))
//       }
//    )
// }
// else{
//    const result = request.get(
//       options,
//       function(error, response, body) {
//       console.log('get response:', JSON.stringify(body, 0, 2))
//       }
//    )
// }

