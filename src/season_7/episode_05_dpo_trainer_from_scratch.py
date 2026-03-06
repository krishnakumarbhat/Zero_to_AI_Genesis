import numpy as np


def softmax(x):
    z = x - np.max(x)
    e = np.exp(z)
    return e / e.sum()


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def build_preference_data():
    return [
        ("policy remote", "submit request portal", "ignore manager email"),
        ("policy pto", "submit request hr portal", "skip approval process"),
        ("policy travel", "upload receipt expense portal", "send random invoice"),
        ("policy insurance", "check benefits hr portal", "post details public"),
        ("policy equipment", "request stipend through portal", "buy anything no receipt"),
    ]


def build_vocab(prefs):
    tokens = set()
    for p, w, l in prefs:
        tokens.update((p + " " + w + " " + l).split())
    vocab = sorted(tokens)
    stoi = {w: i for i, w in enumerate(vocab)}
    itos = {i: w for w, i in stoi.items()}
    return stoi, itos


def ids(text, stoi):
    return [stoi[t] for t in text.split()]


def bow_vec(token_ids, vocab_size):
    v = np.zeros(vocab_size)
    for token_id in token_ids:
        v[token_id] += 1
    if v.sum() > 0:
        v /= v.sum()
    return v


def seq_logprob_and_grad(prompt_ids, resp_ids, W, b, vocab_size):
    total_logp = 0.0
    gW = np.zeros_like(W)
    gb = np.zeros_like(b)

    ctx = prompt_ids.copy()
    for tok in resp_ids:
        x = bow_vec(ctx, vocab_size)
        logits = x @ W + b
        p = softmax(logits)
        total_logp += np.log(p[tok] + 1e-12)

        grad_logits = -p
        grad_logits[tok] += 1.0
        gW += np.outer(x, grad_logits)
        gb += grad_logits

        ctx.append(tok)

    return float(total_logp), gW, gb


def preference_accuracy(data, W, b, stoi):
    wins = 0
    for prompt, y_w, y_l in data:
        p = ids(prompt, stoi)
        w = ids(y_w, stoi)
        l = ids(y_l, stoi)
        lp_w, _, _ = seq_logprob_and_grad(p, w, W, b, len(stoi))
        lp_l, _, _ = seq_logprob_and_grad(p, l, W, b, len(stoi))
        wins += int(lp_w > lp_l)
    return wins / len(data)


def train_dpo(data, W, b, W_ref, b_ref, stoi, beta=0.2, lr=0.08, epochs=250):
    n = len(data)
    for ep in range(epochs):
        grad_W = np.zeros_like(W)
        grad_b = np.zeros_like(b)
        epoch_loss = 0.0

        for prompt, y_w, y_l in data:
            p = ids(prompt, stoi)
            w = ids(y_w, stoi)
            l = ids(y_l, stoi)

            lp_w, gW_w, gb_w = seq_logprob_and_grad(p, w, W, b, len(stoi))
            lp_l, gW_l, gb_l = seq_logprob_and_grad(p, l, W, b, len(stoi))

            lp_w_ref, _, _ = seq_logprob_and_grad(p, w, W_ref, b_ref, len(stoi))
            lp_l_ref, _, _ = seq_logprob_and_grad(p, l, W_ref, b_ref, len(stoi))

            z = beta * ((lp_w - lp_w_ref) - (lp_l - lp_l_ref))
            sig = sigmoid(z)
            epoch_loss += -np.log(sig + 1e-12)

            coeff = -(1.0 - sig) * beta
            grad_W += coeff * (gW_w - gW_l)
            grad_b += coeff * (gb_w - gb_l)

        W -= lr * (grad_W / n)
        b -= lr * (grad_b / n)

        if (ep + 1) % 50 == 0:
            print(f"epoch {ep+1:03d} | dpo loss={epoch_loss/n:.6f}")

    return W, b


def main():
    data = build_preference_data()
    stoi, _ = build_vocab(data)

    rng = np.random.default_rng(42)
    V = len(stoi)
    W = rng.normal(0, 0.02, size=(V, V))
    b = np.zeros(V)

    W_ref = W.copy()
    b_ref = b.copy()

    acc_before = preference_accuracy(data, W, b, stoi)
    W, b = train_dpo(data, W, b, W_ref, b_ref, stoi, beta=0.25, lr=0.1, epochs=300)
    acc_after = preference_accuracy(data, W, b, stoi)

    print("\nSeason 7 / Ep 05 - DPO Trainer from Scratch")
    print(f"Preference accuracy before: {acc_before:.4f}")
    print(f"Preference accuracy after:  {acc_after:.4f}")
    print("Model parameters were updated directly via DPO gradient.")


if __name__ == "__main__":
    main()
