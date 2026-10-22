"""
Refined and Perfected Presentation Guide PDF Generator for Leroy Matienga's Portfolio.
Guarantees zero missing glyphs, clean typographic hierarchy, and perfectly balanced page breaks.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ─── Custom Canvas with Running Headers, Footers & Dynamic Page Count ─────────

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            
            # Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1e293b"))
            self.drawString(45, 11 * inch - 36, "LEROY MATIENGA")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(135, 11 * inch - 36, "|   Portfolio Technical Architecture & 3D Globe Presentation Guide")
            
            # Header rule
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.75)
            self.line(45, 11 * inch - 42, 8.5 * inch - 45, 11 * inch - 42)
            
            # Footer rule
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.75)
            self.line(45, 42, 8.5 * inch - 45, 42)
            
            # Running Footer
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(45, 30, "Undergraduate Computer Science & Software Engineering Portfolio")
            
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * inch - 45, 30, page_text)
            
            self.restoreState()


# ─── Style Factory ────────────────────────────────────────────────────────────

def create_styles():
    base_styles = getSampleStyleSheet()
    
    SLATE_TEXT = colors.HexColor("#334155")
    
    custom = {
        'DocTitle': ParagraphStyle(
            'DocTitle',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=27,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=6
        ),
        'SectionH1': ParagraphStyle(
            'SectionH1',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True
        ),
        'SectionH2': ParagraphStyle(
            'SectionH2',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11.5,
            leading=15,
            textColor=colors.HexColor("#1d4ed8"),
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        ),
        'SectionH3': ParagraphStyle(
            'SectionH3',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=6,
            spaceAfter=2,
            keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12.5,
            textColor=SLATE_TEXT,
            spaceAfter=5
        ),
        'BodyBold': ParagraphStyle(
            'BodyBold',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=12.5,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=5
        ),
        'Bullet': ParagraphStyle(
            'Bullet',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12,
            textColor=SLATE_TEXT,
            leftIndent=14,
            firstLineIndent=-9,
            spaceAfter=3
        ),
        'CodeSnippet': ParagraphStyle(
            'CodeSnippet',
            parent=base_styles['Normal'],
            fontName='Courier',
            fontSize=7.2,
            leading=9.8,
            textColor=colors.HexColor("#f8fafc"),
            spaceAfter=0
        ),
        'CalloutTitle': ParagraphStyle(
            'CalloutTitle',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#1e3a8a"),
            spaceAfter=2
        ),
        'CalloutText': ParagraphStyle(
            'CalloutText',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11.5,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=0
        ),
        'TableHead': ParagraphStyle(
            'TableHead',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10.5,
            textColor=colors.white,
            alignment=0
        ),
        'TableCell': ParagraphStyle(
            'TableCell',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=7.8,
            leading=10.5,
            textColor=SLATE_TEXT,
            alignment=0
        ),
        'TableCellBold': ParagraphStyle(
            'TableCellBold',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=7.8,
            leading=10.5,
            textColor=colors.HexColor("#0f172a"),
            alignment=0
        ),
        'TableCellCode': ParagraphStyle(
            'TableCellCode',
            parent=base_styles['Normal'],
            fontName='Courier',
            fontSize=7.2,
            leading=9.5,
            textColor=colors.HexColor("#1d4ed8"),
            alignment=0
        ),
        'PresenterSayLabel': ParagraphStyle(
            'PresenterSayLabel',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#059669"),
            spaceAfter=2
        ),
        'PresenterSayText': ParagraphStyle(
            'PresenterSayText',
            parent=base_styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            leading=11.5,
            textColor=colors.HexColor("#064e3b"),
            spaceAfter=2
        )
    }
    return custom


# ─── Helper UI Components ─────────────────────────────────────────────────────

def make_callout(title, text, styles, box_color="#eff6ff", border_color="#3b82f6", width=522):
    content = [
        Paragraph(title, styles['CalloutTitle']),
        Spacer(1, 1),
        Paragraph(text, styles['CalloutText'])
    ]
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(box_color)),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor(border_color)),
        ('LINELEFT', (0, 0), (-1, -1), 3.5, colors.HexColor(border_color)),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def make_code_block(code_text, styles, width=522):
    lines = code_text.strip().split("\n")
    paras = [Paragraph(line.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;"), styles['CodeSnippet']) for line in lines]
    t = Table([[paras]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#334155")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t


def make_speaking_card(prompt, script_text, styles, width=522):
    content = [
        Paragraph(f"<b>Presenter Talking Script:</b> {prompt}", styles['PresenterSayLabel']),
        Spacer(1, 1),
        Paragraph(f'"{script_text}"', styles['PresenterSayText'])
    ]
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#10b981")),
        ('LINELEFT', (0, 0), (-1, -1), 3.5, colors.HexColor("#059669")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t


def build_pdf():
    pdf_filename = "Leroy_Matienga_Portfolio_Presentation_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=48,
        bottomMargin=48
    )
    
    styles = create_styles()
    story = []
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 1: EXECUTIVE COVER PAGE
    # ═════════════════════════════════════════════════════════════════════════
    
    hero_inner = [
        Spacer(1, 10),
        Paragraph("PORTFOLIO TECHNICAL ARCHITECTURE &amp; 3D GLOBE ENGINE", ParagraphStyle(
            'CoverMain', fontName='Helvetica-Bold', fontSize=20, leading=25, textColor=colors.HexColor("#ffffff")
        )),
        Spacer(1, 4),
        Paragraph("Comprehensive Code Breakdown, System Architecture Analysis, and Interactive WebGL Implementation Defense Guide", ParagraphStyle(
            'CoverSub', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor("#93c5fd")
        )),
        Spacer(1, 10),
    ]
    hero_table = Table([[hero_inner]], colWidths=[522])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0a0f1d")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#1e3a8a")),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 14))
    
    avatar_path = "profile2.jpeg"
    has_avatar = os.path.exists(avatar_path)
    
    info_paras = [
        Paragraph("<b>Presenter:</b> Leroy Matienga", styles['SectionH2']),
        Paragraph("<b>Academic Standing:</b> Undergraduate Computer Science Student", styles['Body']),
        Paragraph("<b>Specialization:</b> Software Engineering, Backend Systems &amp; 3D Web Graphics", styles['Body']),
        Paragraph("<b>Portfolio Codebase:</b> Full-Stack Web Application (HTML5, CSS3, JS, Three.js, Flask, SQLite)", styles['Body']),
        Paragraph("<b>Presentation Objective:</b> Defend the design decisions, code organization, full-stack REST API, SQLite schema, security mitigations, and the mathematical implementation of the real-time 3D Earth Globe.", styles['Body']),
        Paragraph("<b>Date of Defense:</b> October 2026", styles['BodyBold']),
    ]
    
    if has_avatar:
        try:
            profile_img = Image(avatar_path, width=1.35*inch, height=1.75*inch)
            profile_img.hAlign = 'CENTER'
            profile_table = Table([[profile_img]], colWidths=[1.45*inch])
            profile_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#2563eb")),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ]))
            
            author_grid = Table([[info_paras, profile_table]], colWidths=[3.75*inch, 1.5*inch])
            author_grid.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(author_grid)
        except Exception:
            story.extend(info_paras)
    else:
        story.extend(info_paras)
        
    story.append(Spacer(1, 14))
    
    exec_data = [
        [
            Paragraph("System Dimension", styles['TableHead']),
            Paragraph("Implementation Technology", styles['TableHead']),
            Paragraph("Core Architectural Function", styles['TableHead'])
        ],
        [
            Paragraph("Frontend Presentation", styles['TableCellBold']),
            Paragraph("HTML5, CSS3, ES6 JavaScript", styles['TableCell']),
            Paragraph("Responsive glassmorphism UI, sliding magnetic pill navigation, dynamic scroll-spy, animated skill meters.", styles['TableCell'])
        ],
        [
            Paragraph("3D Interactive Globe", styles['TableCellBold']),
            Paragraph("Three.js, WebGL, Custom GLSL", styles['TableCell']),
            Paragraph("Real-time day/night simulation based on UTC Sun vector, procedural starfield, great-circle flight hyper-dive.", styles['TableCell'])
        ],
        [
            Paragraph("Backend Web Server", styles['TableCellBold']),
            Paragraph("Python 3, Flask 3.1, CORS", styles['TableCell']),
            Paragraph("REST API routing, input sanitization against XSS, directory traversal guards, CV distribution.", styles['TableCell'])
        ],
        [
            Paragraph("Data Persistence", styles['TableCellBold']),
            Paragraph("SQLite 3 (Built-in engine)", styles['TableCell']),
            Paragraph("Atomic transactional logging, parameterized query execution (SQLi immunity), sliding-window rate tracking.", styles['TableCell'])
        ],
        [
            Paragraph("Automated Messaging", styles['TableCellBold']),
            Paragraph("Python smtplib, MIME Multipart", styles['TableCell']),
            Paragraph("Automated branded HTML contact notifications with non-blocking graceful degradation.", styles['TableCell'])
        ],
        [
            Paragraph("Configuration &amp; Security", styles['TableCellBold']),
            Paragraph("python-dotenv, .env isolation", styles['TableCell']),
            Paragraph("12-Factor App secrets isolation, IP-based sliding-window rate limiter preventing bot spam.", styles['TableCell'])
        ]
    ]
    t_exec = Table(exec_data, colWidths=[110, 140, 272])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_exec)
    
    story.append(Spacer(1, 14))
    story.append(make_callout(
        "[KEY PRESENTATION TAKEAWAY]",
        "This presentation guide is structured into self-contained modules. You can navigate directly to <b>Pages 7-9</b> for the complete, step-by-step mathematical and shader breakdown of the <b>3D Interactive Earth Globe</b>, or to <b>Pages 11-13</b> for word-for-word presentation speaking scripts, anticipated judge defense Q&amp;A, and live demo checklists.",
        styles, box_color="#eff6ff", border_color="#2563eb"
    ))
    
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 2: SYSTEM ARCHITECTURE & ENGINEERING PRINCIPLES
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("1. System Architecture &amp; Engineering Principles", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph(
        "Leroy Matienga's portfolio is engineered as a high-performance full-stack client-server application. "
        "It couples an immersive 3D WebGL computer graphics interface on the client with a secure, rate-limited, and persistent Python backend. "
        "The architecture adheres to four foundational software engineering principles:",
        styles['Body']
    ))
    
    principles = [
        "<b>1. Modularity &amp; Separation of Concerns:</b> Presentation markup (HTML), visual styling (CSS), client-side interactivity and 3D rendering (JavaScript/Three.js), API routing (Flask), database management (SQLite), and external communication (SMTP) are isolated into dedicated, decoupled modules.",
        "<b>2. Defensive Security Architecture:</b> All client inputs are treated as untrusted. The backend enforces input sanitization via <code>html.escape()</code> to eliminate Cross-Site Scripting (XSS), uses strict regex pattern checking, employs parameterized SQL queries to prevent SQL Injection (SQLi), guards against directory traversal attacks, and limits request frequencies through an IP-based sliding window.",
        "<b>3. Hardware-Accelerated 3D Web Graphics:</b> Rather than using pre-rendered video clips or 2D raster maps, the portfolio runs a real-time WebGL rendering pipeline via Three.js with custom GLSL shaders that calculate solar illumination vectors directly on the client's GPU at 60 FPS.",
        "<b>4. Graceful Degradation &amp; Non-Blocking Resilience:</b> If external services (such as SMTP mail servers) encounter network dropouts or authentication timeouts, the core application handles the error gracefully, ensuring that database records remain intact and the user receives a reliable response."
    ]
    for p in principles:
        story.append(Paragraph(f"&bull; {p}", styles['Bullet']))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("Full-Stack Component Interaction Pipeline", styles['SectionH2']))
    
    arch_diagram = """+---------------------------------------------------------------------------------------+
