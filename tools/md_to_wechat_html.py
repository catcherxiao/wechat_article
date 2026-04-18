import argparse
from pathlib import Path
from typing import Optional


STYLE_PRESETS = {
    "rational_finance": {
        "strong_color": "#c7372f",
        "section": "max-width: 720px; margin: 0 auto; padding: 8px 16px 36px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif; font-size: 17px; line-height: 1.9; color: #202124; background:#ffffff;",
        "h1": "margin: 0 0 18px; font-size: 28px; line-height: 1.42; font-weight: 800; letter-spacing: 0.2px; color: #202124;",
        "p": "margin: 0 0 16px; font-size: 17px; line-height: 1.9; color: #202124; letter-spacing: 0.2px;",
        "risk": "margin: 22px 0 0; padding: 10px 12px; font-size: 13px; line-height: 1.75; color: #8a9199; background: #fafafa; border-left: 3px solid #e5e7eb;",
        "h2": "display: inline-block; margin: 18px 0 16px; padding: 6px 10px; font-size: 17px; line-height: 1.7; font-weight: 800; color: #b42318; background: #fff1f1; border-radius: 2px;",
        "blockquote": "margin: 20px 0; padding: 12px 14px; background: #f7f8fa; border-left: 3px solid #d14b4b; border-radius: 2px;",
        "quote_p": "margin: 0; font-size: 16px; line-height: 1.85; color: #4b5563;",
        "ul": "margin: 0 0 18px; padding: 0 0 0 22px;",
        "li": "margin: 8px 0; font-size: 16px; line-height: 1.9; color: #202124;",
        "hr": "border: 0; border-top: 1px solid #eceef1; margin: 28px 0;",
        "footnote_label": "margin: 0 0 10px; font-size: 13px; line-height: 1.7; color: #8a9199;",
        "footnote_ul": "margin: 0; padding: 0 0 0 20px; font-size: 13px; line-height: 1.7; color: #8a9199;",
    },
    "opinion_commentary": {
        "strong_color": "#b42318",
        "section": "max-width: 700px; margin: 0 auto; padding: 10px 16px 36px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif; font-size: 17px; line-height: 1.86; color: #1f2937; background:#ffffff;",
        "h1": "margin: 0 0 18px; font-size: 29px; line-height: 1.4; font-weight: 800; letter-spacing: 0.1px; color: #111827;",
        "p": "margin: 0 0 15px; font-size: 17px; line-height: 1.86; color: #1f2937; letter-spacing: 0.15px;",
        "risk": "margin: 22px 0 0; padding: 10px 12px; font-size: 13px; line-height: 1.75; color: #8a9199; background: #fbfbfb; border-left: 3px solid #ead1d1;",
        "h2": "display: inline-block; margin: 20px 0 16px; padding: 6px 11px; font-size: 17px; line-height: 1.7; font-weight: 800; color: #9f1239; background: #fff4f6; border-radius: 2px;",
        "blockquote": "margin: 22px 0; padding: 12px 14px; background: #faf7f7; border-left: 3px solid #c2410c; border-radius: 2px;",
        "quote_p": "margin: 0; font-size: 16px; line-height: 1.82; color: #4b5563;",
        "ul": "margin: 0 0 18px; padding: 0 0 0 22px;",
        "li": "margin: 8px 0; font-size: 16px; line-height: 1.85; color: #1f2937;",
        "hr": "border: 0; border-top: 1px solid #eee7e7; margin: 28px 0;",
        "footnote_label": "margin: 0 0 10px; font-size: 13px; line-height: 1.7; color: #8a9199;",
        "footnote_ul": "margin: 0; padding: 0 0 0 20px; font-size: 13px; line-height: 1.7; color: #8a9199;",
    },
    "deep_feature": {
        "strong_color": "#b9382f",
        "section": "max-width: 760px; margin: 0 auto; padding: 12px 18px 42px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif; font-size: 17px; line-height: 1.96; color: #202124; background:#ffffff;",
        "h1": "margin: 0 0 22px; font-size: 28px; line-height: 1.48; font-weight: 800; letter-spacing: 0.15px; color: #202124;",
        "p": "margin: 0 0 18px; font-size: 17px; line-height: 1.96; color: #202124; letter-spacing: 0.18px;",
        "risk": "margin: 24px 0 0; padding: 10px 12px; font-size: 13px; line-height: 1.8; color: #8a9199; background: #fafafa; border-left: 3px solid #ececec;",
        "h2": "display: inline-block; margin: 22px 0 18px; padding: 6px 10px; font-size: 17px; line-height: 1.72; font-weight: 800; color: #8f2d23; background: #fff7f5; border-radius: 2px;",
        "blockquote": "margin: 22px 0; padding: 13px 14px; background: #f8f8f8; border-left: 3px solid #d6b4b0; border-radius: 2px;",
        "quote_p": "margin: 0; font-size: 16px; line-height: 1.9; color: #52525b;",
        "ul": "margin: 0 0 20px; padding: 0 0 0 22px;",
        "li": "margin: 9px 0; font-size: 16px; line-height: 1.92; color: #202124;",
        "hr": "border: 0; border-top: 1px solid #efefef; margin: 32px 0;",
        "footnote_label": "margin: 0 0 10px; font-size: 13px; line-height: 1.75; color: #8a9199;",
        "footnote_ul": "margin: 0; padding: 0 0 0 20px; font-size: 13px; line-height: 1.75; color: #8a9199;",
    },
}


