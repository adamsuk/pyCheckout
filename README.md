# pyCheckout
Python based checkout for groceries. This consists of a python package including a CLI.

### Expected use

Call the CLI with space separated strings of the items in your shopping cart (reoccuring instances for multiple quantities).

e.g.

`python cli.py Bread Milk Soup Milk`

### How to use this tool

- Run the `cli.py` file with python 3
- If issues are encountered create a conda environment with one of the `environment-<OS>.yml` files in the root of this directory.
- Use space-separated strings as input arguments

### How to run the tests

Run `test_shop.py` in the `tests` directory in `pyCheckout`, e.g. from the `pyCheckout` directory:

`python tests/test_shop.py`

### Gotchas
There aren't too many gotchas given the size of the package, but these currently include:
- The prices_file and discounts_file require a certain data shape.
- The code is less defensive than it could be (e.g. json data shape checks).
- The CLI has not been tested, it's very small, but it has a possibility of bugs.
- No CI or automated linting
- Package bugs! ... there could be a fair few but hopefully this is sufficiently tested
