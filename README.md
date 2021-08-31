# Calcucator Telegram bot
This is the calculator bot. Uesrs can send him arithmetic expressions and
he replies with the answer. Parsing is realised as recursive descent parser
with AST building. The calculation is performed by traversing the resulting
tree.

Also this bot supports the cache of last preformed operations by certain
user. The user can request it with `/print_cache`. ***The bot generates a
"cache" file while it is running. Do not create files with that name nearby!***

Supported operations: `+`, `-`, `*`, `/` and `()`.

Bot commands:
- `/start` - start bot.
- `/help` - for help.
- `/print_cache` - show last 5 operations.

Used library: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

## Contents

* [How to deploy locally](#how-to-deploy-locally)
* [Run tests locally](#run-tests-locally)
* [How to check if it works](#how-to-check-if-it-works)
* [Deployment on your server](#deployment-on-your-server)
* [Deployment on Heroku](#installation-and-deploying-on-heroku)

## How to deploy locally

1. Firstly, you will need the following tools:
    - [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
    - [python3](https://www.python.org/downloads/)
    - [python-telegram-bot library](https://github.com/python-telegram-bot/python-telegram-bot)

2. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/romanhabibov/calculator-bot calculator-bot
    cd calculator-bot
    ```

3. You need to get a token for your bot. Go to your Telegram client, open
a chat with @BotFather, send him `/start` and then send `/newbot`. Choose
a username for your bot.
Now, you recieved a message from @BotFather with your bot's token. Copy it and
set it as evironment variable:
    ```bash
    export CB_TOKEN=<yourbottoken>
    ```

4. Run the bot:
    ```bash
    python3 bot.py
    ```

[Back to contents](#contents)

## Run tests locally

You can test `calculator.py` module working.

1. Install [pytest](https://docs.pytest.org/en/6.2.x/getting-started.html).

2. Run tests with:
    ```bash
    pytest test_calculator.py
    ```

[Back to contents](#contents)

## How to check if it works

You can find your bot in Telegram by his username. Just send commands or expressions to your bot.
If he doesn't answer, the service is most likely lying down. Check Heroku logs:
```bash
heroku logs
```

[Back to contents](#contents)

## Deployment on your server

With this deployment method, the bot should work using [webhooks](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#creating-a-self-signed-certificate-using-openssl).
Clone the rpository [this way](#how-to-deploy-locally). You need to configure the app
with environment variables:
- `CB_MODE` - set the value 'webhook'.
- `CB_TOKEN` - step 3 [here](#how-to-deploy-locally).
- `CB_PORT` - the port can be one of `443`, `80`, `88` or `8443`.
- `CB_WEBHOOK_URL` - url without "https:" and slashes (e.g. "yourherokuappname.herokuapp.com").
- `CB_KEY` and `CB_CERT` - paths to files generated [this way](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#a-ssl-certificate).

[Back to contents](#contents)

## Deployment on Heroku

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/romanhabibov/calculator-bot calculator-bot
    cd calculator-bot
    ```

2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up).
Login / [create](https://signup.heroku.com/dc) a Heroku account. Go back to the command line and type:
    ```bash
    heroku login
    ```

3. Once you are logged in, go back to the command line. Type in:
    ```bash
    heroku create
    ```
    to create your new webapp. Here, heroku will assign your webapp a name as
    as the link to your webapp, which should be of the format "https://\<yourherokuappname\>.herokuapp.com/".
    Set it as heroku evironment variable without 'https:" and slashes:
    ```bash
    heroku config:set CB_WEBHOOK_URL=<yourherokuappname>.herokuapp.com
    ```

3. Get the token [this way](#how-to-deploy-locally) and set in as heroku evironment variable:
    ```bash
    heroku config:set CB_TOKEN=<yourbottoken>
    ```

4. Set the port of app and mode:
    ```bash
    heroku config:set CB_PORT=80
    heroku config:set CB_MODE=webhook
    ```

5. Finally, deploy your bot:
    ```bash
    heroku git:remote -a <yourherokuappname>
    git push heroku master
    ```

[Back to contents](#contents)
