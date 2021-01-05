# Deploy to Heroku remote

### Check heroku variables by cli
```
cd mydiary
heroku config
```
### Make sure that the variables are like below:
```
DATABASE_URL:         postgres://gnbyifmpaxbsxk:cba1a94dd0fe23ce0627e61415ec8907c501c5d12d9a24c8530938133cce04be@ec2-54-196-89-124.compute-1.amazonaws.com:5432/d579o1f4mnihkp
FLASK_APP:            mydiary.py
FLASK_CONFIG:         heroku
FLASK_DEBUG:          0
GOOGLE_CLIENT_ID:     (omitted)
GOOGLE_CLIENT_SECRET: (omitted)
TWITTER_API_KEY:      (omitted)
TWITTER_API_SECRET:   (omitted)
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

### Check SSL redirect
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
