# Orchestration design evolution

This is the evidence-backed chronology of a solo developer experimenting with
role-based AI systems in Houston, Texas. It distinguishes original work from
upstream software, prompt-level personas from executable components and
historical artifacts from later reconstruction.

## December 2025 — the focused boardroom

The Synesthetic Soundscapes repository began as an AI-assisted operating package
for a real Houston festival concept timed with the 2026 FIFA World Cup. On
December 25, I created six synthetic diligence lenses—finance, operations,
industry analysis, legal, marketing and investor review—to attack a forecast
that claimed approximately $65.9M of profit.

This was a focused design. The event decision did not need a synthetic company;
it needed six forms of resistance. The review cut unsupported revenue,
preserved grounded planning costs, normalized inflated or duplicated expenses
and produced a reported $5M–$7M base-case range.

It still failed to eliminate a definition gap between pre-contingency and fully
loaded expenses. The first lesson was therefore:

> Structured disagreement improves assumptions, but persona diversity cannot
> repair weak state management.

## January 2026 — the lobster runtime

Peter Steinberger's open-source personal-assistant project began as Clawd,
briefly became Moltbot and was renamed OpenClaw on January 29, 2026. Its mascot
and heritage are intentionally lobster-themed. See the creator's
[naming history](https://openclaw.ai/blog/introducing-openclaw) and the
[upstream repository](https://github.com/openclaw/openclaw).

On January 29, I imported the Moltbot-era codebase into a private working
repository named `ClawdBot`. Over the following day I used that copy to explore
Linux CLI build repair, CI configuration, rejected-call hangup behavior and
memory-query performance.

This was **not** an original Alex-built runtime. The correct attribution is:

- Peter Steinberger and the OpenClaw community created the upstream platform.
- I used a private working copy to study, configure and modify parts of it.
- Only my incremental experiments and operating configuration belong in my
  portfolio.

## February 2026 — an operating agent named K2

The smaller private `openclaw` repository captured my actual operating layer,
not the full upstream source. I created K2's identity, work rules, heartbeat
schedule and repository registry.

On February 15, the workspace added a concrete local-CI workflow:

1. heartbeat checks detected new or updated pull requests;
2. K2 delegated test and lint work to a coding role;
3. results were tracked by commit SHA to prevent duplicate validation;
4. pass/fail findings were returned to pull requests; and
5. Jules sessions were monitored and routed into the same validation loop.

That is stronger portfolio evidence than merely cloning OpenClaw. It shows a
persistent operational agent coordinating real software work with explicit
state and a human owner.

The raw workspace is not suitable for public release. It contains personal
context, operational identifiers and historical credentials. This public case
describes the architecture without reproducing that data.

## March 2026 — the 21-role synthetic company

Diggs Money OS began on March 7 and quickly expanded into a fictional operating
company with four layers:

| Layer | Designed function |
|---|---|
| Human principal | Objectives, capital decisions and irreversible approvals |
| Maestro + Magnus | Orchestration protocol and executive decomposition |
| Turing-Prime, Madison and Ledger | Technical, marketing and financial challenge |
| Nodes 01–17 | Infrastructure, content, distribution, acquisition and reporting |

The implementation included a Next.js control plane, event spine, mission
ledger, dashboards and specialist routing. But the taxonomy drifted, several
characters expanded beyond their original jobs and not every role was an
independently deployed agent.

The correct description is a **21-role synthetic organization** or
**role-based orchestration experiment**, not “21 autonomous production
agents.”

The second lesson was:

> More roles create more coverage, but they also multiply ambiguity unless
> authority and state are mechanically enforced.

## Mid-2026 — production constraints

The lessons became concrete in shipped consumer products:

- deterministic game state remained outside model control;
- user-confirmed truth anchored generated content;
- safety and cost gates ran in code rather than persona instructions; and
- persistent character behavior was separated from scoring authority.

The production pattern is less theatrical and more reliable: models generate
and challenge; code owns invariants; a human owns release.

## July 2026 — reconstruction and audit

The original boardroom repository preserved scenario analysis but not executable
Monte Carlo or regression code. On July 28, I reconstructed the decision core
as a seeded 100,000-trial simulation with standardized regression and tests
that block definition drift.

The design I would use now is:

1. AI roles submit structured objections against named assumptions.
2. Each objection carries an evidence class, proposed range and expected
   effect.
3. A deterministic build regenerates every view from one schema.
4. Invariant tests block release when totals or definitions fail to reconcile.
5. Monte Carlo and sensitivity analysis quantify remaining uncertainty.
6. A human makes the capital or release decision.

The chronology is not “more agents became smarter.” It is:

> Focused disagreement led to persistent operations, persistent operations
> expanded into organizational breadth, and breadth finally collapsed into
> auditable control.
