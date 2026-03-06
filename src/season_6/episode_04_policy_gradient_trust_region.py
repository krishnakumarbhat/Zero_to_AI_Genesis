import numpy as np


def softmax(logits):
    z = logits - np.max(logits)
    e = np.exp(z)
    return e / e.sum()


def kl_divergence(p, q):
    return float(np.sum(p * (np.log(p + 1e-12) - np.log(q + 1e-12))))


def estimate_advantages(returns: np.ndarray, values: np.ndarray):
    return returns - values


def trpo_like_step(logits_old: np.ndarray, advantages: np.ndarray, actions: np.ndarray, delta_kl: float = 0.01):
    logits = logits_old.copy()
    pi_old = softmax(logits_old)

    grad = np.zeros_like(logits)
    for a, adv in zip(actions, advantages):
        one_hot = np.zeros_like(logits)
        one_hot[a] = 1.0
        grad += adv * (one_hot - pi_old)
    grad /= len(actions)

    lr = 1.0
    for _ in range(20):
        cand = logits_old + lr * grad
        pi_new = softmax(cand)
        kl = kl_divergence(pi_old, pi_new)
        if kl <= delta_kl:
            logits = cand
            break
        lr *= 0.5
    return logits, pi_old, softmax(logits)


def main():
    logits_old = np.array([0.1, -0.2, 0.0])
    returns = np.array([1.2, 0.4, 1.5, -0.1, 0.7, 1.0])
    values = np.array([0.8, 0.5, 0.9, 0.1, 0.6, 0.7])
    actions = np.array([0, 1, 0, 2, 0, 2])

    adv = estimate_advantages(returns, values)
    logits_new, pi_old, pi_new = trpo_like_step(logits_old, adv, actions)

    print("\nSeason 6 / Ep 04 - Advantage + TRPO-style update")
    print("Old policy:", np.round(pi_old, 4))
    print("New policy:", np.round(pi_new, 4))
    print("KL(old||new):", round(kl_divergence(pi_old, pi_new), 6))
    print("Mean advantage used:", round(float(np.mean(adv)), 4))


if __name__ == "__main__":
    main()
