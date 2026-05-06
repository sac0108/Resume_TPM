from pathlib import Path
import math

OUT = Path('Sachin_Saxena_TPM_CV.pdf')
W, H = 612, 792  # US Letter points
M = 24
SIDEBAR_W = 169
NAVY = (13/255, 27/255, 42/255)
NAVY2 = (19/255, 42/255, 66/255)
GOLD = (201/255, 162/255, 39/255)
GOLD_SOFT = (243/255, 231/255, 189/255)
WHITE = (1,1,1)
SOFT = (246/255,248/255,251/255)
INK = (23/255,32/255,51/255)
MUTED = (92/255,102/255,122/255)
LINE = (217/255,222/255,232/255)

ops=[]

def esc(s):
    return s.replace('\\','\\\\').replace('(','\\(').replace(')','\\)').replace('\u2022','-')

def color(c):
    ops.append(f"{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} rg")

def stroke_color(c):
    ops.append(f"{c[0]:.3f} {c[1]:.3f} {c[2]:.3f} RG")

def rect(x,y,w,h,c=None,stroke=None,lw=1):
    if c: color(c); ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")
    if stroke: stroke_color(stroke); ops.append(f"{lw:.2f} w {x:.2f} {y:.2f} {w:.2f} {h:.2f} re S")

