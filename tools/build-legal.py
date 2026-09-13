#!/usr/bin/env python3
"""Render legal/*.md to privacy.html and terms.html.

Wording is never touched: the converter only maps Markdown structure to
HTML. [FILL IN ...] and [LAWYER REVIEW ...] markers are wrapped in a muted
span so outstanding items are visible on the page until they are stripped.
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = re.compile(r"\[(FILL IN|LAWYER REVIEW)[^\]]*\]")

def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\b([\w.+-]+@joinblacklink\.com)\b", r'<a href="mailto:\1">\1</a>', out)
    out = re.sub(r"\b(ico\.org\.uk)\b", r'<a href="https://\1" rel="noopener">\1</a>', out)
    out = MARK.sub(lambda m: f'<span class="marker">{m.group(0)}</span>', out)
    return out

def render(md: str) -> tuple[str, str, str]:
    lines = md.splitlines()
    body, i, title, meta = [], 0, "", ""
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# "):
            title = ln[2:].strip(); i += 1; continue
        if ln.startswith("**Version") and not meta:
            meta = inline(ln.strip("*").strip()); i += 1; continue
        if ln.startswith("## "):
            body.append(f"<h2>{inline(ln[3:].strip())}</h2>"); i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"-+", c) for c in cells):
                    rows.append(cells)
                i += 1
            head, *rest = rows
            t = ["<div class=\"table-wrap\"><table><thead><tr>"]
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in rest:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            body.append("".join(t)); continue
        m_ul = re.match(r"^- (.*)", ln); m_ol = re.match(r"^\d+\. (.*)", ln)
        if m_ul or m_ol:
            tag = "ul" if m_ul else "ol"; items = []
            pat = r"^- (.*)" if m_ul else r"^\d+\. (.*)"
            while i < len(lines) and re.match(pat, lines[i]):
                items.append(f"<li>{inline(re.match(pat, lines[i]).group(1))}</li>"); i += 1
            body.append(f"<{tag}>" + "".join(items) + f"</{tag}>"); continue
        if ln.strip() == "":
            i += 1; continue
        # paragraph: consecutive non-blank lines; a bare line break in the
        # source (contact blocks) becomes <br> so the layout survives
        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "- ")) and not re.match(r"^\d+\. ", lines[i]):
            para.append(inline(lines[i].strip())); i += 1
        body.append("<p>" + "<br>".join(para) + "</p>")
    return title, meta, "\n".join(body)

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · Blacklink</title>
  <meta name="description" content="{title} for the Blacklink app and joinblacklink.com.">
  <link rel="icon" href="favicon.png">
  <link rel="stylesheet" href="fonts/fonts.css">
  <style>
    :root {{
      --bg: #000000; --surface: #141414; --border: #262626; --border-strong: #3f3f3f;
      --text: #ffffff; --text-secondary: #a3a3a3; --text-muted: #767676;
      --font-display: "Archivo Black", "Arial Black", Impact, sans-serif;
      --font-body: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    }}
    html, body {{ margin: 0; background: var(--bg); color: var(--text); }}
    body {{ font-family: var(--font-body); font-size: 17px; line-height: 1.7; -webkit-font-smoothing: antialiased; }}
    .wrap {{ max-width: 680px; margin: 0 auto; padding: 40px 20px 80px; }}
    @media (min-width: 720px) {{ .wrap {{ padding: 72px 24px 120px; }} }}
    .top {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 40px; }}
    .brand {{ font-family: var(--font-display); font-size: 14px; letter-spacing: 3px; text-transform: uppercase; color: var(--text); text-decoration: none; }}
    .other {{ color: var(--text-muted); font-size: 13px; text-decoration: underline; text-underline-offset: 3px; }}
    .other:hover {{ color: var(--text); }}
    h1 {{ font-family: var(--font-display); font-size: 30px; line-height: 1.15; letter-spacing: 1px; text-transform: uppercase; margin: 0 0 10px; }}
    @media (min-width: 720px) {{ h1 {{ font-size: 36px; }} }}
    .meta {{ color: var(--text-secondary); font-size: 14px; margin: 0 0 36px; padding-bottom: 28px; border-bottom: 1px solid var(--border); }}
    h2 {{ font-family: var(--font-display); font-size: 17px; letter-spacing: 1.5px; text-transform: uppercase; margin: 44px 0 12px; line-height: 1.3; }}
    p, li {{ color: var(--text-secondary); }}
    p {{ margin: 0 0 18px; }}
    strong {{ color: var(--text); font-weight: 600; }}
    ul, ol {{ padding-left: 22px; margin: 0 0 20px; }}
    li {{ margin: 0 0 8px; }}
    li::marker {{ color: var(--text-muted); }}
    a {{ color: var(--text); text-decoration: underline; text-underline-offset: 3px; text-decoration-color: var(--border-strong); }}
    a:hover {{ text-decoration-color: var(--text); }}
    .table-wrap {{ overflow-x: auto; margin: 0 0 24px; border: 1px solid var(--border); border-radius: 8px; }}
    table {{ border-collapse: collapse; width: 100%; min-width: 560px; font-size: 15px; line-height: 1.5; }}
    th, td {{ text-align: left; vertical-align: top; padding: 12px 14px; border-bottom: 1px solid var(--border); }}
    th {{ color: var(--text); font-weight: 600; background: var(--surface); }}
    tr:last-child td {{ border-bottom: 0; }}
    /* outstanding items: visible, muted, easy to find */
    .marker {{ color: var(--text-muted); background: var(--surface); border: 1px dashed var(--border-strong); border-radius: 4px; padding: 0 5px; font-size: 0.92em; }}
    footer {{ margin-top: 72px; padding-top: 24px; border-top: 1px solid var(--border); color: var(--text-muted); font-size: 13px; line-height: 1.7; }}
    footer a {{ color: var(--text-secondary); }}
  </style>
</head>
<body>
  <main class="wrap">
    <nav class="top"><a class="brand" href="/">Blacklink</a><a class="other" href="{other_href}">{other_label}</a></nav>
    <h1>{title}</h1>
    <p class="meta">{meta}</p>
{body}
    <footer>
      © 2026 Blacklink · Operated by Kai O’Donnell, trading as Blacklink · <a href="mailto:hello@joinblacklink.com">hello@joinblacklink.com</a><br>
      <a href="/">Home</a> · <a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms of Use</a>
    </footer>
  </main>
</body>
</html>
"""

PAGES = {
    "legal/blacklink-privacy-policy.md": ("privacy.html", "/terms", "Terms of Use"),
    "legal/blacklink-terms-of-use.md": ("terms.html", "/privacy", "Privacy Policy"),
}
for src, (dst, other_href, other_label) in PAGES.items():
    title, meta, body = render((ROOT / src).read_text(encoding="utf-8"))
    (ROOT / dst).write_text(TEMPLATE.format(title=title, meta=meta, body=body, other_href=other_href, other_label=other_label), encoding="utf-8")
    print(f"{dst}: {len(body)} chars, markers={len(MARK.findall((ROOT / src).read_text()))}")
