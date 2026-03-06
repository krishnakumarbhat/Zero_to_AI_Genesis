import numpy as np


def make_continuous_batch(n: int = 128, seed: int = 42):
    rng = np.random.default_rng(seed)
    s = rng.uniform(-2.0, 2.0, size=(n, 1))
    a_star = 0.8 * s
    return s, a_star


def actor(s, theta):
    return s @ theta


def critic_q(s, a):
    return -((a - 0.8 * s) ** 2)


def ddpg_step(theta, s, lr=0.1):
    a = actor(s, theta)
    dq_da = -2.0 * (a - 0.8 * s)
    grad_theta = np.mean(dq_da * s, axis=0, keepdims=True).T
    theta_new = theta + lr * grad_theta
    return theta_new, float(np.mean(critic_q(s, actor(s, theta_new))))


def soft_value_objective(s, mean_a, log_std, alpha=0.2, n_samples=8, seed=42):
    rng = np.random.default_rng(seed)
    std = np.exp(log_std)
    total = 0.0
    for _ in range(n_samples):
        eps = rng.normal(size=mean_a.shape)
        a = mean_a + std * eps
        reward_term = np.mean(critic_q(s, a))
        entropy_term = 0.5 * np.log(2 * np.pi * np.e * (std**2) + 1e-12)
        total += reward_term + alpha * float(np.mean(entropy_term))
    return total / n_samples


def main():
    s, _ = make_continuous_batch()
    theta = np.array([[0.0]])

    q_before = float(np.mean(critic_q(s, actor(s, theta))))
    for _ in range(20):
        theta, _ = ddpg_step(theta, s, lr=0.05)
    q_after = float(np.mean(critic_q(s, actor(s, theta))))

    mean_a = actor(s, theta)
    sac_obj = soft_value_objective(s, mean_a, log_std=np.array([[np.log(0.3)]]), alpha=0.2)

    print("\nSeason 6 / Ep 05 - DDPG + SAC (toy)")
    print("Actor parameter theta:", np.round(theta.ravel(), 4))
    print("Q before update:", round(q_before, 4))
    print("Q after DDPG-like update:", round(q_after, 4))
    print("SAC objective r + alpha*H:", round(float(sac_obj), 4))


if __name__ == "__main__":
    main()
