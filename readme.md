# Deploy to Heroku remote

### Check heroku variables by cli
```
cd mydiary
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

### Push the codes to heroku repository
```
git push heroku master
```
### Deploy
```
heroku maintenance:on
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

## Keep application running on Heroku

[UptimeRobot](https://uptimerobot.com/)