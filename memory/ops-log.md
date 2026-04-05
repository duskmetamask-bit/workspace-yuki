
## 2026-04-05 Evening Ops Log

### Mewy (Hermes) Changes

**Problem:** DuckDuckGo blocked at server IP. 470+ failed searches/day. Gateway crashing due to GEMINI_API_KEY missing from config.

**Fixes applied:**

1. **Removed Google provider** from openclaw.json — was crashing gateway. Replaced imageModel.primary with minimax/MiniMax-M2.7 (⚠️ this is a TEXT model, not vision — image analysis still broken)

2. **Disabled 3 duplicate cron jobs:**
   - Emmy — SaaS Research (duplicate #2)
   - Happy Harold — AI Research (duplicate #2)
   - Morning Briefing (duplicate #2)

3. **Changed 8 active research crons from 1hr → 3hr:**
   - Felix — Money Opportunities
   - Felix — Money Research
   - Felix Money Scan
   - Emmy — SaaS Research
   - Happy Harold — AI Research
   - Happy Harold — AI Research + Forecast
   - Happy Harold AI Scan
   - Content Scout

**New search volume:** ~1,920/month (down from 7,200+)

**⚠️ Still broken:** Image analysis (image model). Gemini removed, MiniMax-M2.7 doesn't support vision. Need to fix imageModel config.

