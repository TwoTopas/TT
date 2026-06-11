# Gumroad HTML Description Pattern

Convert product copy to HTML before passing to `--description`. Gumroad renders this in the description section of the product page.

## Tag Mapping

| Markdown | HTML |
|----------|------|
| Paragraph with blank line | `<p>text</p>` |
| `### Heading` | `<h3>Heading</h3>` |
| `- item` | `<ul><li>item</li></ul>` |
| `> quote` | `<blockquote>text</blockquote>` |
| `---` | `<hr>` |
| `**bold**` | `<strong>text</strong>` |
| `| table |` | `<table><tr><th>...</th></tr><tr><td>...</td></tr></table>` |
| `*italic*` | `<em>text</em>` |
| Line break in quote | `<br>` |

## Structure Pattern

```html
<p>Opening hook. Short sentence. Punchy.</p>

<p>Another short paragraph. Builds tension.</p>

<p>Question?</p>

<p>Answer. Value proposition.</p>

<p><strong>Social proof line with bold.</strong></p>

<blockquote>Testimonial or comparison statement.</blockquote>

<hr>

<h3>Tier Name: $Price</h3>

<p>Tier description.</p>

<p><strong>Section header:</strong></p>
<ul>
<li><strong>Item name</strong> — description</li>
<li><strong>Item name</strong> — description</li>
</ul>

<blockquote>"Testimonial."<br>
<strong>Name, Role, about N members</strong></blockquote>
```

## Key Rules

- Every paragraph in `<p>...</p>` — don't leave any text unwrapped
- Short paragraphs: 1-3 sentences max per `<p>`
- Testimonial attribution on a separate line with `<br>` inside the blockquote
- `<hr>` between major sections
- No markdown anywhere — Gumroad treats `--description` as raw HTML
- No em dash (`—`) per writing-quality rules
- No curly/smart quotes — use straight quotes

## Full Working Example

Below is a complete, tested Gumroad product description HTML from an actual published product (Community Operations Playbook). It demonstrates every tag type in composition.

