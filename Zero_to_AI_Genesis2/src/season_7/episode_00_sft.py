import numpy as np


def softmax(x):
    z = x - np.max(x, axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def build_data():
    pairs = [
        ("policy remote", "submit request portal"),
        ("policy pto", "submit request hr portal"),
        ("policy travel", "upload receipt expense portal"),
        ("policy insurance", "check benefits hr portal"),
    ]
    return pairs


def tokenize_dataset(pairs):
    vocab = sorted({tok for p, r in pairs for tok in (p + " " + r).split()})
    stoi = {w: i for i, w in enumerate(vocab)}
    itos = {i: w for w, i in stoi.items()}
    xs, ys = [], []
    for p, r in pairs:
        p_ids = [stoi[t] for t in p.split()]
        r_ids = [stoi[t] for t in r.split()]
        for i in range(len(r_ids)):
            ctx = p_ids + r_ids[:i]
            target = r_ids[i]
            xs.append(ctx)
            ys.append(target)
    return xs, np.array(ys), stoi, itos


def bow_vector(ids, vocab_size):
    v = np.zeros(vocab_size)
    for idx in ids:
        v[idx] += 1
    if v.sum() > 0:
        v /= v.sum()
    return v


def train_sft(xs, ys, vocab_size, epochs=500, lr=0.5):
    W = np.zeros((vocab_size, vocab_size))
    b = np.zeros(vocab_size)

    for _ in range(epochs):
        X = np.stack([bow_vector(x, vocab_size) for x in xs])
        logits = X @ W + b
        probs = softmax(logits)

        y_onehot = np.eye(vocab_size)[ys]
        grad = (probs - y_onehot) / len(xs)
        W -= lr * (X.T @ grad)
        b -= lr * grad.sum(axis=0)
    return W, b


def generate(prompt, W, b, stoi, itos, max_new_tokens=4):
    ctx = [stoi[t] for t in prompt.split() if t in stoi]
    out = []
    for _ in range(max_new_tokens):
        x = bow_vector(ctx, len(stoi))
        probs = softmax((x @ W + b)[None, :])[0]
        tok = int(np.argmax(probs))
        out.append(itos[tok])
        ctx.append(tok)
    return " ".join(out)


def main():
    pairs = build_data()
    xs, ys, stoi, itos = tokenize_dataset(pairs)
    W, b = train_sft(xs, ys, vocab_size=len(stoi), epochs=800, lr=0.35)

    prompt = "policy travel"
    response = generate(prompt, W, b, stoi, itos, max_new_tokens=4)

    print("\nSeason 7 / Ep 00 - SFT (from scratch toy)")
    print("Prompt:", prompt)
    print("Generated:", response)
    print("SFT objective: minimize token-level cross entropy")


if __name__ == "__main__":
    main()