def line(x1,y1,x2,y2,c=GOLD,lw=1):
    stroke_color(c); ops.append(f"{lw:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

def circle(x,y,r,c):
    k=0.5522847498*r
    color(c)
    ops.append(f"{x+r:.2f} {y:.2f} m {x+r:.2f} {y+k:.2f} {x+k:.2f} {y+r:.2f} {x:.2f} {y+r:.2f} c {x-k:.2f} {y+r:.2f} {x-r:.2f} {y+k:.2f} {x-r:.2f} {y:.2f} c {x-r:.2f} {y-k:.2f} {x-k:.2f} {y-r:.2f} {x:.2f} {y-r:.2f} c {x+k:.2f} {y-r:.2f} {x+r:.2f} {y-k:.2f} {x+r:.2f} {y:.2f} c f")

def text(x,y,s,size=9,font='F1',c=INK):
    color(c)
    ops.append(f"BT /{font} {size:.2f} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({esc(s)}) Tj ET")

def width(s,size,font='F1'):
    # approximate Helvetica widths, good enough for wrapping
    factor = 0.55 if font!='F2' else 0.58
    return len(s)*size*factor

def wrap(s,maxw,size,font='F1'):
    words=s.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if width(t,size,font)<=maxw or not cur:
            cur=t
        else:
            lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def paragraph(x,y,s,maxw,size=8.2,leading=10.2,c=MUTED,font='F1'):
    for ln in wrap(s,maxw,size,font):
        text(x,y,ln,size,font,c); y-=leading
    return y

def bullet(x,y,s,maxw,size=7.15):
    text(x,y,'•',size,'F2',GOLD)
    return paragraph(x+8,y,s,maxw-8,size,9.1,MUTED,'F1')-1

def pill(x,y,s):
    w=width(s,7.0,'F2')+11
    rect(x,y-3,w,13,None,stroke=GOLD,lw=.6)
    text(x+5,y+1,s,7,'F2',WHITE)
    return x+w+4

# backgrounds
rect(0,0,W,H,WHITE)
rect(0,0,SIDEBAR_W,H,NAVY)
rect(0,0,6,H,GOLD)

# Sidebar
x=22; y=742
rect(x,y-2,45,45,None,stroke=GOLD,lw=1.4)
text(x+9,y+12,'SS',20,'F2',GOLD)
y-=30
text(x,y-25,'Sachin',24,'F2',WHITE)
text(x,y-49,'Saxena',24,'F2',WHITE)
y-=74
text(x,y,'TECHNICAL PROGRAM MANAGER',8.7,'F2',GOLD)
y-=23

def side_title(y,t):
    text(x,y,t.upper(),8,'F2',GOLD); line(x,y-5,SIDEBAR_W-18,y-5,GOLD,.7); return y-18

y=side_title(y,'Contact')
for s in ['San Francisco Bay Area, CA','sachin.saxena@example.com','linkedin.com/in/sachinsaxena','Open to TPM, Senior TPM, and AI Platform roles']:
    y=paragraph(x,y,s,SIDEBAR_W-38,7.4,9.2,(231/255,236/255,243/255)); y-=1

y-=4; y=side_title(y,'Core strengths')
px=x; py=y
for tag in ['AI/ML Programs','Cloud Platforms','Roadmaps','OKRs','Agile','Risk Mgmt','Executive Comms','Partner Ops','Data Strategy','Compliance']:
    tw=width(tag,7,'F2')+11
    if px+tw>SIDEBAR_W-16: px=x; py-=17
    px=pill(px,py,tag)
y=py-22

y=side_title(y,'Leadership profile')
y=paragraph(x,y,'TPM leader translating ambiguous strategy into measurable execution across engineering, product, security, data, legal, finance, and customer teams.',SIDEBAR_W-38,7.3,9.2,(231/255,236/255,243/255)); y-=5
rect(x,y-38,SIDEBAR_W-42,42,NAVY2); rect(x,y-38,3,42,GOLD)
y=paragraph(x+8,y-11,'Known for crisp operating cadence, data-backed decisions, and calm escalation management for business-critical launches.',SIDEBAR_W-58,7.1,8.8,WHITE); y-=7

y=side_title(y,'Education')
text(x,y,'M.S., Computer Science',7.8,'F2',WHITE); y-=10
y=paragraph(x,y,'University program focused on distributed systems, databases, and software engineering.',SIDEBAR_W-38,7.1,8.8,(231/255,236/255,243/255)); y-=5
text(x,y,'B.E., Engineering',7.8,'F2',WHITE); y-=10
y=paragraph(x,y,'Technical foundation in systems thinking and product delivery.',SIDEBAR_W-38,7.1,8.8,(231/255,236/255,243/255)); y-=8

y=side_title(y,'Certifications')
y=paragraph(x,y,'PMP • Certified ScrumMaster • AWS Cloud Practitioner • SAFe Agilist',SIDEBAR_W-38,7.3,9.2,(231/255,236/255,243/255))

# Main
mx=SIDEBAR_W+24; mw=W-mx-24; y=748
summary='Senior Technical Program Manager with 12+ years leading complex software, cloud, data, and AI-enabled platform initiatives from concept through launch. Builds trusted cross-functional teams, removes delivery friction, and converts strategy into reliable execution systems that improve customer outcomes, operational efficiency, and executive visibility.'
y=paragraph(mx,y,summary,mw,8.4,10.7,MUTED); y-=12

# metrics
card_w=(mw-14)/3
for i,(big,small) in enumerate([('$45M+','portfolio value governed across multi-year transformation programs'),('30%','cycle-time reduction through roadmap hygiene and dependency management'),('99.9%','launch readiness bar for production services and customer migrations')]):
    cx=mx+i*(card_w+7); rect(cx,y-48,card_w,48,SOFT); rect(cx,y-3,card_w,3,GOLD)
    text(cx+7,y-21,big,15,'F2',NAVY)
    paragraph(cx+7,y-33,small,card_w-14,6.7,7.8,MUTED)
y-=65

def section_header(y,title):
    line(mx,y+4,mx+18,y+4,GOLD,2.3); text(mx+26,y,title.upper(),9.7,'F2',NAVY); return y-15

y=section_header(y,'Experience')
tline_x=mx+5; line(tline_x,y+5,tline_x,294,GOLD,1.3)

def job(y,title,date,company,bullets):
    circle(tline_x,y+3,4,GOLD)
    text(mx+17,y,title,9.1,'F2',INK); text(mx+mw-width(date,7.1,'F2'),y,date,7.1,'F2',GOLD); y-=11
    text(mx+17,y,company,7.4,'F2',MUTED); y-=10
    for b in bullets: y=bullet(mx+17,y,b,mw-17,6.95)
    return y-8

y=job(y,'Senior Technical Program Manager','2021–Present','Enterprise Cloud & AI Platform Organization',[
'Own end-to-end delivery for strategic cloud, data, and AI platform roadmaps spanning 8+ engineering squads and multiple business stakeholders.',
'Established planning rituals, dependency maps, launch reviews, and risk burn-down dashboards that improved release predictability by 30%.',
'Led executive operating reviews for capacity, budget, privacy, compliance, customer adoption, and incident-readiness decisions.'
])
y=job(y,'Technical Program Manager','2017–2021','SaaS Product & Infrastructure Teams',[
'Delivered API modernization, identity, analytics, and reliability programs serving enterprise customers across regulated environments.',
'Coordinated product, engineering, SRE, security, support, and go-to-market milestones for launches with zero critical customer escalations.',
'Introduced KPI scorecards and retrospectives that surfaced scope tradeoffs earlier and increased stakeholder confidence.'
])
y=job(y,'Program Manager / Engineering Lead','2012–2017','Digital Transformation & Systems Integration',[
'Managed distributed teams delivering enterprise workflow, reporting, migration, and integration programs for global clients.',
'Translated customer requirements into technical plans, release schedules, test strategy, and adoption playbooks.'
])

y=section_header(y+2,'Selected achievements')
card_h=54; gap=8; cw=(mw-gap)/2
cards=[('AI platform launch','Coordinated model evaluation, responsible-AI controls, telemetry, and rollout gates to move a new AI-assisted workflow from pilot to production.'),('Cloud migration','Orchestrated phased customer migration plan, dependency sequencing, and support readiness that reduced cutover risk and accelerated adoption.'),('Operational excellence','Built a single source of truth for risks, milestones, decisions, and metrics, enabling faster executive decisions and fewer late surprises.'),('Customer trust','Partnered with security and legal teams on privacy reviews, compliance evidence, and incident playbooks for enterprise readiness.')]
for idx,(h,p) in enumerate(cards):
    row=idx//2; col=idx%2; cx=mx+col*(cw+gap); cy=y-row*(card_h+8)
    rect(cx,cy-card_h,cw,card_h,WHITE,LINE,.7); rect(cx,cy-card_h,3,card_h,GOLD)
    text(cx+8,cy-13,h,8.1,'F2',NAVY)
    paragraph(cx+8,cy-25,p,cw-16,6.85,8.3,MUTED)
y-=2*(card_h+8)+2

y=section_header(y,'Tools & methods')
px=mx; py=y
for tag in ['Jira','Confluence','Asana','Smartsheet','Power BI','Tableau','SQL','Python','AWS','Azure','GCP','GitHub','Figma','OKRs','RACI','RAID']:
    tw=width(tag,7.0,'F2')+12
    if px+tw>mx+mw: px=mx; py-=16
    rect(px,py-3,tw,13,GOLD_SOFT,stroke=(226/255,204/255,119/255),lw=.5)
    text(px+6,py+1,tag,7,'F2',(95/255,74/255,8/255))
    px+=tw+4
bottom=py-18
if bottom < 24:
    raise SystemExit(f'Content overflow: bottom at {bottom:.1f} pt')

# Build PDF
stream='\n'.join(ops).encode('latin-1','replace')
objs=[]
objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {W} {H}] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 4 0 R >>".encode())
objs.append(b"<< /Length "+str(len(stream)).encode()+b" >>\nstream\n"+stream+b"\nendstream")
objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

pdf=bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
offsets=[]
for i,o in enumerate(objs,1):
    offsets.append(len(pdf)); pdf.extend(f"{i} 0 obj\n".encode()+o+b"\nendobj\n")
xref=len(pdf)
pdf.extend(f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode())
for off in offsets:
    pdf.extend(f"{off:010d} 00000 n \n".encode())
pdf.extend(f"trailer << /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
OUT.write_bytes(pdf)
print(f'Wrote {OUT} ({len(pdf)} bytes); bottom margin {bottom:.1f} pt; pages=1')
