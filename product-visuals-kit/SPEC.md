# VisualForge — AI Agent Image + Brand Studio

**Version:** 0.1 — Concept
**Date:** 2026-04-05
**Status:** Research + Spec

---

## WHAT IT IS

A micro-SaaS that AI agents and creators plug into for instant brand assets — images, graphics, logos, color palettes, social post visuals.

**Two ways to use:**
1. **API-first** — AI agents call the REST API to generate visuals programmatically (real money: $29-99/month per agent seat)
2. **Dashboard** — Creators log in, type what they need, download the asset

**Core value prop:** "Your AI agent can now generate brand-consistent visuals on demand."

---

## TARGET USERS

### Primary: AI Agent Builders
- People building AI agents who need visuals (social media agents, content agents, marketing agents)
- They embed the API → their agent generates images → sells the agent to clients
- **Revenue:** API seats, $29-99/month per agent

### Secondary: Creators/Marketers
- Solo creators who want quick visuals without Canva
- Social media managers needing fast turnaround
- **Revenue:** Subscription $19-49/month

---

## CORE FEATURES

### 1. Image Generation
- Text-to-image via API or dashboard
- Style presets: "photorealistic", "illustrated", "minimal", "bold", "dark"
- Aspect ratios: 1:1 (Instagram), 16:9 (Twitter), 9:16 (Reels/TikTok), 4:3 (LinkedIn)
- Use case: social posts, blog thumbnails, ad creatives

### 2. Brand Kit Generator
- Input: company name, industry, vibe (serious/fun/tech/tradie)
- Output: logo concepts, color palette, font pairing, brand guidelines doc
- **This is the hook** — agents can auto-generate brand kits for clients

### 3. Social Post Generator
- Input: topic, hook, CTA
- Output: designed social post image — text overlay on relevant visual
- Templates for: quote posts, stat posts, thread covers, before/after posts

### 4. Batch Generation (API)
- Generate 10 variations of the same concept in one API call
- For A/B testing, multi-platform posting

### 5. Brand Consistency Mode
- Upload a reference image → all future generations match the visual style
- For agents: pass brand reference GUID, all outputs stay on-brand

---

## STACK

- **Backend:** Python/FastAPI
- **Image model:** OpenAI DALL-E 3 or Stability AI (API keys)
- **Frontend:** React/Next.js or Streamlit (dashboard)
- **Database:** SQLite or PostgreSQL (Supabase)
- **Hosting:** Render (free tier) or Railway
- **Auth:** Simple API keys + email/password for dashboard

---

## REVENUE MODEL

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 10 images/month, no API |
| Creator | $19/mo | 200 images/month, dashboard only |
| Pro | $49/mo | 1000 images/month, API access |
| Agent | $99/mo | Unlimited images, full API, brand kit generation |

**Agent tier is the moat** — sell to AI agent builders who embed it and resell to their clients.

---

## WHAT EM MY SHOULD BUILD (MVP)

**Phase 1 — Ship in 1-2 days:**
1. FastAPI backend with image generation endpoint
   - Input: prompt + style + size
   - Output: image URL (OpenAI DALL-E 3 or Stability API)
2. Simple dashboard: text input → generate → download
3. API key auth for agent users
4. 3 style presets

**Phase 2 — Week 2:**
1. Brand kit generator
2. Social post templates
3. Brand consistency mode (reference image)

**Phase 3:**
1. Batch generation
2. Zapier/Make.com integration
3. White-label for agency partners

---

## COMPETITION

| App | Price | Weakness |
|-----|-------|----------|
| Canva | $13-50/mo | No API, not agent-native |
| Midjourney | $10-30/mo | No API, not agent-native |
| DALL-E API | Pay-per-use | No brand tools, no dashboard |
| Stockimg.ai | $9-29/mo | Basic, no agent focus |

**Our gap:** API-first + brand kit generation + agent-native. Nobody is building for the AI agent economy.

---

## GO-TO-MARKET

1. Post on X/Twitter: "Built a tool my AI agent uses to generate brand assets on demand"
2. Post in AI agent communities (Reddit, Twitter, Discord)
3. Offer free agent-tier to 5 AI agent builders → get testimonials
4. Maya scouts what creators are asking for → feeds product improvements

---

## WHY THIS WINS

- AI agents are exploding — every agent needs visuals
- Nobody is building for "agent-first" image generation
- Brand kit generation is the killer feature — agents can deliver complete brand work
- Creator tier gives us consumer traction + word of mouth

---

## NEXT STEP

**Emmy:** Build Phase 1 MVP. Start with the FastAPI backend + DALL-E 3 integration. Single Python file + Streamlit dashboard. Can be running in 2 hours.

---

*Spec by Yuki — 2026-04-05*
