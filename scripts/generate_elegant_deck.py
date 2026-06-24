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
PDF = OUT / "Open_Agent_Safety_Kit_Grant_Deck_Elegant.pdf"

W, H = landscape(letter)
NAVY = colors.HexColor("#07111F")
NAVY2 = colors.HexColor("#0E1B2D")
INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#64748B")
BLUE = colors.HexColor("#3B82F6")
CYAN = colors.HexColor("#38BDF8")
MINT = colors.HexColor("#34D399")
GREEN = colors.HexColor("#10B981")
AMBER = colors.HexColor("#F59E0B")
RED = colors.HexColor("#EF4444")
PAPER = colors.HexColor("#F8FAFC")
CARD = colors.HexColor("#FFFFFF")
LINE = colors.HexColor("#D7E1EE")

c = canvas.Canvas(str(PDF), pagesize=landscape(letter))
c.setTitle("Open Agent Safety Kit Grant Deck")
c.setAuthor("Carly17")


def rect(x, y, w, h, fill, stroke=None, radius=0):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    else:
        c.setStrokeColor(fill)
    if radius:
        c.roundRect(x, y, w, h, radius, stroke=1 if stroke else 0, fill=1)
    else:
        c.rect(x, y, w, h, stroke=1 if stroke else 0, fill=1)


def txt(text, x, y, size: float = 12, color=INK, font="Helvetica", leading=None, max_width=None):
    c.setFillColor(color)
    c.setFont(font, size)
    if max_width is None:
        c.drawString(x, y, text)
        return y - (leading or size * 1.25)
    words = text.split()
    line = ""
    yy = y
    lead = leading or size * 1.35
    for word in words:
        test = (line + " " + word).strip()
        if stringWidth(test, font, size) <= max_width:
            line = test
        else:
            c.drawString(x, yy, line)
            yy -= lead
            line = word
    if line:
        c.drawString(x, yy, line)
        yy -= lead
    return yy


def title(text, subtitle=None, dark=False):
    color = colors.white if dark else INK
    sub = colors.HexColor("#BFD7FF") if dark else MUTED
    txt(text, 0.65*inch, H-0.82*inch, 26, color, "Helvetica-Bold")
    if subtitle:
        txt(subtitle, 0.65*inch, H-1.12*inch, 10.5, sub, max_width=8.9*inch)


def footer(n, dark=False):
    col = colors.HexColor("#6B7A90") if dark else colors.HexColor("#94A3B8")
    c.setFillColor(col)
    c.setFont("Helvetica", 7.5)
    c.drawString(0.55*inch, 0.28*inch, "Open Agent Safety Kit • MIT open source • github.com/Carlys17/open-agent-safety-kit")
    c.drawRightString(W-0.55*inch, 0.28*inch, str(n))


def bg_dark():
    rect(0, 0, W, H, NAVY)
    rect(0, 0, W, H, NAVY)
    # soft technical grid
    c.setStrokeColor(colors.HexColor("#10243B"))
    c.setLineWidth(0.3)
    for x in range(0, int(W), 42):
        c.line(x, 0, x, H)
    for y in range(0, int(H), 42):
        c.line(0, y, W, y)
    # orbit circles
    c.setStrokeColor(colors.HexColor("#1E3A5F"))
    c.setLineWidth(1.1)
    c.circle(8.9*inch, 5.6*inch, 1.3*inch, stroke=1, fill=0)
    c.circle(9.55*inch, 5.9*inch, 0.72*inch, stroke=1, fill=0)
    rect(8.95*inch, 5.58*inch, 1.28*inch, 1.28*inch, BLUE, radius=18)
    rect(8.46*inch, 5.2*inch, 0.62*inch, 0.62*inch, MINT, radius=14)


def bg_light():
    rect(0, 0, W, H, PAPER)
    rect(0, H-0.08*inch, W, 0.08*inch, BLUE)


def card(x, y, w, h, head, body, accent=BLUE):
    rect(x, y, w, h, CARD, LINE, radius=10)
    rect(x, y+h-0.08*inch, w, 0.08*inch, accent, radius=0)
    txt(head, x+0.18*inch, y+h-0.33*inch, 11.5, INK, "Helvetica-Bold", max_width=w-0.35*inch)
    txt(body, x+0.18*inch, y+h-0.65*inch, 9.2, MUTED, max_width=w-0.35*inch)


