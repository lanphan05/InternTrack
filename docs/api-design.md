# InternTrack Data and API Design

## Purpose

The API stores and retrieves internship applications for one user. The first
implementation may store data in memory while we develop the endpoints.
Before the MVP is complete, SQLite will replace in-memory storage so records
survive a server restart.

## Application record

| Field | Type | Rule |
|---|---|---|
| id | Integer | Unique ID assigned by the server; clients cannot choose it |
| company | String | Required; must contain non-whitespace characters |
| role | String | Required; must contain non-whitespace characters |
| link | String or null | Optional job-posting link |
| status | String | `wishlist`, `applied`, `interview`, `offer`, or `rejected`; defaults to `wishlist` |
| date_applied | Date or null | Optional; formatted as `YYYY-MM-DD` in JSON |
| notes | String | Optional; defaults to an empty string |

When creating or updating a record, the client sends every field except `id`.
The server returns the saved record, including its `id`.

## Endpoints

| Method | Path | Purpose | Success |
|---|---|---|---|
| POST | `/applications` | Create an application | `201 Created` and the saved record |
| GET | `/applications` | List applications | `200 OK` and an array |
| GET | `/applications/{id}` | Get one application | `200 OK` and the record |
| PUT | `/applications/{id}` | Replace an application | `200 OK` and the updated record |
| DELETE | `/applications/{id}` | Delete an application | `204 No Content` |

### Create an application

`POST /applications`

Example request:

```json
{
  "company": "IBM",
  "role": "Software Developer Intern",
  "link": "https://example.com/job",
  "status": "applied",
  "date_applied": "2026-11-26",
  "notes": "Applied through the careers page."
}
```

On success, return `201 Created` with the saved fields and a new `id`.
Invalid input returns `422`; no application is saved.

### List and filter applications

`GET /applications` returns all applications. If none exist, it returns `[]`.

`GET /applications?status=applied` returns only applications whose status is
`applied`. A valid status with no matches returns `[]`. An unsupported status
returns `422`.

### Get one application

`GET /applications/{id}` returns the application with that ID. If it does not
exist, return `404 Not Found`.

### Replace an application

`PUT /applications/{id}` accepts the application fields except `id`. Because
this is a full replacement, omitted optional fields take their documented
defaults. A successful request returns the complete updated record.

Invalid input returns `422` and leaves the saved record unchanged. An unknown
ID returns `404`.

### Delete an application

`DELETE /applications/{id}` removes the record and returns `204 No Content`
with an empty response body. An unknown ID returns `404`.

## Health check

`GET /health` returns `200 OK` and `{"status": "ok"}`.

## First release boundaries

This API serves a single user and has no accounts or login. Do not deploy
personal application records on a publicly accessible instance without
protecting access. Skill extraction and resume matching are planned for a
later release.
