# Iterative Visual Refinement Protocol
## When the user says "still not good" or "差别不大"

## Background
This user has strong visual taste and will reject designs that are "close but not quite." They told me "还是差了点" (still lacking) and "你自己审核一下" (review yourself). Do NOT wait for them to point out every flaw — self-critique first before presenting.

## The Process
When user rejects a visual result:

### Phase 1: Self-Audit (before presenting)
Check these specifically before showing:
1. **Spacing**: Is row height adequate? Font-size proportional to container? (38px min for data rows)
2. **Color hierarchy**: Can you distinguish headers from data at a glance? 3 levels max (title, header, data)
3. **Contrast**: Is text readable against its background? Avoid low-contrast gray on gray
4. **Consistency**: Are all sections using the same padding/margin/style? No orphans
5. **Alignment**: Left-align text, right-align numbers — no mixing

### Phase 2: User Says "Still Not Good"
1. Re-read the design spec references immediately
2. Identify the MOST specific complaint: spacing? color? font? contrast?
3. Don't guess — compare your output against a known-good reference (Apple style, Stripe, Linear)
4. Apply ONE category of fix at a time, then present for feedback
5. Common failure patterns in this user's feedback:
   - "行高太低" — Increase row height, it's likely too tight
   - "配色无区分" — Increase contrast between sections
   - "还是差了点" — Usually means the design doesn't look premium enough. Add more whitespace, reduce colors

### Phase 3: Reference-Driven Fixes
- When in doubt, make MORE whitespace
- When in doubt, use FEWER colors (max 3 beyond black/white/gray)
- When in doubt, make text SMALLER for secondary info (9.5pt) and BIGGER for headers (11pt+)
- Apple design rule: everything that CAN be light gray, SHOULD be light gray