def pill(text, x, y, w, color):
    rect(x, y, w, 0.34*inch, color, radius=12)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(x+w/2, y+0.115*inch, text)

# 1 cover
bg_dark()
txt("Open Agent", 0.72*inch, 4.95*inch, 38, colors.white, "Helvetica-Bold")
txt("Safety Kit", 0.72*inch, 4.48*inch, 38, colors.white, "Helvetica-Bold")
txt("Open-source safety tests for AI agents before real-world deployment.", 0.78*inch, 3.95*inch, 15, colors.HexColor("#DDEBFF"), max_width=6.4*inch)
pill("RUNNABLE DEMO", 0.78*inch, 3.25*inch, 1.55*inch, BLUE)
pill("MIT OPEN SOURCE", 2.48*inch, 3.25*inch, 1.65*inch, MINT)
pill("GRANT ASK: $25K", 4.28*inch, 3.25*inch, 1.68*inch, AMBER)
txt("For solo builders and open-source teams who need transparent checks for agent tool use, verification, and failure modes.", 0.78*inch, 2.62*inch, 12.5, colors.HexColor("#BFD7FF"), max_width=6.1*inch)
footer(1, dark=True)
c.showPage()

# 2 problem
bg_light(); title("The problem", "Agents are no longer only answering. They are taking actions.")
card(0.72*inch, 4.65*inch, 2.95*inch, 1.35*inch, "False success", "Agent claims a deploy, upload, test, or transaction worked without evidence.", RED)
card(4.03*inch, 4.65*inch, 2.95*inch, 1.35*inch, "Unsafe tool use", "Shell, file writes, API calls, infrastructure, and wallets can create real side effects.", AMBER)
card(7.34*inch, 4.65*inch, 2.95*inch, 1.35*inch, "Closed evaluation", "Private benchmarks are hard for small builders to inspect, adapt, or trust.", BLUE)
txt("The key failure pattern", 0.78*inch, 3.75*inch, 16, INK, "Helvetica-Bold")
rect(0.78*inch, 2.15*inch, 9.55*inch, 1.25*inch, colors.HexColor("#EEF6FF"), LINE, radius=12)
txt("Agent takes action → skips verification → reports success → builder trusts an unverified result", 1.05*inch, 2.88*inch, 18, NAVY, "Helvetica-Bold", max_width=8.7*inch)
txt("A wrong answer is bad. A wrong action that looks successful is worse.", 1.05*inch, 2.48*inch, 12, MUTED, max_width=8.7*inch)
footer(2)
c.showPage()

# 3 solution architecture
bg_light(); title("The solution", "A local, inspectable safety layer for agent traces.")
# flow diagram
x0, y0 = 0.78*inch, 4.15*inch
steps = [("Agent trace", "messages + tool calls"), ("Open rules", "evidence-based checks"), ("Risk report", "score + recommendation"), ("CI gate", "block unsafe merges")]
for i,(h,b) in enumerate(steps):
    x = x0 + i*2.55*inch
    rect(x, y0, 1.95*inch, 1.05*inch, CARD, LINE, radius=12)
    txt(h, x+0.18*inch, y0+0.68*inch, 12, INK, "Helvetica-Bold")
    txt(b, x+0.18*inch, y0+0.42*inch, 8.6, MUTED, max_width=1.55*inch)
    if i < len(steps)-1:
        c.setStrokeColor(BLUE); c.setLineWidth(2); c.line(x+1.95*inch+0.12*inch, y0+0.52*inch, x+2.38*inch, y0+0.52*inch)
        c.setFillColor(BLUE); c.circle(x+2.38*inch, y0+0.52*inch, 3.2, stroke=0, fill=1)

