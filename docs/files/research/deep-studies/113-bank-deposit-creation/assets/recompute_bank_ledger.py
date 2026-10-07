#!/usr/bin/env python3
"""Recompute an invented two-bank ledger, in units of 10,000 yuan.

Python 3, standard library only. No rates, policies, or real bank data are used.
Each event updates both sides of the affected balance sheets. Results are JSON
on stdout; redirect to a file if desired. All arithmetic here is exact integer
arithmetic. The proof is accounting consistency, not economic forecasting.
"""
import json
from copy import deepcopy


def initial():
    return {
        name: {"reserves": 20, "loans": {"legacy": 80, "Lin": 0},
               "deposits": {"existing": 90, "Lin": 0, "seller": 0,
                            "employee": 0}, "equity": 10}
        for name in ("A", "B")
    }


def snapshot(banks, event):
    out = {"event": event, "banks": deepcopy(banks)}
    for bank in out["banks"].values():
        bank["total_loans"] = sum(bank["loans"].values())
        bank["total_deposits"] = sum(bank["deposits"].values())
        bank["total_assets"] = bank["reserves"] + bank["total_loans"]
        bank["balance_error"] = (
            bank["total_assets"] - bank["total_deposits"] - bank["equity"])
        assert bank["balance_error"] == 0
        assert bank["reserves"] >= 0
        assert min(bank["deposits"].values()) >= 0
        assert min(bank["loans"].values()) >= 0
    out["system"] = {
        "customer_deposits": sum(b["total_deposits"] for b in out["banks"].values()),
        "central_bank_reserves": sum(b["reserves"] for b in banks.values()),
        "loans": sum(b["total_loans"] for b in out["banks"].values()),
        "equity": sum(b["equity"] for b in banks.values()),
    }
    return out


def lend(banks, name, customer, amount):
    banks[name]["loans"][customer] += amount
    banks[name]["deposits"][customer] += amount


def pay(banks, from_bank, payer, to_bank, payee, amount):
    assert banks[from_bank]["deposits"][payer] >= amount
    banks[from_bank]["deposits"][payer] -= amount
    banks[to_bank]["deposits"][payee] += amount
    if from_bank != to_bank:
        assert banks[from_bank]["reserves"] >= amount
        banks[from_bank]["reserves"] -= amount
        banks[to_bank]["reserves"] += amount


def repay(banks, paying_bank, customer, lending_bank, amount):
    assert banks[paying_bank]["deposits"][customer] >= amount
    assert banks[lending_bank]["loans"][customer] >= amount
    banks[paying_bank]["deposits"][customer] -= amount
    banks[lending_bank]["loans"][customer] -= amount
    if paying_bank != lending_bank:
        assert banks[paying_bank]["reserves"] >= amount
        banks[paying_bank]["reserves"] -= amount
        banks[lending_bank]["reserves"] += amount


def run():
    banks = initial()
    main = [snapshot(banks, "initial")]
    lend(banks, "A", "Lin", 10)
    main.append(snapshot(banks, "A creates loan and Lin deposit of 10"))
    pay(banks, "A", "Lin", "B", "seller", 10)
    main.append(snapshot(banks, "Lin buys machine; A settles with B"))
    pay(banks, "B", "seller", "B", "Lin", 10)
    main.append(snapshot(banks, "seller pays Lin for a service within B"))
    repay(banks, "B", "Lin", "A", 10)
    main.append(snapshot(banks, "Lin repays A from account at B"))
    assert main[0]["system"] == main[-1]["system"]
    assert [x["system"]["customer_deposits"] for x in main] == [180, 190, 190, 190, 180]
    assert [x["system"]["central_bank_reserves"] for x in main] == [40]*5
    assert [x["system"]["loans"] for x in main] == [160, 170, 170, 170, 160]

    banks = initial()
    lend(banks, "A", "Lin", 10)
    same_bank = [snapshot(banks, "A lends 10 before same-bank repayment")]
    repay(banks, "A", "Lin", "A", 10)
    same_bank.append(snapshot(banks, "same-bank principal repayment"))
    assert same_bank[-1]["system"] == main[0]["system"]

    banks = initial()
    # A customer's legacy loan pays interest. For this isolated example the
    # receipt and recognition coincide; there is no accrued-interest receivable,
    # no tax, no other expense, and profit is retained until the wage payment.
    interest = [snapshot(banks, "independent interest example before receipt")]
    banks["A"]["deposits"]["existing"] -= 1
    banks["A"]["equity"] += 1
    interest.append(snapshot(banks, "interest of 1 received and retained"))
    banks["A"]["deposits"]["employee"] += 1
    banks["A"]["equity"] -= 1
    interest.append(snapshot(banks, "A pays wage of 1 to its own depositor"))
    assert [s["system"]["customer_deposits"] for s in interest] == [180, 179, 180]
    assert [s["system"]["loans"] for s in interest] == [160]*3

    banks = initial()
    banks["A"]["loans"]["legacy"] -= 6
    banks["A"]["equity"] -= 6
    loss = snapshot(banks, "independent loss of 6, no earlier provision in this toy ledger")
    assert loss["banks"]["A"]["total_assets"] == 94
    assert loss["banks"]["A"]["equity"] == 4
    assert loss["system"]["customer_deposits"] == 180

    banks = initial()
    pay(banks, "A", "existing", "B", "Lin", 10)
    nonbank = snapshot(banks, "friend lends existing deposit; private loan outside bank ledger")
    assert nonbank["system"]["customer_deposits"] == 180
    assert nonbank["system"]["loans"] == 160
    return {"unit": "10,000 yuan; all invented", "main_sequence": main,
            "same_bank_repayment": same_bank, "interest_and_wage": interest,
            "loss": loss, "nonbank_transfer": nonbank,
            "all_balance_identities_and_expected_totals_passed": True}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
