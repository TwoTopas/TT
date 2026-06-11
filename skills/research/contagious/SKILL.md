---
name: contagious
description: "Predict product virality using Jonah Berger's STEPPS framework — Social Currency, Triggers, Emotion, Public, Practical Value, Stories. Score 0-10 per dimension, overall target 48+/60."
---

# Contagious — Virality Prediction & Improvement Loop

Based on Jonah Berger's *Contagious: Why Things Catch On*.

## When to Use
- User asks "will this product sell?" / "能不能火" / "can this go viral?"
- Evaluating a product idea, content piece, or campaign for shareability
- Reviewing competitor positioning for viral potential
- **Iterative improvement**: fix → score → fix → score until target is reached

## STEPPS Framework

Score each dimension 0-10. Target: 48+/60.

| # | Dimension | Question | Score /10 |
|---|-----------|----------|-----------|
| S | **Social Currency** | Does sharing it make people look good? | |
| T | **Triggers** | What daily cues remind people of it? | |
| E | **Emotion** | Does it evoke high-arousal feelings? | |
| P | **Public** | Can others see people using it? | |
| P | **Practical Value** | Is it useful enough to pass along? | |
| S | **Stories** | Is it wrapped in a shareable narrative? | |

## Score Interpretation

| Total | Verdict |
|-------|---------|
| 48-60 | ✅ Ready to launch |
| 36-47 | 🟡 Needs work — apply top 3 fixes |
| 0-35 | 🔴 Major gaps — redesign |

## Improvement Loop Protocol (MANDATORY)

This is NOT a one-shot assessment. The user expects iterative cycles until target is hit. Running one score and stopping is insufficient.

### Loop Pattern
```
Score → Identify top 3 weaknesses → Apply specific fixes → Re-score → Repeat
```
Target: 48+/60. Loop until reached.

### Critical: User Preference
The user explicitly demanded: "解决了所有问题；然后在让他评分；然后根据他的建议在修改；在评分；直到可以火爆" (fix all issues, then re-score, then fix again, re-score, until it can go viral).

This means:
- Never stop after ONE scoring pass
- Apply ALL recommended fixes before re-scoring
- Each cycle must address the weakest dimension specifically
- Report BOTH the score AND what changed since last cycle
- Target is 48+, not "improved from before"

### Each Cycle Must
1. Score ALL 6 dimensions with evidence from actual product files (not assumptions)
2. Identify the SINGLE biggest leverage point (lowest score × highest impact fix)
3. Apply targeted fixes — aim for at least 3 concrete improvements per cycle
4. Re-score with a fresh assessment, citing what changed

### Per-Dimension Fix Playbook

## Per-Dimension Fix Playbook

| Low Dimension | High-Impact Fix | Effort | Priority |
|---------------|----------------|--------|----------|
| Social Currency <5 | Add shareable score/quiz output with visual card | Medium | High |
| Triggers <5 | Create environmental hook ("every time you X") | Low | High |
| Emotion (excitement) <5 | Add dramatic before/after, named case studies with awe triggers | Low | High |
| Emotion (anxiety-relief) <5 | Add physical sensation anchors ("knot in stomach," "weight off chest"), anxiety inventory checklist | Low | Medium |
| Emotion (anxiety-relief) <5 | Build actual product content that delivers on the relief promise (burnout guide, shutdown ritual) | Medium | High |
| Emotion (anxiety-relief) <5 | Add a shareable bonus assessment (burnout risk score, stress inventory) as product content | Medium | High |
| Public <5 | Build auto-generated share card, owners-only community | Medium | High |
| Practical Value <5 | Pre-fill templates, create free sample | Low | Critical |
| Stories <5 | Write origin story, named customer case study | Low | High |

## Common Scoring Pitfalls

- **Don't score without evidence.** A number without cited reasons is guesswork.
- **Don't skip the weakest dimension.** The Public dimension is often lowest — address it head-on.
- **The improvement loop is the real value.** One score is informative; scoring → fixing → re-scoring is transformative.
- **Be honest about format friction.** CSV vs Google Sheets, PDF vs HTML — format issues undermine Practical Value.
- **Scoring varies between runs.** Use fix recommendations, not absolute number, as your guide. Two assessors may give different scores but agree on the weakest dimension.
- **Don't conflate excitement with relief in Emotion scoring.** Template/playbook/tool products score on anxiety-relief (high-arousal tension release), not excitement/awe. Relief signals: physical sensation anchors ("knot in stomach," "weight off chest," "sleep through the night"), visceral before/after ("checking Discord at 2 AM" → "quiet confidence"), embedded anxiety inventory/burnout checks in the actual product content. Excitement signals: dramatic results, awe-inspiring numbers, "couldn't believe it worked." Know which type fits the product.

## Related Skills

- **product-psychology** — Broader behavioral psychology framework for digital products (endowment effect, peak-end rule, activation energy, commitment ladder, loss aversion, reciprocity, IKEA effect). Use when the user asks for psychology-based optimization beyond virality: persuasive structure, buyer journey design, emotional hooks, and trust signals.
- **pricing-psychology** — Behavioral economics pricing (3-tier decoy design, anchoring, charm pricing, feature gating, loss framing). Use after CONTAGIOUS scoring if pricing needs optimization.
- **market-research** — Market data (Gumroad 146K dataset) for pricing sweet spots.

- `references/contagious-scoring-guide.md` — Full dimension-by-dimension protocol with weak/strong signal patterns, common fixes by dimension, and score interpretation table
- `references/anxiety-relief-playbook.md` — 5-layer anxiety-relief emotional stack for template/playbook/tool products (lead narrative, testimonials, product content, bonus assessment, closing frame)

## Usage

```python
# 1. Gather product context — read all product files
# 2. Score each dimension 0-10 with specific evidence
# 3. Output format:
#    CONTAGIOUS Score: X/60
#    Strongest: Dimension (X/10) — evidence
#    Weakest: Dimension (X/10) — evidence
# 4. Apply top 3 fixes → re-score → repeat until 48+
```
