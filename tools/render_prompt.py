import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a prompt template with draft input.")
    parser.add_argument("-t", "--template", required=True)
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--must-keep", default="")
    parser.add_argument("--expand-points", default="")
    parser.add_argument("--outline", default="")
    args = parser.parse_args()

    template = Path(args.template).read_text(encoding="utf-8")
    draft = Path(args.input).read_text(encoding="utf-8")
    rendered = (
        template.replace("{{DRAFT_TEXT}}", draft)
        .replace("{{MUST_KEEP}}", args.must_keep)
        .replace("{{EXPAND_POINTS}}", args.expand_points)
        .replace("{{OUTLINE_TEXT}}", args.outline)
    )
    Path(args.output).write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
