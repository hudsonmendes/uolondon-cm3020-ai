from argparse import ArgumentParser
from .models.markov import MarkovNLG


def parse_args():
    ap = ArgumentParser()
    ap.add_argument("--model", type=str, required=False, default="markov", help="which NLG?")
    ap.add_argument("--tokens", type=int, required=False, default=20, help="How many words?")
    ap.add_argument("--context", type=str, required=False, help="How do you want to start?")
    return ap.parse_args()


def get_model(name: str):
    assert name
    name = name.lower().strip()
    if name == "markov":
        return MarkovNLG()
    raise Exception(f"Model Unknown: {name}")


def read_dataset(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as fh:
        return fh.read()


if __name__ == "__main__":
    args = parse_args()
    model = get_model(args.model)
    model.train(read_dataset("./data/sonets.txt"))
    print(model.generate(n=args.tokens, context=args.context))
