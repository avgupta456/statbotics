# Statbotics API

The Statbotics Python API queries the Statbotics backend and returns data in a JSON format. It is distributed via PyPI.

## Testing

```
pip install pytest
pytest tests/
```

## Deployment

1. Update `version` in `pyproject.toml`
2. Delete old distributions in `/dist`
3. Run the following scripts:

```
pip install build twine
python -m build
twine upload dist/*
```
