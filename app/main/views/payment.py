from flask.helpers import url_for
import stripe
import json
from flask import current_app, jsonify, request, redirect
from flask_login import current_user
from config import Config
from .. import main
from ... import db
from ...models import User

# Setup Stripe python client library
stripe.api_key = Config.STRIPE_SECRET_KEY
stripe.api_version = Config.STRIPE_API_VERSION

@main.route('/setup', methods=['GET'])
def get_publishable_key():
    json_obj = jsonify({
        'publishableKey': Config.STRIPE_PUBLISHABLE_KEY,
        'jpyPriceId': Config.JPY_PRICE_ID,
        'usdPriceId': Config.USD_PRICE_ID,
    })
    return json_obj

# Fetch the Checkout Session to display the JSON result on the success page
@main.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('session_id')
    checkout_session = stripe.checkout.Session.retrieve(id)

    user=current_user._get_current_object()
    user.stripe_customer = checkout_session['customer']
    user.stripe_status = checkout_session['payment_status']
    db.session.commit()
    
    # return jsonify(checkout_session)
    return redirect(url_for('.account'))


@main.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = json.loads(request.data)
    domain_url = request.url_root

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

        item_dict={
            "price": data['priceId'],
            "quantity": 1,
        }

        if data['priceId'] == Config.JPY_PRICE_ID:
            item_dict['tax_rates'] = [Config.TAX_RATE_ID]
        
        checkout_session = stripe.checkout.Session.create(
            
            success_url=domain_url +
            "checkout-session?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "account",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[item_dict],
            # subscription_data={
            #     'default_tax_rates': [os.getenv('TAX_RATE_ID')],
            # },
        )
        return jsonify({'sessionId': checkout_session['id']})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@main.route('/customer-portal', methods=['GET'])
def customer_portal():
    # data = json.loads(request.data)
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID. 
    # Typically this is stored alongside the authenticated user in your database. 
    # checkout_session_id = data['sessionId']
    # checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
    user=current_user._get_current_object()
    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = request.url_root + "account"
    # return_url = os.getenv("DOMAIN")

    session = stripe.billing_portal.Session.create(
        customer=user.stripe_customer,
        return_url=return_url)
    # return jsonify({'url': session.url})
    return redirect(session.url)


@main.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = Config.STRIPE_WEBHOOK_SECRET
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    # https://stripe.com/docs/billing/invoices/overview#workflow-overview
    if event_type == 'checkout.session.completed':
        # Payment is successful and the subscription is created.
        # # You should provision the subscription.
        current_app.logger.info('event_type= %s', event_type)
        current_app.logger.info('data_object= %s', data_object)
    
    if event_type == 'invoice.paid':
        # Continue to provision the subscription as payments continue to be made.
        # # Store the status in your database and check when a user accesses your service.
        # # This approach helps you avoid hitting rate limits.
        current_app.logger.info('event_type= %s', event_type)
        current_app.logger.info('data_object= %s', data_object)
        customer = data_object['customer']
        status = data_object['status']
        _update_user_status(customer, status)

    if event_type == 'invoice.payment_failed':
        # The payment failed or the customer does not have a valid payment method.
        # The subscription becomes past_due. Notify your customer and send them to the
        # customer portal to update their payment information.
        current_app.logger.info('event_type= %s', event_type)
        current_app.logger.info('data_object= %s', data_object)
        customer = data_object['customer']
        status = data_object['status']
        _update_user_status(customer, status)

    if event_type == 'invoice.deleted':
        current_app.logger.info('event_type= %s', event_type)
        current_app.logger.info('data_object= %s', data_object)
        customer = data_object['customer']
        status = data_object['status']
        _update_user_status(customer, status)
            
    return jsonify({'status': 'success'})

def _update_user_status(customer, status):
      user=User.query.filter_by(stripe_customer=customer).first()
      if user is not None:
        user.stripe_customer = customer
        user.stripe_status = status
        db.session.commit()
