"""Create visibly labeled A3 DRAFT poster. Run locally after inserting screenshot/member data."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph

BASE=Path(__file__).resolve().parent
OUT=BASE/'docs'/'FinBridge_AI_A3_Poster_DRAFT.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
FONTS='/usr/share/fonts/truetype/dejavu'
if (Path(FONTS)/'DejaVuSans.ttf').exists():
    pdfmetrics.registerFont(TTFont('Poster', str(Path(FONTS)/'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('PosterBold', str(Path(FONTS)/'DejaVuSans-Bold.ttf')))
    P,PB='Poster','PosterBold'
else:
    P,PB='Helvetica','Helvetica-Bold'
W,H=landscape(A3)
C={"base":"#081422","card":"#102238","alt":"#14283e","line":"#29475f",
   "text":"#ecf5ff","muted":"#bed0e1","teal":"#2ddcb7","blue":"#77b6ff",
   "gold":"#f7ca74","white":"#ffffff","pink":"#f6a8ab"}
cv=canvas.Canvas(str(OUT),pagesize=(W,H))
cv.setTitle('FinBridge AI — A3 Academic Poster [Draft: Needs Team Details and Real Screenshot]')


def rect(x,y,w,h,color,r=0,stroke=None):
    cv.setFillColor(HexColor(color))
    cv.setStrokeColor(HexColor(stroke or color))
    cv.roundRect(x,y,w,h,r,stroke=int(stroke is not None),fill=1)


def txt(x,y,text,size=10,color='text',bold=False):
    cv.setFont(PB if bold else P,size)
    cv.setFillColor(HexColor(C.get(color,color)))
    cv.drawString(x,y,text)


def ptext(x,top,width,html,size=10,leading=None,color='text',bold=False):
    style=ParagraphStyle(name='para',fontName=PB if bold else P,fontSize=size,
        leading=leading or size*1.52,textColor=HexColor(C.get(color,color)),
        spaceBefore=0,spaceAfter=0,allowWidows=0,allowOrphans=0)
    para=Paragraph(html,style)
    _,height=para.wrap(width,1000)
    para.drawOn(cv,x,top-height)
    return height


def card(x,y,w,h,title,eyebrow=None):
    rect(x,y,w,h,C['card'],12,stroke=C['line'])
    top=y+h-18
    if eyebrow:
        txt(x+16,top,eyebrow,8,'teal',True)
        top-=22
    txt(x+16,top,title,14,'text',True)
    return top-15


def line(x1,y1,x2,y2,color='line',width=1):
    cv.setStrokeColor(HexColor(C.get(color,color)))
    cv.setLineWidth(width)
    cv.line(x1,y1,x2,y2)


rect(0,0,W,H,C['base'])
rect(0,H-107,W,107,'#102d43')
rect(32,H-108,82,4,'#39e0be')
txt(33,H-39,'UNIVERSITI TEKNOLOGI PETRONAS  |  INTERNATIONAL FINANCIAL MANAGEMENT',10,'teal',True)
txt(33,H-73,'FinBridge AI  /  Finance Tutor + Scenario Engine',27,'white',True)
txt(34,H-94,'Turn international finance theory into an interactive decision lab for non-finance students.',11,'muted')
rect(W-215,H-83,183,41,'#224b55',10)
txt(W-200,H-57,'CLO3  ·  3 VARIABLES',12,'teal',True)
txt(W-200,H-73,'Interest  |  Inflation  |  FX',9,'white')

rect(32,H-164,W-64,45,C['alt'],9,stroke=C['line'])
txt(47,H-136,'COURSE  GFB3043 / GEB3043',11,'text',True)
txt(47,H-155,'GROUP [XX]  |  STUDENTS: [FULL NAME • STUDENT ID • IT / IS / CS] × up to five',9,'gold',True)
txt(W-292,H-136,'SEMESTER  SEP 2026',10,'muted',True)
txt(W-292,H-155,'DRAFT • add real identities',9,'pink')

x1,x2,x3=32,410,788
cw=370
# LEFT COLUMN
Top=card(x1,523,cw,140,'The learning problem','01  ·  ISSUE & AUDIENCE')
ptext(x1+16,Top-4,cw-32,
      '<b>For:</b> non-finance Malaysian university students planning overseas tuition or learning international finance.<br/>'
      '<b>Pain point:</b> beginners reverse the MYR/USD direction, mix inflation effects with interest rates, and mistake an IRP forward for a guaranteed future spot.',10.0)

Top=card(x1,332,cw,180,'How the application works','02  ·  FUNCTIONAL WORKFLOW')
steps=[('1','Set synthetic inputs','MYR/USD, MY/US rates, inflation, years, USD cost'),
       ('2','Run finance engine','Exact PPP, IRP, Fisher and IFE calculations'),
       ('3','Explore shocks','Compare three cases; change one rate by ±2.5 pp'),
       ('4','Learn and check','Tutor feedback, quiz, audit trail, CSV/JSON')]
y=Top-15
for n,heading,desc in steps:
    rect(x1+16,y-6,24,24,'#1b534f',6)
    txt(x1+23,y+2,n,11,'teal',True)
    txt(x1+50,y+5,heading,10.1,'text',True)
    txt(x1+50,y-9,desc,8.2,'muted')
    y-=33

Top=card(x1,97,cw,224,'Explicit CLO3 finance linkage','03  ·  CORRECT THEORY & QUOTE')
PACES=[('PPP · inflation','Sₜ = S₀ × [(1+πMY)/(1+πUS)]ᵀ'),
       ('Covered IRP · interest','F = S₀ × [(1+iMY)/(1+iUS)]ᵀ'),
       ('Fisher · expected real rate','r = (1+i)/(1+πexpected) − 1'),
       ('IFE / UIP · expectation','Expected spot uses i gap; not a forward contract.')]
y=Top-12
for heading,formula in PACES:
    txt(x1+17,y,heading,10.3,'teal',True)
    txt(x1+17,y-17,formula,9.0,'text')
    y-=33
rect(x1+15,105,cw-30,25,'#213c4f',5)
ptext(x1+23,125,cw-47,'<b>Quote:</b> MYR/USD rises → MYR depreciates; falls → appreciates.',8.2)

# MIDDLE COLUMN
Top=card(x2,420,cw,243,'Working prototype view','04  ·  SCREENSHOT REQUIRED')
rect(x2+16,Top-184,cw-32,175,'#0c1c2b',8,stroke='#43687f')
line(x2+29,Top-37,x2+cw-29,Top-37,'line')
txt(x2+32,Top-26,'FINBRIDGE AI   |   SCENARIO ENGINE',10,'teal',True)
txt(x2+44,Top-73,'PASTE A GENUINE STREAMLIT',14,'gold',True)
txt(x2+44,Top-93,'BROWSER SCREENSHOT HERE',14,'gold',True)
ptext(x2+44,Top-111,cw-88,'App source is provided; live screenshot cannot be verified in this build environment.',9.0,color='muted')
# Screenshot placeholder intentionally kept visible until the group inserts an actual capture.

Top=card(x2,176,cw,234,'3 independently verified numerical cases','05  ·  ILLUSTRATIVE, 1 YEAR')
ptext(x2+16,Top-2,cw-32,'S₀ = 4.50 MYR/USD; US i = 5%; US π = 2%; tuition = USD 12,000.',9.3)
# table
X=x2+15; wcol=[125,60,63,90]
y=Top-50
rect(X,y-1,cw-30,25,'#244152',4)
for xx,v in zip([X+7,X+135,X+195,X+253],['CASE','MY i','MY π','PPP  |  IRP']):
    txt(xx,y+8,v,8,'text',True)
rows=[('01 Baseline','4.0%','3.0%','4.5441  |  4.4571'),
      ('02 Inflation','4.0%','6.5%','4.6985  |  4.4571'),
      ('03 Interest','7.0%','3.0%','4.5441  |  4.5857')]
for j,row in enumerate(rows):
    yy=y-29-j*30
    if j%2==0: rect(X,yy-9,cw-30,29,'#172f46',3)
    for xx,v in zip([X+7,X+135,X+195,X+253],row):txt(xx,yy+3,v,8.15,'text',j==0)
txt(X+3,y-111,'Inflation shock → PPP rises; interest shock → IRP rises.',8.5,'gold',True)
txt(X+3,y-124,'PPP tuition: RM 54,529 → RM 56,382 (inflation shock).',8.0,'muted')

Top=card(x2,97,cw,69,'Accuracy checks')
ptext(x2+15,Top-1,cw-30,'18 automated tests passed; 6 independent Decimal/parity checks in the engine; CSV/JSON export preserves assumptions.',8.7)

# RIGHT COLUMN
Top=card(x3,514,cw,159,'Main interpretation','07  ·  PLAIN LANGUAGE')
ptext(x3+16,Top-2,cw-32,
      'Malaysia expected inflation &gt; US inflation → <b>relative PPP</b> suggests MYR depreciation.<br/><br/>'
      'Higher MY nominal interest at unchanged US i → <b>covered IRP</b> raises MYR/USD forward; it does <b>not</b> promise tomorrow’s spot.<br/><br/>'
      'Fisher links expected inflation to nominal vs real rates.',9.65)

Top=card(x3,353,cw,150,'Market fit & future rollout','08  ·  VALUE & FEASIBILITY')
ptext(x3+16,Top-1,cw-32,
      '<b>Alternatives:</b> lecture slides, spreadsheet calculators, generic chatbots.<br/>'
      '<b>Why this differs:</b> coherent MYR/USD scenario engine, checked math, beginner feedback and misconception quiz.<br/>'
      '<b>Adoption:</b> free lecturer-led pilot; later campus hosting, official data feeds, mobile testing and language support.',9.7)

Top=card(x3,220,cw,123,'Responsible modelling','09  ·  LIMITATIONS')
ptext(x3+16,Top-2,cw-32,
      'All rates are <b>fictional</b>. PPP may diverge from short-run spot. IRP assumes no arbitrage, matching-term yields and minimal frictions. IFE / UIP requires additional expectation/risk assumptions. No live prices, tested learning gains or guaranteed forecasts.',9.55)

Top=card(x3,97,cw,112,'Institutional references','10  ·  TRACEABLE SOURCES')
ptext(x3+16,Top-2,cw-32,
      'CFA Institute (2026), <i>Currency Exchange Rates</i> • cfainstitute.org/insights/.../currency-exchange-rates-understanding-equilibrium-value<br/>'
      'Rogerson / CME (2024), <i>Covered Interest Parity</i> • cmegroup.com/articles/whitepapers/...<br/>'
      'Callen / IMF (2018), <i>Purchasing Power Parity</i> • imf.org/en/publications/fandd/...<br/>'
      'St. Louis Fed (2023), <i>Adjusting for Inflation</i> • stlouisfed.org/publications/page-one-economics/...',7.15,leading=11.7)

# footer
rect(32,23,W-64,61,'#1a344a',9)
ptext(47,69,W-100,'<b>DRAFT FOR GROUP COMPLETION:</b> Insert actual group number, full member names / student IDs / IT-IS-CS programmes, actual app screenshot, personal contributions, verified references and group recording before uploading.',9.5,color='gold')
ptext(47,42,W-100,'Course deadline: <b>16 November 2026 (Monday), before 11:59 PM MYT</b> · Poster A3 PDF + approximately 10-minute video MP4 / permitted link · Submitted by group leader.',9.2)
# Link annotations to the full sources, alongside truncated printed bibliography.
for yy, url in [
    (178,'https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/currency-exchange-rates-understanding-equilibrium-value'),
    (163,'https://www.cmegroup.com/articles/whitepapers/covered-interest-parity-implied-forward-foreign-exchange-swaps-cross-currency-basis-and-cme-estr-futures.html'),
    (148,'https://www.imf.org/en/publications/fandd/issues/series/back-to-basics/purchasing-power-parity-ppp'),
    (133,'https://www.stlouisfed.org/publications/page-one-economics/2023/01/03/adjusting-for-inflation')]:
    cv.linkURL(url,(x3+16,yy-6,x3+cw-20,yy+7),relative=0,thickness=0)
cv.save()
print(OUT)
