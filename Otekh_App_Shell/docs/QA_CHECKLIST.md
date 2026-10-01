# OTEKH Release QA Checklist

## Identity

- Correct OTEKH asset and product name used.
- Logo is not stretched, recoloured, or crowded.
- App icon remains identifiable at 32 px.

## Visual system

- Components use shared tokens rather than hard-coded near-matches.
- Gold is reserved for selection, active data, and primary action.
- No gradients, gloss, fake depth, or decorative shadows.
- Typography follows the three-family role system.
- Spacing follows the 4 px scale.

## Interaction

- Hover, focus, active, selected, disabled, loading, offline, error, and success states exist where relevant.
- Unsaved work is visible.
- Destructive actions name the object and consequence.
- Long processes expose progress and safe cancellation.

## Accessibility

- Keyboard path completed.
- Focus is visible.
- Contrast checked.
- Status does not rely on colour alone.
- Accessible names and labels verified.
- Zoom/reflow and reduced motion checked.
- Charts have an accessible alternative.

## Data and trust

- Storage/sync location is accurate.
- Model or automated processing is identified where relevant.
- Generated and verified knowledge are distinguished.
- Permissions, access level, and provenance are visible for archive material.
- Error messages do not expose secrets or sensitive paths.

## Privacy and security

- App functions fully with all cookies blocked or cleared (no feature depends on a cookie).
- No tracking of any kind: no analytics, advertising, fingerprinting, or third-party identifiers; no cookie/consent banners.
- At most one first-party `HttpOnly; SameSite=Lax` session cookie, used only as an optional fallback for the header token — see `SECURITY_PRIVACY.md`.
- Passwords masked in every UI field; stored salted+hashed; bootstrap credentials in the gitignored `auth` file only.
- Admin-only features hidden for other roles in the UI and re-enforced on the server.
- Session tokens never appear in URLs; logout invalidates them server-side.

## Platform

- macOS package and window behaviour checked.
- Linux package, font availability, and filesystem paths checked.
- Offline start and reconnection checked.
- Narrow layout checked where web/mobile support is promised.

