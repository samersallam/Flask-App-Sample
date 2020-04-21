"""
To run the test:
pytest

To run the test on multiple cores:
pytest -n 3 # 3 is number of processes

To run the test that inside a file has a specific keyword in the name of the file
pytest -k keyword

To run the test with a specific marker
pytest -m marker

To run the test with more details:
pytest --setup-show
pytest --setup-show  --disable-pytest-warnings

Unittest:
https://www.youtube.com/watch?v=6tNS--WetLI&t=413s

Unittest and pytest:
https://www.youtube.com/watch?v=_wSPEoYWX9M&t=834s

Useful link for flask and pytest
https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/?fbclid=IwAR1Xf65En75TKGqND1aBDvYM9c32Xoa_8O2MIVLAwohyDUWHuKjX4hiXp_8

Fixture factory
https://www.youtube.com/watch?v=vpRGmY-s3ak

Flaky tests (for non-deterministic behaviour)
https://docs.pytest.org/en/latest/flaky.html

Useful article for parameterizing tests and fixtures
https://medium.com/ideas-at-igenius/fixtures-and-parameters-testing-code-with-pytest-d8603abb390a

# Mock testing
# https://pypi.org/project/pytest-mock/
# https://stackoverflow.com/questions/41195826/testing-schedule-library-python-time-and-events
"""