checks = [
    ("False success", "success claim without tool evidence"),
    ("Missing verification", "side effect without readback/status"),
    ("Secret exposure", "tokens, keys, env, wallets"),
    ("Dangerous shell", "destructive commands and pipe-to-shell"),
    ("Network writes", "POST/PUT/DELETE without allowlist"),
    ("Web3 receipt gaps", "transactions without receipt/status"),
]
for i,(h,b) in enumerate(checks):
    row, col = divmod(i, 3)
    card(0.78*inch + col*3.22*inch, 1.65*inch - row*0.82*inch, 2.85*inch, 0.62*inch, h, b, [BLUE,MINT,AMBER,RED,CYAN,GREEN][i])
footer(3)
c.showPage()

# 4 demo
bg_light(); title("Runnable proof", "The repo already includes a CLI, examples, tests, and GitHub Actions.")
rect(0.75*inch, 4.35*inch, 4.55*inch, 1.38*inch, NAVY2, radius=12)
txt("$ oask run examples/traces/unsafe_false_success.json --format markdown", 0.98*inch, 5.25*inch, 10.5, colors.HexColor("#E5F0FF"), "Courier-Bold", max_width=4.05*inch)
txt("Agent: ‘I created the repository, deployed it, and everything is working.’", 0.98*inch, 4.82*inch, 10, colors.HexColor("#AFC7E8"), max_width=3.95*inch)
rect(5.68*inch, 4.35*inch, 4.55*inch, 1.38*inch, colors.HexColor("#FEF2F2"), colors.HexColor("#FECACA"), radius=12)
txt("FAIL • Risk score: 30/100", 5.96*inch, 5.23*inch, 17, RED, "Helvetica-Bold")
txt("Finding: false-success-without-evidence", 5.96*inch, 4.86*inch, 11, INK, "Helvetica-Bold")
txt("Recommendation: require a test, status check, readback, receipt, or health check before success claims.", 5.96*inch, 4.58*inch, 9.5, MUTED, max_width=3.95*inch)
# proof cards
card(0.78*inch, 2.45*inch, 2.95*inch, 1.05*inch, "Package", "Installable Python project with `oask` CLI.", BLUE)
card(4.03*inch, 2.45*inch, 2.95*inch, 1.05*inch, "Tests", "Unit tests verify safe and unsafe behavior.", MINT)
card(7.28*inch, 2.45*inch, 2.95*inch, 1.05*inch, "CI", "GitHub Actions runs on push and pull request.", GREEN)
txt("Repository: github.com/Carlys17/open-agent-safety-kit", 0.78*inch, 1.45*inch, 12.5, NAVY, "Helvetica-Bold")
footer(4)
c.showPage()

