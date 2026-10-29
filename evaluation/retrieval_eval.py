"""Measure retrieval Hit@5 on clinician-reviewed JSONL cases."""
import argparse
import json
import re
from pathlib import Path

from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]


def read_docs():
    result = []
    for path in (ROOT / "data" / "markdown").rglob("*.md"):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        headings = re.split(r"(?m)^(#{1,3})\s+(.+?)\s*$", content)
        for i in range(1, len(headings), 3):
            title = headings[i + 1]
            text = headings[i + 2] if i + 2 < len(headings) else ""
            if len(text.strip()) > 80:
                result.append((path.relative_to(ROOT / "data" / "markdown").as_posix(), title, f"{title}\n{text[:1800]}"))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    parser.add_argument("--model", default="intfloat/multilingual-e5-base")
    args = parser.parse_args()
    cases = [json.loads(line) for line in Path(args.cases).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not cases:
        raise SystemExit("Không có ca đánh giá trong JSONL.")
    docs = read_docs()
    model = SentenceTransformer(args.model)
    vectors = model.encode(["passage: " + d[2] for d in docs], normalize_embeddings=True, show_progress_bar=True)
    hits = 0
    for case in cases:
        q = model.encode(["query: " + case["query"]], normalize_embeddings=True)[0]
        scores = vectors @ q
        top = sorted(range(len(docs)), key=lambda i: float(scores[i]), reverse=True)[:5]
        src = case["relevant_source"].replace("\\", "/")
        sec = case.get("relevant_section", "").casefold()
        found = any(docs[i][0] == src and (not sec or sec in docs[i][1].casefold()) for i in top)
        hits += int(found)
    print(json.dumps({"model": args.model, "cases": len(cases), "hit_at_5": round(hits / len(cases), 4), "hits": hits}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
