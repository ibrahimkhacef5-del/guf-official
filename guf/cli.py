"""CLI for guf (Git URL in Files)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .extractor import (
    extract_from_directory,
    extract_from_file,
    extract_urls,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="guf",
        description="guf = Git URL in Files. استخرج كل الروابط من ملف أو مجلد.",
    )
    parser.add_argument(
        "path",
        help="مسار ملف أو مجلد (استخدم '-' للقراءة من stdin)",
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        default=True,
        help="ابحث داخل المجلدات الفرعية (افتراضي: True)",
    )
    parser.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="لا تبحث داخل المجلدات الفرعية",
    )
    parser.add_argument(
        "-e", "--extensions",
        nargs="*",
        default=None,
        help="فلترة بامتدادات معينة مثل: .py .md",
    )
    parser.add_argument(
        "--only-git",
        action="store_true",
        help="اظهر فقط روابط Git",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="اطبع النتيجة بصيغة JSON",
    )
    parser.add_argument(
        "--show-hidden",
        action="store_true",
        help="لا تتجاهل الملفات المخفية",
    )
    return parser


def _is_git_url(url: str) -> bool:
    return (
        url.startswith("git@")
        or url.startswith("git://")
        or url.startswith("ssh://")
        or url.endswith(".git")
        or "github.com" in url
        or "gitlab.com" in url
        or "bitbucket.org" in url
    )


def _print_results(results: dict[str, list[str]], only_git: bool, as_json: bool) -> int:
    total = 0
    filtered: dict[str, list[str]] = {}

    for file, urls in results.items():
        if only_git:
            urls = [u for u in urls if _is_git_url(u)]
        if urls:
            filtered[file] = urls
            total += len(urls)

    if as_json:
        print(json.dumps(filtered, indent=2, ensure_ascii=False))
        return total

    if not filtered:
        print("لا توجد روابط مطابقة.", file=sys.stderr)
        return 0

    for file, urls in filtered.items():
        print(f"\n📄 {file}")
        for u in urls:
            print(f"   • {u}")

    print(f"\n✅ الإجمالي: {total} رابط في {len(filtered)} ملف", file=sys.stderr)
    return total


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    path = args.path

    try:
        if path == "-":
            text = sys.stdin.read()
            urls = extract_urls(text)
            results = {"<stdin>": urls} if urls else {}
        else:
            p = Path(path)
            if p.is_file():
                urls = extract_from_file(p)
                results = {str(p): urls} if urls else {}
            elif p.is_dir():
                results = extract_from_directory(
                    p,
                    recursive=args.recursive,
                    extensions=args.extensions,
                    skip_hidden=not args.show_hidden,
                )
            else:
                print(f"❌ المسار غير موجود: {p}", file=sys.stderr)
                return 2
    except Exception as e:
        print(f"❌ خطأ: {e}", file=sys.stderr)
        return 1

    count = _print_results(results, only_git=args.only_git, as_json=args.json)
    return 0 if count >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
