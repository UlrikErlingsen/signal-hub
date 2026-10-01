# Security policy

## Supported version

The latest released version of the Hub and the app tags it pins receive security fixes. A vulnerability inside a
tool belongs in that tool's repository; the Hub then pins the fixed release.

## Reporting

Report suspected vulnerabilities privately to the repository owner before public disclosure. Do not include real
customer or respondent data in a report.

## Deployment note

The Hub has no authentication layer. A public deployment needs TLS, upload limits, logging and retention policy,
dependency updates and isolation appropriate to the data people might upload. The Hub writes nothing to disk; uploads
live in the Streamlit session's memory and disappear when the session ends.
