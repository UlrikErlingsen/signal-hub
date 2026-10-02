# Privacy

Signal Hub does not implement telemetry, advertising, user accounts, tracking pixels, analytics scripts, external AI
calls or outbound data uploads. Files you upload are processed in the running Streamlit session's memory by the tool
you opened. They are never written to the server's disk, and they disappear when the session ends.

The Figtree typeface is embedded in the app (SIL Open Font License), so pages make no request to Google Fonts
or any other third-party host.

If someone deploys the Hub, that operator controls infrastructure logs, retention, backups and network access and
must document those practices separately. Do not upload personal or confidential data to a deployment you do not
control. Each tool's own privacy notes still apply; see its repository.
