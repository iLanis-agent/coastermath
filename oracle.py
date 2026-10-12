import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def money(c): return "$" + str(c // 100) + "." + str(c % 100).zfill(2)
def fmt(x): return str(jsnum(x))
def rnd(x): return math.floor(x + 0.5)

def yield_plan(sheetWCm, sheetHCm, diameterCm):
    if not (sheetWCm > 0) or not (sheetHCm > 0) or not (diameterCm > 0):
        return {"error": "sheet size and coaster diameter must be positive"}
    across = math.floor(sheetWCm / diameterCm)
    down = math.floor(sheetHCm / diameterCm)
    coasters = across * down
    waste = jsnum(rnd((1 - coasters * 0.785 * diameterCm * diameterCm / (sheetWCm * sheetHCm)) * 100 * 10) / 10)
    return {"across": across, "down": down, "coasters": coasters, "wastePct": waste}

def set_plan(sets, coastersPerSet, sheetYield, sheetPriceDollars):
    if not (sets > 0) or not (coastersPerSet > 0) or not (sheetYield > 0) or not (sheetPriceDollars > 0):
        return {"error": "sets, coasters, yield and sheet price must be positive"}
    needed = sets * coastersPerSet
    sheets = math.ceil(needed / sheetYield)
    cost = rnd(sheets * sheetPriceDollars * 100)
    return {"needed": needed, "sheets": sheets, "costCents": cost, "perSetCents": rnd(cost / sets)}

def price_plan(costPerSetDollars, hoursPerSet, rateDollars, marginPct):
    if not (costPerSetDollars > 0) or not (hoursPerSet > 0) or not (rateDollars > 0) or not (marginPct >= 0):
        return {"error": "cost, hours and rate must be positive"}
    base = rnd(costPerSetDollars * 100) + rnd(hoursPerSet * rateDollars * 100)
    return {"baseCents": base, "priceCents": rnd(base * (1 + marginPct / 100))}

def render_yield(r, sheetWCm, sheetHCm, diameterCm):
    return ("A " + fmt(sheetWCm) + " x " + fmt(sheetHCm) + " cm sheet at " + fmt(diameterCm) + " cm a coaster: "
            + fmt(r["across"]) + " across and " + fmt(r["down"]) + " down, " + plural(r["coasters"], "coaster")
            + ", " + fmt(r["wastePct"]) + "% of the sheet as waste.")

def render_set(r, sets, coastersPerSet, sheetYield, sheetPriceDollars):
    return (plural(sets, "set") + " of " + fmt(coastersPerSet) + " coasters: " + fmt(r["needed"]) + " coasters, "
            + plural(r["sheets"], "sheet") + " at $" + fmt(sheetPriceDollars) + " - " + money(r["costCents"])
            + " of material, " + money(r["perSetCents"]) + " a set.")

def render_price(r, costPerSetDollars, hoursPerSet, rateDollars, marginPct):
    return (money(rnd(costPerSetDollars * 100)) + " of material and " + fmt(hoursPerSet) + " "
            + ("hour" if hoursPerSet == 1 else "hours") + " at $" + fmt(rateDollars) + " an hour with a "
            + fmt(marginPct) + "% margin: " + money(r["baseCents"]) + " to break even, price a set at "
            + money(r["priceCents"]) + ".")

cases = []
for a in [(60, 90, 10), (40, 60, 12), (50, 50, 9), (0, 90, 10)]:
    r = yield_plan(*a)
    cases.append({"fn": "yieldPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_yield(r, *a)})
for a in [(6, 4, 54, 8), (12, 6, 15, 5), (10, 4, 25, 6), (0, 4, 54, 8)]:
    r = set_plan(*a)
    cases.append({"fn": "setPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_set(r, *a)})
for a in [(6.2, 0.5, 15, 25), (2.08, 0.75, 12, 40), (4.5, 1, 10, 30), (0, 0.5, 15, 25)]:
    r = price_plan(*a)
    cases.append({"fn": "pricePlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_price(r, *a)})

with open("expected.json", "w") as f:
    f.write(json.dumps(cases, separators=(",", ":")) + "\n")
print("wrote", len(cases), "cases")