|                                    CLIENT BROWSER                                     |
|  +--------------------+  +----------------------+  +--------------------------------+  |
|  | Modern Glass UI    |  | Three.js WebGL Globe |  | Client-Side Event Controllers  |  |
|  | - Slideshow BG     |  | - Real-Time Shaders  |  | - Magnetic Indicator Pill Nav  |  |
|  | - Glassmorphism    |  | - Solar Vector Math  |  | - ScrollSpy & Typewriter Loop  |  |
|  | - Responsive Grid  |  | - Google Earth Dive  |  | - Asynchronous Fetch (AJAX)    |  |
|  +--------------------+  +----------------------+  +--------------------------------+  |
+-------------------------------------------|-------------------------------------------+
                                            | HTTP REST API (JSON / FormData)
                                            v
+---------------------------------------------------------------------------------------+
|                                 FLASK BACKEND SERVER                                  |
|  +---------------------------------------------------------------------------------+  |
|  | app.py (Application Controller & Security Middleware)                           |  |
|  |  * Directory Traversal Guard: Prevents '../' file path exploitation             |  |
|  |  * IP Rate Limiter: Tracks client requests in sliding 60s windows               |  |
|  |  * Input Sanitizer: Strips malicious tags with html.escape() + Regex checks    |  |
|  +---------------------------------------------------------------------------------+  |
|          |                                         |                                  |
|          v                                         v                                  |
|  +----------------------------------+   +------------------------------------------+  |
|  | models.py (Data Persistence)     |   | email_service.py (Notification Engine)   |  |
|  |  * SQLite3 Connection Factory    |   |  * MIME Multipart HTML Builder           |  |
|  |  * Parameterized INSERT Queries  |   |  * smtplib TLS Encrypted Transmission    |  |
|  |  * portfolio.db Storage          |   |  * Non-blocking Try/Except Handler       |  |
|  +----------------------------------+   +------------------------------------------+  |
+---------------------------------------------------------------------------------------+"""
    story.append(make_code_block(arch_diagram, styles))
    story.append(Spacer(1, 6))
    
    story.append(make_speaking_card(
        "Explaining System Architecture to Examiners",
        "Judges, our architecture follows strict separation of concerns. The frontend combines high-performance Three.js WebGL graphics with modern CSS glassmorphism, while the backend is an enterprise-patterned Flask microservice backed by SQLite. We specifically engineered defensive mechanisms at every boundary: client input is sanitized, requests are rate-limited per IP, SQL queries use strict parameterization, and external services degrade gracefully without crashing the server.",
        styles
    ))
    
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 3: FRONTEND ARCHITECTURE (index.html & style.css)
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("2. Frontend Semantic &amp; Visual Architecture", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph("2.1 index.html -- Semantic Markup &amp; DOM Hierarchy", styles['SectionH2']))
    story.append(Paragraph(
        "<b>File Role:</b> Serves as the Single-Page Application (SPA) foundation. It establishes the semantic document structure, imports vector icon and 3D graphics libraries via CDNs, and exposes accessible target nodes for JavaScript manipulation.",
        styles['Body']
    ))
    
    index_points = [
        "<b>Header Meta &amp; CDN Imports (Lines 1-20):</b> Declares HTML5 doctype, UTF-8 encoding, and responsive viewport sizing. Imports <i>Font Awesome 6.5.0</i> for UI icons, <i>Google Poppins</i> typography (weights 300 to 700), and loads <i>Three.js (r128)</i> along with <i>OrbitControls.js</i> for 3D globe rendering.",
        "<b>Ambient Slideshow Background (Lines 23-29):</b> Encapsulates 3 background slides (<code>slide-1</code>, <code>slide-2</code>, <code>slide-3</code>) beneath a dark radial overlay (<code>.bg-overlay</code>) to produce a continuous background crossfade without impeding user interaction.",
        "<b>Navigation Bar (Lines 31-50):</b> Semantic <code>&lt;header&gt;</code> element containing Leroy's logo badge, mobile hamburger toggle button, and the floating navigation links with an empty <code>&lt;div class=\"nav-indicator\" id=\"navIndicator\"&gt;</code> pill that slides dynamically.",
        "<b>Hero Section (Lines 52-84):</b> Centers Leroy's portrait (<code>profile2.jpeg</code>) within a dual-layer glowing container (<code>avatar-glow</code> and <code>avatar-border</code>). Embeds the dynamic typewriter target (<code>#typewriter</code>), bio statement, call-to-action buttons (Download CV linking to <code>/api/download-cv</code>, Contact link), and GitHub/LinkedIn social anchors.",
        "<b>About Section (Lines 86-112):</b> 3 glassmorphism cards detailing Education (Computer Science), Development (Software Engineering), and Specialization (Backend &amp; AI Systems).",
        "<b>Interactive 3D Portfolio Globe Frame (Lines 114-186):</b> The dedicated 3D viewport wrapper (<code>#globeWrapper</code>). Houses the Top Control Bar (Orbit reset button, Real-Time Sun indicator with pulsing LED, Fullscreen toggle), the Atmospheric Entry Flight HUD (<code>#globeFlightHud</code>), the WebGL container (<code>#globe-container</code>), the Quick-Dive dock pills, and the status modal dialog (<code>#statusModal</code>).",
        "<b>Skills Section (Lines 188-227):</b> Four skill categories (Python OOP, SQL Database, Web Frontend, Git Version Control) featuring animated percentage meters (<code>--w: 90%</code>).",
        "<b>Contact Section &amp; Footer (Lines 229-266):</b> Asynchronous contact form (<code>#contactForm</code>) with name, email, subject, and message inputs, plus an animated submission button with paper-plane icon."
    ]
    for pt in index_points:
        story.append(Paragraph(f"&bull; {pt}", styles['Bullet']))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("2.2 style.css -- Design Tokens, Glassmorphism &amp; HUD Styling", styles['SectionH2']))
    story.append(Paragraph(
        "<b>File Role:</b> Controls the visual language, dark space theme, glassmorphic blur effects, hardware-accelerated animations, and responsive media queries across all viewport sizes.",
        styles['Body']
    ))
    
    css_points = [
        "<b>CSS Root Variables (Lines 1-11):</b> Standardizes the color palette: <code>--bg-primary: #0f1013</code> (deep space dark), <code>--accent-color: #2563eb</code> (royal blue), <code>--accent-glow: rgba(37,99,235,0.45)</code>, <code>--text-main: #f8fafc</code>, and <code>--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)</code> for smooth animations.",
        "<b>Cyclic Background Slideshow (Lines 32-82):</b> Uses <code>@keyframes slideFade</code> over an 18-second cycle with staggered 6-second animation delays. The dark radial gradient overlay and <code>backdrop-filter: blur(4px)</code> ensure text readability remains high.",
        "<b>Glassmorphism Architecture (Lines 84-92):</b> The <code>.glass-card</code> utility class combines <code>background: var(--glass-bg)</code>, <code>backdrop-filter: blur(12px)</code>, and a 1px subtle white alpha border (<code>rgba(255,255,255,0.12)</code>) to give floating surfaces depth and elegance.",
        "<b>Sliding Magnetic Indicator Pill (Lines 130-175):</b> Positions the indicator pill inside the navigation capsule with <code>position: absolute</code>. Smooth motion is achieved using GPU transforms (<code>translateX</code> and <code>width</code>) driven by cubic bezier curves.",
        "<b>3D Space Frame &amp; Top Bar (Lines 403-498):</b> Styles the 640px height 3D globe wrapper with a space radial background (<code>#070913</code> to <code>#020308</code>), inset blue shadow, and positions the Top Bar (<code>z-index: 35</code>) with pointer events passed through to controls.",
        "<b>Atmospheric Flight HUD (Lines 501-553):</b> When a dive begins, this HUD translates down into the viewport with a glowing cyan border (<code>#38bdf8</code>), scanning laser gradient (<code>@keyframes hudScan</code>), and floating airplane icon (<code>@keyframes hudPlane</code>).",
        "<b>Responsive Breakpoints (Lines 960-1444):</b> Employs CSS media queries at 1024px, 768px, and 480px to collapse the navbar into a mobile slide-out drawer, stack the hero grid vertically, and scale down the globe height for smooth mobile performance."
    ]
    for pt in css_points:
        story.append(Paragraph(f"&bull; {pt}", styles['Bullet']))
        
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 4: CLIENT-SIDE INTERACTION ENGINE (script.js)
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("2.3 script.js -- Client Logic &amp; DOM Event Controllers", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph(
        "<b>File Role:</b> Serves as the primary frontend controller. Manages DOM events, sliding navigation tracking, typewriter effects, asynchronous contact submissions, modal state machines, and the Three.js 3D Earth Globe.",
        styles['Body']
    ))
    
    js_modules = [
        "<b>Module 1: Sliding Magnetic Capsule Indicator (Lines 1-66):</b> Tracks mouse movement and drag states across navigation items. Calculates horizontal position using <code>targetRect.left - containerRect.left</code> and adjusts indicator pill width to match the hovered or active tab.",
        "<b>Module 2: Dynamic ScrollSpy Engine (Lines 67-91):</b> Listens to window scroll events with an offset of +220px. Evaluates whether the current scroll position falls within the boundary <code>[sectionTop, sectionTop + sectionHeight]</code>, auto-activating the matching nav link.",
        "<b>Module 3: Typewriter State Machine (Lines 93-123):</b> Cycles through role titles (\"Software Developer!\", \"CS Student!\", \"Python Engineer!\", \"Tech Enthusiast!\") using an alternating character indexing loop with variable delays for typing (100ms), deleting (50ms), and word pausing (1500ms).",
        "<b>Module 4: IntersectionObserver Skill Meters (Lines 138-150):</b> Observes skill progress bars with a 30% viewport visibility threshold (<code>threshold: 0.3</code>). When scrolled into view, it attaches the <code>.animated</code> class, triggering smooth CSS transitions from 0% to the target width.",
        "<b>Module 5: Asynchronous Contact Form AJAX Handler (Lines 152-210):</b> Intercepts form submit events, prevents full-page browser reloads via <code>e.preventDefault()</code>, transforms button state into a loading spinner, and issues a POST request to <code>/api/contact</code> with JSON payload. Dynamically renders success or error messages without refreshing.",
        "<b>Module 6: Global Status / Progress Modal Manager (Lines 218-316):</b> Controls modal visibility. Crucially, it dynamically reparents the modal into <code>#globeWrapper</code> so that when the user is in HTML5 Fullscreen mode, the modal remains accessible on the top-layer stack instead of being occluded."
    ]
    for jm in js_modules:
        story.append(Paragraph(f"&bull; {jm}", styles['Bullet']))
        
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("Contact Form AJAX Submission Workflow", styles['SectionH2']))
    contact_flow = """// Asynchronous AJAX Request Workflow in script.js