def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def render_inline(s: str, strong_color: str) -> str:
    out = []
    i = 0
    strong = False
    while i < len(s):
        if s.startswith("**", i):
            strong = not strong
            out.append(
                "</strong>"
                if not strong
                else f'<strong style="font-weight: 800; color: {strong_color};">'
            )
            i += 2
            continue
        out.append(escape_html(s[i]))
        i += 1
    if strong:
        out.append("</strong>")
    return "".join(out)


def convert(
    md: str, title_override: Optional[str] = None, preset: str = "rational_finance"
) -> str:
    styles = STYLE_PRESETS.get(preset, STYLE_PRESETS["rational_finance"])
    lines = md.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    title = None
    blocks: list[tuple[str, object]] = []
    footnotes: list[str] = []
    has_risk_note = any(
        token in md for token in ["风险提示", "不构成投资建议", "市场有风险"]
    )

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
        '  <body style="margin:0; padding:0; background:#ffffff;">',
        f'    <section style="{styles["section"]}">',
    ]

    if title:
        parts.append(
            f'      <h1 style="{styles["h1"]}">'
            + render_inline(title, styles["strong_color"])
            + "</h1>"
        )

    for kind, payload in blocks:
        if kind == "p":
            text = str(payload)
            if any(token in text for token in ["风险提示", "不构成投资建议", "市场有风险"]):
                parts.append(
                    f'      <p style="{styles["risk"]}">'
                    + render_inline(text, styles["strong_color"])
                    + "</p>"
                )
            else:
                parts.append(
                    f'      <p style="{styles["p"]}">'
                    + render_inline(text, styles["strong_color"])
                    + "</p>"
                )
        elif kind == "h2":
            parts.append(
                f'      <h2 style="{styles["h2"]}">'
                + render_inline(str(payload), styles["strong_color"])
                + "</h2>"
            )
        elif kind == "quote":
            parts.append(f'      <blockquote style="{styles["blockquote"]}">')
            parts.append(
                f'        <p style="{styles["quote_p"]}">'
                + render_inline(str(payload), styles["strong_color"])
                + "</p>"
            )
            parts.append("      </blockquote>")
        elif kind == "ul":
            parts.append(f'      <ul style="{styles["ul"]}">')
            for item in payload:  # type: ignore[assignment]
                parts.append(
                    f'        <li style="{styles["li"]}">'
                    + render_inline(str(item), styles["strong_color"])
                    + "</li>"
                )
            parts.append("      </ul>")
        elif kind == "hr":
            parts.append(f'      <hr style="{styles["hr"]}" />')

    if footnotes:
        parts.append(f'      <hr style="{styles["hr"]}" />')
        parts.append(f'      <p style="{styles["footnote_label"]}">参考</p>')
        parts.append(f'      <ul style="{styles["footnote_ul"]}">')
        for fn in footnotes:
            parts.append(
                f'        <li style="margin: 6px 0;">'
                + render_inline(fn, styles["strong_color"])
                + "</li>"
            )
        parts.append("      </ul>")

    if not has_risk_note:
        parts.append(
            f'      <p style="{styles["risk"]}">'
            "风险提示：本文仅代表个人观点，不构成投资建议。市场有风险，投资需谨慎。"
            "</p>"
        )
    parts.append("    </section>")
    parts.append("  </body>")
    parts.append("</html>")
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--title", default=None)
    parser.add_argument(
        "--preset",
        default="rational_finance",
        choices=sorted(STYLE_PRESETS.keys()),
        help="排版风格预设",
    )
    args = parser.parse_args()

    md = Path(args.input).read_text(encoding="utf-8")
    html = convert(md, title_override=args.title, preset=args.preset)
    Path(args.output).write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
