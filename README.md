### Dependencias
```
pip install python-dotenv
pip install requests beautifulsoup4 schedule
pip install selenium
```


### Config
* Create a .env file in the root with your credentials. Like:

```
SENDER_EMAIL=seu@email.com
APP_PASSKEY=sua_senha_de_aplicativo
LOG_EMAIL=email_de_log@gmail.com
```

#### If you are using an ARM machine or other architecture that does not natively support the Chrome driver, make sure to download the driver for your architecture and save it in the project root with the name "chromedriver" only.
