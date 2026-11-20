# Content data schema

The seed JSON files are plain arrays. The admin workspace normalizes each record to plain fields with a generated `id`, `lang`, `status`, `translationGroup`, `createdAt`, and `updatedAt`. Top-level exports use `{ "schemaVersion": 1, "exportedAt": "ISO-8601", "collections": { ... } }`.

- `projects.json`: `name`, HTTPS `url` (optional), `category`, `status`, `description`, `role`, `technologies`, HTTPS `repository`, and `screenshot`; optional `plannedModules` is a string array.
- `education.json`: `period`, `institution`, `location`, `program`, `description`, and `status`.
- `timeline.json`: `date` (ISO date or null), `label`, `title`, `description`, `category`, and optional `dateToBeConfirmed`.

Admin content remains local to the owner's browser until exported. Never put private data in the repository. Imported exports are validated before storage.
