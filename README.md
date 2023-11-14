Took script from here https://github.com/beartype/beartype/issues/58 and rewrote it a little

```bash
poetry install
poetry shell
python -m main

#timeit assert       time: 0.0392 seconds
#timeit beartype     time: 0.1139 seconds
#timeit pydantic     time: 0.1637 seconds
```