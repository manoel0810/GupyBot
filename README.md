### Dependencies
``` BASH
pip install python-dotenv
pip install requests beautifulsoup4 schedule
pip install selenium
```


### Config
* Create a .env file in the root with your credentials. Like:

``` RAW
SENDER_EMAIL=seu@email.com
APP_PASSKEY=sua_senha_de_aplicativo
LOG_EMAIL=email_de_log@gmail.com
```

* Create a json group file named __groups.json__, as following in the project root:

``` JSON
{
    "groups": [
        {
            "url": "link to your gupy page filter. Only Gupy links!",
            "emails": [
                "e-mails to send"
            ],
            "groupId": 1, 
            "engine": "gupy",
            "dataset": "gupy.txt"
        }
    ]
}
```
* You can have more than one group

#### If you are using an ARM machine or other architecture that does not natively support the Chrome driver, make sure to download the driver for your architecture and save it in the project root with the name "chromedriver" only.
