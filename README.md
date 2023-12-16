# Delete-Right-After

This project provides a simple background service that scans your Exchange inbox for fake phishing emails originating
from KnowBe4 and either archives or deletes them based on settings.

|                                                                                                          Main Branch                                                                                                          |                                                                                                          Dev Branch                                                                                                          |
|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| [![CodeQL](https://github.com/AzorianSolutions/delete-right-after/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/AzorianSolutions/delete-right-after/actions/workflows/codeql-analysis.yml) | [![CodeQL](https://github.com/AzorianSolutions/delete-right-after/actions/workflows/codeql-analysis.yml/badge.svg?branch=dev)](https://github.com/AzorianSolutions/delete-right-after/actions/workflows/codeql-analysis.yml) |

## TL;DR - Linux

To get started quickly with a simple deployment, execute the following `bash` / `shell` commands on a Debian Linux
based system with `git` installed:

```
git clone https://github.com/AzorianSolutions/delete-right-after.git
cd delete-right-after
./deploy/bare-metal/linux/debian.sh
source venv/bin/activate
```

Once you have finished setting up the environment, you must now configure the app. To do this, you should edit the
settings in the `/etc/delete-right-after/config.env` file. Once you have finished editing the settings, you can perform
OAuth2 authentication with your Exchange account by running the following command:

```
dra auth
```

This will open a browser window and prompt you to log in to your Exchange account. Once you have logged in, you will be
prompted to authorize the app to access your account. Once you have authorized the app, you will be redirected to a
blank page. You can follow the CLI prompts to copy the URL from the browser and paste it into the CLI. Once you have
pasted the URL into the CLI, you can press enter to continue.

Once you have finished authenticating the app, you can start the app by running the following command:

```
dra run
```

## TL;DR - Windows

Start with checking out the project's official repository using git. The official repository can be
cloned from `https://github.com/AzorianSolutions/delete-right-after.git`.

```
cd C:/Path/To/Project/Root
python3 -m venv venv
venv\Scripts\activate
pip install -e .
copy deploy\config\defaults.env deploy\config\production.env
```

Edit the default settings as needed in `deploy\config\production.env`.

Then, run the following commands each time you want to activate the project for use:

```
cd C:/Path/To/Project/Root
venv\Scripts\activate
for /F %A in (deploy\config\production.env) do SET %A
dra auth
dra run
```

## Project Documentation

### Configuration

Delete-Right-After is configured via environment variables. Please refer to the default values
in [deploy/config/defaults.env](./deploy/config/defaults.env) for a list of the
environment variables that can be set.

To see the concrete implementation of the settings associated with the environment variables, please see the
[src/app/config.py](./src/app/config.py) file.

### CLI Flags

The following CLI flags are supported for the `dra run` command:

| Flag              | Description                                       |
|-------------------|---------------------------------------------------|
| `--help`          | Show the help message and exit.                   |
| `-d` `--debug`    | Runs the command in debug mode.                   |
| `-del` `--delete` | Deletes matched emails instead of archiving them. |
| `-dr` `--dry-run` | Runs the command in dry-run simulation mode.      |

### Contributing

This project is not currently accepting outside contributions. If you're interested in participating in the project,
please contact the project owner.

## [Security Policy](./.github/SECURITY.md)

Please see our [Security Policy](./.github/SECURITY.md).

## [Support Policy](./.github/SUPPORT.md)

Please see our [Support Policy](./.github/SUPPORT.md).

## [Code of Conduct](./.github/CODE_OF_CONDUCT.md)

Please see our [Code of Conduct](./.github/CODE_OF_CONDUCT.md).

## [License](./LICENSE)

This project is released under the MIT license. For additional information, [see the full license](./LICENSE).

## Donate

Like my work?

<a href="https://www.buymeacoffee.com/AzorianMatt" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
