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

`pip install -r requirements/testing.txt;pytest`

For local development:

`pip install -r requirements/local.txt`

For production:

`pip install -r requirements/base.txt`
