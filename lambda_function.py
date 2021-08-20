import datetime, decimal, os
import json
import authorize
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY') 

_PRICE_ID_LIGHT = os.getenv('STRIPE_PRICE_ID_LIGHT')
_PRICE_ID_PREMIUM = os.getenv('STRIPE_PRICE_ID_PREMIUM')
_SUBSCRIPTION_PAGE_URL = os.getenv('SUBSCRIPTION_PAGE_URL')

_EVENT_KEY_PATH_PARAMETER = 'pathParameters'
_EVENT_KEY_QUERY_STRING_PARAMETER = 'queryStringParameters'
_EVENT_KEY_HTTP_METHOD = 'httpMethod'
_PARAM_KEY_PRICE_TYPE = 'price_type'
_PRICE_TYPE_LIGHT = 'light'
_PRICE_TYPE_PREMIUM = 'premium'


_RESPONSE_303 = {
        'statusCode': 303,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }

_RESPONSE_400 = {
        'statusCode': 400,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }

_RESPONSE_403 = {
        'statusCode': 403,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }


_RESPONSE_500 = {
        'statusCode': 500,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }


def lambda_handler(event, context):
    print('event:', event)
    query_string_parameters = event[_EVENT_KEY_QUERY_STRING_PARAMETER]
    print("query_string_parameters:", query_string_parameters)

    alert_id = None
    if_create_new_alert = True
    if _PATH_PARAMETER_ALERT in path_parameters:
        alert_id = path_parameters[_PATH_PARAMETER_ALERT]
        if_create_new_alert = False

    if _EVENT_KEY_BODY not in event:
        res = _RESPONSE_400
        res['body'] = json.dumps('event body is not found.'.format(alert_id=alert_id))
        return res

    body = event[_EVENT_KEY_BODY]
    if body is None:
        res = _RESPONSE_400
        res['body'] = json.dumps('request body is not found.'.format(alert_id=alert_id))
        return res

    print('body:', body)
    body = json.loads(body)
    print('json body:', body)

    payload = json.loads(body)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    const sig = request.headers['stripe-signature'];
    event = None

    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Passed signature verification
    return HttpResponse(status=200)

    result = {}

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(result, cls=DecimalEncoder)
    }

