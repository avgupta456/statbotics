# Statbotics API

The Statbotics Python API queries the Statbotics backend and returns data in a JSON format. It is distributed via PyPI.

## Testing

Requires Python 3.8+.

```
pip install pytest
pytest tests/
```

## Documentation

Requires Python 3.8+. Production builds are triggered directly on the Read the Docs website. You may need to comment out cache control for the build to succeed.

```
pip install sphinx
pip install sphinx_rtd_theme
cd docs
make html
```

## Deployment

Requires Python 3.8+. Requires a PyPI account.

1. Update `version` in `pyproject.toml` and `docs/conf.py`
2. Delete old distributions in `/dist`
3. Run the following scripts:

```
pip install build twine
python -m build
twine upload dist/*
```
