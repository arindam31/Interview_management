# DB design

## APPS
- Candidate
- Staff (username, group, permission)
- CandidateProcess
 - InterviewRound
  - Schedule, result, staff, shared_notes
- postions
  - position
  - skill

- postings (is a job posting for a position)
  - Job opening (we can open, close) [posting date, closing date, Position]

## ENV creation for different environments:
On a CI/CD pipeline:

`pip install -r requirements/testing.txt`

For local development:

`pip install -r requirements/local.txt`

For production:

`pip install -r requirements/base.txt`

# ENV file contents (create inside dir "imt")
Mandatory fields and their examples
```markdown
  SECRET_KEY=some_real_secret
  DEBUG=False # Caps bool
  DJANGO_ENV=local/default   # one of these options only
  ALLOWED_HOSTS="127.0.0.1,localhost"   # comma separated ip addresses
```

## Checking code
The project is equipped with flake8. It helps identify errors against PEP8 standard and much more.

Usage:
`flake8`

## Running tests.

- Tests are located under imt/tests.
- Pytest is used.
- To run all tests (you need to be in imt folder in terminal.): 
  - `pytest`
  - `pytest -s` # To see prints too
  - `pytest -s -k "Some class or test name keyword"` # To see prints too
  - Using coverage: `coverage run -m pytest`
  - Using coverage to see a summary: `coverage report`
  - Using coverage to see HTML report: `coverage html` # check htmlcov folder for results under (imt folder)

## Running project
There are few ways and both should always be working.
- While in dir: imt > 
  `python manage.py runserver`

- docker run 
- docker compose up --build # More on docker in documents directory