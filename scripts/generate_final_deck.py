from __future__ import annotations

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "supporting-materials"
OUT.mkdir(exist_ok=True)
PDF = OUT / "Open_Agent_Safety_Kit_Grant_Deck_Final.pdf"

W, H = landscape(letter)

BG = colors.HexColor("#F7F8FA")
INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#5B6472")
NAVY = colors.HexColor("#07111F")
BLUE = colors.HexColor("#2563EB")
GREEN = colors.HexColor("#059669")
AMBER = colors.HexColor("#D97706")
RED = colors.HexColor("#DC2626")
LINE = colors.HexColor("#D9E0EA")
CARD = colors.white
SOFT_BLUE = colors.HexColor("#EAF1FF")
SOFT_GREEN = colors.HexColor("#EAF8F2")
SOFT_AMBER = colors.HexColor("#FFF5E6")
SOFT_RED = colors.HexColor("#FFF0F0")

c = canvas.Canvas(str(PDF), pagesize=landscape(letter))
c.setTitle("Open Agent Safety Kit Grant Deck")
c.setAuthor("Carly17")


def set_bg(dark: bool = False):
    c.setFillColor(NAVY if dark else BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    if not dark:
        c.setFillColor(BLUE)
        c.rect(0, H - 0.08 * inch, W, 0.08 * inch, fill=1, stroke=0)


def wrap_text(s: str, font: str, size: float, max_w: float) -> list[str]:
    words = s.split()
    lines = []
    line = ""
    for word in words:
        candidate = (line + " " + word).strip()
        if not line or stringWidth(candidate, font, size) <= max_w:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text(s: str, x: float, y: float, size: float, color=INK, font: str = "Helvetica", max_w: float | None = None, line_spacing: float = 1.4) -> float:
    c.setFillColor(color)
    c.setFont(font, size)
    lead = size * line_spacing
    if max_w is None:
        c.drawString(x, y, s)
        return y - lead
    lines = wrap_text(s, font, size, max_w)
    for i, line in enumerate(lines):
        c.drawString(x, y - i * lead, line)
    return y - len(lines) * lead


def footer(page: int, dark: bool = False):
    col = colors.HexColor("#8AA0B8") if dark else colors.HexColor("#94A3B8")
    c.setFillColor(col)
    c.setFont("Helvetica", 8)
    c.drawString(0.6 * inch, 0.35 * inch, "Open Agent Safety Kit • github.com/Carlys17/open-agent-safety-kit")
    c.drawRightString(W - 0.6 * inch, 0.35 * inch, str(page))


def header(title: str, subtitle: str = ""):
    y = H - 0.85 * inch
    y = draw_text(title, 0.7 * inch, y, 26, INK, "Helvetica-Bold")
    if subtitle:
        draw_text(subtitle, 0.7 * inch, y + 0.1 * inch, 11, MUTED, "Helvetica", max_w=9.2 * inch)


def round_rect(x, y, w, h, fill, stroke=LINE, radius=12):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def card(x, y, w, h, title: str, body: str, accent=BLUE, fill=CARD):
    round_rect(x, y, w, h, fill)
    c.setFillColor(accent)
    c.roundRect(x, y + h - 0.1 * inch, w, 0.1 * inch, 8, fill=1, stroke=0)
    draw_text(title, x + 0.22 * inch, y + h - 0.38 * inch, 13, INK, "Helvetica-Bold", max_w=w - 0.44 * inch)
    draw_text(body, x + 0.22 * inch, y + h - 0.74 * inch, 10, MUTED, "Helvetica", max_w=w - 0.44 * inch, line_spacing=1.35)


# ─── Slide 1: Cover ──────────────────────────────────────────────────────────
set_bg(True)
draw_text("Open Agent", 0.85 * inch, 6.0 * inch, 42, colors.white, "Helvetica-Bold")
draw_text("Safety Kit", 0.85 * inch, 5.2 * inch, 42, colors.white, "Helvetica-Bold")
draw_text("Open-source safety tests for AI agents before real-world deployment.", 0.87 * inch, 4.35 * inch, 15, colors.HexColor("#DDEBFF"), max_w=6.0 * inch)
# motif - right side, away from all text
c.setFillColor(BLUE); c.roundRect(8.2 * inch, 5.0 * inch, 1.2 * inch, 1.2 * inch, 20, fill=1, stroke=0)
c.setFillColor(colors.HexColor("#38BDF8")); c.roundRect(7.7 * inch, 4.5 * inch, 0.7 * inch, 0.7 * inch, 14, fill=1, stroke=0)
c.setFillColor(GREEN); c.roundRect(8.9 * inch, 4.3 * inch, 0.45 * inch, 0.45 * inch, 10, fill=1, stroke=0)
# info box at bottom
round_rect(0.85 * inch, 2.65 * inch, 6.2 * inch, 0.85 * inch, colors.HexColor("#10243B"), colors.HexColor("#244A73"))
draw_text("Public-good toolkit for builders who need transparent checks for agent tool use, verification, and failure modes.", 1.08 * inch, 3.12 * inch, 11.5, colors.HexColor("#CFE2FF"), max_w=5.7 * inch)
draw_text("Grant ask: $25,000  •  Maintainer: Carly17", 0.87 * inch, 2.1 * inch, 13, colors.HexColor("#BFD7FF"), "Helvetica-Bold")
footer(1, True)
c.showPage()

# ─── Slide 2: Problem ────────────────────────────────────────────────────────
set_bg(); header("Why now", "AI agents are moving from chat into real actions: code, files, infrastructure, APIs, and protocols.")
card(0.75*inch, 4.15*inch, 2.95*inch, 1.5*inch, "The new risk", "An agent can take action, skip verification, and still report success.", RED, SOFT_RED)
card(4.0*inch, 4.15*inch, 2.95*inch, 1.5*inch, "Small builders", "Independent teams cannot use expensive closed evaluation systems.", AMBER, SOFT_AMBER)
card(7.25*inch, 4.15*inch, 2.95*inch, 1.5*inch, "Open gap", "Safety rules need to be inspectable, adaptable, and locally runnable.", BLUE, SOFT_BLUE)
# callout at bottom
round_rect(1.05*inch, 2.0*inch, 8.9*inch, 1.2*inch, CARD)
draw_text("Failure pattern", 1.35*inch, 2.8*inch, 12, MUTED, "Helvetica-Bold")
draw_text("action  ->  no verification  ->  false success  ->  user trusts the result", 1.35*inch, 2.38*inch, 17, INK, "Helvetica-Bold", max_w=8.2*inch)
footer(2)
c.showPage()

# ─── Slide 3: Solution ───────────────────────────────────────────────────────
set_bg(); header("What the toolkit does", "A local CLI evaluates agent traces and returns evidence-based safety findings.")
xs = [0.85, 3.1, 5.35, 7.6]
labels = [("1", "Trace", "messages +\ntool calls"), ("2", "Rules", "open safety\nchecks"), ("3", "Report", "score +\nevidence"), ("4", "CI", "block risky\nworkflows")]
for i, (n, h, b) in enumerate(labels):
    x = xs[i] * inch
    round_rect(x, 4.15*inch, 1.65*inch, 1.15*inch, CARD)
    draw_text(n, x + 0.15*inch, 4.88*inch, 22, BLUE, "Helvetica-Bold")
    draw_text(h, x + 0.52*inch, 4.95*inch, 13, INK, "Helvetica-Bold")
    draw_text(b, x + 0.52*inch, 4.62*inch, 9.5, MUTED, max_w=0.95*inch, line_spacing=1.3)
    if i < 3:
        c.setStrokeColor(BLUE); c.setLineWidth(2)
        c.line(x + 1.78*inch, 4.72*inch, (xs[i+1])*inch - 0.12*inch, 4.72*inch)
checks = [
    ("False success", "success without evidence", RED),
    ("Missing verification", "side effects without readback", AMBER),
    ("Secret exposure", "keys, tokens, env, wallets", BLUE),
    ("Unsafe network writes", "POST/PUT/DELETE without allowlist", GREEN),
]
for i, (h, b, col) in enumerate(checks):
    x = (0.85 + (i % 2)*4.75) * inch
    y = (2.5 - (i // 2)*1.0) * inch
    card(x, y, 4.1*inch, 0.78*inch, h, b, col)
footer(3)
c.showPage()

# ─── Slide 4: Demo ───────────────────────────────────────────────────────────
set_bg(); header("Runnable proof", "The repository includes code, tests, examples, CI, and a working demo.")
# left panel - command
round_rect(0.85*inch, 4.05*inch, 4.5*inch, 1.45*inch, colors.HexColor("#0F172A"), colors.HexColor("#1E293B"))
draw_text("Terminal", 1.12*inch, 5.05*inch, 9, colors.HexColor("#64748B"), "Helvetica-Bold")
draw_text("$ oask run unsafe_false_success.json", 1.12*inch, 4.7*inch, 11, colors.HexColor("#E2E8F0"), "Courier-Bold")
draw_text("Agent: deployed and everything is working.", 1.12*inch, 4.35*inch, 10, colors.HexColor("#94A3B8"), max_w=3.8*inch)
# right panel - result
round_rect(5.7*inch, 4.05*inch, 4.3*inch, 1.45*inch, SOFT_RED, colors.HexColor("#F3C4C4"))
draw_text("FAIL", 6.0*inch, 5.15*inch, 28, RED, "Helvetica-Bold")
draw_text("Risk score: 30/100", 6.0*inch, 4.65*inch, 15, INK, "Helvetica-Bold")
draw_text("false-success-without-evidence", 6.0*inch, 4.3*inch, 10, MUTED, "Courier")
# proof numbers
nums = [("5", "tests passing", GREEN), ("CI", "GitHub Actions", BLUE), ("MIT", "open-source", AMBER), ("28", "repo files", BLUE)]
for i, (n, l, col) in enumerate(nums):
    x = (1.0 + i*2.45) * inch
    draw_text(n, x, 2.8*inch, 32, col, "Helvetica-Bold")
    draw_text(l, x, 2.35*inch, 11, MUTED, max_w=2.0*inch)
footer(4)
c.showPage()

# ─── Slide 5: Public good ────────────────────────────────────────────────────
set_bg(); header("Why this is a public good", "Rules, traces, scoring, docs, and examples are open so builders can inspect and improve them.")
card(0.85*inch, 4.3*inch, 2.85*inch, 1.45*inch, "Who benefits", "Solo builders, open-source maintainers, small AI teams, web3 builders, and developers in emerging markets.", BLUE, SOFT_BLUE)
card(4.0*inch, 4.3*inch, 2.85*inch, 1.45*inch, "What stays open", "Rules, example traces, scoring, documentation, CLI, tests, and integration examples.", GREEN, SOFT_GREEN)
card(7.15*inch, 4.3*inch, 2.85*inch, 1.45*inch, "What gets worse if closed", "Small builders depend on hidden private benchmarks they cannot audit or adapt.", RED, SOFT_RED)
round_rect(1.05*inch, 1.8*inch, 8.75*inch, 1.4*inch, CARD)
draw_text("Core thesis", 1.35*inch, 2.78*inch, 12, MUTED, "Helvetica-Bold")
draw_text("Agent safety should be something builders can run locally, not only something platforms sell privately.", 1.35*inch, 2.4*inch, 16, INK, "Helvetica-Bold", max_w=8.0*inch)
footer(5)
c.showPage()

# ─── Slide 6: Roadmap ────────────────────────────────────────────────────────
set_bg(); header("Grant plan", "A $25,000 grant turns the prototype into a stronger public benchmark and toolkit.")
items = [
    ("Month 1", "Benchmark foundation", "20+ curated traces, stable rule IDs, redaction guide, CI docs", BLUE),
    ("Month 2", "Integrations", "Transcript adapters, web3 checks, infrastructure checks, case studies", GREEN),
    ("Month 3", "Public v0.1", "50+ trace benchmark, downstream templates, benchmark report, release", AMBER),
]
for i, (m, h, b, col) in enumerate(items):
    y = 4.75*inch - i*1.28*inch
    c.setFillColor(col); c.roundRect(0.9*inch, y, 1.05*inch, 0.7*inch, 14, fill=1, stroke=0)
    draw_text(str(i+1), 1.27*inch, y + 0.22*inch, 20, colors.white, "Helvetica-Bold")
    round_rect(2.15*inch, y - 0.02*inch, 7.8*inch, 0.78*inch, CARD)
    draw_text(m + "  -  " + h, 2.45*inch, y + 0.46*inch, 13, INK, "Helvetica-Bold")
    draw_text(b, 2.45*inch, y + 0.18*inch, 10.5, MUTED, max_w=7.0*inch)
round_rect(0.9*inch, 0.85*inch, 9.05*inch, 0.85*inch, SOFT_BLUE)
draw_text("Outcome: a usable open benchmark that helps builders verify agent actions before trusting them.", 1.18*inch, 1.28*inch, 12, INK, "Helvetica-Bold", max_w=8.3*inch)
footer(6)
c.showPage()

c.save()
print(f"Generated: {PDF}")
