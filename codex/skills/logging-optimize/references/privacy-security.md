# Privacy and security

Open this reference whenever logs contain user, device, location, credentials, exception text,
control input, run identifiers, or data crossing a trust boundary.

## Boundaries and fields

Start with an allowlist tied to diagnostic queries. Classify fields, minimize values, and define
retention, access, rotation, and deletion behavior for each sink. Do not log secrets, tokens,
passwords, private keys, raw credentials, or unrestricted request/body/device payloads. Hashing or
masking is not automatically safe: check re-identification, linkability, and whether the original
value can be reconstructed.

Redact exception messages and stack traces at the sink or ownership boundary without destroying
the failure class and causal information needed for diagnosis. Sanitize newlines, control
characters, terminal escapes, and delimiter/format injection. Bound string length, collection
size, nesting, and serialization work. Keep sensitive fields out of operator stdout if that output
is collected more broadly than the durable sink.

## Tests

Inject representative secrets, PII, control characters, oversized values, malformed objects, and
untrusted user input. Assert that no forbidden value appears in every output path: console, file,
queue fallback, exception rendering, crash breadcrumb, and test capture. Test permission errors,
disk-full behavior, rotation, retention, and collector failure without leaking the original data
through an error handler. Review access to logs as data, not merely as debugging output.