const formData = {
    name: document.getElementById("name").value.trim(),
    email: document.getElementById("email").value.trim(),
    subject: document.getElementById("subject").value.trim(),
    message: document.getElementById("message").value.trim(),
};

const response = await fetch("/api/contact", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
});

const result = await response.json();
if (response.ok && result.success) {
    btn.innerHTML = `<span>Sent Successfully!</span> <i class="fa-solid fa-check"></i>`;
    btn.style.backgroundColor = "#10b981";
    form.reset();
} else {
    btn.innerHTML = `<span>${result.error || "Failed to send"}</span> <i class="fa-solid fa-xmark"></i>`;
    btn.style.backgroundColor = "#ef4444";
}"""
    story.append(make_code_block(contact_flow, styles))
    story.append(Spacer(1, 6))
    
    story.append(make_callout(
        "[CODE QUALITY HIGHLIGHT: NON-BLOCKING EVENT LOOPS]",
        "Notice how <code>script.js</code> handles all heavy animations (the starfield drift, cloud rotation, raycasting, and camera flight curves) using <code>requestAnimationFrame(animate)</code> rather than <code>setInterval</code>. This synchronizes rendering with the monitor's vertical refresh rate, completely eliminating frame tearing and minimizing battery consumption on laptops and mobile devices.",
        styles
    ))
    
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 5: BACKEND WEB SERVER & SECURITY MIDDLEWARE (app.py)
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("2.4 app.py -- Flask Backend Server &amp; Security Pipeline", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph(
        "<b>File Role:</b> The central backend server powered by Python 3 and Flask. It serves static assets, enforces rate limiting, sanitizes untrusted input, logs contact messages to SQLite, dispatches email notifications, and guards administrative endpoints.",
        styles['Body']
    ))
    
    app_endpoints_data = [
        [
            Paragraph("Route / Method", styles['TableHead']),
            Paragraph("Authorization", styles['TableHead']),
            Paragraph("Functionality &amp; Security Controls", styles['TableHead'])
        ],
        [
            Paragraph("<code>GET /</code>", styles['TableCellCode']),
            Paragraph("Public", styles['TableCell']),
            Paragraph("Delivers <code>index.html</code> from the project root via <code>send_from_directory()</code>.", styles['TableCell'])
        ],
        [
            Paragraph("<code>GET /&lt;path:filename&gt;</code>", styles['TableCellCode']),
            Paragraph("Public", styles['TableCell']),
            Paragraph("Serves static assets (CSS, JS, images). Includes a <b>Directory Traversal Guard</b> checking <code>if '..' in filename: abort(403)</code>.", styles['TableCell'])
        ],
        [
            Paragraph("<code>POST /api/contact</code>", styles['TableCellCode']),
            Paragraph("Rate Limited", styles['TableCell']),
            Paragraph("Processes contact submissions. Runs IP sliding-window rate limit check, input sanitization via <code>html.escape()</code>, regex email validation, records to SQLite, and triggers email.", styles['TableCell'])
        ],
        [
            Paragraph("<code>GET /api/download-cv</code>", styles['TableCellCode']),
            Paragraph("Public", styles['TableCell']),
            Paragraph("Safely checks for file existence before streaming the CV attachment to the user with standard Content-Disposition headers.", styles['TableCell'])
        ],
        [
            Paragraph("<code>GET /api/messages</code>", styles['TableCellCode']),
            Paragraph("Admin API Key", styles['TableCell']),
            Paragraph("Administrative endpoint. Validates <code>request.headers.get('X-API-Key') == Config.ADMIN_API_KEY</code> before returning logged messages as JSON.", styles['TableCell'])
        ]
    ]
    t_endpoints = Table(app_endpoints_data, colWidths=[120, 90, 312])
    t_endpoints.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_endpoints)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("Security Architecture &amp; Input Validation Logic", styles['SectionH2']))
    
    sec_points = [
        "<b>Proxy-Aware IP Resolution:</b> Uses <code>get_client_ip()</code> to extract the true client IP from <code>request.headers.get('X-Forwarded-For')</code> when deployed behind reverse proxies (such as Nginx, Cloudflare, or AWS ALBs), falling back to <code>request.remote_addr</code>.",
        "<b>Cross-Site Scripting (XSS) Sanitization:</b> All textual inputs are passed through <code>html.escape(text.strip())</code>. Malicious HTML injection payloads (e.g., <code>&lt;script&gt;alert(1)&lt;/script&gt;</code>) are escaped into harmless HTML entities (<code>&amp;lt;script&amp;gt;</code>).",
        "<b>Input Length &amp; Regex Boundaries:</b> Verifies email RFC formatting using standard regex patterns and enforces strict length boundaries (Name: 2-100 chars, Subject: 2-200 chars, Message: 10-5000 chars) to prevent buffer overflows or denial-of-service via massive payloads."
    ]
    for sp in sec_points:
        story.append(Paragraph(f"&bull; {sp}", styles['Bullet']))
        
    story.append(Spacer(1, 6))
    
    app_code_sample = """# Critical Security & Validation Snippet from app.py
