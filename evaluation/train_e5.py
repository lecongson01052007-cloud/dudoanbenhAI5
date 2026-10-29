"""Fine-tune multilingual-e5 with verified query/positive pairs (run on Colab/GPU)."""
import argparse
import json
from pathlib import Path

from sentence_transformers import InputExample, SentenceTransformer, losses
from torch.utils.data import DataLoader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--base-model", default="intfloat/multilingual-e5-base")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()
    rows = [json.loads(line) for line in Path(args.train).read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) < 10:
        raise SystemExit("Cần tối thiểu 10 cặp câu hỏi/đoạn nguồn đã được rà soát để bắt đầu thử nghiệm.")
    examples = [InputExample(texts=["query: " + row["query"], "passage: " + row["positive_text"]]) for row in rows]
    model = SentenceTransformer(args.base_model)
    loader = DataLoader(examples, shuffle=True, batch_size=args.batch_size)
    loss = losses.MultipleNegativesRankingLoss(model)
    model.fit(train_objectives=[(loader, loss)], epochs=args.epochs, warmup_steps=max(1, int(len(loader) * args.epochs * 0.1)), output_path=args.output, show_progress_bar=True)
    print(f"Đã lưu mô hình thử nghiệm tại {args.output}. Đánh giá bằng tập test độc lập trước khi báo cáo.")


if __name__ == "__main__":
    main()
