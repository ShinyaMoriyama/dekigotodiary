# Run locally
Clone repository in your work directory
```
git clone https://github.com/ShinyaMoriyama/dekigotodiary
```
Create .env file and edit it to set environment valiables by running app
```
cp .env.example .env
```
Create virtual environment so that you can install packages by repository 
```
python3 -m venv venv
source venv/bin/activate
```
Install packages
```
pip install -r requirements/common.txt
```
Export environment varialbes which are needed to run flask
```
export FLASK_APP=mydiary.py
```
Run application
```
flask run
```
Check the URL if the top page shows correctly

http://127.0.0.1:5000/

# Deploy to Heroku

### Check heroku variables by cli
```
cd dekigotodiary
heroku config
```
### Make sure that the variables are like below:
```
CSRF_SECRET_KEY:              (omitted)
DATABASE_URL:                 (omitted)
FLASK_APP:                    mydiary.py
FLASK_CONFIG:                 heroku
FLASK_DEBUG:                  0
GOOGLE_CLIENT_ID:             (omitted)
GOOGLE_CLIENT_SECRET:         (omitted)
HEROKU_STRIPE_WEBHOOK_SECRET: (omitted)
LIVE_JPY_PRICE_ID:            (omitted)
LIVE_STRIPE_PUBLISHABLE_KEY:  (omitted)
LIVE_STRIPE_SECRET_KEY:       (omitted)
LIVE_STRIPE_WEBHOOK_SECRET:   (omitted)
LIVE_TAX_RATE_ID:             (omitted)
LIVE_USD_PRICE_ID:            (omitted)
STRIPE_API_VERSION:           (omitted)
STRIPE_LIVE:                  1
TWITTER_API_KEY:              (omitted)
TWITTER_API_SECRET:           (omitted)
```
If you add or change the variable, set it as below:
```
heroku config:set FLASK_APP=flasky.py
```

### Push the codes to heroku repository and deploy
```
heroku maintenance:on
git push heroku master
heroku run flask deploy
heroku restart
heroku maintenance:off
```
### View logs
```
heroku logs
heroku logs -t
```

# Useful commands and reference pages

## Check SSL redirect
```
http https://dekigoto.herokuapp.com
http http://dekigoto.herokuapp.com
curl -I https://dekigoto.herokuapp.com
curl -I http://dekigoto.herokuapp.com
```
If access via "http", request header includes "location" which indicates that SSL redirect works well.

## Localization and internationalization

[The Flask Mega-Tutorial Part XIII: I18n and L10n](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n)

For the first time
- create .mo file
```
cd mydiary
flask translate init ja
```
  make sure to create /app/translations/ja/LC_MESSAGES/messages.po

- edit `msgstr` in /app/translations/ja/LC_MESSAGES/messages.po

- compile
```
flask translate compile
```
  make sure to create /app/translations/ja/LC_MESSAGES/messages.mo

For the second time or later
- update .mo file
```
cd mydiary
flask translate update
```
  make sure to update /app/translations/ja/LC_MESSAGES/messages.po

- edit `msgstr` in /app/translations/ja/LC_MESSAGES/messages.po

- compile
```
flask translate compile
```
  make sure to update /app/translations/ja/LC_MESSAGES/messages.mo

## Favicon

[favicon.io](https://favicon.io/)

## Free images

[Adobe Stock](https://stock.adobe.com/)

## Legal documents

[Terms and conditions](https://www.termsandconditionsgenerator.com/live.php?token=CcU4nZarxfTNRPxbtVBqPrCSQgRv0CPM)

[Privacy policies](https://www.privacypolicygenerator.info/live.php?token=Z7wXCepBT1BYQurT4JRTcGASnY8UrhAV)

[Webサイトの利用規約](https://kiyaku.jp/)

[特定商取引法ガイド ](https://www.no-trouble.caa.go.jp/what/mailorder/)

## Keep application running on Heroku

[UptimeRobot](https://uptimerobot.com/)

## Flask logger

[Change the format of default_handler in Flask](https://stackoverflow.com/questions/55357513/how-to-change-flask-logging-debug-screen-output-format)

## Stripe

[Create subscriptions with Checkout](https://stripe.com/docs/billing/subscriptions/checkout)

[GitHub](https://github.com/stripe-samples/checkout-single-subscription)

## Share the URL with Twitter

[Cards with Twitter](https://developer.twitter.com/en/docs/twitter-for-websites/cards/guides/getting-started)