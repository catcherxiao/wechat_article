import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the revision prompt template.")
    parser.add_argument("-t", "--template", default="prompts/wechat_revision_v1.md")
    parser.add_argument("-f", "--full-text", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--target-text", default=None)
    parser.add_argument("--request", required=True)
    parser.add_argument(
        "--mode",
        choices=["full", "selection"],
        default="full",
        help="full rewrites the whole article; selection rewrites only target text.",
    )
    args = parser.parse_args()

    template = Path(args.template).read_text(encoding="utf-8")
    full_text = Path(args.full_text).read_text(encoding="utf-8")
    target_text = (
        Path(args.target_text).read_text(encoding="utf-8")
        if args.target_text
        else full_text
    )
    mode_text = (
        "只修改用户选中的局部段落。只输出修改后的选中段落，用于替换原选区。"
        if args.mode == "selection"
        else "修改整篇文章。只输出修改后的完整文章。"
    )

    rendered = (
        template.replace("{{REVISION_MODE}}", mode_text)
        .replace("{{FULL_TEXT}}", full_text)
        .replace("{{TARGET_TEXT}}", target_text)
        .replace("{{REVISION_REQUEST}}", args.request)
    )
    Path(args.output).write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
