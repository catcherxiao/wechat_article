import argparse
from pathlib import Path
from typing import Optional


def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def render_inline(s: str) -> str:
    out = []
    i = 0
    strong = False
    while i < len(s):
        if s.startswith("**", i):
            strong = not strong
            out.append(
                "</strong>"
                if not strong
                else '<strong style="font-weight: 800;">'
            )
            i += 2
            continue
        out.append(escape_html(s[i]))
        i += 1
    if strong:
        out.append("</strong>")
    return "".join(out)


def convert(md: str, title_override: Optional[str] = None) -> str:
    lines = md.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    title = None
    blocks: list[tuple[str, object]] = []
    footnotes: list[str] = []

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        if not line:
            i += 1
            continue

        if line.startswith("[^") and "]: " in line:
            footnotes.append(line)
            i += 1
            continue

        if line.startswith("# "):
            if title is None:
                title = line[2:].strip()
                i += 1
                continue
            blocks.append(("h2", line[2:].strip()))
            i += 1
            continue

        if line.startswith("## "):
            blocks.append(("h2", line[3:].strip()))
            i += 1
            continue

        if line == "---":
            blocks.append(("hr", None))
            i += 1
            continue

        if line.startswith("> "):
            blocks.append(("quote", line[2:].strip()))
            i += 1
            continue

        if line.startswith("- "):
            items = []
            while i < len(lines):
                l2 = lines[i].strip()
                if not l2.startswith("- "):
                    break
                items.append(l2[2:].strip())
                i += 1
            blocks.append(("ul", items))
            continue

        blocks.append(("p", line))
        i += 1

    doc_title = title_override or title or "公众号文章"

    parts = [
        "<!doctype html>",
        '<html lang="zh-CN">',
        "  <head>",
        '    <meta charset="utf-8" />',
        '    <meta name="viewport" content="width=device-width, initial-scale=1" />',
        f"    <title>{escape_html(doc_title)}</title>",
        "  </head>",
        "  <body>",
        '    <section style="max-width: 720px; margin: 0 auto; padding: 8px 10px; font-family: -apple-system, BlinkMacSystemFont, \'PingFang SC\', \'Hiragino Sans GB\', \'Microsoft YaHei\', Arial, sans-serif; font-size: 17px; line-height: 1.85; color: #1f2329;">',
        '      <p style="margin: 0 0 14px; font-size: 13px; line-height: 1.65; color: #8a8f98;">声明：本文仅代表个人观点，不构成投资建议；转载/引用请注明出处。<br />风险提示：市场有风险，投资需谨慎。</p>',
    ]

    if title:
        parts.append(
            '      <h1 style="margin: 0 0 14px; font-size: 26px; line-height: 1.35; font-weight: 800; letter-spacing: 0.2px;">'
            + render_inline(title)
            + "</h1>"
        )

    for kind, payload in blocks:
        if kind == "p":
            parts.append(f'      <p style="margin: 0 0 14px;">{render_inline(str(payload))}</p>')
        elif kind == "h2":
            parts.append(
                '      <h2 style="margin: 0 0 10px; font-size: 20px; line-height: 1.45; font-weight: 800;">'
                + render_inline(str(payload))
                + "</h2>"
            )
        elif kind == "quote":
            parts.append(
                '      <blockquote style="margin: 12px 0; padding: 10px 12px; background: #f7f8fa; border-left: 4px solid #d0021b;">'
            )
            parts.append(f'        <p style="margin: 0;">{render_inline(str(payload))}</p>')
            parts.append("      </blockquote>")
        elif kind == "ul":
            parts.append('      <ul style="margin: 0 0 14px; padding: 0 0 0 22px;">')
            for item in payload:  # type: ignore[assignment]
                parts.append(f'        <li style="margin: 6px 0;">{render_inline(str(item))}</li>')
            parts.append("      </ul>")
        elif kind == "hr":
            parts.append('      <hr style="border: 0; border-top: 1px solid #eceef1; margin: 18px 0;" />')

    if footnotes:
        parts.append('      <hr style="border: 0; border-top: 1px solid #eceef1; margin: 18px 0;" />')
        parts.append('      <p style="margin: 0 0 10px; font-size: 13px; line-height: 1.65; color: #8a8f98;">参考</p>')
        parts.append('      <ul style="margin: 0; padding: 0 0 0 22px; font-size: 13px; line-height: 1.65; color: #8a8f98;">')
        for fn in footnotes:
            parts.append(f'        <li style="margin: 6px 0;">{render_inline(fn)}</li>')
        parts.append("      </ul>")

    parts.append('      <p style="margin: 18px 0 0; font-size: 13px; line-height: 1.65; color: #8a8f98;"><em>风险提示：本文仅代表个人观点，不构成投资建议。市场有风险，投资需谨慎。</em></p>')
    parts.append("    </section>")
    parts.append("  </body>")
    parts.append("</html>")
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--title", default=None)
    args = parser.parse_args()

    md = Path(args.input).read_text(encoding="utf-8")
    html = convert(md, title_override=args.title)
    Path(args.output).write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
