# Security & Legal Baseline

Default standing rule. Applies before launch and on every material change. If this baseline conflicts with a project-specific instruction, the stricter rule wins. If a rule is consciously waived for a project, document the waiver and the reason in that project's docs.

## Original pre-launch checklist (preserve verbatim)

→ privacy policy if you collect user data
→ know where user data is stored
→ check security headers
→ scan against OWASP basics
→ look for SQL injection / XSS / auth issues
→ make sure .env values are not leaking
→ check API responses for sensitive data
→ remove secrets from logs
→ never expose API keys in frontend code
→ move keys server-side or behind a proxy
→ add rate limits before someone burns your API bill

---

## Extended security baseline

### Secrets & credentials

→ no API keys, tokens, or passwords in client-side JS, HTML, or build artifacts
→ .env never committed; verify .gitignore covers `.env`, `.env.local`, `.env.*.local`, `*.pem`, `*.key`
→ run gitleaks or trufflehog against the repo before every push to a public remote
→ rotate any key that ever touched a public commit, even if force-pushed (assume it was scraped)
→ secrets stored in a vault or platform secret manager, not in code, not in chat history, not in screenshots
→ separate keys per environment (dev, staging, prod) so a leaked dev key cannot touch prod data
→ every key has a documented owner, expiration, and rotation schedule
→ BYOK by default for any tool touching paid third-party APIs

### Transport & headers

→ HTTPS enforced site-wide; HTTP redirects to HTTPS
→ HSTS header set with `max-age=31536000; includeSubDomains`; preload only after verifying every subdomain is HTTPS
→ Content-Security-Policy set; no `unsafe-inline` or `unsafe-eval` unless justified and documented
→ X-Frame-Options: DENY (or CSP `frame-ancestors 'none'`)
→ X-Content-Type-Options: nosniff
→ Referrer-Policy: strict-origin-when-cross-origin
→ Permissions-Policy locks down camera, microphone, geolocation, payment unless required
→ CORS allowlist is explicit; never `Access-Control-Allow-Origin: *` on authenticated endpoints
→ Subresource Integrity (SRI) hashes on every script loaded from a CDN
→ run securityheaders.com against production; B grade is the floor, A is the target

### Auth & sessions

→ passwords hashed with bcrypt, argon2, or scrypt; never md5, sha1, or plaintext
→ MFA available for any account with paid access, admin access, or PII access
→ session cookies set HttpOnly, Secure, SameSite=Lax (Strict for high-sensitivity flows)
→ session tokens rotated on privilege change (login, password reset, role grant)
→ account lockout or progressive delay after repeated failed login attempts
→ password reset tokens expire in under 60 minutes and are single-use
→ OAuth state parameter validated on every redirect back from provider
→ logout invalidates the session server-side, not just by clearing the client cookie
→ JWT secrets long and rotated; algorithm pinned (never accept `alg: none`)

### Authorization

