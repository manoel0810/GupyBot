### Dependencies
``` BASH
pip install python-dotenv requests
```


### Config
* Create a .env file in the root with your credentials. Make sure your account is enabled to use the SMTP service and that it is a Gmail account:

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
            "keys": ["your search key, ie: .net", "another key, ie: python"],
            "emails": [
                "email1@to.send",
                "email2@to.send"
            ],
            "groupId": 1, 
            "remoteOnly": true,
            "skip": false
        }
    ]
}
```
* You can have more than one group