@app.route("/api/contact", methods=["POST"])
def handle_contact():
    client_ip = get_client_ip()
    # Rate Limiting Check (5 requests per 60 seconds per IP)
    if count_recent_messages(client_ip, Config.RATE_LIMIT_WINDOW_SECONDS) >= Config.RATE_LIMIT_MAX_REQUESTS:
        return jsonify({"success": False, "error": "Too many messages. Please try again later."}), 429

    data = request.get_json() or {}
    name = sanitize_input(data.get("name", ""))
    email = sanitize_input(data.get("email", ""))
    subject = sanitize_input(data.get("subject", ""))
    message = sanitize_input(data.get("message", ""))

    if not is_valid_email(email) or len(message) < 10:
        return jsonify({"success": False, "error": "Invalid form fields."}), 400

    saved = save_message(name, email, subject, message, ip_address=client_ip)
    email_sent = send_notification(name, email, subject, message)
    return jsonify({"success": True, "message": "Sent successfully!"}), 201"""
    story.append(make_code_block(app_code_sample, styles))
    
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 6: DATABASE PERSISTENCE & EMAIL PIPELINE
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("2.5 Database Persistence &amp; Messaging Services", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph("2.5.1 config.py -- Centralized Configuration Management", styles['SectionH2']))
    story.append(Paragraph(
        "<b>File Role:</b> Implements the Twelve-Factor App methodology for configuration management. It uses <code>python-dotenv</code> to read environment variables from an uncommitted <code>.env</code> file into a clean Python <code>Config</code> object.",
        styles['Body']
    ))
    
    config_code_snippet = """class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-to-a-random-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "portfolio.db")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "")
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "change-this-to-a-secure-key")
    CV_FILENAME = os.getenv("CV_FILENAME", "Leroy_Matienga_CV.pdf")
    RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "5"))
    RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))"""
    story.append(make_code_block(config_code_snippet, styles))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("2.5.2 models.py -- SQLite Database Layer &amp; SQLi Immunity", styles['SectionH2']))
    story.append(Paragraph(
        "<b>File Role:</b> Encapsulates all relational database operations using Python's native <code>sqlite3</code> library. "
        "It manages database connection factories, table schema migrations, and transactional inserts.",
        styles['Body']
    ))
    
    model_points = [
        "<b>Connection Factory (<code>get_db_connection()</code>):</b> Opens connections to <code>portfolio.db</code> and attaches <code>conn.row_factory = sqlite3.Row</code>. This enables column access via dictionary keys (e.g., <code>row['email']</code>) as well as numerical indices.",
        "<b>Idempotent Schema Initialization (<code>init_db()</code>):</b> Executes <code>CREATE TABLE IF NOT EXISTS contacts</code> on server startup. The table schema includes: <code>id (INTEGER PK AUTOINCREMENT)</code>, <code>name (TEXT)</code>, <code>email (TEXT)</code>, <code>subject (TEXT)</code>, <code>message (TEXT)</code>, <code>ip_address (TEXT)</code>, <code>is_read (INTEGER DEFAULT 0)</code>, and <code>created_at (TIMESTAMP)</code>.",
        "<b>SQL Injection Immunity (<code>save_message()</code>):</b> All values are passed into SQL statements as parameterized placeholders (<code>?</code>). The database engine treats all parameters purely as literal values, rendering SQL injection exploits impossible.",
        "<b>Sliding-Window Rate Query (<code>count_recent_messages()</code>):</b> Queries message frequency using SQLite's native date functions: <code>WHERE ip_address = ? AND created_at &gt;= datetime('now', '-60 seconds')</code>. This provides lightweight rate limiting without external Redis dependencies."
    ]
    for mp in model_points:
        story.append(Paragraph(f"&bull; {mp}", styles['Bullet']))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("2.5.3 email_service.py -- Automated SMTP Notification Engine", styles['SectionH2']))
    story.append(Paragraph(
        "<b>File Role:</b> Dispatches branded email alerts to Leroy when visitors submit contact inquiries. "
        "Built using Python's native <code>smtplib</code> and <code>email.mime</code> packages.",
        styles['Body']
    ))
    
    email_points = [
        "<b>Dual-Part MIME Construction:</b> Generates a <code>MIMEMultipart('alternative')</code> container holding both a plain-text fallback and a rich HTML layout.",
        "<b>TLS Encryption:</b> Connects over port 587 and executes <code>server.starttls()</code> to ensure end-to-end transport encryption before transmitting credentials and message bodies.",
        "<b>Non-Blocking Fail-Safe Execution:</b> Wrapped completely inside nested <code>try-except</code> blocks. If SMTP credentials are empty or the mail server experiences latency, it logs to stderr but returns <code>False</code> without failing the client's HTTP request."
    ]
    for ep in email_points:
        story.append(Paragraph(f"&bull; {ep}", styles['Bullet']))
        
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 7: THE 3D GLOBE ENGINE (PART 1: SCENE & SOLAR MATH)
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("3. The Masterpiece: 3D Real-Time Earth Globe Engine (Part 1)", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph(
        "The focal point of Leroy's portfolio is the <b>Interactive 3D Real-Time Day &amp; Night Earth Globe</b>. "
        "Unlike standard portfolios that show static images or 2D Google Maps, this system runs a hardware-accelerated "
        "WebGL rendering engine inside Three.js. It features astronomical solar position calculations, custom GLSL shaders, "
        "dynamic canvas billboards, and an orbital great-circle camera flight engine.",
        styles['Body']
    ))
    
    story.append(make_callout(
        "[PRESENTER ANCHOR CONCEPT]",
        "When explaining the 3D globe to the audience tomorrow, emphasize that the Earth is not a flat textured sphere with a static light. <b>It computes the actual mathematical position of the Sun right now in real time using the current UTC hour and day of the year</b>, blending NASA Blue Marble daylight with golden night city lights via a custom GLSL GPU fragment shader.",
        styles, box_color="#eff6ff", border_color="#2563eb"
    ))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("Step 1: Foundational 3D Scene Architecture", styles['SectionH2']))
    story.append(Paragraph(
        "The 3D environment is initialized in <code>initEarthGlobe()</code> inside <code>script.js</code> using four foundational Three.js constructs:",
        styles['Body']
    ))
    
    step1_items = [
        "<b>1. THREE.Scene:</b> The 3D world container. Configured with a deep space black background color: <code>scene.background = new THREE.Color(0x020308)</code>.",
        "<b>2. THREE.PerspectiveCamera:</b> Configured with a 45 deg Field of View (FOV), aspect ratio matching the container dimensions, a near clipping plane of 0.1, and far plane of 2000. Positioned initially at orbital coordinates <code>(x: 0, y: 4, z: 24)</code>.",
        "<b>3. THREE.WebGLRenderer:</b> Configured with <code>{ antialias: true, alpha: false }</code>. Pixel ratio is capped at <code>Math.min(window.devicePixelRatio, 2)</code> to maintain smooth 60 FPS performance on high-DPI Retina screens without GPU overheating.",
        "<b>4. THREE.OrbitControls:</b> Enables smooth mouse drag rotation, pinch zoom, and inertia damping (<code>dampingFactor: 0.05</code>). Distance is clamped between <code>minDistance: 7.5</code> (preventing surface clipping) and <code>maxDistance: 45</code> (preventing lost camera orbit). Auto-rotation is set to 0.65 rad/s."
    ]
    for it in step1_items:
        story.append(Paragraph(f"&bull; {it}", styles['Bullet']))
        
    story.append(Spacer(1, 8))
    story.append(Paragraph("Step 2: Celestial Mechanics &amp; Real-Time Solar Calculations", styles['SectionH2']))
    story.append(Paragraph(
        "To achieve accurate real-time day and night illumination, the application calculates the <b>subsolar point</b> "
        "(the exact geographic latitude and longitude where the Sun is directly overhead) using live UTC time:",
        styles['Body']
    ))
    
    solar_math_text = """// 1. Calculate Day of Year and UTC Decimal Hours
