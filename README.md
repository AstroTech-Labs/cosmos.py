# Python SDK for the Cosmos Ecosystem

<p><sub>(Unfamiliar with Cosmos?  <a href="https://docs.terra.money/">Check out the Cosmos Network Docs</a>)</sub></p>

This (SDK) in Python is a simple library toolkit for building software that can interact with the supported Cosmos blockchains and provides simple abstractions over core data structures, serialization, key management, and API request generation.

Note - This is currently a W.I.P.

## Features

- This SDK follows a module specific approach, and new Cosmos Modules will be added to the SDK on a priority basis.
- Written in Python with extensive support libraries
- Versatile support for key management solutions

❗ This SDK currently does not support Terra Classic. If you want to communicate with Terra Classic, use terra-sdk==2.x

<br/>

## Requirements

Cosmos.py SDK requires <a href="https://www.python.org/downloads/">Python v3.7+</a>.

## Installation

<sub>**NOTE:** _All code starting with a `$` is meant to run on your terminal (a bash prompt). All code starting with a `>>>` is meant to run in a python interpreter, like <a href="https://pypi.org/project/ipython/">ipython</a>._</sub>

Cosmos SDK can be installed (preferably in a `virtual environment` from PyPI using `pip`) as follows:
  
```
$ pip install -U cosmos_SDK
```

<sub>_You might have `pip3` installed instead of `pip`; proceed according to your own setup._<sub>

## Usage Examples

```
from cosmos_sdk.client.lcd import LCDClient
from cosmos_sdk.key.mnemonic import MnemonicKey

mnemonic = <MNEMONIC_PHRASE>

# Terra client
terra_client = LCDClient(chain_id="phoenix-1", url="https://phoenix-lcd.terra.dev")
mk = MnemonicKey(mnemonic,"terra")
terra_wallet = terra_client.wallet(mk)

# Persistence client
persistence_client = LCDClient(chain_id="core-1", url="http://rest.core.persistence.one")
mk = MnemonicKey(mnemonic,"persistence")
persistence_wallet = persistence_client.wallet(mk)
```


## Dependencies

Cosmos SDK uses <a href="https://python-poetry.org/">Poetry</a> to manage dependencies. To get set up with all the required dependencies, run:

```
$ pip install poetry
$ poetry install
```

If you encounter "version solving failed." error, try `poetry add <package_name>`, followed by `poetry lock` and then `poetry install`


<br/>

# Contributing

Community contribution, whether it's a new feature, correction, bug report, additional documentation, or any other feedback is always welcome. Please read through this section to ensure that your contribution is in the most suitable format for us to effectively process.

<br/>

# License

This reporitory was forked from  <a href="https://github.com/terra-money/terra.py">Terra SDK</a> and is being repurposed from there on. 

