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

7. Edit the `config.json` file and its values if necessary.

    The `config.json` file stores public options, settings, properties, configuration, and preferences.
