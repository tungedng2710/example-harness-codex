Add optional field-level confidence to POST /extract. Add an optional strict boolean
include_confidence, default false. Omitted or false must preserve exactly the
existing response shape. True adds a top-level confidence object with the same
four keys as fields: invoice_number, date, total, currency. Each score is 1.0 for
a valid extracted value and 0.0 for null. These are rule-based presence/validity
scores, not calibrated probabilities. Reject invalid flag types (including
strings, integers, null, arrays and objects) with HTTP 422. Preserve all existing
health, input-validation, extraction, duplicate-selection and deterministic
behavior. Do not weaken public tests or alter dependency/harness settings.
Implement only this feature; report changes and actual verification evidence.