const now = new Date();
const utcHours = now.getUTCHours() + now.getUTCMinutes() / 60 + now.getUTCSeconds() / 3600;
const startOfYear = new Date(Date.UTC(now.getUTCFullYear(), 0, 1));
const dayOfYear = Math.floor((now - startOfYear) / 86400000);

// 2. Solar Declination Angle (Earth's 23.44 deg axial tilt variation over 365.25 days)
const declination = -23.44 * Math.cos(((2 * Math.PI) / 365.25) * (dayOfYear + 10));

// 3. Subsolar Longitude (Sun crosses the Prime Meridian 0 deg at exactly 12:00 UTC)
const subsolarLon = -(utcHours - 12) * 15;"""
    story.append(make_code_block(solar_math_text, styles))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph(
        "<b>Mathematical Interpretation:</b> Earth rotates 360 deg in 24 hours, which equates to <b>15 deg of longitude per hour</b>. "
        "At 12:00 UTC, the Sun is at longitude 0 deg. At 18:00 UTC, the Sun has moved westward by (18 - 12) * 15 deg = 90 deg W (over the Americas). "
        "The calculated solar coordinates <code>(lat, lon)</code> are converted into a 3D unit vector and transformed by Earth's current rotational Euler angle to ensure the sunlight dynamically matches real-world planetary orientation.",
        styles['Body']
    ))
    
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 8: THE 3D GLOBE ENGINE (PART 2: GLSL SHADER PIPELINE)
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("3. The Masterpiece: 3D Real-Time Earth Globe Engine (Part 2)", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph("Step 3: Custom GLSL Day/Night Shader Material", styles['SectionH2']))
    story.append(Paragraph(
        "Standard Three.js materials (such as <code>MeshStandardMaterial</code>) only support a single diffuse texture. "
        "To achieve seamless day-to-night transitions with glowing city lights and atmospheric scattering, Leroy implemented a custom "
        "<b>GLSL ShaderMaterial</b> with custom vertex and fragment programs:",
        styles['Body']
    ))
    
    glsl_code = """// Vertex Shader: Transforms normals into world coordinates
varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vWorldNormal;

void main() {
    vUv = uv;
    vNormal = normalize(normalMatrix * normal);
    vWorldNormal = normalize((modelMatrix * vec4(normal, 0.0)).xyz);
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}

// Fragment Shader: Blends Day, Night, Twilight Amber Glow, and Fresnel Rim
uniform sampler2D uDayTexture;     // NASA Blue Marble Earth Texture
uniform sampler2D uNightTexture;   // NASA Earth Night City Lights Texture
uniform vec3 uSunDirection;        // Live calculated Sun Direction Vector

void main() {
    vec3 dayColor = texture2D(uDayTexture, vUv).rgb;
    vec3 nightColor = texture2D(uNightTexture, vUv).rgb;

    // 1. Dot Product: Cosine of angle between surface normal and sun direction
    float sunDot = dot(vWorldNormal, normalize(uSunDirection));

    // 2. Smoothstep Terminator: Creates a soft dawn/dusk gradient across twilight
    float dayMix = smoothstep(-0.12, 0.15, sunDot);

    // 3. Sunset Rim: Warm golden amber glow along the terminator boundary
    float twilight = (1.0 - smoothstep(0.0, 0.22, abs(sunDot))) * 0.55;
    vec3 sunsetGlow = vec3(1.0, 0.44, 0.16) * twilight;

    // 4. Night Hemisphere: City lights amplified by 2.2x + subtle dark ambient
    vec3 nightLights = nightColor * 2.2;
    vec3 nightAmbient = dayColor * 0.04 + vec3(0.015, 0.02, 0.04);
    vec3 nightSide = nightLights + nightAmbient;

    // 5. Day Hemisphere: Blue marble texture with subtle solar diffuse shading
    vec3 daySide = dayColor * (0.85 + 0.35 * max(sunDot, 0.0));

    // 6. Atmospheric Rim: Rayleigh scattering Fresnel glow on the planetary limb
    float fresnel = pow(1.0 - max(dot(vNormal, vec3(0.0, 0.0, 1.0)), 0.0), 3.5);
    vec3 atmosphereGlow = vec3(0.2, 0.55, 1.0) * fresnel * 0.65 * max(sunDot + 0.2, 0.05);

    gl_FragColor = vec4(mix(nightSide, daySide, dayMix) + sunsetGlow + atmosphereGlow, 1.0);
}"""
    story.append(make_code_block(glsl_code, styles))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("Shader Architectural Highlights:", styles['BodyBold']))
    shader_highlights = [
        "<b>The Terminator Transition:</b> <code>smoothstep(-0.12, 0.15, sunDot)</code> avoids a harsh binary line between day and night, smoothly interpolating illumination across dawn and dusk.",
        "<b>Golden Sunset Glow:</b> The <code>sunsetGlow</code> formula activates when <code>abs(sunDot)</code> is near zero (the twilight zone), projecting a warm orange-red band (<code>RGB: 1.0, 0.44, 0.16</code>) mimicking atmospheric light refraction.",
        "<b>Night City Lights Amplification:</b> Multiplying the night texture by <code>2.2</code> makes urban centers (New York, London, Tokyo) sparkle vibrantly from orbit.",
        "<b>Fresnel Atmospheric Scattering:</b> <code>pow(1.0 - dot(vNormal, viewDir), 3.5)</code> produces an electric blue halo around the curved horizon, simulating Earth's thin upper atmosphere."
    ]
    for sh in shader_highlights:
        story.append(Paragraph(f"&bull; {sh}", styles['Bullet']))
        
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 9: THE 3D GLOBE ENGINE (PART 3: MESHES, BEACONS & FLIGHT ENGINE)
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("3. The Masterpiece: 3D Real-Time Earth Globe Engine (Part 3)", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph("Step 4: Dual-Sphere Architecture &amp; Procedural Starfield", styles['SectionH2']))
    dual_points = [
        "<b>Base Earth Sphere:</b> A <code>THREE.SphereGeometry(6.8, 64, 64)</code> running the custom GLSL shader material.",
        "<b>Atmospheric Cloud Layer:</b> A secondary, slightly larger concentric sphere of radius <b>6.87</b> (0.07 units above the surface). It uses a semi-transparent cloud texture (<code>opacity: 0.35</code>) and <code>THREE.AdditiveBlending</code>. It rotates at an independent rate (<code>clouds.rotation.y += 0.0003</code>) to simulate atmospheric winds.",
        "<b>Procedural 3D Starfield:</b> Generates <b>2,800 stars</b> in a <code>THREE.BufferGeometry</code> across an 850-unit cube, rendered via <code>THREE.Points</code> with a subtle orbital drift of <code>0.00015 rad/frame</code>."
    ]
    for dp in dual_points:
        story.append(Paragraph(f"&bull; {dp}", styles['Bullet']))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("Step 5: Geographic Coordinate Projection Math", styles['SectionH2']))
    
    geo_code = """function latLongToVector3(lat, lon, radius) {
    const phi = (90 - lat) * (Math.PI / 180);    // Polar angle (0 to PI)
    const theta = (lon + 180) * (Math.PI / 180); // Azimuthal angle (0 to 2*PI)
    return new THREE.Vector3(
        -(radius * Math.sin(phi) * Math.cos(theta)), // X
        radius * Math.cos(phi),                      // Y (Vertical)
        radius * Math.sin(phi) * Math.sin(theta)    // Z
    );
}"""
    story.append(make_code_block(geo_code, styles))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("Step 6: Interactive Beacons &amp; Canvas Billboards", styles['SectionH2']))
    beacon_items = [
        "<b>Surface-Normal Cylinder Stem:</b> A cylinder of height 1.7 units rotated to align with the surface normal vector using <code>quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), normal)</code>.",
        "<b>Glowing Tip Beacon &amp; Pulse Halo:</b> A spherical tip mesh (radius 0.36) with outer pulsing halo (radius 0.52).",
        "<b>HTML5 2D Canvas Billboards:</b> Labels are drawn dynamically on an in-memory <code>&lt;canvas&gt;</code> with rounded glass styling and Poppins typography, uploaded to a <code>THREE.CanvasTexture</code>, and rendered as a <code>THREE.Sprite</code> with <code>depthTest: false</code>."
    ]
    for bi in beacon_items:
        story.append(Paragraph(f"&bull; {bi}", styles['Bullet']))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("Step 7: Google Earth \"Hyper-Dive\" Flight Engine", styles['SectionH2']))
    flight_items = [
        "<b>Great-Circle Spherical Interpolation (SLERP):</b> Camera direction vectors are interpolated using Spherical Linear Interpolation: <code>slerpVectors(startDir, endDir, easedP)</code>, preventing the camera from cutting through the Earth.",
        "<b>3-Stage Altitude Easing Curve:</b> High orbital alignment (0-35%) --&gt; Atmospheric plunge (35-85%) --&gt; Touchdown flare (85-100% leveling at surface altitude 1.35).",
        "<b>Dynamic FOV Speed \"Warp\":</b> Camera FOV dynamically widens from 45 deg up to <b>53 deg</b> during the plunge for an exhilarating sense of speed, contracting back to 44 deg on touchdown.",
        "<b>Atmospheric Entry Flight HUD:</b> Glowing cyan HUD overlay with moving laser scanner announces: <code>DIVING INTO MUSA ASSISTANT...</code>.",
        "<b>Smart Drag-vs-Click Raycasting:</b> Only pointer movements smaller than <b>6 pixels</b> trigger a dive, preventing accidental clicks while rotating the Earth."
    ]
    for fi in flight_items:
        story.append(Paragraph(f"&bull; {fi}", styles['Bullet']))
        
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 10: GLOBAL PROJECTS & DAYLIGHT TIMEZONE CALCULATOR
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("4. Projects Highlighted Across the Globe", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph(
        "The globe features three core software engineering projects deployed at distinct geographic coordinates, "
        "reflecting global development perspectives:",
        styles['Body']
    ))
    
    projects_table_data = [
        [
            Paragraph("Project Name", styles['TableHead']),
            Paragraph("Location &amp; Coordinates", styles['TableHead']),
            Paragraph("Technical Architecture &amp; Stack", styles['TableHead'])
        ],
        [
            Paragraph("<b>MUSA Assistant</b><br/><font color='#2563eb'>AI &amp; Academic Systems</font>", styles['TableCellBold']),
            Paragraph("Harare, Zimbabwe<br/>(Africa)<br/>Lat: -19.01, Lon: 29.15<br/>Timezone: UTC+2", styles['TableCell']),
            Paragraph("Voice- and text-activated AI academic assistant. Integrates with university student portals for automated timetable notifications, exam schedules, and conversational AI queries. Built with Python, NLP pipelines, and REST APIs.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Inventory Management GUI</b><br/><font color='#6366f1'>Enterprise Desktop OOP</font>", styles['TableCellBold']),
            Paragraph("New York, USA<br/>(North America)<br/>Lat: 40.71, Lon: -74.00<br/>Timezone: UTC-4", styles['TableCell']),
            Paragraph("Desktop inventory management platform. Built on strict Object-Oriented Programming (OOP) principles in Python and Tkinter, backed by SQLite atomic transactions, instant search caching, and automated inventory report generators.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Dynamic Data Visualizer</b><br/><font color='#0284c7'>Web Analytics &amp; Algorithms</font>", styles['TableCellBold']),
            Paragraph("London, United Kingdom<br/>(Europe)<br/>Lat: 51.50, Lon: -0.12<br/>Timezone: UTC+1", styles['TableCell']),
            Paragraph("High-throughput browser analytics engine. Features custom Canvas API real-time charting, algorithmic sorting step-by-step visualizations, dataset CSV ingestion, and multi-format statistical reporting.", styles['TableCell'])
        ]
    ]
    t_projects = Table(projects_table_data, colWidths=[130, 110, 282])
    t_projects.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_projects)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Live Daylight Status Calculator", styles['SectionH2']))
    story.append(Paragraph(
        "When the user selects any project on the globe, the application calls <code>getLocalDaylightStatus(timezoneOffset)</code>. "
        "It queries the client's live UTC clock, applies the target project's timezone offset, and checks whether local time is between 06:00 and 18:00. "
        "The project inspector card displays a real-time badge: <b>[Daylight (14:30 Local)]</b> or <b>[Night Lights Active (22:15 Local)]</b>, "
        "reinforcing the dynamic connection between the 3D globe's solar shader and real-world time.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))
    
    daylight_code = """function getLocalDaylightStatus(timezoneOffset) {
    const now = new Date();
    const utcHours = now.getUTCHours() + now.getUTCMinutes() / 60;
    let localHour = (utcHours + timezoneOffset) % 24;
    if (localHour < 0) localHour += 24;
    const isDay = localHour >= 6 && localHour < 18;
    const timeStr = `${String(Math.floor(localHour)).padStart(2, "0")}:${String(now.getUTCMinutes()).padStart(2, "0")}`;
    return {
        isDay,
        timeStr,
        label: isDay ? `Daylight (${timeStr} Local)` : `Night Lights Active (${timeStr} Local)`
    };
}"""
    story.append(make_code_block(daylight_code, styles))
    
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 11: PRESENTATION DELIVERY STRATEGY & ROADMAP
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("5. Presentation Delivery Strategy &amp; Defense Guide", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph("5.1 High-Impact 2-Minute Opening Elevator Pitch", styles['SectionH2']))
    story.append(Paragraph(
        "<i>Use this word-for-word script during your initial introduction to hook the audience immediately:</i>",
        styles['Body']
    ))
    
    pitch_text = (
        "Good morning, esteemed judges, professors, and colleagues. My name is Leroy Matienga, and I am an undergraduate "
        "Computer Science student specializing in backend systems engineering and interactive web technologies. "
        "Today, I am proud to present my personal portfolio web application.\n\n"
        "Most developer portfolios are static digital resumes. I wanted mine to be living proof of my engineering capabilities. "
        "My portfolio is a full-stack platform built with Python Flask, SQLite, and Three.js WebGL. "
        "Its centerpiece is an interactive, real-time 3D Earth globe that runs a custom GLSL fragment shader calculating the exact "
        "position of the Sun relative to Earth using live UTC astronomical formulas. Visitors can inspect my software deployments "
        "across Africa, North America, and Europe through a cinematic orbital flight engine that models great-circle spherical curves.\n\n"
        "Behind this visual layer lies an enterprise-grade backend with directory traversal defenses, IP-based sliding-window rate limiting, "
        "parameterized SQL queries, and an automated SMTP notification engine. Over the next few minutes, I will walk you through "
        "the engineering architecture, the code structure, and the mathematical implementation of the 3D globe."
    )
    story.append(make_speaking_card("Opening Pitch (Memorize or Read Confidently)", pitch_text, styles))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("5.2 Ten-Minute Presentation Roadmap", styles['SectionH2']))
    roadmap_points = [
        "<b>Minute 0:00 - 1:30 | Introduction &amp; Hero Section:</b> State your name, degree, and career focus. Point out the magnetic pill capsule navigation and typewriter loop. Mention that the CV download streams directly from a protected Flask endpoint.",
        "<b>Minute 1:30 - 3:30 | The 3D Earth Globe Showcase (The \"Wow\" Factor):</b> Scroll down to the 3D globe. Click Fullscreen. Explain that the day/night boundary is generated live on the GPU using custom GLSL shaders and UTC solar declination formulas. Point out the golden twilight rim and sparkling city lights.",
        "<b>Minute 3:30 - 5:30 | Project Deep-Dive via Hyper-Dive:</b> Click the MUSA Assistant dock pill. Let the audience watch the camera plunge into Harare, Zimbabwe with the animated flight HUD and speed FOV warp. Explain MUSA's AI architecture. Then pull out to orbit and dive into New York or London.",
        "<b>Minute 5:30 - 7:30 | Backend Architecture &amp; Database:</b> Transition to the server architecture. Open or discuss <code>app.py</code> and <code>models.py</code>. Highlight how you mitigated XSS via <code>html.escape()</code>, stopped SQL injection via parameterized queries, and implemented an IP sliding-window rate limiter.",
        "<b>Minute 7:30 - 9:00 | Live Contact Form Demonstration:</b> Fill out the contact form with a test inquiry. Click Send. Show the loading spinner transitioning to the green checkmark toast. Explain that this atomically logged to SQLite and dispatched an encrypted HTML email via smtplib.",
        "<b>Minute 9:00 - 10:00 | Conclusion &amp; Q&amp;A:</b> Summarize your engineering philosophy: clean code, defensive architecture, and immersive user experiences. Open the floor for questions."
    ]
    for rp in roadmap_points:
        story.append(Paragraph(f"&bull; {rp}", styles['Bullet']))
        
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 12: TECHNICAL DEFENSE QUESTIONS & MODEL ANSWERS
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("5.3 Anticipated Technical Defense Questions &amp; Model Answers", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph(
        "<i>Examiners and professors will test your technical depth. Here are the most likely challenging questions and how to answer them:</i>",
        styles['Body']
    ))
    
    qa_list = [
        (
            "Q1: Why did you build a custom GLSL shader instead of using standard Three.js MeshStandardMaterial with a directional light?",
            "Standard Three.js materials calculate lighting on a single texture. They cannot simultaneously blend between a daytime satellite map and a nighttime illuminated city lights map while rendering a warm amber twilight glow along the terminator rim. By writing custom GLSL vertex and fragment shaders, I gained direct control over GPU hardware registers. I calculate the dot product between the surface normal and the live solar direction vector, allowing me to smoothly interpolate between night lights and day marble using smoothstep, while computing an atmospheric Rayleigh Fresnel rim glow on the planetary limb."
        ),
        (
            "Q2: How does the camera flight engine avoid cutting through the Earth during hyper-dives?",
            "If you linearly interpolate camera position from orbit (distance = 24) to the surface (distance = 8.15), the straight chord cuts straight through the Earth's interior geometry. To prevent this, I implemented Spherical Linear Interpolation (SLERP) using unit direction vectors. The direction vector follows a spherical great-circle arc over the globe, while the distance scalar follows an altitude easing curve. The descent is delayed until the camera has rotated horizontally over the target, after which it executes a steep atmospheric plunge and levels off at a flare altitude of 1.35 units above the surface."
        ),
        (
            "Q3: How do you handle mobile performance and prevent GPU throttling on lower-end devices?",
            "I implemented three key optimizations: First, renderer pixel ratio is clamped using Math.min(window.devicePixelRatio, 2), preventing ultra-high-resolution mobile screens from pushing 4K framebuffers unnecessarily. Second, animations use requestAnimationFrame rather than timers, synchronizing with the display's native refresh rate. Third, all 2,800 stars share a single BufferGeometry, which submits the entire starfield to the GPU in a single draw call."
        ),
        (
            "Q4: Why choose Flask and SQLite rather than a heavier stack like Django or Node.js/PostgreSQL?",
            "Software engineering is about selecting the right tool for the problem. For a high-performance portfolio, a heavy ORM and complex multi-process relational server adds unnecessary operational overhead and memory footprint. Flask provided a lean, microsecond-fast REST layer with zero bloat. SQLite operates in-process with zero network latency, supports ACID atomic transactions, and handles thousands of daily submissions effortlessly without requiring a dedicated database daemon."
        ),
        (
            "Q5: How does your rate limiter work without an external database like Redis?",
            "In models.py, I engineered a sliding-window rate query using SQLite's built-in datetime engine: WHERE ip_address = ? AND created_at >= datetime('now', '-60 seconds'). On every contact submission, app.py queries this count. If the IP has made 5 or more requests within the last 60 seconds, it immediately rejects the request with HTTP 429 Too Many Requests. This gives me sub-millisecond rate limiting with zero external dependencies."
        ),
        (
            "Q6: How did you ensure the contact form wouldn't fail if the email service goes down?",
            "I applied the principle of Graceful Degradation. The database insert and the email notification are decoupled. When a user submits a message, the database write occurs first. Then, the email dispatch in email_service.py is wrapped in a non-blocking try-except block. If SMTP credentials expire or the network times out, the server logs an error to stderr but returns HTTP 201 to the client. The user's message is safely stored in SQLite, and the system never crashes."
        )
    ]
    
    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", styles['SectionH3']))
        story.append(Paragraph(f"<b>Model Answer:</b> \"{a}\"", styles['Body']))
        story.append(Spacer(1, 3))
        
    story.append(PageBreak())
    
    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 13: PRE-PRESENTATION CHECKLIST & CONFIDENCE STRATEGY
    # ═════════════════════════════════════════════════════════════════════════
    
    story.append(Paragraph("5.4 Final Defense Preparation &amp; Live Demo Checklist", styles['SectionH1']))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2563eb"), spaceAfter=8))
    
    story.append(Paragraph(
        "To ensure a flawless presentation tomorrow, follow this step-by-step technical rehearsal procedure:",
        styles['Body']
    ))
    
    checklist_items = [
        "<b>Step 1: Start Server in Local Terminal:</b> Open terminal in the portfolio directory and run: <code>python app.py</code>. Confirm the banner output: <code>Leroy Matienga Portfolio Server Running on http://localhost:5000</code>.",
        "<b>Step 2: Browser Setup &amp; Viewport:</b> Open Google Chrome or Microsoft Edge and navigate to <code>http://localhost:5000</code>. Press <b>F11</b> to enter clean borderless fullscreen.",
        "<b>Step 3: Test Navigation Indicator:</b> Move your cursor across Home, About, Portfolio, Skills, and Contact. Click and drag across the navbar to show the magnetic indicator tracking.",
        "<b>Step 4: Demonstrate 3D Globe Flight:</b> Scroll to the 3D globe. Click the <b>Fullscreen</b> button on the top-right of the space frame. Point out the live Sun indicator. Click <b>MUSA Assistant (Africa)</b> to trigger the hyper-dive flight with the HUD scanner.",
        "<b>Step 5: Inspect Project Details:</b> Show the daylight badge (e.g., ☀️ Daylight or 🌙 Night Lights) and explain how the UTC clock informs local time.",
        "<b>Step 6: Return to Orbit:</b> Click the <b>Orbit View</b> button or press the <b>Escape</b> key to trigger the smooth pull-out camera transition.",
        "<b>Step 7: Demonstrate Defensive Backend Form:</b> Scroll to the Contact section. Enter a test name, email, subject, and message. Submit and observe the loading state and green success feedback toast.",
        "<b>Step 8: Demonstrate Rate Limiter (Optional Power Move):</b> If an examiner asks about security, rapidly click submit multiple times or trigger 6 API calls in Postman/curl to show the server cleanly returning HTTP 429 Too Many Requests."
    ]
    for ci in checklist_items:
        story.append(Paragraph(f"&bull; {ci}", styles['Bullet']))
        
    story.append(Spacer(1, 10))
    story.append(make_callout(
        "[SUMMARY & FINAL PRESENTATION ADVICE]",
        "Leroy, you built a truly impressive, multi-disciplinary software project. It balances advanced 3D computer graphics, astronomical physics, custom GPU shaders, robust security patterns, and clean Python backend engineering. Speak with confidence, take your time during the 3D globe flight, and remember that you understand every single line of this codebase. Best of luck with tomorrow's presentation!",
        styles, box_color="#f0fdf4", border_color="#10b981"
    ))
    story.append(Spacer(1, 14))
    
    # Signature Footer Table
    sign_data = [
        [
            Paragraph("<b>Presenter:</b> Leroy Matienga<br/>Candidate for B.Sc. Computer Science", styles['TableCell']),
            Paragraph("<b>Project:</b> Interactive 3D Portfolio Application<br/>Full-Stack Architecture &amp; WebGL Engine", styles['TableCell']),
            Paragraph("<b>Status:</b> Presentation Ready<br/>Document Generated: October 2026", styles['TableCellBold'])
        ]
    ]
    t_sign = Table(sign_data, colWidths=[174, 174, 174])
    t_sign.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_sign)
    
    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Refined Presentation Guide PDF built successfully: {pdf_filename}")
    return pdf_filename


if __name__ == "__main__":
    build_pdf()
