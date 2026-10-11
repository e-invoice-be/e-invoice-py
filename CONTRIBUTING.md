## Setting up the environment

### With Rye

We use [Rye](https://rye.astral.sh/) to manage dependencies because it will automatically provision a Python environment with the expected Python version. To set it up, run:

```sh
$ ./scripts/bootstrap
```

Or [install Rye manually](https://rye.astral.sh/guide/installation/) and run:

```sh
$ rye sync --all-features
```

You can then run scripts using `rye run python script.py` or by activating the virtual environment:

```sh
# Activate the virtual environment - https://docs.python.org/3/library/venv.html#how-venvs-work
$ source .venv/bin/activate

# now you can omit the `rye run` prefix
$ python script.py
```

### Without Rye

Alternatively if you don't want to install `Rye`, you can stick with the standard `pip` setup by ensuring you have the Python version specified in `.python-version`, create a virtual environment however you desire and then install dependencies using this command:

```sh
$ pip install -r requirements-dev.lock
```

## Modifying/Adding code

All code in this repository is maintained by hand. There is no code generator, so you can edit any file,
and your changes go through a normal pull request.

The SDK follows the [OpenAPI spec](https://api.e-invoice.be/api/openapi.json) of the API. When the spec changes,
the SDK is updated by hand.

### Adding or changing an endpoint

1. Add or change the method in the resource module in `src/e_invoice_api/resources/`, for example
   `src/e_invoice_api/resources/stats.py`. Each resource has a synchronous and an asynchronous class
   (`StatsResource` and `AsyncStatsResource`) and the matching `WithRawResponse` and `WithStreamingResponse`
   classes. Keep all of them in sync.
2. Add or change the types in `src/e_invoice_api/types/`. Request params are `TypedDict`s
   (for example `stats_retrieve_params.py`) and responses are Pydantic models (for example
   `stats_retrieve_response.py`). Export new types from `src/e_invoice_api/types/__init__.py`.
3. For a new resource, also export its classes from `src/e_invoice_api/resources/__init__.py` and add it to the
   clients in `src/e_invoice_api/_client.py`.
4. Add or change the entry for the method in `api.md`.
5. Add tests in `tests/api_resources/`, for example `tests/api_resources/test_stats.py`. The tests mock the HTTP
   layer with [respx](https://lundberg.github.io/respx/). `tests/utils.py` has helpers for paginated endpoints.
6. Run the linters and the tests as described below.

## Adding and running examples

You can add example scripts to the `examples/` directory.

```py
# add an example to examples/<your-example>.py

#!/usr/bin/env -S rye run python
…
```

```sh
$ chmod +x examples/<your-example>.py
# run the example against your api
$ ./examples/<your-example>.py
```

## Using the repository from source

If you’d like to use the repository from source, you can either install from git or link to a cloned repository:

To install via git:

```sh
$ pip install git+ssh://git@github.com/e-invoice-be/e-invoice-py.git
```

Alternatively, you can build from source and install the wheel file:

Building this package will create two files in the `dist/` directory, a `.tar.gz` containing the source files and a `.whl` that can be used to install the package efficiently.

To create a distributable version of the library, all you have to do is run this command:

```sh
$ rye build
```

Then to install:

```sh
$ pip install ./path-to-wheel-file.whl
```

## Running tests

The tests use [pytest](https://docs.pytest.org/) and mock the HTTP layer with [respx](https://lundberg.github.io/respx/).
You do not have to start a server.

```sh
$ ./scripts/test
```

This runs the test suite, and then runs it again with Pydantic v1. Arguments are passed on to `pytest`, so you can
run one file:

```sh
$ ./scripts/test tests/api_resources/test_stats.py
```

## Linting and formatting

This repository uses [ruff](https://github.com/astral-sh/ruff) to lint and format the code, and
[ty](https://github.com/astral-sh/ty) to check the types.

To lint:

```sh
$ ./scripts/lint
```

To format and fix all ruff issues automatically:

```sh
$ ./scripts/format
```

### Type checking

`./scripts/lint` runs `ty check` on `src` and `tests`. To run only the type checker:

```sh
$ rye run typecheck
```

The configuration is in the `[tool.ty]` sections of `pyproject.toml`. To suppress a diagnostic, use
`# ty: ignore[<rule>]` with the name of the rule. A suppression without a rule name, a `# type: ignore` comment
or a suppression that is not necessary is an error.

Our users check their code with pyright and mypy. These tools are not dev dependencies. A separate script runs
pinned versions of them with [`uvx`](https://docs.astral.sh/uv/) on one file, `tests/typecheck/consumer.py`,
which uses the public API as a user does:

```sh
$ ./scripts/typecheck-consumers
```

The script needs [uv](https://docs.astral.sh/uv/getting-started/installation/) on your `PATH`.
`./scripts/bootstrap` installs it on macOS.

When you change the public API, add the new usage to that file.

ty replaced pyright (strict mode) and mypy. With our configuration, ty does not have these checks:

- Reports of unknown or partially unknown types (pyright `reportUnknownMemberType`, `reportUnknownArgumentType`,
  `reportUnknownVariableType`, `reportUnknownParameterType`; mypy `warn_return_any`).
- Reports of missing annotations (pyright `reportMissingParameterType`; mypy `disallow_untyped_defs`,
  `disallow_incomplete_defs`, `disallow_untyped_calls`).
- Reports of a class that has `Any` as a base class (mypy `disallow_subclassing_any`).
- Reports of unreachable code (mypy `warn_unreachable`).
- Reports of unused variables, classes and functions (pyright `reportUnusedVariable`, `reportUnusedClass`,
  `reportUnusedFunction`). ruff reports unused imports.
- The check of the public type completeness (`pyright --verifytypes`).

ty has a smaller check for comparisons, `in` tests and `isinstance` calls that always give the same result
(pyright `reportUnnecessaryComparison`, `reportUnnecessaryContains`, `reportUnnecessaryIsInstance`; mypy
`strict_equality`). The ty rule `redundant-condition-strict` reports them only when they are a condition, for
example of an `if` statement, and not when the branch only raises an exception.

## Publishing and releases

Releases are automated. A GitHub workflow keeps a release pull request with the title `release: X.Y.Z` up to date
with the changes on `main`. When this pull request is merged, the version is tagged, a GitHub release is created
and the package is published to PyPI.

The release pull request builds the changelog from the commit messages, so use
[Conventional Commits](https://www.conventionalcommits.org/) (for example `feat:` and `fix:`) for the commits that land on `main`.

If the automated publish fails, you may want to publish manually.

### Publish with a GitHub workflow

You can publish to PyPI by running [the `Publish PyPI` GitHub action](https://www.github.com/e-invoice-be/e-invoice-py/actions/workflows/publish-pypi.yml). This requires an organization or repository secret to be set up.

### Publish manually

If you need to manually release a package, you can run the `bin/publish-pypi` script with a `PYPI_TOKEN` set on
the environment.
