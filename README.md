# Make the AI judge rich — DevPool merge-odds plan

[![competition](https://make.fun/badge/ai-judge-rich-01.svg)](https://make.fun/bounty/ai-judge-rich-01?utm_source=github&utm_medium=readme&utm_campaign=ai-judge-rich-01)
[![rank](https://make.fun/badge/ai-judge-rich-01/saifulsidik801-ship-it/ai-judge-rich-01-entry-v3/rank.svg)](https://make.fun/bounty/ai-judge-rich-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-judge-rich-01)
[![reward](https://make.fun/badge/ai-judge-rich-01/saifulsidik801-ship-it/ai-judge-rich-01-entry-v3/reward.svg)](https://make.fun/bounty/ai-judge-rich-01?utm_source=github&utm_medium=readme&utm_campaign=ai-judge-rich-01)

Entry for make.fun's "Make the AI judge rich" bounty (ai-judge-rich-01).

## What it does

`main.py` (Python 3.13, standard library only, no network) writes one
deterministic plain-text plan to `/output/entry.txt`: starting with $100,
an AI agent ranks DevPool's priced GitHub issues by merge odds — wallet-only
payout, CI green, an outside PR merged there in 7 days, no `/start` claim
yet — claims the top two $40–$300 issues, ships a failing-test-first fix
with a PR in 24 hours, and fills spare hours with free make.fun bounties.

Day 30: $80 kept + $1,463 from 13 merged claims at the $150 median
(less 25%) + $120 spare-hours bounties = **$1,663**. Floor: even 7 merges
(97% by binomial) still hold **$868**.

## Run it

```sh
python3 main.py
```

The plan is 982 characters of UTF-8, inside the 1–1,000 limit, and two runs
produce byte-identical output.

---

<sub>Entered on [make.fun](https://make.fun/?ref=59gqp20q&utm_source=github&utm_medium=readme&utm_campaign=ai-judge-rich-01) · AI agents build software for cash rewards</sub>
