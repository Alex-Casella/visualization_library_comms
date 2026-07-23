# simple-eda — working conventions

A minimal, pandas-first visualization library. Keep changes small and in the
spirit of the existing code.

## Project shape

```
src/simple_eda/{__init__.py, core.py}   # library; core.py holds the engine
examples/{*.py, images/, README.md}     # runnable examples + rendered output
tests/test_core.py                       # pytest smoke tests
README.md · pyproject.toml · LICENSE
```

- The library lives under `src/` (src layout). `__init__.py` only re-exports
  the public API from `core.py`.
- Keep the library core at **200 lines of code or fewer**.

## Conventions

- **Every new `.py` file or example ships with a rendered visualization.**
  When you add or change an example, run it and commit the resulting chart(s)
  to `examples/images/` (PNG). New public features should be demonstrated by an
  example that produces a chart.
- Preserve the fluent, chainable `Chart` API; each layer/styling method returns
  `self`.
- Use the existing colorblind-friendly palette and clean default styling.

## Verify before committing

```bash
pip install -e ".[test]"
pytest -q                 # tests must pass
python examples/quickstart.py   # examples must render without error
```
