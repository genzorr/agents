# Pi accounts

The canonical account tool is [genzorr/pi-accounts](https://github.com/genzorr/pi-accounts). Its repository owns the CLI, synthetic auth/UX tests, readable account and email display, manual selection and rename, quota checks, and optional native macOS/Linux hourly maintenance. Follow its versioned README for Node/Pi requirements, installation, browser versus optional device login, inspection and uninstall. Agents does not keep a second auth implementation or manage the external package's installed files.

The tool remains Pi-only: it uses Pi's native OAuth and credential-storage primitives with a small private saved-account pool. Account/workspace ID is identity; email is display metadata. There is no Codex/CMA credential migration or shared token-refresh owner. A working saved Pi account does not require another login just because the CLI display or package installation changes.

For an older Agents-managed installation, follow `pi-setup.md` to preview explicit retirement of unchanged legacy CLI and maintenance files before installing the standalone package. Keep user login/switch operations idle, pause the legacy timer and let an active refresh finish. The private Pi auth store, account pool, selection and sessions remain in place. Never force an npm overwrite of a foreign or legacy wrapper.

Agents retains canonical ownership of the `agentic-local` extension and instruction/skill distribution. Those are separate from the standalone auth package. Reviewed source and installed-state evidence belong in the local work record or PR. Updating the Agents checkout does not update the separately installed account package; use its maintenance-safe update procedure.
