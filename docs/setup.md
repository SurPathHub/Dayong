## Bot Account Setup

Follow the instructions here: https://discordpy.readthedocs.io/en/stable/discord.html

## Bot Setup

> You may also perform the steps listed below directly on your fork of the GitHub repository.

1. `git clone` Your fork of Dayong to your local machine.

2. Go to the project root directory.

    ```
    cd Dayong
    ```

3. Create a copy of `.env.example`. Don't forget to omit the `.example` at the end.

    On Linux and Unix
    ```
    cp .env.example .env
    ```

    On Windows
    ```
    copy .env.example .env
    ```

4. Edit the `.env` file and add your credentials to the corresponding variables.

5. Install [poetry](https://github.com/python-poetry/poetry#installation). Check if poetry is installed by running `poetry --version`.

6. Run `poetry shell`. This will create or start the virtual environment.

7. Run `poetry install`. This will install the project and its dependencies.

8. Edit the `config.json` file and its values as necessary.

    The `config.json` file stores public options, settings, properties, configuration, and preferences.

9. Generate an up-to-date `requirements.txt` file containing Dayong's dependencies.

    ```
    poetry export -f requirements.txt -o requirements.txt
    ```

10. After setting up Dayong, `git commit` and `git push` your changes.

11. [Deploy!](../README.md#deployment)
