## Task 4 — Women's T20 Cricket Matches

Objective:
- Provide live odds, news aggregation, and AI-driven analysis specifically for international and domestic women's T20 matches.

Scope:
- Focus on upcoming women's T20 matches worldwide (international and major domestic leagues).
- Aggregate odds (when available), recent news, and produce an AI analysis with specific betting and tactical insights.

Deliverables:
- Quick match summary (teams, time, key players)
- Data-informed analysis listing: form, pitch/weather factors, matchup advantages, and injury/availability flags.
- Prediction with confidence level and optional betting recommendation.
- Short action list for follow-up (e.g., monitor toss, late injuries, pitch report link)

Data sources / hints for the agent:
- The Odds API (if women-specific sport keys exist) or other odds providers
- News via Tavily or DuckDuckGo News search
- Official match pages, cricket boards, and social feeds for late updates

Prompt guidance for AI Analysis:
"You are a cricket analyst focused on women's T20. Use available odds and recent news. Highlight key players, pitch/weather impact, and any squad changes. Provide a prediction with confidence and a short betting recommendation if applicable. Reference any news items or odds used."

Acceptance criteria:
- The agent's UI should expose women T20 as a selectable format.
- Analysis should reference odds and news when available.
- Task file exists here for maintainers to edit or expand.

Notes:
- If the Odds API uses a different sport key naming for women's competitions, update the `get_cricket_events` sport key mapping in `cricket_agent.py` accordingly.
