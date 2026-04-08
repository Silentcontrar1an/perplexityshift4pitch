"""
Shift4 Payments (FOUR) — Long Thesis
Investment Pitch PDF — Nicholas Steiglehner, Michigan Ross
Perplexity Pitch Prompt Competition, April 2026
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
import os

# ── FONTS ─────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('Inter', '/home/user/workspace/pdf_fonts/InterVariable.ttf'))
# Use Helvetica variants for bold/italic since Inter is variable
FONT_BODY   = 'Helvetica'
FONT_BOLD   = 'Helvetica-Bold'
FONT_ITALIC = 'Helvetica-Oblique'
FONT_BOLDITALIC = 'Helvetica-BoldOblique'

# ── COLORS (Pershing Square palette) ──────────────────────────────────────
PS_NAVY   = HexColor('#1A3C6B')   # primary blue — titles, nav
PS_GREEN  = HexColor('#4A7B40')   # banner green
PS_YELLOW = HexColor('#FFFFC0')   # yellow callout bg
PS_YELLOW_BORDER = HexColor('#C8C800')
PS_BLUE_MID = HexColor('#2E6DA4') # secondary blue — links, consensus
PS_RED    = HexColor('#C0392B')   # negative / warning
PS_BODY   = HexColor('#1A1A1A')
PS_MUTED  = HexColor('#555555')
PS_FAINT  = HexColor('#888888')
PS_LIGHT_BLUE = HexColor('#EBF3FA')
TABLE_HEADER_BG = PS_NAVY

W, H = letter
MARGIN = 0.85 * inch
COL_WIDTH = W - 2 * MARGIN

# ── STYLES ────────────────────────────────────────────────────────────────
def make_styles():
    return {
        'cover_title': ParagraphStyle('cover_title',
            fontName=FONT_BOLDITALIC, fontSize=36, leading=42,
            textColor=PS_NAVY, spaceAfter=8),
        'cover_subtitle': ParagraphStyle('cover_subtitle',
            fontName=FONT_ITALIC, fontSize=16, leading=20,
            textColor=PS_BLUE_MID, spaceAfter=6),
        'cover_tagline': ParagraphStyle('cover_tagline',
            fontName=FONT_ITALIC, fontSize=12, leading=16,
            textColor=PS_MUTED, spaceAfter=20),
        'cover_name': ParagraphStyle('cover_name',
            fontName=FONT_BOLD, fontSize=12, textColor=PS_NAVY, spaceAfter=2),
        'cover_school': ParagraphStyle('cover_school',
            fontName=FONT_BODY, fontSize=11, textColor=PS_MUTED, spaceAfter=2),
        'cover_date': ParagraphStyle('cover_date',
            fontName=FONT_BODY, fontSize=10, textColor=PS_FAINT),
        'section_title': ParagraphStyle('section_title',
            fontName=FONT_BOLDITALIC, fontSize=20, leading=24,
            textColor=PS_NAVY, spaceBefore=6, spaceAfter=4),
        'banner': ParagraphStyle('banner',
            fontName=FONT_BOLD, fontSize=10, leading=14,
            textColor=white, spaceAfter=0),
        'body': ParagraphStyle('body',
            fontName=FONT_BODY, fontSize=10, leading=15,
            textColor=PS_BODY, spaceAfter=8),
        'body_bold': ParagraphStyle('body_bold',
            fontName=FONT_BOLD, fontSize=10, leading=15,
            textColor=PS_BODY, spaceAfter=8),
        'yellow': ParagraphStyle('yellow',
            fontName=FONT_BOLDITALIC, fontSize=10, leading=14,
            textColor=PS_BODY),
        'source': ParagraphStyle('source',
            fontName=FONT_BODY, fontSize=8, leading=11,
            textColor=PS_FAINT, spaceAfter=4),
        'subsection': ParagraphStyle('subsection',
            fontName=FONT_BOLDITALIC, fontSize=13, leading=16,
            textColor=PS_NAVY, spaceBefore=12, spaceAfter=4),
        'bullet': ParagraphStyle('bullet',
            fontName=FONT_BODY, fontSize=10, leading=14,
            textColor=PS_BODY, spaceAfter=4,
            leftIndent=12, firstLineIndent=0),
        'table_header': ParagraphStyle('table_header',
            fontName=FONT_BOLD, fontSize=8.5, leading=11,
            textColor=white),
        'table_body': ParagraphStyle('table_body',
            fontName=FONT_BODY, fontSize=9, leading=12,
            textColor=PS_BODY),
        'table_green': ParagraphStyle('table_green',
            fontName=FONT_BOLD, fontSize=9, leading=12,
            textColor=PS_GREEN),
        'table_blue': ParagraphStyle('table_blue',
            fontName=FONT_BOLD, fontSize=9, leading=12,
            textColor=PS_BLUE_MID),
        'table_red': ParagraphStyle('table_red',
            fontName=FONT_BODY, fontSize=9, leading=12,
            textColor=PS_RED),
    }

S = make_styles()

# ── HELPER FLOWABLES ──────────────────────────────────────────────────────
class Banner(Flowable):
    def __init__(self, text, bg=PS_GREEN, width=COL_WIDTH, padding=10):
        Flowable.__init__(self)
        self.text = text
        self.bg = bg
        self.width = width
        self.padding = padding
        self._style = ParagraphStyle('b', fontName=FONT_BOLD, fontSize=10,
                                     leading=14, textColor=white)
        self._para = Paragraph(text, self._style)
        self._para.wrap(width - 2*padding, 9999)
        self.height = self._para.height + 2*padding + 4

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.width, self.height, 3, fill=1, stroke=0)
        self._para.drawOn(c, self.padding, self.padding + 2)

class YellowBox(Flowable):
    def __init__(self, text, width=COL_WIDTH, padding=10):
        Flowable.__init__(self)
        self.width = width
        self.padding = padding
        style = ParagraphStyle('y', fontName=FONT_BOLDITALIC, fontSize=10,
                               leading=14, textColor=PS_BODY)
        self._para = Paragraph(text, style)
        self._para.wrap(width - 2*padding, 9999)
        self.height = self._para.height + 2*padding + 4

    def draw(self):
        c = self.canv
        c.setFillColor(PS_YELLOW)
        c.setStrokeColor(PS_YELLOW_BORDER)
        c.roundRect(0, 0, self.width, self.height, 3, fill=1, stroke=1)
        self._para.drawOn(c, self.padding, self.padding + 2)

def rule():
    return HRFlowable(width='100%', thickness=2.5, color=PS_NAVY,
                      spaceAfter=8, spaceBefore=2)

def section_header(title, banner_text, src=None):
    out = []
    out.append(Spacer(1, 0.15*inch))
    out.append(Paragraph(title, S['section_title']))
    out.append(rule())
    out.append(Banner(banner_text))
    out.append(Spacer(1, 0.1*inch))
    return out

def close_section(yellow_text, src_text=None):
    out = []
    out.append(Spacer(1, 0.1*inch))
    out.append(YellowBox(yellow_text))
    if src_text:
        out.append(Spacer(1, 0.06*inch))
        out.append(Paragraph(f"Source: {src_text}", S['source']))
    return out

def make_table(headers, rows, col_widths=None, alt_rows=True):
    """Build a styled PS-format table."""
    if col_widths is None:
        col_widths = [COL_WIDTH / len(headers)] * len(headers)

    hrow = [Paragraph(h, S['table_header']) for h in headers]
    data = [hrow]
    for r in rows:
        data.append([Paragraph(str(c), S['table_body']) if not isinstance(c, Paragraph) else c for c in r])

    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), TABLE_HEADER_BG),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('GRID', (0,0), (-1,-1), 0.4, HexColor('#C5D9E8')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]
    if alt_rows:
        for i in range(2, len(data), 2):
            style_cmds.append(('BACKGROUND', (0,i), (-1,i), PS_LIGHT_BLUE))

    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(style_cmds))
    return t

def p(text, style='body'):   return Paragraph(text, S[style])
def b(text):                  return Paragraph(f"<b>{text}</b>", S['body'])
def sp(n=0.1):                return Spacer(1, n*inch)

# ── PAGE TEMPLATE ─────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(PS_NAVY)
    canvas.rect(0, H - 0.4*inch, W, 0.4*inch, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont(FONT_BOLD, 9)
    canvas.drawString(MARGIN, H - 0.28*inch, "SHIFT4 PAYMENTS (FOUR) — LONG THESIS")
    canvas.setFont(FONT_BODY, 9)
    canvas.drawRightString(W - MARGIN, H - 0.28*inch, "Nicholas Steiglehner | Michigan Ross")
    # Footer
    canvas.setFillColor(PS_FAINT)
    canvas.setFont(FONT_BODY, 7.5)
    canvas.drawString(MARGIN, 0.35*inch, "This is not investment advice. For informational purposes only.")
    canvas.drawRightString(W - MARGIN, 0.35*inch, f"Page {doc.page}")
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    canvas.restoreState()

# ── BUILD STORY ───────────────────────────────────────────────────────────
def build_story():
    story = []

    # ══ COVER PAGE ══════════════════════════════════════════════════════
    story.append(sp(2.0))
    story.append(Paragraph("Shift4 Payments", S['cover_title']))
    story.append(Paragraph("(FOUR) — Long", S['cover_title']))
    story.append(sp(0.15))
    story.append(Paragraph("The Modern Rails of Commerce", S['cover_subtitle']))
    story.append(sp(0.1))
    story.append(Paragraph(
        "Shift4 is being priced as a leveraged software integrator at peak complexity. "
        "It is a toll-road on physical commerce with fixed-rate debt and $500M of annual FCF. "
        "The market is confusing the balance sheet with the business.",
        S['cover_tagline']))
    story.append(sp(0.5))

    # Cover metrics table
    cover_data = [
        [Paragraph(h, S['table_header']) for h in ['ENTRY PRICE', '5-YR TARGET', 'IRR', 'EV/EBITDA FY26']],
        [p('$42.56', 'body_bold'), Paragraph('<font color="#4A7B40"><b>$284+</b></font>', S['body']),
         Paragraph('<font color="#4A7B40"><b>49%</b></font>', S['body']),
         Paragraph('<font color="#2E6DA4"><b>6.78×</b></font>', S['body'])],
    ]
    cover_t = Table(cover_data, colWidths=[COL_WIDTH/4]*4)
    cover_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PS_NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#C5D9E8')),
    ]))
    story.append(cover_t)
    story.append(sp(1.5))
    story.append(HRFlowable(width='100%', thickness=1, color=HexColor('#CCCCCC')))
    story.append(sp(0.2))
    story.append(Paragraph("Nicholas Steiglehner", S['cover_name']))
    story.append(Paragraph("University of Michigan, Ross School of Business", S['cover_school']))
    story.append(Paragraph("Perplexity Pitch Prompt Competition — April 2026", S['cover_date']))
    story.append(PageBreak())

    # ══ 1. INVESTMENT THESIS ════════════════════════════════════════════
    story += section_header(
        "Shift4 Trades at the Cheapest Valuation in Its Six-Year Public History",
        "A founder-led compounder at 6.78× FY2026E EBITDA — the market is pricing two temporary "
        "concerns as permanent impairment. Both resolve on a calendar that is public knowledge."
    )
    story.append(p("Shift4 is a <b>founder-led, capital-light compounder</b> in the early innings of global scale. "
        "It earns a recurring toll on every transaction it touches, combining network economics with the pricing power "
        "of deeply integrated vertical software. Since 2021, GRLNF has grown more than 4×, EBITDA margins have expanded "
        "600bps to ~50%, and FCF has gone from negative to $500M annually."))
    story.append(p("<b>Growth is self-determined — not macro-dependent.</b> Revenue is driven by new merchant wins and "
        "backlog conversion, not underlying consumer spending. The blended spread of 62bps has remained stable even "
        "as Shift4 moves upmarket and expands internationally. This is pricing power, not volume inflation."))

    # Business metrics table
    biz_rows = [
        ['GRLNF / Revenue', '$1.0B', '$2.6B', '$4.2B', Paragraph('<b><font color="#4A7B40">+4.2×</font></b>', S['table_body'])],
        ['EBITDA', '~$160M', '$366M', '$970M', Paragraph('<b><font color="#4A7B40">+6.1×</font></b>', S['table_body'])],
        ['Free Cash Flow', '($105M)', '$251M', '$500M', Paragraph('<b><font color="#4A7B40">Positive</font></b>', S['table_body'])],
        ['E2E Payment Volume', '~$46B', '$109B', '$209B', Paragraph('<b><font color="#4A7B40">+4.5×</font></b>', S['table_body'])],
        ['Countries', '~5', '~20', '75+', Paragraph('<b><font color="#4A7B40">Global franchise</font></b>', S['table_body'])],
    ]
    story.append(make_table(['METRIC', 'FY2021A', 'FY2023A', 'FY2025A', 'CHANGE'], biz_rows,
                            [COL_WIDTH*0.30, COL_WIDTH*0.16, COL_WIDTH*0.16, COL_WIDTH*0.16, COL_WIDTH*0.22]))
    story.append(sp(0.15))

    story.append(Paragraph("The Quasi-LBO Framework", S['subsection']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=PS_NAVY, spaceAfter=6))
    story.append(p("In private equity, returns decompose cleanly: revenue growth, margin expansion, exit multiple, "
        "and the cumulative impact of free cash flow used to pay down debt or repurchase equity. The equity check "
        "compounds not only because the business grows, but because <b>leverage amplifies the value accruing above "
        "a relatively fixed debt layer</b>. Every dollar of EV growth disproportionately benefits the equity holder. "
        "The same framework applies to public equities — it's just rarely used."))
    story.append(p("Start with enterprise value rather than earnings per share. Project EBITDA forward. Apply a "
        "conservative exit multiple. Bridge back to equity after accounting for cumulative FCF and share count changes. "
        "P/E reflects the current interest burden — it doesn't reflect the migration of value from the debt tranche "
        "to the equity tranche as free cash flow accumulates. <b>This isn't financial engineering, it's structural math.</b>"))
    story.append(p("When the answers to the five questions are yes — Is the business durable? Is growth self-determined? "
        "Is the balance sheet safe? Is management rational? Does the current EV allow for attractive IRR without multiple "
        "expansion? — and leverage adds structural convexity rather than risk, the opportunity resembles "
        "<b>a small buyout hiding in plain sight.</b>"))
    story.append(p("<i>The weighing machine, in time, tends to respect arithmetic. $FOUR is a textbook example of this.</i>"))
    story += close_section(
        "The market's entire bear thesis is one sentence: elevated leverage and an unproven acquisition. "
        "Both are temporary, measurable, and resolving on a calendar that is public knowledge.",
        "Perplexity Finance (perplexity.ai/finance/FOUR), Shift4 earnings filings, PitchBook"
    )
    story.append(PageBreak())

    # ══ 2. WHY IT'S CHEAP ═══════════════════════════════════════════════
    story += section_header(
        "The Market Is Pricing Two Temporary Concerns as Permanent",
        "Peak leverage of 3.73× in Q1 2026 is the designed peak — not a structural flaw. "
        "Global Blue contributes $200M+ EBITDA before any cross-sell synergies."
    )
    disc_rows = [
        [Paragraph('<b>Market Sees</b>', S['table_body']), Paragraph('<b>Reality</b>', S['table_body'])],
        ['3.7× leverage — scary', 'Peaks Q1 2026, drops every quarter for 2 years to 2.0×'],
        ['GAAP P/E of 18×', 'FCF yield 14.1%, PEG 0.24'],
        ['Complex cap structure', 'TRA eliminated forever, deleverage on autopilot'],
        ['M&A integration risk', 'Same playbook executed 10+ times successfully'],
        ['Global Blue dilution', 'Contributes $200M+ EBITDA on TFS/DCC alone; zero synergy in guide'],
    ]
    story.append(make_table(['MARKET SEES', 'REALITY'], disc_rows[1:],
                            [COL_WIDTH*0.40, COL_WIDTH*0.60]))
    story.append(sp(0.1))
    story.append(p("<b>On leverage:</b> Q1 2026 is deliberately the peak. Three one-time cash drains hit simultaneously: "
        "TRA final payment ($139M, gone forever), Bambora acquisition ($84M), and $255M in buybacks. Management guided "
        "3.73× explicitly to show they fit within the 3.75× covenant. By Q4 2026 leverage reaches 2.99× on its own "
        "arithmetic. Sub-3× leverage = credit upgrade territory and institutional re-entry."))
    story.append(p("<b>On Global Blue:</b> The acquisition was underwritten on international market entry (75 countries "
        "instantly) and TFS leadership — not E2E cross-sell. Global Blue's TFS/DCC business contributes ~$200M+ annual "
        "EBITDA before any cross-sell. Management guides zero synergy in FY2026 — any H2 2026 merchant addition data "
        "is pure upside the market assigns no probability to."))
    story += close_section(
        "Both concerns resolve on a dated, public calendar. Sub-3× leverage by Q4 2026. Cross-sell data visible by H2 2026.",
        "Shift4 earnings filings, management guidance Q4 2025, PitchBook"
    )
    story.append(PageBreak())

    # ══ 3. FINANCIAL MODEL ══════════════════════════════════════════════
    story += section_header(
        "Operating Model: FY2025A → FY2030E",
        "Consensus estimates (Perplexity Finance) through FY2028 anchor the near-term model. "
        "Conservative 12% EBITDA CAGR extends to FY2030 — below the 18% Shift4 has delivered since 2022."
    )
    op_rows = [
        ['Revenue (GRLNF)', '$4,180M', Paragraph('<font color="#2E6DA4">$5,077M ★</font>', S['table_body']),
         Paragraph('<font color="#2E6DA4">$5,786M ★</font>', S['table_body']),
         Paragraph('<font color="#2E6DA4">$6,728M ★</font>', S['table_body']),
         '$7,674M', '$8,749M'],
        ['YoY Growth', '+26%', '+21%', '+14%', '+16%', '+14%', '+14%'],
        ['EBITDA', '$970M', Paragraph('<font color="#2E6DA4">$1,185M ★</font>', S['table_body']),
         Paragraph('<font color="#2E6DA4">$1,367M ★</font>', S['table_body']),
         Paragraph('<font color="#2E6DA4">$1,599M ★</font>', S['table_body']),
         '$1,791M', Paragraph('<b><font color="#4A7B40">$2,006M</font></b>', S['table_body'])],
        ['Free Cash Flow', '$500M', Paragraph('<font color="#2E6DA4">$549M ★</font>', S['table_body']),
         Paragraph('<font color="#2E6DA4">$684M ★</font>', S['table_body']),
         '$780M', '$880M', '$990M'],
        ['FCF / Share', '$5.78', '$7.47', '$9.24', '$10.54', '$11.89',
         Paragraph('<b><font color="#4A7B40">$13.38</font></b>', S['table_body'])],
        ['EV/EBITDA (at $42.56)', '8.3×', Paragraph('<b><font color="#4A7B40">6.8×</font></b>', S['table_body']),
         '5.9×', '5.1×', '4.5×', '4.0×'],
    ]
    cw = [COL_WIDTH*0.23] + [COL_WIDTH*0.77/6]*6
    story.append(make_table(['METRIC','FY2025A','FY2026E','FY2027E','FY2028E','FY2029E','FY2030E'], op_rows, cw))
    story.append(Paragraph("★ = consensus estimates (Perplexity Finance). FY2029E–FY2030E = author projections at 12% EBITDA CAGR.", S['source']))
    story.append(sp(0.1))
    story.append(p("<b>The EV/EBITDA compression tells the story:</b> At $42.56, FOUR trades at 6.8× FY2026E EBITDA. "
        "At 10× FY2030E EBITDA (below its public market average), implied equity value = $231/share — "
        "before World Cup, Global Blue cross-sell, or gateway conversion upside."))
    story.append(sp(0.15))

    story.append(Paragraph("Deleverage: 3.73× → 2.00× in 8 Quarters", S['subsection']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=PS_NAVY, spaceAfter=6))
    delev_rows = [
        ['Q4 25A', '3.69×', '$964M', '$970M', '—', ''],
        [Paragraph('<b><font color="#C0392B">Q1 26E</font></b>', S['table_body']),
         Paragraph('<b><font color="#C0392B">3.73×</font></b>', S['table_body']),
         Paragraph('<font color="#C0392B">$556M</font>', S['table_body']),
         Paragraph('<font color="#C0392B">$1,070M</font>', S['table_body']),
         Paragraph('<font color="#C0392B">+$70M</font>', S['table_body']),
         Paragraph('<i>Pain Quarter: $478M one-time cash drain</i>', S['table_body'])],
        ['Q2 26E', '3.53×', '$414M', '$1,170M', '+$148M', '$1B buyback COMPLETE'],
        [Paragraph('<b>Q4 26E</b>', S['table_body']),
         Paragraph('<b><font color="#4A7B40">2.99×</font></b>', S['table_body']),
         '$631M', '$1,307M', '+$145M',
         Paragraph('<b><font color="#4A7B40">SUB-3× ACHIEVED</font></b>', S['table_body'])],
        [Paragraph('<b>Q4 27E</b>', S['table_body']),
         Paragraph('<b><font color="#4A7B40">2.00×</font></b>', S['table_body']),
         '$748M', '$1,580M', '+$175M',
         Paragraph('<b><font color="#4A7B40">Near investment grade</font></b>', S['table_body'])],
    ]
    story.append(make_table(['QUARTER','LEVERAGE','CASH','LTM EBITDA','FCF','KEY EVENT'],
                            delev_rows,
                            [COL_WIDTH*0.11, COL_WIDTH*0.11, COL_WIDTH*0.12, COL_WIDTH*0.14, COL_WIDTH*0.11, COL_WIDTH*0.41]))
    story += close_section(
        "Sub-3× leverage by Q4 2026 equals credit upgrade territory. Institutional mandates currently excluded "
        "from FOUR become buyers on a schedule.",
        "Shift4 earnings filings, management guidance Q4 2025"
    )
    story.append(PageBreak())

    # ══ 4. VALUATION ════════════════════════════════════════════════════
    story += section_header(
        "Three Independent Methods. One Conclusion.",
        "DCF implies $149/share floor. Sum-of-parts implies $97 at today's depressed multiples. "
        "Precedent transactions imply $196. All at a current price of $42.56."
    )
    val_rows = [
        ['DCF (10% WACC, 3% TGR)',
         Paragraph('<b><font color="#4A7B40">$149</font></b>', S['table_body']), '+251%',
         'All 25/25 sensitivity cells imply upside. Bear floor: $91 (still 2.1× current).'],
        ['Sum-of-Parts (zero synergy)',
         Paragraph('<b><font color="#4A7B40">$97</font></b>', S['table_body']), '+128%',
         'Americas 9×, Global Blue 7×, SkyTab 15× — at today\'s depressed sector multiples.'],
        ['Precedent Transactions (median 15×)',
         Paragraph('<b><font color="#4A7B40">$196</font></b>', S['table_body']), '+361%',
         'EVO Payments 14×, Heartland 26×, Ingenico 20×, WorldPay 12×. FOUR at 6× = 57% discount.'],
        [Paragraph('<b>Conservative 5-Year Exit (10×)</b>', S['table_body']),
         Paragraph('<b><font color="#4A7B40">$284</font></b>', S['table_body']),
         Paragraph('<b><font color="#4A7B40">+567%</font></b>', S['table_body']),
         '6.67× MOIC | 49% IRR | 12% EBITDA CAGR | No multiple expansion required.'],
    ]
    story.append(make_table(['METHOD', 'IMPLIED PRICE', 'VS. $42.56', 'NOTES'], val_rows,
                            [COL_WIDTH*0.30, COL_WIDTH*0.15, COL_WIDTH*0.12, COL_WIDTH*0.43]))
    story.append(sp(0.1))
    story.append(p("On management guide alone (zero beat): GRLNF +29%, EBITDA $1,190M, FCF $500M. "
        "EV/EBITDA <b>6.0×</b>. FCF yield <b>14.1%</b>. PEG ratio <b>0.24</b>. "
        "Founder bought $13.7M at $44–48. Short interest 33% of float at 12.9% borrow rate."))
    story += close_section(
        "Name another 29% GRLNF grower at 6.0× EBITDA — on guide — with the founder buying $13.7M at the lows.",
        "Perplexity Finance, CB Insights M&A database, Capital IQ precedent transactions"
    )
    story.append(PageBreak())

    # ══ 5. DIFFERENTIATED ANALYSES ══════════════════════════════════════
    story += section_header(
        "Differentiated Analyses — Only Possible with Perplexity",
        "Three original analyses built from primary sources that are not in any sell-side note."
    )

    story.append(Paragraph("I. The Volume Signal: Structural, Not Cyclical", S['subsection']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=PS_NAVY, spaceAfter=6))
    story.append(p("As US hotel RevPAR declined in 2025, Shift4's E2E payment volume grew 23–27%. "
        "The spread between FOUR's growth and its end-markets' growth averaged <b>37 percentage points</b> "
        "over 8 consecutive quarters. Volume growth is a function of new merchant activations and "
        "gateway-to-E2E conversions — not same-store consumer spending. These are categorically different variables."))
    vol_rows = [
        ['Q1 2024', '+49.8%', '+3%', Paragraph('<b><font color="#4A7B40">+47pp</font></b>', S['table_body'])],
        ['Q4 2024', '+49.2%', '+1%', Paragraph('<b><font color="#4A7B40">+48pp</font></b>', S['table_body'])],
        ['Q2 2025', '+24.9%', '−1%', Paragraph('<b><font color="#4A7B40">+26pp</font></b>', S['table_body'])],
        ['Q4 2025', '+23.6%', '−1%', Paragraph('<b><font color="#4A7B40">+25pp</font></b>', S['table_body'])],
        [Paragraph('<b>8Q Average</b>', S['table_body']),
         Paragraph('<b>+39.2%</b>', S['table_body']),
         Paragraph('<b>+0.5%</b>', S['table_body']),
         Paragraph('<b><font color="#4A7B40">+37pp</font></b>', S['table_body'])],
    ]
    story.append(make_table(['QUARTER','FOUR E2E VOLUME YOY','US HOTEL REVPAR YOY','SPREAD'], vol_rows,
                            [COL_WIDTH*0.22]*4))

    story.append(sp(0.15))
    story.append(Paragraph("II. Gateway-to-E2E Conversion: $141M Hiding in the Existing Base", S['subsection']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=PS_NAVY, spaceAfter=6))
    story.append(p("Shift4 has ~$150B of gateway-only volume earning 15bps. Converting to E2E earns 62bps — "
        "a <b>4.1× revenue uplift</b> requiring zero new merchants, zero M&A, and zero macro tailwind. "
        "Bambora's acquisition (Q1 2026) added $90B of gateway volume to the conversion pipeline."))
    gw_rows = [
        ['Bear', '10%', '$15B', '+$70M', '+$35M', '+$0.41'],
        [Paragraph('<b>Base</b>', S['table_body']),
         '<b>20%</b>', '<b>$30B</b>', '<b>+$141M</b>',
         Paragraph('<b><font color="#4A7B40">+$70M</font></b>', S['table_body']),
         Paragraph('<b><font color="#4A7B40">+$0.82</font></b>', S['table_body'])],
        ['Bull', '35%', '$52.5B', '+$247M', '+$124M', '+$1.43'],
    ]
    story.append(make_table(['SCENARIO','CONV %','VOLUME','INCR. REV','INCR. EBITDA','FCF/SHARE UPLIFT'],
                            gw_rows, [COL_WIDTH*0.14]*6))

    story.append(sp(0.15))
    story.append(Paragraph("III. Insider Conviction: $46M at Every Major Dip", S['subsection']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=PS_NAVY, spaceAfter=6))
    story.append(p("Jared Isaacman has made 10 open-market purchases since IPO. His weighted average cost basis is <b>$63.56</b>. "
        "He bought $16.3M in August 2025 (the day Global Blue closed) and $4M in March 2026 at the 52-week low — "
        "simultaneously with the company's $1B buyback. Two buyers, same conclusion, same timing."))
    ins_rows = [
        ['Nov 2022', '$41.80', '120,000', '$5.0M', 'Rate-hike compression'],
        ['Aug 2025', '$82.81', '196,426', Paragraph('<b>$16.3M ← Largest</b>', S['table_body']), 'Day Global Blue closed'],
        ['Mar 2026', '$44.79 avg', '89,520', '$4.0M', '52-week low, active buyback'],
        [Paragraph('<b>Total</b>', S['table_body']), Paragraph('<b>$63.56 avg</b>', S['table_body']),
         Paragraph('<b>725K shares</b>', S['table_body']),
         Paragraph('<b><font color="#4A7B40">$46.1M</font></b>', S['table_body']), '10 transactions since IPO'],
    ]
    story.append(make_table(['DATE','PRICE','SHARES','VALUE','CONTEXT'], ins_rows,
                            [COL_WIDTH*0.14, COL_WIDTH*0.16, COL_WIDTH*0.16, COL_WIDTH*0.16, COL_WIDTH*0.38]))
    story += close_section(
        "These three analyses — the volume signal, the gateway conversion model, and the insider conviction map — "
        "are not in any sell-side research note. They required primary source analysis only possible with Perplexity Computer.",
        "Shift4 earnings filings, CoStar/STR Hotel RevPAR, SEC Form 4 filings, OpenInsider.com"
    )
    story.append(PageBreak())

    # ══ 6. BEAR CASE & CATALYSTS ═════════════════════════════════════════
    story += section_header(
        "The Bear Case, Steelmanned and Answered",
        "The entire bear thesis is: elevated leverage and an unproven acquisition. "
        "Both are temporary, measurable, and resolving on a public timeline."
    )
    bear_rows = [
        [Paragraph('<b>Bear:</b> 3.73× leverage — covenant breach risk', S['table_body']),
         Paragraph('Q1 is the PEAK by design. Three one-time drains ($478M combined). Management guided '
                   '3.73× explicitly. By Q4 2026: 2.99× on its own arithmetic. Fixed-rate debt, long maturities.',
                   S['table_body'])],
        [Paragraph('<b>Bear:</b> Global Blue cross-sell never materializes', S['table_body']),
         Paragraph('Acquisition underwritten on intl. market entry and TFS leadership — not cross-sell. '
                   'Global Blue contributes $200M+ EBITDA from TFS/DCC alone. FY26 guide embeds zero synergy.',
                   S['table_body'])],
        [Paragraph('<b>Bear:</b> Stock has been "cheap" for 2 years — value trap', S['table_body']),
         Paragraph('Catalyst path is specific and dated: May \'26 (leverage peaked), Aug \'26 (buyback done), '
                   'Q4 \'26 (sub-3× = institutional re-entry), Aug \'27 (conv. note repaid, shorts forced to cover).',
                   S['table_body'])],
        [Paragraph('<b>Bear:</b> Lauber unproven as standalone CEO', S['table_body']),
         Paragraph('President/CSO since 2018. EBITDA margins held 49%+ through Global Blue integration. '
                   'Company went from 3K to 6K employees and 75 countries under his leadership. '
                   'Isaacman bought $4M at the lows in March 2026.',
                   S['table_body'])],
    ]
    story.append(make_table(['BEAR ARGUMENT', 'COUNTER'], bear_rows, [COL_WIDTH*0.40, COL_WIDTH*0.60]))
    story.append(sp(0.1))

    story.append(Paragraph("Catalyst Timeline", S['subsection']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=PS_NAVY, spaceAfter=6))
    cat_rows = [
        ['May 2026', 'Q1 Earnings', '3.73× leverage (better than feared 4.0×+). Pain quarter absorbed.'],
        ['Jun 2026', 'FIFA World Cup', '78 US games, Shift4 processes ~64% of venues. DCC activated for intl. fans.'],
        ['Aug 2026', 'Q2 Earnings', 'Guidance raise likely. $1B buyback complete. ~18.8M shares retired.'],
        ['Q4 2026', 'Sub-3× Leverage', 'Credit upgrade territory. Institutional mandates reopen.'],
        ['Feb 2027', 'FY2026 Report', 'Sub-3× confirmed. New buyback authorization likely.'],
        ['Aug 2027', 'Conv. Note Repaid', '$632M debt eliminated. Conv. hedgers forced to cover (~1-1.5M shares).'],
        ['May 2028', 'Preferred Converts', '$60M/yr dividend eliminated. Clean cap structure.'],
    ]
    story.append(make_table(['DATE', 'EVENT', 'SIGNIFICANCE'], cat_rows,
                            [COL_WIDTH*0.14, COL_WIDTH*0.20, COL_WIDTH*0.66]))
    story += close_section(
        "True downside: EBITDA miss 15% AND 5× multiple compression simultaneously → ~$14/share. "
        "That requires both operational failure and multiple compression at once. "
        "Base case: $149–$284. Asymmetry: −$28 downside vs. +$107–$242 upside.",
        "Author analysis, Shift4 earnings filings, convertible note indenture"
    )
    story.append(PageBreak())

    # ══ 7. POSITION FRAMEWORK ═══════════════════════════════════════════
    story += section_header(
        "Why I Own This",
        "Conservative assumptions — 12% EBITDA CAGR, flat margins, 10× exit multiple — "
        "imply $284/share, a 6.67× MOIC, and a 49% IRR. No multiple expansion required."
    )
    pos_rows = [
        [Paragraph('<b>Is the business durable?</b>', S['table_body']),
         '28-year track record. 98%+ merchant retention. Embedded PMS/POS creates $250K–$1M switching costs. '
         '#1 in US hotels (~40%), stadiums (~75%), luxury retail globally.'],
        [Paragraph('<b>Is the growth self-determined?</b>', S['table_body']),
         'Backlog conversion and gateway-to-E2E migration, not consumer spending. '
         'Executed through COVID, rate hikes, and tariff uncertainty without missing.'],
        [Paragraph('<b>Is the balance sheet safe?</b>', S['table_body']),
         'Fixed-rate debt, maturities well into next decade. 3.73× peaks Q1, drops to 2.00× by Q4 2027. '
         '$964M starting cash, $500M+ annual FCF.'],
        [Paragraph('<b>Is management rational?</b>', S['table_body']),
         'Founder bought $46M in open-market purchases. $5.5B deployed at ~6× EBITDA returns. '
         'TRA elimination = $440M transferred to shareholders. $1B buyback at 6× EV/EBITDA.'],
        [Paragraph('<b>Attractive IRR without multiple expansion?</b>', S['table_body']),
         '49% IRR at 10× exit multiple on conservative EBITDA projections. '
         '6.78× EV/EBITDA with +29% GRLNF growth. PEG ratio 0.24.'],
    ]
    story.append(make_table(['QUESTION', 'ANSWER (YES)'], pos_rows, [COL_WIDTH*0.28, COL_WIDTH*0.72]))
    story.append(sp(0.15))

    final_metrics = [
        [Paragraph(h, S['table_header']) for h in ['ENTRY', 'TARGET', 'MOIC', 'IRR', 'EXIT MULTIPLE', 'EXIT YEAR']],
        ['$42.56', Paragraph('<b><font color="#4A7B40">$284</font></b>', S['table_body']),
         Paragraph('<b><font color="#4A7B40">6.67×</font></b>', S['table_body']),
         Paragraph('<b><font color="#4A7B40">49%</font></b>', S['table_body']),
         Paragraph('10× FY2030E<br/>EBITDA', S['table_body']), '2030'],
    ]
    fm_t = Table(final_metrics, colWidths=[COL_WIDTH/6]*6)
    fm_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PS_NAVY),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#C5D9E8')),
    ]))
    story.append(fm_t)
    story += close_section(
        "The position is sized for conviction, not consensus. When the market misclassifies an asset, "
        "the gap between price and value is not a risk — it is the entire opportunity. "
        "The weighing machine, in time, tends to respect arithmetic.",
        "Author model, Shift4 earnings filings"
    )
    story.append(PageBreak())

    # ══ 8. BUILT WITH PERPLEXITY ════════════════════════════════════════
    story += section_header(
        "Built with Perplexity Computer",
        "Every insight was produced using Perplexity Computer, Perplexity Finance, "
        "CB Insights, PitchBook, and Statista — in iterative multi-turn research sessions."
    )
    px_rows = [
        ['Earnings Transcript Analysis',
         '8 consecutive FOUR earnings calls. ~400,000 words analyzed. Confidence/caution ratio tracked '
         'quarterly — surfaces a regime change no sell-side note has quantified.'],
        ['CEO Podcast Extraction',
         'Full Taylor Lauber ICR podcast (31 min, March 2026) extracted via YouTube auto-captions. '
         '"Blackstone playbook" for international, DCC terminal strategy surfaced.'],
        ['World Cup Venue Model',
         'All 11 US World Cup venues researched individually. DCC revenue modeled from FIFA '
         'attendance projections and international fan spend benchmarks. Not in any analyst model.'],
        ['Global Blue Cross-Sell Model',
         'Revenue per converted merchant built from Global Blue TFS take rate (~3%) and '
         'Shift4\'s 62bps spread. Three penetration scenarios. Bear/base/bull: $100M/$175M/$250M.'],
        ['PitchBook Premium',
         'FOUR IPO at $1.85B post-money on $737M revenue (June 2020). Today: $4.2B revenue, '
         '$970M EBITDA — same market cap. The dislocation only visible with primary funding data.'],
        ['CB Insights Premium',
         'Payments M&A consolidation wave. Integrated businesses acquired at 12–26× EBITDA. '
         'FOUR at 6× is the clearest expression of this valuation gap in the public market.'],
        ['Statista Premium',
         'Hotel market $112B US annual revenue. DCC market $8.4B growing 9.9% CAGR to 2034. '
         'Duty-free/TFS market $46.7B growing 6.5% CAGR. Anchors the TAM analysis.'],
        ['25-Cell DCF Sensitivity',
         'Full DCF matrix (5 WACC × 5 TGR). All 25/25 cells imply upside from $42.56. '
         'Bear floor: $91/share (still 2.1× current price).'],
    ]
    story.append(make_table(['RESEARCH CAPABILITY', 'OUTPUT & INSIGHT'], px_rows,
                            [COL_WIDTH*0.28, COL_WIDTH*0.72]))
    story += close_section(
        "A traditional research workflow for this pitch would have required 3–4 weeks of analyst time. "
        "Perplexity Computer completed every step in hours — with live primary source data, "
        "programmatic analysis across 400K+ words, and interactive tools no PDF deck can replicate.",
        "Perplexity Computer, Perplexity Finance, CB Insights, PitchBook, Statista, SEC EDGAR"
    )

    return story

# ── GENERATE PDF ──────────────────────────────────────────────────────────
OUTPUT = "/home/user/workspace/four-pitch-repo/financial-models/FOUR_Investment_Pitch_Steiglehner.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=0.65*inch, bottomMargin=0.65*inch,
    title="Shift4 Payments (FOUR) — Long Thesis | Nicholas Steiglehner, Michigan Ross",
    author="Perplexity Computer",
)

story = build_story()
doc.build(story, onFirstPage=on_first_page, onLaterPages=on_page)

size = os.path.getsize(OUTPUT)
print(f"PDF generated: {OUTPUT}")
print(f"Size: {size/1024:.0f} KB")
