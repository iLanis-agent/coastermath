# Coaster math

Coasters from a cork sheet, sets for the gift list, and a price that pays for your evening. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/coastermath/

## The three tools

- **Yield plan** - `yieldPlan(sheetWCm, sheetHCm, diameterCm)`: coasters per sheet and the waste share.
- **Set plan** - `setPlan(sets, coastersPerSet, sheetYield, sheetPriceDollars)`: sheets to buy, material cost and cost per set.
- **Price plan** - `pricePlan(costPerSetDollars, hoursPerSet, rateDollars, marginPct)`: break-even and selling price.

## Labeled norms (illustrative estimates, not rules)

- Labeled layout: a simple grid, a circle taking about 78.5% of its square. Prices, hours and rates are your own inputs; the shop's tags and your own clock win.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (12 cases, 63 checks)

Regenerate the oracle expectations: `python3 oracle.py`
