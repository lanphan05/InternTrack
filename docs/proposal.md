# InternTrack Project Proposal

Prepared by Lan Phan · November 26, 2026 · Draft for review

InternTrack is a single-user application for tracking internship applications. This proposal defines a small first release with persistent application records, then a separately evaluated skill comparison feature. The initial product is designed for a student developer to build and demonstrate with requirements, tests, code review, and a deployed release.

## 1 Team Information

Team name: InternTrack. This proposal assumes a solo portfolio project; confirm course team requirements before submission.

| Team member | Primary roles                                            | Relevant skills and experience                                        |
|-------------|----------------------------------------------------------|---------------------------------------------------------------------------|
| Lan Phan    | Requirements, interface, backend, testing and deployment | Computer science background; Python, FastAPI and React project experience |

## 2 Project Title

InternTrack Internship Application Tracker

## 3 Project Overview

InternTrack is a web application that helps students record internship opportunities and follow each application from a wishlist through its final outcome. It combines an application list, status filtering, and a detail view so users can find a posting, remember what they submitted, and update their progress.

The first release supports application tracking and persistent storage. A later phase will extract skills from a pasted job posting and compare them with an editable list of resume skills. This phase will show the underlying matched and missing skills alongside any percentage so the result can be explained and tested.

## 4 Problem and Motivation

Internship applicants often split information between browser bookmarks, spreadsheets, notes, and job sites. A link may disappear, and a status change may not be recorded consistently. Looking through several sources makes it harder to decide which applications need attention. InternTrack gives one student a structured, searchable record of their own process.

The proposal assumes that one student is willing to enter application details manually and that a lightweight status list is sufficient for the initial workflow. User interviews or trial use may reveal a need for deadlines, status history, or reminders; those are outside the first release. The system does not submit applications on the user’s behalf.

## 5 Customers Users and Other Stakeholders

### 5.1 Customer or Client

The initial client is the student developer, acting as the product owner and deciding which tracking workflow is useful. For a course submission, the instructor reviews the proposal and evidence of implementation. A broader student audience is a possible future customer group, not a committed multiuser requirement.

### 5.2 Users

Primary user: a student tracking their own internship applications. There are no administrator or recruiter roles in the first release. Prospective recruiters viewing the portfolio are stakeholders in the demonstration, not users of private application data.

## 6 User Needs

- Record company, role, link, application date, status and notes in one place.

- Find applications by status and open their details quickly.

- Correct mistaken entries and remove duplicates.

- Keep entries after closing or restarting the application.

- Understand which skills a posting requests and which are absent from an editable personal skill list in a later release.

## 7 Major Features

| Feature                      | Description                                                              | User    | Priority |
|------------------------------|--------------------------------------------------------------------------|---------|--------------|
| Application records          | Create, view, update and delete internship records                       | Student | Must Have    |
| Persistent storage           | Keep records after application restart                                   | Student | Must Have    |
| List and filter              | View all records and filter by status                                    | Student | Must Have    |
| Web interface                | List, add and view record details; edit and delete through API initially | Student | Must Have    |
| Skill extraction             | Identify and normalize skills from a pasted posting                      | Student | Should Have  |
| Skill comparison             | Show matched and missing skills and overlap percentage                   | Student | Should Have  |
| Status history and reminders | Record transitions and alert on deadlines                                | Student | Could Have   |

MVP: application records, persistent storage, status filtering, and a working list/add/detail interface. The API additionally supports editing and deletion. Skill analysis is a second release and does not block MVP acceptance. Public deployment requires access control or sanitized demonstration data because this first release has no login.

## 8 Initial User Stories and Acceptance Criteria

### US-01 Add application

As a student, I want to record an internship application so I can keep its details together.

Acceptance criteria: A valid company and role create one record with a unique ID; missing or blank required values are rejected without saving; omitted status defaults to Wishlist.

### US-02 List applications

As a student, I want to see my applications so I can review my search.

Acceptance criteria: The list shows company, role and status for every stored record; an empty collection shows an understandable empty state.

### US-03 View details

As a student, I want to open one record so I can see its link, date and notes.

Acceptance criteria: An existing ID returns all saved fields; an unknown ID returns 404.

### US-04 Filter by status

As a student, I want to filter by status so I can focus on one stage.

Acceptance criteria: Each defined status returns only matching records; clearing the filter restores all records; a valid status without matches returns an empty list.

### US-05 Edit application

As a student, I want to correct a record so it reflects new information.

Acceptance criteria: A valid update returns and persists the new values; invalid input leaves the old values intact; an unknown ID returns 404.

### US-06 Delete application

As a student, I want to remove a mistaken entry so my list stays accurate.

Acceptance criteria: Deleting an existing record removes it; a later read returns 404; deleting an unknown ID returns 404.

### US-07 Keep records

As a student, I want records to survive a restart so I can return to my search.

Acceptance criteria: Records and unique IDs remain valid after the service restarts.

