# Dayong
<<<<<<< HEAD
![License mit](https://img.shields.io/badge/license-MIT-brightgreen)
[![Python version](https://img.shields.io/badge/python-3.9.7-blue.svg)](https://www.python.org/downloads/release/python-397/)
![Codestyle](https://img.shields.io/badge/code%20style-black-black)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/SurPathHub/Dayong)

Dayong is dedicated to helping Discord servers build and manage their communities.

- Multipurpose —lots of features, lots of automation.
- Self-hosted and easy to deploy —just a few more steps to take.
- Free and open-source —tinker with it, and feel free to contribute to its improvement!
- Modular —easily add extensions and features.

> For setup and installation and setup instructions, please refer to the [documentation](./docs/README.md).

## Deployment

### Setup

Please make sure you've set up Dayong, do so by following the [setup instructions](./docs/setup.md).

Dayong comes with an `app.json` file for creating an app on Heroku from a GitHub repository.

If your fork is public, you can use the following button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy) 

Otherwise, access the following link and replace `$YOUR_REPOSITORY_LINK$` with your repository link.

```
https://heroku.com/deploy?template=$YOUR_REPOSITORY_LINK$
```

## Contributing

Check the [contributing guide](./.github/CONTRIBUTING.md) to learn more about the development process and how you can test your changes.

## Code of Conduct

Read our [Code of Conduct](https://github.com/SurPathHub/support/blob/main/CODE_OF_CONDUCT.md).

## License

Distributed under the MIT License. See [LICENSE](/LICENSE) for more information.
=======

## Installation

Download the source code:

```
git clone https://github.com/SurPathHub/Dayong.git
```

## Bot Account Setup

Follow the instructions here: https://discordpy.readthedocs.io/en/stable/discord.html

## Project Setup

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

## Usage

1. From the project root directory, run:

    ```
    python dayong
    ```

2. Open your Discord application. Go to the server where you invited the bot and run `[your command prefix]help`. For instance: `.help` or `!help`. The dot prefix is the default.
>>>>>>> c0e265d... docs: explain setup and usage
