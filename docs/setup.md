## Bot Account Setup

Follow the instructions here: https://discordpy.readthedocs.io/en/stable/discord.html

## Bot Setup

1. Go to the project root directory.

    ```
    cd Dayong
    ```

2. Create a copy of `.env.example`. Don't forget to omit the `.example` at the end.

    On Linux and Unix
    ```
    cp .env.example .env
    ```

    On Windows
    ```
    copy .env.example .env
    ```

3. Edit the `.env` file and add your credentials to the corresponding variables.

4. Install [poetry](https://github.com/python-poetry/poetry#installation). Check if poetry is installed by running `poetry --version`.

5. Run `poetry shell`. This will create or start the virtual environment.

6. Run `poetry install`. This will install the project and its dependencies.

## Welcome Message for New Member

1. Modify the welcome message by changing the value(s) of the following in `Dayong/dayong/config.json`.
    ```
    {
        "embeddings": {
            "greetings_channel":"<channel name where the greetings will be prompted>",
            "readme_channel_id": <id of the channel you want to tag>,
            "description": "<your greetings>",
            "color": <integer value of the color you want to use>

            "greetings_field": {
                "<n>": {
                    "name": "field's name"
                    "value": "field's value"
                },
                ...
            }
        }
    }
    ```
> You can have as many `greetings_field` you want. However, make sure that its inner key(s) is an integer (starting with 0) since it will be used inside a `for` loop.