### US-08 Compare skills

As a student, I want to compare a posting with my saved skills so I can see what to emphasize or learn.

Acceptance criteria: A later release shows normalized matched and missing skills; percentage equals matches divided by posting skills, times 100; zero posting skills yields no percentage; provider failure does not prevent application tracking.

## 9 Functional Requirements

| ID   | Requirement                                                                                             | Story           |
|------|---------------------------------------------------------------------------------------------------------|---------------------|
| FR1  | The system shall create a record with company, role, optional link, status, date and notes.             | US-01               |
| FR2  | The system shall reject blank company or role and unsupported statuses.                                 | US-01               |
| FR3  | The system shall list all applications and retrieve a record by ID.                                     | US-02, US-03        |
| FR4  | The system shall filter records by a supported status.                                                  | US-04               |
| FR5  | The system shall replace the fields of an existing record after validation.                             | US-05               |
| FR6  | The system shall delete an existing record.                                                             | US-06               |
| FR7  | The system shall return 404 for a missing record on detail, update and delete requests.                 | US-03, US-05, US-06 |
| FR8  | The system shall retain records and unique IDs across server restarts.                                  | US-07               |
| FR9  | The interface shall allow users to add and list records and inspect details.                            | US-01–US-03         |
| FR10 | The later release shall store an editable skill list and show normalized matched and missing skills.    | US-08               |
| FR11 | The later release shall calculate an explainable overlap percentage or show unavailable when undefined. | US-08               |

## 10 User Interface Sketches and Navigation

Preliminary low fidelity screen sketches follow. They describe the first release, with skill analysis marked as a later screen.

### Application list

```text
Header: InternTrack | Add button
Status filter: All / Wishlist / Applied / Interview / Offer / Rejected
Rows: Company | Role | Status | Date
```

**User action:** Choose Add, change the filter or open a row.

### Add application

```text
Company [ ] Role [ ] Job link [ ]
Status [Wishlist] Date applied [ ]
Notes [ ]
[Save] [Cancel]
```

**User action:** Save valid fields or return to the list.

### Application details

```text
Company and role | Status
Link | Date applied | Notes
[Back] [Edit via API in initial release]
```

**User action:** Read the complete record and return to the list.

### Skill comparison later

```text
Posting text [ ]
Saved resume skills [edit list]
Matched skills | Missing skills | Overlap
```

**User action:** Paste a posting, inspect extracted skills and review the comparison.

Navigation: Application list → Add application → Application list → Application details → Application list. The future skill comparison screen opens from application details. The first release does not include a login screen.

## 11 Example User Workflows

Workflow 1: Lan finds a software engineering internship and opens the Add application screen. She enters the employer and role, saves it as Wishlist, and sees it in the list. Later she updates its status to Applied through the API. She restarts the service, filters by Applied, opens the record, and sees the saved details. Screens: list → add → list → details; API: update; list → details after restart.

Workflow 2, later phase: Lan pastes the job description into skill comparison and reviews the extracted skill names. She edits her saved skills, sees matched and missing skills and the calculated overlap, then returns to the application details. If analysis is unavailable, she can still open and update the application.

## 12 Proposed Technologies

| Component              | Proposed technology                                          | Reason                                                                                        |
|------------------------|--------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| Front end              | Simple server-rendered page or minimal HTML and JavaScript   | Delivers list, filter and add form without delaying the MVP; React is a possible later iteration. |
| Back end               | Python and FastAPI                                           | Provides validation, typed API contracts and interactive API documentation.                       |
| Database               | SQLite locally; PostgreSQL if supported by selected hosting  | Persistent records locally, with a deployment option for a managed relational database.           |
| Testing                | pytest and FastAPI TestClient                                | Verifies CRUD behavior and error cases automatically.                                             |
| Version control and CI | Git, GitHub and GitHub Actions                               | Supports feature branches, pull requests and automated test runs.                                 |
| Skill analysis later   | IBM watsonx.ai through a replaceable provider interface      | Allows skill extraction while keeping tests deterministic through a fake provider.                |
| Deployment             | IBM Cloud, subject to current service limits and cost review | Creates a public demonstration after private data is protected or replaced with sample data.      |

## 13 Development and Evaluation Plan

Work in short branches: requirements and API design; CRUD API; persistence; minimal interface; test and CI improvements; deployment; then optional skill analysis. Each pull request includes the story IDs, acceptance evidence, and any unresolved risk. Verify the MVP with API tests, a restart persistence check, and a complete add/filter/view flow. Evaluate future extraction against a manually labeled set of 10 postings, reporting actual recall, false positives and response time rather than claiming a target in advance.

## 14 Scope and Open Questions

Outside scope: automated job submissions, browser scraping, email access, multiple user accounts, reminders, and full resume upload. Before public release decide whether to add authentication or show only sample data. Confirm whether this is submitted as a solo project and whether the instructor expects a particular front end stack or additional course deliverables.
