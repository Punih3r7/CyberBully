#!/usr/bin/env python3
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

FIG = "work/Premier-University-Chattogram-CSE-Thesis-Template-main/figures"

HEADBLUE = RGBColor(31,78,121)
GREEN    = RGBColor(84,130,53)
ORANGE   = RGBColor(197,90,17)
OURROW   = RGBColor(255,242,204)
ROWLIGHT = RGBColor(222,235,247)
DARK     = RGBColor(26,26,26)
WHITE    = RGBColor(255,255,255)
GREY     = RGBColor(110,110,110)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

def add_slide():
    return prs.slides.add_slide(BLANK)

def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def rect(slide, l,t,w,h, color, line=None):
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l,t,w,h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(1)
    sp.shadow.inherit = False
    return sp

def textbox(slide, l,t,w,h, text, size=18, color=DARK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri"):
    tb = slide.shapes.add_textbox(l,t,w,h); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font
    return tb

def header(slide, title, tag=""):
    rect(slide, 0,0, SW, Inches(1.15), HEADBLUE)
    rect(slide, 0, Inches(1.15), SW, Inches(0.07), ORANGE)
    textbox(slide, Inches(0.5), Inches(0.12), Inches(11.2), Inches(0.95), title, size=28, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if tag:
        textbox(slide, Inches(10.6), Inches(0.12), Inches(2.5), Inches(0.95), tag, size=12, color=WHITE, bold=True, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def footer(slide, n):
    textbox(slide, Inches(0.4), Inches(7.05), Inches(9), Inches(0.4),
            "Explainable Cyberbullying Detection  •  RoBERTa + LIME", size=10, color=GREY)
    textbox(slide, Inches(12.3), Inches(7.05), Inches(0.8), Inches(0.4), str(n), size=11, color=GREY, align=PP_ALIGN.RIGHT)

def bullets(slide, l,t,w,h, items, size=20, gap=10):
    tb = slide.shapes.add_textbox(l,t,w,h); tf = tb.text_frame; tf.word_wrap=True
    for i,(txt, lvl, bold, col) in enumerate(items):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.level = lvl; p.space_after = Pt(gap)
        run = p.add_run(); run.text = ("•  " if lvl==0 else "–  ")+txt
        run.font.size = Pt(size); run.font.bold = bold
        run.font.color.rgb = col; run.font.name="Calibri"
    return tb

def pic_fit(slide, path, cx, top, max_w, max_h):
    """place image centred horizontally at cx, scaled to fit max_w x max_h."""
    from PIL import Image
    iw, ih = Image.open(path).size
    ar = iw/ih
    w = max_w; h = int(w/ar)
    if h > max_h:
        h = max_h; w = int(h*ar)
    left = int(cx - w/2)
    slide.shapes.add_picture(path, left, top, width=w, height=h)
    return w,h

def style_table(tbl, header_fill=HEADBLUE, header_color=WHITE, body_size=14, header_size=15,
                highlight_last=False, zebra=True):
    nrows=len(tbl.rows); ncols=len(tbl.columns)
    for r in range(nrows):
        for c in range(ncols):
            cell = tbl.cell(r,c)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left=Inches(0.08); cell.margin_right=Inches(0.08)
            cell.margin_top=Inches(0.03); cell.margin_bottom=Inches(0.03)
            para = cell.text_frame.paragraphs[0]
            para.alignment = PP_ALIGN.LEFT if c==0 else PP_ALIGN.CENTER
            for run in para.runs:
                run.font.name="Calibri"
                if r==0:
                    run.font.bold=True; run.font.size=Pt(header_size); run.font.color.rgb=header_color
                else:
                    run.font.size=Pt(body_size); run.font.color.rgb=DARK
            if r==0:
                cell.fill.solid(); cell.fill.fore_color.rgb=header_fill
            elif highlight_last and r==nrows-1:
                cell.fill.solid(); cell.fill.fore_color.rgb=OURROW
            elif zebra and r%2==0:
                cell.fill.solid(); cell.fill.fore_color.rgb=ROWLIGHT
            else:
                cell.fill.solid(); cell.fill.fore_color.rgb=WHITE

def make_table(slide, l,t,w,h, data, colw=None, **kw):
    rows=len(data); cols=len(data[0])
    gf = slide.shapes.add_table(rows, cols, l,t,w,h)
    tbl = gf.table
    if colw:
        for i,cw in enumerate(colw): tbl.columns[i].width=cw
    for r in range(rows):
        for c in range(cols):
            tbl.cell(r,c).text = str(data[r][c])
    style_table(tbl, **kw)
    return tbl

n=0
def nxt():
    global n; n+=1; return n

# ============ SLIDE 1 : TITLE ============
s = add_slide()
rect(s, 0,0, SW, SH, WHITE)
rect(s, 0,0, SW, Inches(2.0), HEADBLUE)
rect(s, 0, Inches(2.0), SW, Inches(0.08), ORANGE)
textbox(s, Inches(0.8), Inches(0.35), Inches(11.7), Inches(1.5),
        "Explainable Cyberbullying Detection Using Deep Learning and Transformer Models with LIME",
        size=30, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
textbox(s, Inches(0.8), Inches(2.4), Inches(11.7), Inches(0.5),
        "A Binary Detector (RoBERTa) with Word-Level Explanations", size=20, color=ORANGE, bold=True)
bullets(s, Inches(0.8), Inches(3.4), Inches(11.7), Inches(2.6), [
    ("Presented by:  Mohammad Asmual Hoque Yousha  (0222210005101121)",0,True,DARK),
    ("                      Md Mostafa Kamal Anna  (0222210005101129)",0,True,DARK),
    ("Supervised by:  Ms. Tanni Dhoom, Assistant Professor",0,False,DARK),
    ("Department of Computer Science and Engineering",0,False,GREY),
    ("Premier University, Chattogram  •  October 2026",0,False,GREY),
], size=18, gap=8)
footer(s, nxt())
set_notes(s, "[BOTH / Speaker 1 opens] Good morning. We are presenting our thesis on explainable cyberbullying detection. "
           "Our system detects whether an online comment is bullying or not, using a RoBERTa transformer, and — unlike most "
           "prior work — it also explains WHY, using LIME. ANIMATION: let the title bar fade in, then the names appear.")

# ============ SLIDE 2 : PROBLEM & MOTIVATION ============
s = add_slide(); header(s, "The Problem & Why It Matters", "Speaker 1")
bullets(s, Inches(0.6), Inches(1.5), Inches(7.1), Inches(5.2), [
    ("Millions of comments are posted daily on YouTube, Reddit, Facebook.",0,True,DARK),
    ("A large share is hostile — and manual moderation cannot keep up.",0,False,DARK),
    ("Most existing detectors give only a label, no reason.",0,True,ORANGE),
    ("A black-box moderation decision is hard to trust or appeal.",0,False,DARK),
    ("Our goal: high accuracy  +  a clear explanation for every decision.",0,True,GREEN),
], size=20, gap=14)
pic_fit(s, f"{FIG}/class_distribution.png", Inches(10.3), Inches(1.7), Inches(5.0), Inches(4.6))
footer(s, nxt())
set_notes(s, "[Speaker 1] Social media produces a huge volume of comments and a lot of it is harmful. "
           "Humans cannot moderate it all. The bigger problem: existing detectors just output 'bullying' with no reason, "
           "so the decision cannot be trusted or challenged. Our aim is both accuracy AND transparency. "
           "ANIMATION: reveal the bullet points one by one; the chart appears last.")

# ============ SLIDE 3 : OBJECTIVES & CONTRIBUTIONS ============
s = add_slide(); header(s, "Objectives & Contributions", "Speaker 1")
bullets(s, Inches(0.6), Inches(1.5), Inches(12.1), Inches(5.3), [
    ("Build a binary detector (Bullying vs Not-Bullying) on multi-platform data.",0,True,DARK),
    ("Compare four models: Logistic Regression, LSTM, GRU, RoBERTa.",0,False,DARK),
    ("Beat the base paper (Esan et al., 77%) — on our data AND on their own data.",0,True,DARK),
    ("Add LIME so every prediction can be explained word by word.",0,True,GREEN),
    ("Give an honest multi-dataset comparison against two reference studies.",0,False,DARK),
], size=22, gap=16)
footer(s, nxt())
set_notes(s, "[Speaker 1] Our objectives: build the detector, compare four models from a simple baseline up to a transformer, "
           "beat the base paper's accuracy and verify it on more than one dataset, and — the key novelty — add LIME explanations. "
           "ANIMATION: each objective flies/fades in one at a time.")

# ============ SLIDE 4 : RELATED WORK ============
s = add_slide(); header(s, "Related Work — Where We Fit", "Speaker 1")
data=[["Study","Best Model","Accuracy","Explainable"],
 ["Esan et al. (2024)  [base]","LSTM","77.00%","No"],
 ["Ogunleye & Dharmaraj (2023)","RoBERTa","87.00%","No"],
 ["Muneer et al. (2023)","BERT+biLSTM+CNN","97.40%","No"],
 ["Alrowais (2024)","RoBERTa + GloVe","95.00%","No"],
 ["Sihab-Us-Sakib (2024)","XLM-RoBERTa","82.61%","No"],
 ["Azhar & Runa (2025)","RoBERTa","83.90%","No"],
 ["Our Work","RoBERTa + LIME","92.33%","Yes"]]
make_table(s, Inches(0.8), Inches(1.45), Inches(11.7), Inches(5.2), data,
           colw=[Inches(4.6),Inches(3.6),Inches(1.9),Inches(1.6)],
           highlight_last=True, body_size=15, header_size=16)
textbox(s, Inches(0.8), Inches(6.75), Inches(11.7), Inches(0.5),
        "We reviewed 12 studies — almost none explain their decisions. That gap is our contribution.",
        size=14, color=ORANGE, bold=True)
footer(s, nxt())
set_notes(s, "[Speaker 1] We reviewed twelve studies. Some reach very high accuracy, but look at the last column — "
           "almost all say 'No' to explainability. Our work (highlighted) reaches 92.33% AND is explainable. "
           "ANIMATION: bring in the table, then highlight the last 'Our Work' row.")

# ============ SLIDE 5 : DATASET ============
s = add_slide(); header(s, "Dataset", "Speaker 1")
bullets(s, Inches(0.5), Inches(1.4), Inches(4.6), Inches(5.0), [
    ("~4,000 English comments",0,True,DARK),
    ("1,000 self-collected: YouTube, Reddit, Facebook",0,False,DARK),
    ("3,000 from Jigsaw toxic-comment corpus",0,False,DARK),
    ("Near-balanced:  2,059 Not-Bullying / 1,941 Bullying",0,True,GREEN),
    ("0 = Not-Bullying,  1 = Bullying",0,False,GREY),
    ("Avg length ~22.6 words",0,False,GREY),
], size=18, gap=12)
pic_fit(s, f"{FIG}/class_distribution.png", Inches(7.6), Inches(1.6), Inches(3.4), Inches(2.6))
pic_fit(s, f"{FIG}/text_length.png",       Inches(11.1), Inches(1.6), Inches(3.4), Inches(2.6))
textbox(s, Inches(6.0), Inches(4.5), Inches(7.1), Inches(0.5),
        "Left: class balance.     Right: comment-length distribution.", size=13, color=GREY)
footer(s, nxt())
set_notes(s, "[Speaker 1] Our dataset has about 4,000 English comments — a thousand we collected ourselves from three platforms, "
           "and three thousand from the public Jigsaw corpus. The classes are almost evenly balanced, so accuracy is a fair measure. "
           "ANIMATION: bullets first, then the two charts slide in from the right.")

# ============ SLIDE 6 : DATASET EXAMPLES ============
s = add_slide(); header(s, "Dataset Examples (6 Bully Types)", "Speaker 1")
data=[["Comment","Label","Type"],
 ["Show this video and Ronaldo's stats to him.","Not-Bullying","--"],
 ["Bolton is a clown","Bullying","Troll"],
 ["Religion is primitive and a big waste of time.","Bullying","Religion"],
 ["death to the infidel, whoever that may be","Bullying","Threat"],
 ["This is what happens when you elect a moron.","Bullying","Political"],
 ["Mass immigration is destroying the West.","Bullying","Racism"]]
make_table(s, Inches(0.7), Inches(1.5), Inches(11.9), Inches(4.6), data,
           colw=[Inches(7.9),Inches(2.1),Inches(1.9)], body_size=15, header_size=16)
textbox(s, Inches(0.7), Inches(6.3), Inches(11.9), Inches(0.5),
        "Strong wording alone is not bullying — the task needs context, not keywords.", size=14, color=ORANGE, bold=True)
footer(s, nxt())
set_notes(s, "[Speaker 1] Here are real labelled examples covering all six bully types we recorded. "
           "Notice the task is not just keyword spotting — a strongly worded comment is not automatically bullying. "
           "ANIMATION: reveal rows top-to-bottom.")

# ============ SLIDE 7 : METHODOLOGY PIPELINE ============
s = add_slide(); header(s, "Methodology — The Pipeline", "Speaker 1")
pic_fit(s, f"{FIG}/diag_pipeline.png", Inches(6.66), Inches(1.45), Inches(9.2), Inches(5.3))
footer(s, nxt())
set_notes(s, "[Speaker 1 — hand over after this] This is our full pipeline: collect data, clean and de-duplicate (we de-duplicate AFTER "
           "cleaning, which improved every model), reduce to a binary label, split 70/15/15, train the four models, evaluate, and finally "
           "run LIME on the best model. My teammate will now take over with the models and results. "
           "ANIMATION: reveal the boxes step by step following the arrows.")

# ============ SLIDE 8 : MODELS + WHY LIME ============
s = add_slide(); header(s, "Models & Why LIME", "Speaker 2")
bullets(s, Inches(0.5), Inches(1.4), Inches(6.0), Inches(4.0), [
    ("Four models, simple → advanced:",0,True,DARK),
    ("TF-IDF + Logistic Regression (baseline)",1,False,DARK),
    ("LSTM and GRU (read word order)",1,False,DARK),
    ("RoBERTa (pretrained transformer)",1,True,GREEN),
    ("LIME = model-agnostic, local, word-level, lightweight",0,True,ORANGE),
], size=18, gap=10)
pic_fit(s, f"{FIG}/diag_limeflow.png", Inches(9.6), Inches(2.0), Inches(6.6), Inches(3.2))
textbox(s, Inches(6.6), Inches(5.3), Inches(6.5), Inches(1.0),
        "LIME perturbs the comment, watches RoBERTa's probability, and scores each word.",
        size=13, color=GREY)
footer(s, nxt())
set_notes(s, "[Speaker 2] Thank you. We trained four models from a simple baseline up to RoBERTa. "
           "For explanations we chose LIME because it is model-agnostic, explains one comment at a time, gives word-level reasons, "
           "and is lightweight. This diagram shows how LIME works. ANIMATION: bullets first, then the flow diagram.")

# ============ SLIDE 9 : RESULTS ============
s = add_slide(); header(s, "Results — RoBERTa Wins", "Speaker 2")
data=[["Model","Accuracy","Precision","Recall","F1-Score"],
 ["Logistic Regression","83.33%","83.62%","83.33%","83.27%"],
 ["GRU","85.33%","85.36%","85.33%","85.34%"],
 ["LSTM","87.33%","87.33%","87.33%","87.33%"],
 ["RoBERTa (our model)","92.33%","92.36%","92.33%","92.33%"]]
make_table(s, Inches(1.2), Inches(1.7), Inches(10.9), Inches(3.4), data,
           colw=[Inches(3.3),Inches(1.9),Inches(1.9),Inches(1.9),Inches(1.9)],
           highlight_last=True, body_size=16, header_size=17)
textbox(s, Inches(1.2), Inches(5.4), Inches(10.9), Inches(1.2),
        "RoBERTa: 92.33% — 5 points above the best recurrent model, and far above the base paper's 77%.",
        size=16, color=GREEN, bold=True)
footer(s, nxt())
set_notes(s, "[Speaker 2] Here are the results on our test set. The pattern is clean: the linear baseline is solid, the recurrent "
           "models improve on it, and RoBERTa is the clear winner at 92.33% — five points ahead and well above the base paper's 77%. "
           "ANIMATION: reveal rows top-to-bottom, highlight the RoBERTa row.")

# ============ SLIDE 10 : CONFUSION MATRIX ============
s = add_slide(); header(s, "Confusion Matrices — All Four Models", "Speaker 2")
pic_fit(s, f"{FIG}/cm_combined.png", Inches(6.66), Inches(1.4), Inches(9.0), Inches(5.3))
footer(s, nxt())
set_notes(s, "[Speaker 2] All four confusion matrices on one scale. Every model gets most cases right (dark diagonal), "
           "but RoBERTa (bottom-right) has the fewest and most balanced errors — only 19 false positives and 27 missed. "
           "ANIMATION: zoom/fade the figure in; optionally point to the RoBERTa panel.")

# ============ SLIDE 11 : LIME EXPLAINABILITY ============
s = add_slide(); header(s, "LIME — Explaining Correct Predictions", "Speaker 2")
pic_fit(s, f"{FIG}/out_hates.png", Inches(3.5), Inches(1.5), Inches(6.2), Inches(3.0))
pic_fit(s, f"{FIG}/lime_hates.png", Inches(10.3), Inches(1.5), Inches(5.4), Inches(3.0))
textbox(s, Inches(0.5), Inches(5.0), Inches(12.3), Inches(1.5),
        "“Everyone hates you, just go away” → Bullying (93.30%). "
        "LIME shows the words that drove it: hates, you, away. The decision is transparent and defensible.",
        size=16, color=DARK, bold=False)
footer(s, nxt())
set_notes(s, "[Speaker 2] This is LIME in action on a correct case. The left is the actual program output; the right is the bar chart. "
           "The model flagged it as bullying because of 'hates', 'you', 'away' — exactly what a human would point to. "
           "ANIMATION: show the output screenshot first, then the bar chart, then the caption.")

# ============ SLIDE 12 : SARCASM FAILURE ============
s = add_slide(); header(s, "Honest Limitation — Sarcasm", "Speaker 2")
pic_fit(s, f"{FIG}/out_sarcasm.png", Inches(3.6), Inches(1.45), Inches(6.4), Inches(3.1))
pic_fit(s, f"{FIG}/lime_sarcasm.png", Inches(10.4), Inches(1.45), Inches(5.3), Inches(3.1))
textbox(s, Inches(0.5), Inches(5.0), Inches(12.3), Inches(1.6),
        "“Wow, you're really smart... said no one ever.” → predicted Not-Bullying (WRONG). "
        "Positive words (Wow, really, said) fool the model. LIME makes this failure visible — a strength of explainability.",
        size=16, color=ORANGE, bold=False)
footer(s, nxt())
set_notes(s, "[Speaker 2] We are honest about weaknesses. This sarcastic comment is actually bullying, but the model said "
           "Not-Bullying with high confidence. LIME shows why: the positive-sounding words won. Sarcasm is a known hard problem — "
           "and note that WITHOUT explainability this error would be invisible. ANIMATION: output first, then chart, then caption.")

# ============ SLIDE 13 : SOCIAL IMPACT + CONCLUSION ============
s = add_slide(); header(s, "Social Impact & Conclusion", "Speaker 2")
bullets(s, Inches(0.6), Inches(1.4), Inches(12.1), Inches(5.3), [
    ("Protects vulnerable users; reduces moderator burden.",0,False,DARK),
    ("Explainable decisions → fairer, reviewable moderation.",0,True,GREEN),
    ("Best used human-in-the-loop (assist, not replace).",0,False,DARK),
    ("Conclusion: RoBERTa best in every setting + LIME adds trust.",0,True,DARK),
    ("Beats the base paper (77%) on our data (92.33%) and theirs (89.01%).",0,False,DARK),
], size=21, gap=16)
footer(s, nxt())
set_notes(s, "[Speaker 2] Beyond the numbers: used responsibly, with a human in the loop, this system can protect users and make "
           "moderation fairer because every decision can be explained. In conclusion, RoBERTa was best in every setting and LIME "
           "adds the trust that prior work lacks. ANIMATION: reveal points one by one.")

# ============ SLIDE 14 : FUTURE WORK + THANKS ============
s = add_slide(); header(s, "Future Work & Thank You", "Speaker 2")
bullets(s, Inches(0.6), Inches(1.4), Inches(12.1), Inches(4.0), [
    ("Close the training gap (reference code hit 95.25% on our data).",0,False,DARK),
    ("Make the model sarcasm-aware.",0,False,DARK),
    ("Bring back fine-grained bully types.",0,False,DARK),
    ("Multilingual: Bangla + English + Hindi, with type.",0,True,GREEN),
], size=20, gap=12)
rect(s, Inches(2.5), Inches(5.6), Inches(8.3), Inches(1.1), HEADBLUE)
textbox(s, Inches(2.5), Inches(5.6), Inches(8.3), Inches(1.1), "Thank You  —  Questions?",
        size=28, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
footer(s, nxt())
set_notes(s, "[Speaker 2] Future work: close the training gap, handle sarcasm, bring back the fine-grained types, and extend to "
           "Bangla, English and Hindi together. Thank you — we're happy to take questions. ANIMATION: bullets, then the Thank-You bar.")

out="Thesis_Presentation.pptx"
prs.save(out)
print("saved", out, "slides:", len(prs.slides._sldIdLst))