→ every endpoint checks the caller has permission for the specific resource being touched (broken access control is OWASP A01)
→ never trust client-sent user IDs, tenant IDs, or role flags for authorization decisions
→ admin routes sit behind a separate auth layer or IP allowlist
→ object-level checks: a user can only read or modify rows they own
→ horizontal access control tested before launch (try to read user B's data while logged in as user A)

### Input & output

→ all user input validated server-side; client-side validation is UX, not security
→ parameterized queries or ORM bindings for every database call; no string concatenation of SQL
→ output encoded for the context it lands in (HTML body, HTML attribute, JS string, URL component)
→ file uploads: extension allowlist, MIME verification, magic-byte verification, malware scan if public, size cap, storage outside the webroot
→ size limits on every request body, JSON payload, and upload
→ SSRF protection: validate any URL the server fetches; block private IP ranges (10.x, 172.16-31.x, 192.168.x, 169.254.x, ::1, fc00::/7) and metadata endpoints (169.254.169.254)
→ never use `eval`, `new Function()`, `dangerouslySetInnerHTML`, or `shell=True` on user-controlled input

### Rate limits & abuse

→ per-IP and per-user rate limits on every public endpoint
→ stricter limits on auth endpoints (login, signup, password reset, email verification)
→ tightest limits on anything that costs money (LLM calls, SMS, email, paid third-party APIs)
→ Cloudflare or equivalent WAF in front of the origin for DDoS and bot mitigation
→ captcha or proof-of-work on public signup, contact, and password-reset forms
→ webhook endpoints verify HMAC signature before processing the body
→ hard ceiling on per-user spend before lockout, not just per-request rate

### Data handling

→ database connections require TLS
→ application database user has minimum required permissions; no superuser, no DROP, no CREATE in prod
→ PII encrypted at rest where the platform supports it
→ no PII in URLs, query strings, or referrer headers
→ no PII in logs, analytics events, error reports, or screenshots saved for debugging
→ payment data never touches our servers; Stripe or processor handles card capture; PCI scope minimized
→ backup data treated with the same protections as live data

### Logging & monitoring

→ no secrets, tokens, passwords, session IDs, or full PII in any log line
→ admin and sensitive actions logged with actor ID, timestamp, IP, action, target resource
→ error reporting (Sentry or equivalent) configured to scrub PII before transmission
→ uptime monitor on every public endpoint
→ alerts wired up for auth failure spikes, 5xx spikes, latency spikes, cost spikes on metered APIs
→ log retention defined and enforced; default 30 days for ops logs, 1 year for audit logs

### Dependencies & supply chain

→ run `npm audit`, `pip-audit`, or equivalent before launch; zero high or critical findings
→ Dependabot or Renovate enabled on every repo
→ no abandoned packages (no commits in 2+ years) without a conscious documented choice
→ lockfile committed (package-lock.json, yarn.lock, pnpm-lock.yaml, requirements.txt with hashes)
→ pin major versions in production builds
→ verify package names before install (typosquatting is real); copy from official docs, never type from memory

### DNS & email infrastructure

→ SPF, DKIM, and DMARC records configured on every domain that sends mail
→ DMARC policy at `p=reject` for production sending domains after a monitoring period
→ CAA records limit which certificate authorities can issue certs for the domain
→ DNSSEC enabled where the registrar supports it
→ registrar account on its own MFA, separate from any other login

### Backup & recovery

→ database backed up daily, retention at least 30 days
→ restore tested at least once before launch, then quarterly
→ backups stored in a different region or different provider from primary
→ recovery procedure documented in the project's docs with RTO and RPO targets

### AI / LLM specific

→ user prompts treated as untrusted input; prompt injection defense applied to anything the LLM output then acts on
→ LLM output never executed as code, SQL, shell, or filesystem commands without explicit validation
→ no PII sent to third-party LLM APIs unless the vendor's DPA covers it and the user consented
→ per-user usage caps: token limits, request limits, daily cost ceilings, hard cutoff above ceiling
→ kill switch to disable AI features if the upstream provider behaves badly or pricing changes
→ disclose to users that AI is in use and that output may be wrong; do not present AI output as authoritative human advice
→ prompt and response logs scrubbed of PII; retention under 30 days unless legal hold applies

### Pre-launch verification

→ run OWASP ZAP or Burp Suite baseline scan against staging
→ run securityheaders.com check; B grade minimum
→ run ssllabs.com check; A grade minimum
→ verify no test endpoints, debug routes, swagger UIs, or default admin accounts in prod
→ verify production error pages return generic messages with no stack traces, no framework version, no file paths
→ verify `/.git`, `/.env`, `/wp-config.php`, `/phpinfo.php`, and similar paths return 404 or 403
→ verify robots.txt does not leak sensitive paths by trying to hide them

---

## Legal & compliance baseline

### Required pages on every public site

→ Privacy Policy: what data is collected, why, how long retained, who it is shared with, user rights, contact for data requests
→ Terms of Service: license grant, acceptable use, limitation of liability, indemnity, governing law, dispute resolution, severability
→ Cookie notice if any non-essential cookies are used (GDPR, ePrivacy, CCPA)
→ Refund policy if anything is sold
→ DMCA contact and takedown procedure if user-generated content is hosted
→ Affiliate disclosure on every page with affiliate links (FTC 16 CFR Part 255)
→ Accessibility statement targeting WCAG 2.1 AA

### Data subject rights (GDPR, CCPA, similar regimes)

→ user can export their data in a portable format
→ user can delete their account and all associated data
→ user can see what data is held about them
→ requests fulfilled within 30 days (GDPR) or 45 days (CCPA)
→ data retention policy documented with concrete deletion schedules per data category
→ children's data: COPPA applies under 13 in the US; do not collect without verifiable parental consent

### Consent & marketing disclosure

→ cookie banner with granular consent (accept, reject, customize); no pre-checked boxes; reject is as easy as accept
→ email subscribers double opt-in; every send has an unsubscribe link and a physical mailing address (CAN-SPAM)
→ SMS opt-in is explicit and logged; STOP keyword honored; "msg & data rates may apply" disclosed at opt-in (TCPA)
→ AI-generated content disclosed where required (CA AB 2013, EU AI Act for high-risk uses)
→ subscription auto-renewal disclosed clearly before purchase; cancellation must be as easy as signup (CA, NY, FTC click-to-cancel rule)
→ testimonials and reviews comply with FTC endorsement guides; disclose material connections

### Vendor & subprocessor management

→ maintain a list of every vendor that touches user data (DB host, email sender, analytics, LLM provider, payment processor, CDN, error reporter)
→ Data Processing Agreement signed with each one when handling EU, UK, or California resident data
→ each vendor's privacy policy linked from your own privacy policy
→ breach notification process documented; GDPR requires authority notification within 72 hours

### Business protection

→ LLC, S-Corp, or equivalent entity formed; personal assets shielded
→ EIN obtained; business bank account separate from personal accounts; no commingling
→ trademark search on brand name before launch; file registration if the brand is core
→ work-for-hire and IP assignment clauses in every contractor agreement; signed before work begins
→ E&O or cyber liability insurance for any project with paying customers, PII at scale, or contractual obligations
→ sales tax registration in every state where economic nexus is triggered (Wayfair thresholds vary by state)
→ keep corporate formalities (annual report, registered agent, separate records) to preserve the liability shield

### Industry-specific (apply when relevant)

→ HIPAA if any protected health information is involved
→ GLBA if any consumer financial account data is involved
→ FERPA if student education records are involved
→ COPPA if any user under 13
→ PCI-DSS if card numbers are stored; avoid scope by using Stripe Elements or Checkout
→ SOC 2 Type II if selling to enterprise buyers with security review

---

## Hard rules (never violate)

→ never store passwords in plaintext or reversibly encrypted
→ never log credentials, tokens, session IDs, or raw payment data
→ never put secrets in frontend bundles, public repos, public screenshots, or chat with third parties
→ never use `eval`, `new Function()`, `dangerouslySetInnerHTML`, or `shell=True` on user input
→ never auto-fill payment or identity forms on behalf of users
→ never accept terms, grant permissions, or complete OAuth flows on behalf of users without explicit confirmation in chat
→ never bypass CAPTCHA or bot detection
→ never scrape or compile facial images, biometric data, or PII across multiple sources
→ never deploy to prod from a laptop without 2FA on the deploy account
→ never disable security features (CSRF, signed cookies, rate limits) "temporarily" without a ticket to re-enable

---

## Stack-check before adding tools

Before adopting a new security or compliance tool, verify the lifetime stack and existing platform features do not already solve it. Cloudflare covers WAF, rate limit, DDoS, bot management. Most hosts ship HSTS, TLS, and basic headers out of the box. Stripe handles PCI scope. Many of these baseline items are configuration, not new purchases.

---

## Audit cadence

→ full review of this checklist before every launch
→ quarterly review on any project with paying users or PII
→ immediate review after any incident, dependency CVE that affects the stack, or material feature change
→ rotate keys, review access lists, and re-run scans on the quarterly cadence
