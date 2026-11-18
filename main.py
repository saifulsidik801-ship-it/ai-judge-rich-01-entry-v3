#!/usr/bin/env python3
"""ai-judge-rich-01 entry (round 14 upgrade of v3).

Writes the 30-day plan to /output/entry.txt. Python standard library only,
deterministic, no network. Every dollar figure in the plan is recomputed
here in integer cents and asserted, so the text can never drift from its
own math.
"""

import os
from decimal import Decimal, ROUND_HALF_UP

PLAN = (
    "Make.fun first: escrowed bounties, public judge and payouts. "
    "One agent: 25/week, paid 20, $570.50, $22.82/entry; "
    "top 50: $6,063/946, $6.41/entry, 63% placed. "
    "4 drafts duel on the judge prompt both orders; winner only, then vs top 5. "
    "Rank by $/hour; drop types unpaid after 3. "
    "Day 1: $10 credit, $10 gas, $80 untouched; fees from winnings; 12 open. "
    "DevPool second, checked 17 Nov: 124 priced open, $40,998, median $150; "
    "79 unassigned, 108 under a day; 793 closed, $178,068 paid \u2014 yet its "
    "main org's 100 latest merged PRs: none by an outsider, so 8 claims "
    "$40-$300, only where outsiders merged. "
    "Fail test first, fix, prove on repo suite, PR in 24h; max 2 open; "
    "drop if stalled 5d. "
    "Math: 110 \u00d7 $11.41 (half leader) = $1,255; "
    "DevPool 2 \u00d7 $150 less 25% = $225; audit $125. "
    "Day 30: $80 + $1,255 + $225 + $125 = $1,685. "
    "Floor: 110 \u00d7 $6.41 = $705; DevPool 1 merge (90% binomial) = $113; "
    "+ $125 + $80 = $1,023. "
    "Edge: escrow funded, judge published, winners paid \u2014 no persuading, "
    "only out-write the board."
)


def round_cents(value):
    """Round a fractional-cent value to integer cents, halves up."""
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def dollars(cents):
    """Round integer cents to whole dollars, halves up."""
    return int((Decimal(cents) / Decimal(100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def main():
    # --- Inputs: every number below is either quoted from a published record
    # (make.fun top entries / DevPool live check 17 Nov) or derived from one.
    entries = 110                       # make.fun entries in 30 days (~4/day)
    leader_total_cents = 57050          # leader account: $570.50 paid
    leader_entered = 25                 # ... on 25 entries, paid in 20
    top50_total_cents = 606300          # top 50: $6,063 taken
    top50_entries = 946                 # ... in 946 entries, 63% placed
    devpool_median_price_cents = 15000  # DevPool median $150 (live, 17 Nov)
    devpool_claims = 8                  # secondary DevPool claims, $40-$300
    devpool_median_merges = 2           # honest outsider rate: few merge
    devpool_floor_merges = 1            # floor: a single merge survives
    devpool_fee_pct = 25                # DevPool takes 25%
    audit_cents = 12500                 # second income: audit contest $125
    cash_kept_cents = 8000              # Day 1: $80 of $100 untouched

    # --- Derived rates (integer cents per entry, halves up).
    leader_rate = round_cents(leader_total_cents / leader_entered)  # $22.82
    assert leader_rate == 2282, leader_rate
    assert leader_rate % 2 == 0
    median_rate = leader_rate // 2                                  # half leader
    assert median_rate == 1141, median_rate                          # $11.41
    floor_rate = round_cents(top50_total_cents / top50_entries)      # $6.41
    assert floor_rate == 641, floor_rate

    # --- Median leg (cents, exact).
    makefun_median = entries * median_rate                           # 125510
    devpool_median = devpool_median_merges * devpool_median_price_cents
    devpool_median = devpool_median * (100 - devpool_fee_pct) // 100  # 22500
    day30_cents = cash_kept_cents + makefun_median + devpool_median + audit_cents
    assert day30_cents == 168510, day30_cents                        # $1,685.10

    # --- Floor leg (cents, exact).
    makefun_floor = entries * floor_rate                             # 70510
    devpool_floor = devpool_floor_merges * devpool_median_price_cents
    devpool_floor = devpool_floor * (100 - devpool_fee_pct) // 100    # 11250
    floor_cents = cash_kept_cents + makefun_floor + devpool_floor + audit_cents
    assert floor_cents == 102260, floor_cents                        # $1,022.60

    # --- The rounded components printed in the plan must sum exactly too.
    assert dollars(makefun_median) == 1255
    assert dollars(devpool_median) == 225
    assert dollars(audit_cents) == 125
    assert dollars(cash_kept_cents) == 80
    assert 80 + 1255 + 225 + 125 == 1685
    assert dollars(day30_cents) == 1685
    assert dollars(makefun_floor) == 705
    assert dollars(devpool_floor) == 113
    assert 705 + 113 + 125 + 80 == 1023
    assert dollars(floor_cents) == 1023

    # --- Floor credibility: P(at least 1 merge of 8 at 25%) by binomial.
    p_floor = 1 - (1 - 0.25) ** devpool_claims                       # 0.8999
    assert 0.89 < p_floor < 0.91, p_floor                            # ~90%

    # --- The plan itself: length cap, and every claimed figure present.
    assert len(PLAN) <= 1000, len(PLAN)
    for fragment in (
        "$570.50", "$22.82/entry", "$6,063/946", "$6.41/entry", "63% placed",
        "4 drafts duel", "both orders", "vs top 5", "Rank by $/hour",
        "unpaid after 3", "$10 credit", "$10 gas", "$80 untouched",
        "12 open", "124 priced open", "$40,998", "median $150",
        "79 unassigned", "108 under a day", "793 closed", "$178,068 paid",
        "100 latest merged PRs", "none by an outsider", "8 claims",
        "$40-$300", "PR in 24h", "max 2 open", "stalled 5d",
        "110 \u00d7 $11.41", "$1,255", "2 \u00d7 $150", "$225",
        "audit $125", "$1,685", "110 \u00d7 $6.41", "$705",
        "1 merge (90% binomial)", "$113", "$1,023",
    ):
        assert fragment in PLAN, fragment

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(PLAN + "\n")

    print(PLAN)
    print("chars:", len(PLAN))
    print("day30: $%d (exact $%.2f)" % (dollars(day30_cents), day30_cents / 100))
    print("floor: $%d (exact $%.2f)" % (dollars(floor_cents), floor_cents / 100))
    print("wrote:", out_path)


if __name__ == "__main__":
    main()
