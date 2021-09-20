# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

# Types of Contributions

## Report Bugs

Report bugs at https://github.com/SurPathHub/Dayong/issues.

If you are reporting a bug, please include:

* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

## Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

## Write Documentation

Dayong could always use more documentation, whether as part of the official Dayong docs, in docstrings, or even on the web in blog posts, articles, and such.

## Submit Feedback

The best way to send feedback is to file an issue at https://github.com/SurPathHub/Dayong/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome.

## Get Started

Ready to contribute? Here's how to set up `Dayong` for local development.

1. Fork the `Dayong` repo on GitHub.
2. Clone your fork locally

    ```
    $ git clone https://github.com/SurPathHub/Dayong.git
    ```

3. Install your local copy into a virtualenv. Assuming you have python [poetry](https://github.com/python-poetry/poetry) installed, this is how you set up your fork for local development

    ```
    $ cd Dayong/
    $ poetry shell
    $ poetry install
    ```

4. Create a branch for local development

    ```
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

   Now you can make your changes locally.

<<<<<<< HEAD
5. When you're done making changes, check that your changes pass flake8, pylint, and pyright.

    ```
    $ flake8 dayong
    $ pylint dayong
    $ pyright dayong
=======
5. When you're done making changes, check that your changes pass flake8, pylint and mypy.

    ```
    $ flake8 Dayong
    $ pylint Dayong
    $ mypy Dayong
>>>>>>> 9368de9... docs: add contributing guidelines
    ```

## Commit Message Guidelines
Dayong uses precise rules over how git commit messages can be formatted. This leads to more readable messages that are easy to follow when looking through the project history. But also, git commit messages are used to generate the change log. For instructions, head over to this site: https://www.conventionalcommits.org/en/v1.0.0/.

```
$ git add .
$ git commit -m "<type>(<scope>): <subject>"
<<<<<<< HEAD
=======
$ git push origin name-of-your-bugfix-or-feature
>>>>>>> 9368de9... docs: add contributing guidelines
```

## Pull Request Guidelines

Please open an issue before submitting, unless it's just a typo or some other small error.

Before you submit a pull request, check that it meets these guidelines:

1. If the pull request adds functionality, the docs should be updated. Implement your functionality with a docstring if needed.
2. The pull request should work for Python 3.9 and above.

Before making changes to the code, install the development requirements using

```
$ poetry install
```

Before committing, stage your files and run style and linter checks

```
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 5cd392b... docs: amend contributing guidelines
$ black dayong/  # apply codestyle
$ isort --profile black dayong/  # sort imports
$ flake8 dayong/
$ pylint dayong/
<<<<<<< HEAD
$ pyright dayong/  # optional static type checking
=======
$ black Dayong  # apply codestyle
$ isort --profile black Dayong  # sort imports
$ flake8 Dayong
$ pylint Dayong
$ mypy Dayong  # optional type checking
=======
$ mypy dayong/  # optional type checking
>>>>>>> 5cd392b... docs: amend contributing guidelines
```

## Tips

- Running tests

To run a subset of tests

```
$ pytest -v tests/test_clients.py
>>>>>>> 9368de9... docs: add contributing guidelines
```
