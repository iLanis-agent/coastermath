(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function money(c) { return "$" + Math.floor(c / 100) + "." + ("0" + (c % 100)).slice(-2); }

  function yieldPlan(sheetWCm, sheetHCm, diameterCm) {
    if (!(sheetWCm > 0) || !(sheetHCm > 0) || !(diameterCm > 0)) return { error: "sheet size and coaster diameter must be positive" };
    var across = Math.floor(sheetWCm / diameterCm);
    var down = Math.floor(sheetHCm / diameterCm);
    var coasters = across * down;
    var wastePct = Math.round((1 - coasters * 0.785 * diameterCm * diameterCm / (sheetWCm * sheetHCm)) * 100 * 10) / 10;
    return { across: across, down: down, coasters: coasters, wastePct: wastePct };
  }

  function setPlan(sets, coastersPerSet, sheetYield, sheetPriceDollars) {
    if (!(sets > 0) || !(coastersPerSet > 0) || !(sheetYield > 0) || !(sheetPriceDollars > 0)) return { error: "sets, coasters, yield and sheet price must be positive" };
    var needed = sets * coastersPerSet;
    var sheets = Math.ceil(needed / sheetYield);
    var costCents = Math.round(sheets * sheetPriceDollars * 100);
    var perSetCents = Math.round(costCents / sets);
    return { needed: needed, sheets: sheets, costCents: costCents, perSetCents: perSetCents };
  }

  function pricePlan(costPerSetDollars, hoursPerSet, rateDollars, marginPct) {
    if (!(costPerSetDollars > 0) || !(hoursPerSet > 0) || !(rateDollars > 0) || !(marginPct >= 0)) return { error: "cost, hours and rate must be positive" };
    var baseCents = Math.round(costPerSetDollars * 100) + Math.round(hoursPerSet * rateDollars * 100);
    var priceCents = Math.round(baseCents * (1 + marginPct / 100));
    return { baseCents: baseCents, priceCents: priceCents };
  }

  function renderYield(r, sheetWCm, sheetHCm, diameterCm) {
    return "A " + sheetWCm + " x " + sheetHCm + " cm sheet at " + diameterCm + " cm a coaster: " + r.across + " across and " + r.down + " down, " + plural(r.coasters, "coaster") + ", " + r.wastePct + "% of the sheet as waste.";
  }

  function renderSet(r, sets, coastersPerSet, sheetYield, sheetPriceDollars) {
    return plural(sets, "set") + " of " + coastersPerSet + " coasters: " + r.needed + " coasters, " + plural(r.sheets, "sheet") + " at $" + sheetPriceDollars + " - " + money(r.costCents) + " of material, " + money(r.perSetCents) + " a set.";
  }

  function renderPrice(r, costPerSetDollars, hoursPerSet, rateDollars, marginPct) {
    return money(Math.round(costPerSetDollars * 100)) + " of material and " + hoursPerSet + " " + (hoursPerSet === 1 ? "hour" : "hours") + " at $" + rateDollars + " an hour with a " + marginPct + "% margin: " + money(r.baseCents) + " to break even, price a set at " + money(r.priceCents) + ".";
  }

  var api = { yieldPlan: yieldPlan, setPlan: setPlan, pricePlan: pricePlan, renderYield: renderYield, renderSet: renderSet, renderPrice: renderPrice };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.CoasterMath = api;
})(this);