# 5 why open
bg_dark(); title("Why this should stay open", "Evaluation rules should be inspectable by the builders who depend on them.", dark=True)
rect(0.78*inch, 4.6*inch, 4.45*inch, 1.25*inch, colors.HexColor("#10243B"), colors.HexColor("#244A73"), radius=12)
txt("If closed", 1.02*inch, 5.35*inch, 16, colors.white, "Helvetica-Bold")
txt("Small builders depend on hidden rules, private benchmarks, and tools they cannot adapt to local workflows.", 1.02*inch, 5.02*inch, 10.5, colors.HexColor("#BFD7FF"), max_width=3.85*inch)
rect(5.78*inch, 4.6*inch, 4.45*inch, 1.25*inch, colors.HexColor("#0E3329"), colors.HexColor("#1E7A5B"), radius=12)
txt("If open", 6.02*inch, 5.35*inch, 16, colors.white, "Helvetica-Bold")
txt("Rules, traces, scoring, and examples become shared infrastructure that anyone can audit and improve.", 6.02*inch, 5.02*inch, 10.5, colors.HexColor("#C9FBE7"), max_width=3.85*inch)
txt("Target users", 0.78*inch, 3.5*inch, 17, colors.white, "Helvetica-Bold")
for i, label in enumerate(["solo builders", "open-source maintainers", "small AI teams", "web3 builders", "emerging-market developers"]):
    pill(label.upper(), 0.78*inch + (i%3)*2.35*inch, 2.82*inch - (i//3)*0.52*inch, 2.05*inch, [BLUE,MINT,AMBER,CYAN,GREEN][i])
footer(5, dark=True)
c.showPage()

# 6 roadmap
bg_light(); title("Three-month grant plan", "A small grant turns the prototype into a public benchmark and toolkit.")
months = [("01", "Benchmark foundation", "20+ curated traces, stable rule IDs, redaction guide, CI docs"), ("02", "Integrations", "Transcript adapters, web3 safety pack, infrastructure checks, case studies"), ("03", "Public v0.1", "50+ trace benchmark, downstream templates, benchmark report, release")]
for i,(m,h,b) in enumerate(months):
    y = 4.75*inch - i*1.25*inch
    rect(0.85*inch, y, 0.72*inch, 0.72*inch, BLUE if i==0 else MINT if i==1 else AMBER, radius=16)
    txt(m, 1.04*inch, y+0.26*inch, 15, colors.white, "Helvetica-Bold")
    rect(1.78*inch, y-0.03*inch, 8.05*inch, 0.82*inch, CARD, LINE, radius=10)
    txt(h, 2.05*inch, y+0.48*inch, 13, INK, "Helvetica-Bold")
    txt(b, 2.05*inch, y+0.21*inch, 9.5, MUTED, max_width=7.3*inch)
# metrics
rect(0.85*inch, 1.0*inch, 8.98*inch, 0.75*inch, colors.HexColor("#EEF6FF"), LINE, radius=12)
txt("Success metrics: public traces • rule packs • downstream projects • false-positive feedback • failures caught before deployment", 1.1*inch, 1.29*inch, 11, NAVY, "Helvetica-Bold", max_width=8.4*inch)
footer(6)
c.showPage()

# 7 ask
bg_dark(); title("Funding ask", "25,000 USD to make practical agent safety evaluation usable in the open.", dark=True)
for i,(h,b,col) in enumerate([
    ("40%", "engineering: evaluator, adapters, CI templates", BLUE),
    ("25%", "benchmark curation and trace collection", MINT),
    ("15%", "documentation and tutorials for solo builders", CYAN),
    ("10%", "web3 and infrastructure rule packs", AMBER),
    ("10%", "feedback, maintenance, release work", GREEN),
]):
    x = 0.9*inch + (i%3)*3.05*inch
    y = 4.55*inch - (i//3)*1.35*inch
    rect(x, y, 2.58*inch, 1.05*inch, colors.HexColor("#10243B"), colors.HexColor("#244A73"), radius=12)
    txt(h, x+0.18*inch, y+0.58*inch, 21, col, "Helvetica-Bold")
    txt(b, x+0.92*inch, y+0.66*inch, 9.5, colors.HexColor("#DCEBFF"), max_width=1.45*inch)
txt("Outcome", 0.9*inch, 1.95*inch, 18, colors.white, "Helvetica-Bold")
txt("A usable open benchmark and toolkit that helps independent builders verify agent actions before trusting them.", 0.9*inch, 1.55*inch, 13, colors.HexColor("#BFD7FF"), max_width=8.8*inch)
footer(7, dark=True)
c.showPage()

# 8 close
bg_light(); title("What gets better if this exists", "Agent safety becomes something builders can run, inspect, and improve locally.")
card(0.82*inch, 4.35*inch, 2.9*inch, 1.2*inch, "Before", "Agents can look successful without proof. Safety is hidden behind closed systems.", RED)
card(4.05*inch, 4.35*inch, 2.9*inch, 1.2*inch, "After", "Builders can check traces locally and see exactly why a workflow is risky.", GREEN)
card(7.28*inch, 4.35*inch, 2.9*inch, 1.2*inch, "Open AGI fit", "A shared safety layer that compounds in public instead of private evaluation silos.", BLUE)
txt("Open Agent Safety Kit", 0.82*inch, 2.7*inch, 25, NAVY, "Helvetica-Bold")
txt("github.com/Carlys17/open-agent-safety-kit", 0.82*inch, 2.28*inch, 15, BLUE, "Helvetica-Bold")
txt("Maintainer: Carly17 • solo builder from Indonesia • AI agents, automation, web3 testnets, security research", 0.82*inch, 1.93*inch, 11, MUTED, max_width=8.6*inch)
footer(8)
c.showPage()

c.save()
print(PDF)
