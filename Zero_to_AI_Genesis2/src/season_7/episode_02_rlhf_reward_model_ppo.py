import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def softmax(x):
    z = x - np.max(x)
    e = np.exp(z)
    return e / e.sum()


def train_reward_model(features_w, features_l, epochs=500, lr=0.1):
    w = np.zeros(features_w.shape[1])
    for _ in range(epochs):
        rw = features_w @ w
        rl = features_l @ w
        diff = rw - rl
        grad = -((1 - sigmoid(diff))[:, None] * (features_w - features_l)).mean(axis=0)
        w -= lr * grad
    return w


def ppo_like_update(policy_logits, rewards, actions, beta=0.1, lr=0.3):
    pi_old = softmax(policy_logits)
    adv = rewards - rewards.mean()

    grad = np.zeros_like(policy_logits)
    for a, a_adv in zip(actions, adv):
        onehot = np.zeros_like(policy_logits)
        onehot[a] = 1.0
        grad += a_adv * (onehot - pi_old)
    grad /= len(actions)

    kl_grad = pi_old - softmax(policy_logits)
    policy_logits = policy_logits + lr * (grad - beta * kl_grad)
    return policy_logits, pi_old, softmax(policy_logits)


def main():
    rng = np.random.default_rng(42)

    features_w = rng.normal(loc=0.5, scale=1.0, size=(120, 6))
    features_l = rng.normal(loc=-0.2, scale=1.0, size=(120, 6))
    rm_w = train_reward_model(features_w, features_l)

    action_features = rng.normal(size=(80, 6))
    rm_scores = action_features @ rm_w
    actions = rng.integers(0, 3, size=80)

    logits = np.array([0.2, 0.0, -0.1])
    logits_new, pi_old, pi_new = ppo_like_update(logits, rm_scores, actions, beta=0.2)

    print("\nSeason 7 / Ep 02 - RLHF (RM + PPO-like)")
    print("Reward model pairwise objective optimized (Bradley-Terry)")
    print("Policy old:", np.round(pi_old, 4))
    print("Policy new:", np.round(pi_new, 4))
    print("Logits delta:", np.round(logits_new - logits, 4))


if __name__ == "__main__":
    main()