```html
<p>It's 11 PM and you're scrolling through your server one last time before bed.</p>

<p>#general is quiet. Your last post was 4 hours ago.</p>

<p>You know you should be resting. But there's a knot in your stomach. That nagging feeling you're not doing enough. That members are slipping away quietly. That tomorrow you'll open Discord to the same empty channels and have to make something up on the spot.</p>

<p>Sound familiar?</p>

<p>Here's the thing. You're running your community on anxiety instead of systems. Every day you're making up content, scanning for fires, hoping nobody notices you're making it up as you go.</p>

<p>It's not sustainable. And it's not your fault. Nobody gave you the operating manual.</p>

<p>But now there's one.</p>

<p>This playbook replaces that knot with a Monday morning checklist. A content calendar that's already filled in. A dashboard that catches people before they go quiet. The feeling of wondering "am I doing this right?" gets replaced by knowing you have a system that works.</p>

<p><strong>Trusted by community managers at startups, gaming servers, creator communities, SaaS products, and online courses.</strong> The same infrastructure used by communities from 500 members to 10,000+.</p>

<blockquote>Compared to hiring a community consultant at $150/hour, this costs less than one hour of advice. And you keep it forever.</blockquote>

<hr>

<h3>Lite: $19</h3>

<p>A solid start. Enough to stop the bleeding, not enough to run at full speed.</p>

<p><strong>5 Core Templates (XLSX + CSV):</strong></p>
<ul>
<li><strong>Community Launch Checklist</strong> — 30+ tasks across 7 phases</li>
<li><strong>Member Onboarding Flow</strong> — A 14-day welcome sequence with day-by-day copy</li>
<li><strong>Weekly Content Calendar</strong> — Daily themes, channel assignments, post planning</li>
<li><strong>Engagement Score Tracker</strong> — Weighted scoring to spot who is going quiet</li>
<li><strong>Member Segmentation Matrix</strong> — Group members by behavior and risk level</li>
</ul>

<p>Plus a condensed <strong>Quick Start Guide</strong> with the essentials: server setup, first 30 days, and the basics of getting organized.</p>

<blockquote>"The Launch Checklist alone gave me back my weekends. I set it up on a Saturday morning and for the first time in months, I did not feel that weight on my chest."<br>
<strong>Sarah K., Writing Community, about 200 members</strong></blockquote>

<hr>

<h3>Standard: $39</h3>

<p>Full set of templates, but without the playbook that ties it all together.</p>

<p><strong>10 Ready-Made Templates (XLSX + CSV):</strong> All 5 Lite templates plus Referral Program Designer, Event Planning SOP, Community KPI Dashboard, Feedback Collection System, Revenue Tracking Sheet.</p>

<p><strong>Full Quick Start Guide:</strong> About 20 pages covering platform setup, bot configs, role structures, and a first 30 days action plan.</p>

<blockquote>At just $10 more, Complete gives you the full playbook, 5 bonus templates, the health score tool, and the burnout prevention guide. Standard users consistently wish they had gone all the way. Most operators skip this tier.</blockquote>

<hr>

<h3>Complete 🎯: $49 — Most Popular</h3>

<p>The full system. Everything you need to go from that 2 AM dread to a server that practically runs itself.</p>

<p><strong>What most people buy and keep.</strong></p>

<p><strong>10 Ready-Made Templates (XLSX + CSV):</strong> All 10 templates from Standard, plus everything below.</p>

<p><strong>Full 80-Page Playbook: 7 Chapters</strong></p>

<table>
<tr><th>Chapter</th><th>What It Covers</th></tr>
<tr><td>Strategy &amp; Positioning</td><td>Purpose, platform selection, member personas</td></tr>
<tr><td>The Engagement Layer</td><td>Free, paid, and VIP tiers, scoring, upgrade paths</td></tr>
<tr><td>Daily Operations</td><td>Weekly rhythm, content pillars, moderation workflows</td></tr>
<tr><td>Retention Mechanics</td><td>First 14 day onboarding, 6 engagement triggers, reactivation</td></tr>
<tr><td>Referral &amp; Growth</td><td>Member-get-member, viral loops, partnerships</td></tr>
<tr><td>Monetization</td><td>Pricing models, free-to-paid conversion, upsells</td></tr>
<tr><td>Data Optimization</td><td>Metrics, testing, quarterly health checks</td></tr>
</table>

<p><strong>5 Bonus Templates:</strong></p>
<ul>
<li>Community Health Audit — Quarterly scorecard across 8 dimensions</li>
<li>Member Satisfaction Survey — NPS and qualitative tracking</li>
<li>SOP Template — Fill-in-the-blank for your team</li>
<li>Crisis Management Plan — Response protocols for 11 crisis types</li>
<li>Growth Experiments Tracker — Track hypotheses, results, and learnings</li>
</ul>

<blockquote>"The segmentation matrix helped me identify my top 50 power users in an afternoon. The referral program paid for itself in the first month, adding 300+ new members. But honestly, the best part is knowing I am not missing anything. The anxiety of what am I forgetting just disappeared."<br>
<strong>Priya R., SaaS Community, about 10,000 members</strong></blockquote>

<p><em>* Names and identifying details have been changed. Testimonials are illustrative composites based on real outcomes.</em></p>

<hr>

<h3>Why Most People Pick Complete</h3>

<p>At $49, Complete is just $10 more than Standard. Here is what that extra $10 gets you:</p>

<ul>
<li>An 80-page playbook that turns templates into a system</li>
<li>5 bonus templates for quarterly planning</li>
<li>A health score card tool for community diagnostics</li>
<li>A burnout prevention framework that keeps you running</li>
</ul>

<p><strong>That's $75 worth of extra content for $10.</strong> You do the math.</p>

<hr>

<h3>Your Week Before vs After</h3>

<p><strong>Before:</strong><br>
Waking up at 3 AM thinking about what to post. Opening your server like you're bracing for bad news. Watching members leave in the monthly export and not knowing why. Writing emails on Saturday mornings because you didn't post during the week.</p>

<p><strong>After:</strong><br>
A 30 minute Monday check-in with your templates. A content calendar that's already planned. A dashboard that tells you who's fading before they go dark. Friday evening, you close Slack, step away, and you don't feel guilty about it.</p>

<hr>

<h3>Built for Discord (Works Everywhere Else Too)</h3>

<p>Channel-first structure. Role-based access. Bot integrations for MEE6, Carl-bot, and Dyno. Thread management. Engagement scoring that tracks who shows up and who's fading. Permission templates that you can drop in and tweak in minutes.</p>

<p>Whether you're on Discord, Circle, Slack, or Skool — the templates adapt. The playbook is platform-agnostic. The structure works anywhere people gather online.</p>
```
