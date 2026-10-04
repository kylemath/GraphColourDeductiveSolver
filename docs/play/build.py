#!/usr/bin/env python3
"""Render docs/story/the-long-table.md as the styled play page docs/play/index.html.

Run from anywhere:  python3 docs/play/build.py
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "story" / "the-long-table.md"
OUTPUT = HERE / "index.html"

CAST = {"BUCKY": "bucky", "KAMPER": "kamper", "APPKEN": "appken", "THEO": "theo", "ROSA": "rosa"}
CAST_RE = re.compile(r"\b(" + "|".join(CAST) + r")\b")
SPEECH_RE = re.compile(r"^\*\*([A-Z]+)\*\*:\s*(.*)$")
THOUGHT_RE = re.compile(r"^>\s*\*([A-Za-z]+), inside:\*\s*(.*)$")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def inline(text, cast_caps=False):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(\([^*]+?\))\*", r'<span class="dir">\1</span>', text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    if cast_caps:
        text = CAST_RE.sub(lambda m: f'<span class="cue c-{CAST[m.group(1)]}">{m.group(1).title()}</span>', text)
    return text


def render(md):
    lines = md.split("\n")
    out, toc = [], []
    section = ""
    in_title = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            body = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            out.append(f'<figure class="napkin"><pre>{html.escape(chr(10).join(body))}</pre></figure>')
            continue
        if line.startswith("# "):
            out.append(f'<header class="title"><p class="eyebrow">Four Colour Theorem</p><h1>{inline(line[2:])}</h1>')
            in_title = True
            i += 1
            continue
        if line.startswith("## "):
            section = line[3:]
            sid = slug(section)
            toc.append((sid, section))
            out.append(f'<h2 id="{sid}">{inline(section)}</h2>')
            i += 1
            continue
        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
            i += 1
            continue
        if line.strip() == "---":
            if in_title:
                out.append("</header>")
                in_title = False
            out.append('<hr class="break" aria-hidden="true">')
            i += 1
            continue
        m = THOUGHT_RE.match(line)
        if m:
            who = m.group(1).upper()
            out.append(
                f'<aside class="thought c-{CAST.get(who, "theo")}"><span class="who">{m.group(1)}, inside</span>{inline(m.group(2))}</aside>'
            )
            i += 1
            continue
        m = SPEECH_RE.match(line)
        if m and m.group(1) in CAST:
            who, rest = m.group(1), m.group(2)
            if section == "Dramatis Personae":
                out.append(f'<p class="persona c-{CAST[who]}"><strong>{who.title()}</strong> {inline(rest)}</p>')
            else:
                out.append(
                    f'<div class="line c-{CAST[who]}"><span class="speaker">{who.title()}</span><p>{inline(rest)}</p></div>'
                )
            i += 1
            continue
        if in_title and line.startswith("*"):
            out.append(f'<p class="subtitle">{inline(line.strip()[1:-1])}</p>')
            i += 1
            continue
        if line.startswith("*") and line.rstrip().endswith("*") and not line.startswith("**"):
            out.append(f'<p class="stage">{inline(line.strip()[1:-1], cast_caps=True)}</p>')
            i += 1
            continue
        out.append(f"<p>{inline(line)}</p>")
        i += 1
    return "\n".join(out), toc


def main():
    body, toc = render(SOURCE.read_text())
    toc_html = "\n".join(f'<li><a href="#{sid}">{html.escape(name)}</a></li>' for sid, name in toc)
    nav = (
        '<nav class="toc" aria-label="Scenes"><strong>Scenes</strong><ol>\n'
        + toc_html
        + '\n</ol><span class="source">Plain-text script: <a href="../story/the-long-table.md">the-long-table.md</a></span></nav>'
    )
    body = body.replace("</header>", "</header>\n" + nav, 1)
    page = TEMPLATE.replace("{{BODY}}", body)
    OUTPUT.write_text(page)
    print(f"wrote {OUTPUT.relative_to(HERE.parent.parent)}")


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Long Table</title>
  <meta name="description" content="A play in one long night: three colleagues piece together rumours of a structural Four Colour proof and brainstorm the last gate until dawn.">
  <style>
    :root {
      --bg: #0d1117;
      --raised: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --dim: #b1bac4;
      --faint: #7d8590;
      --bucky: #58a6ff;
      --kamper: #3fb950;
      --appken: #d29922;
      --theo: #bc8cff;
      --rosa: #f85149;
      --napkin: #f3ecdc;
      --napkin-ink: #2b2a27;
      --serif: "Iowan Old Style", Palatino, "Palatino Linotype", Georgia, serif;
      color-scheme: dark;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: var(--serif);
      font-size: 1.08rem;
      line-height: 1.65;
    }
    .script { max-width: 46rem; margin: 0 auto; padding: 3.5rem 1rem 4rem; }
    .title { text-align: center; margin-bottom: 1.5rem; }
    .eyebrow {
      margin: 0 0 0.6rem;
      color: var(--theo);
      font: 650 0.8rem/1.2 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    h1 { margin: 0 0 0.4rem; font-size: clamp(2.2rem, 6vw, 3.2rem); line-height: 1.1; letter-spacing: -0.02em; }
    .subtitle { margin: 0; color: var(--dim); font-style: italic; }
    .toc {
      margin: 0 0 2rem;
      padding: 1rem 1.25rem;
      background: var(--raised);
      border: 1px solid var(--border);
      border-radius: 10px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      font-size: 0.9rem;
    }
    .toc strong { display: block; margin-bottom: 0.4rem; color: var(--faint); font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; font-size: 0.75rem; }
    .toc ol { margin: 0; padding-left: 1.2rem; columns: 2; column-gap: 2rem; }
    .toc a { color: var(--dim); text-decoration: none; }
    .toc a:hover { color: var(--text); }
    .toc .source { display: block; margin-top: 0.6rem; color: var(--faint); }
    .toc .source a { color: var(--bucky); }
    h2 {
      margin: 3rem 0 1.25rem;
      padding-bottom: 0.4rem;
      border-bottom: 1px solid var(--border);
      font-size: 1.55rem;
      letter-spacing: -0.01em;
    }
    h3 { margin: 2.25rem 0 1rem; color: var(--dim); font-size: 1.15rem; font-style: italic; font-weight: 500; }
    p { margin: 0 0 1rem; }
    hr.break { border: 0; height: 10px; margin: 2.5rem auto; width: 64px;
      background: linear-gradient(90deg, var(--rosa) 0 25%, var(--bucky) 25% 50%, var(--kamper) 50% 75%, var(--appken) 75%);
      border-radius: 2px; opacity: 0.75; }
    .persona { padding-left: 0.9rem; border-left: 3px solid var(--who, var(--border)); color: var(--dim); }
    .persona strong { color: var(--who); font-variant: small-caps; letter-spacing: 0.04em; font-size: 1.1em; }
    .stage { margin: 1.25rem 0 1.25rem 1.5rem; color: var(--dim); font-style: italic; }
    .stage em { font-style: normal; }
    .cue { font-style: normal; font-variant: small-caps; letter-spacing: 0.04em; color: var(--who); }
    .line { display: grid; grid-template-columns: 6.5rem 1fr; gap: 0 1rem; margin: 0 0 0.85rem; }
    .speaker {
      padding-top: 0.12rem;
      color: var(--who);
      font-variant: small-caps;
      font-weight: 650;
      letter-spacing: 0.05em;
      text-align: right;
    }
    .line p { margin: 0; }
    .dir { color: var(--faint); font-style: italic; }
    .thought {
      margin: 1rem 0 1.25rem 1.5rem;
      padding: 0.7rem 1rem;
      background: color-mix(in srgb, var(--who) 8%, var(--raised));
      border-left: 3px solid var(--who);
      border-radius: 0 8px 8px 0;
      color: var(--dim);
      font-style: italic;
    }
    .thought .who {
      display: block;
      margin-bottom: 0.2rem;
      color: var(--who);
      font: 600 0.72rem/1.2 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-style: normal;
    }
    .napkin {
      margin: 1.5rem auto;
      max-width: 40rem;
      padding: 1.1rem 1.25rem;
      background: var(--napkin);
      color: var(--napkin-ink);
      border-radius: 3px;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
      transform: rotate(-0.6deg);
      overflow-x: auto;
    }
    .napkin:nth-of-type(even) { transform: rotate(0.5deg); }
    .napkin pre { margin: 0; font: 0.86rem/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    code { font: 0.9em ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; color: var(--text); background: var(--raised); padding: 0.05em 0.3em; border-radius: 4px; }
    a { color: var(--bucky); }
    .c-bucky { --who: var(--bucky); }
    .c-kamper { --who: var(--kamper); }
    .c-appken { --who: var(--appken); }
    .c-theo { --who: var(--theo); }
    .c-rosa { --who: var(--rosa); }
    @media (max-width: 640px) {
      body { font-size: 1rem; }
      .script { padding-top: 2.25rem; }
      .toc ol { columns: 1; }
      .line { grid-template-columns: 1fr; }
      .speaker { text-align: left; }
      .stage, .thought { margin-left: 0.5rem; }
    }
  </style>
</head>
<body>
  <article class="script">
{{BODY}}
  </article>
  <script>
    // Embedded with auto-height on the project page: scroll the parent, not this frame.
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener('click', function (event) {
        var target = document.querySelector(link.getAttribute('href'));
        var frame = null;
        try { frame = window.frameElement; } catch (err) {}
        if (!target || !frame) return;
        event.preventDefault();
        var top = window.parent.scrollY + frame.getBoundingClientRect().top + target.getBoundingClientRect().top - 72;
        window.parent.scrollTo({ top: top, behavior: 'smooth' });
      });
    });
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
