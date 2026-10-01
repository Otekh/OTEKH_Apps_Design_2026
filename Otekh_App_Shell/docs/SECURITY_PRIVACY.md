# OTEKH Security & Privacy Guide

How OTEKH applications handle authentication, sessions, administration, and
privacy. This document is part of the design system — it applies to every
OTEKH web app, and by principle to desktop/Tkinter apps that manage users.

## The no-cookie ethics protocol

**OTEKH apps ship with zero cookie tracking. The lab is not in the business
of surveillance.** Every web app must function properly and securely with
cookies entirely disabled or cleared at any moment.

The rules:

- **No cookies are required.** A user who blocks or deletes every cookie
  must still be able to sign in and use the app fully. Authentication rides
  on a session token sent as a request header (`Authorization: Bearer …`
  or `X-Session-Token`), which the client holds in memory or per-tab
  `sessionStorage` — never in a cookie.
- **No tracking, period.** No analytics cookies, advertising identifiers,
  fingerprinting, third-party pixels, beacons, or cross-site identifiers.
  No exceptions.
- **Cookie fallback is optional and first-party only.** If an app needs an
  HttpOnly cookie so that full-page loads or non-JS clients can attach a
  session, it may set exactly one: first-party, `HttpOnly`,
  `SameSite=Lax`, no `Domain` attribute (host-only), shortest practical
  lifetime. It must contain *only* the session token — no profile data,
  preferences, or identifiers reused across sessions. The app must treat
  it as a convenience copy of the header token, never the source of truth,
  and must keep working when it is absent.
- **Never gate features on consent walls.** There is nothing to consent
  to: no tracking means no cookie banners, no opt-out toggles, no dark
  patterns.
- **Storage is for the user's benefit.** `sessionStorage`/`localStorage`
  may hold UI convenience state (current view, last-opened panel) and the
  live session token. Nothing stored may outlive its purpose, identify the
  user to a third party, or be sent anywhere the user didn't direct.
- **Honest status.** The interface must never claim data is "private" or
  "local" when it is transmitted or shared. See STYLE_GUIDE.md §11 for the
  trust rules this extends.

Both shipped apps already follow this pattern:

- **OTEKH Lab Workspace** — `app/lib/auth-client.ts` keeps the token in
  `sessionStorage` and sends it as `Authorization: Bearer`; the
  `__otekh_session` HttpOnly cookie exists only as a page-load fallback,
  and `app/lib/auth-token.ts` checks the Bearer header first.
- **OTEKH Data Cleaning** — `backend/main.py` resolves sessions from the
  `X-Session-Token` header first and only then from the `session_token`
  cookie; `static/app.js` stores the token in `localStorage` as a
  convenience, not a requirement.

## Authentication

- **Credentials file.** Bootstrap credentials live in a separate `auth`
  file (e.g. `backend/auth`, or `$OTEKH_AUTH_FILE`) with `username=` /
  `password=` lines, read at startup and seeded into the user store.
  Editing the file and restarting rotates the credential. The file is
  gitignored and must never be committed, logged, or rendered in the UI.
- **Password storage.** Passwords are stored as salted hashes (PBKDF2 or
  stronger). Plaintext passwords exist only in the credentials file the
  owner controls.
- **Masked input.** Password fields always use `type="password"` (or a
  masked Tkinter entry) — in the login card, the user manager, share
  prompts, and anywhere else a secret is typed. Never echo passwords to
  logs, status bars, or error messages.
- **Session tokens.** Opaque random tokens (or HMAC-signed payloads) with
  a bounded lifetime. Logout invalidates the token server-side. Do not
  expose tokens in URLs.
- **Login surface.** The shared `.otekh-login` card: full OTEKH logo,
  uppercase display title, labelled User and Password fields, inline
  error text (`otekh-login__error`), one primary Enter action. Passwords
  may be optional for low-privilege read roles, required for
  admin/expert/lead roles.
- **Password reset** (when email exists): single-use tokens with short
  expiry, delivered by email or written to a local `emails/` folder when
  SMTP is not configured.

## Roles and administration

- **Role set.** Each app defines a small ordered role set (e.g.
  `admin / expert / user`, or `admin / lead / member`). Elevated roles
  must require a password.
- **User menu.** The right-aligned `.otekh-menu` in the top bar shows
  `name · role` (role in gold). Standard items, in order: app actions,
  **Profile**, **Manage users** (admin only — hidden for other roles),
  **Sign out** (`--warn`), destructive app actions such as **Shut down**
  (`--danger`, last). Admin items are hidden in the UI *and* enforced
  server-side — hiding alone is not authorization.
- **User management UI.** A modal (`usersModal` pattern): a table of
  users with name, role, and password-set state; an add-user row with
  name, role select, and a masked password field; delete/rename guarded
  by confirmation naming the user.
- **"View as" preview** (optional): admins may preview the app as a lower
  role. Show the active preview state in the menu button
  (`Viewing as member`) and require an explicit "Return to admin" path.
- **Least exposure.** Public/unauthenticated endpoints return the minimum
  needed (e.g. the login user list exposes names and roles only — never
  hashes, emails, or IDs that enable enumeration).

## Sharing and external access

- **Share links are opt-in and password-protected.** Sharing binds the
  server outward only when the operator chooses it at launch; the UI
  shows the link and its password (`SHARE_ENABLED` / `SHARE_PASSWORD`
  pattern). Share sessions expire with the app and get a scoped role,
  never admin.
- **No third-party calls for auth.** Authentication is local — the app's
  own user store, never an external identity service or tracker.
- **Error hygiene.** Errors shown to users never leak absolute paths,
  secrets, tokens, or stack traces. Log details server-side; show the
  user a plain-language cause and next step.

## Idle and shutdown

- Local and lab-hosted apps may expose **idle warning → auto-shutdown**
  (`IDLE_WARN_TIMEOUT` / `IDLE_SHUTDOWN_TIMEOUT`) with an explicit
  "still here" prompt, and a user-menu **Shut down** action reserved for
  the primary/admin user. These keep shared lab machines from running
  unattended sessions — a security feature, not a convenience.

## What must never ship

- Tracking or advertising technology of any kind.
- Cookies that store anything but a single session token.
- Third-party analytics, fonts fetched at runtime, CDN-hosted libraries
  that phone home, or telemetry sent off the user's machine.
- Plaintext passwords in databases, logs, UI, or committed files.
