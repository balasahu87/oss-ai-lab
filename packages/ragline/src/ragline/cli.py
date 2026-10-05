from __future__ import annotations

import argparse
from pathlib import Path

from ragline.index import build_index, load_index, save_index
from ragline.retrieve import pack_citations, retrieve


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="ragline", description="Hybrid RAG CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_index = sub.add_parser("index", help="Index a directory of text/markdown files")
    p_index.add_argument("path", type=Path)
    p_index.add_argument("--out", type=Path, default=Path(".ragline_index"))
    p_index.add_argument("--glob", default="**/*.{md,txt}")

    p_ask = sub.add_parser("ask", help="Retrieve grounded context for a question")
    p_ask.add_argument("question")
    p_ask.add_argument("--index", type=Path, default=Path(".ragline_index"))
    p_ask.add_argument("--top-k", type=int, default=5)

    args = parser.parse_args(argv)

    if args.cmd == "index":
        root: Path = args.path
        files = sorted(
            [
                p
                for p in root.rglob("*")
                if p.is_file() and p.suffix.lower() in {".md", ".txt", ".rst"}
            ]
        )
        if not files:
            raise SystemExit(f"No documents under {root}")
        idx = build_index(files)
        save_index(idx, args.out)
        print(f"Indexed {len(idx.chunks)} chunks from {len(files)} files → {args.out}")
        return

    if args.cmd == "ask":
        idx = load_index(args.index)
        hits = retrieve(idx, args.question, top_k=args.top_k)
        print(pack_citations(hits))
        print("\n---")
        print(f"top_k={len(hits)} sources={[h.chunk.source for h in hits]}")


if __name__ == "__main__":
    main()
