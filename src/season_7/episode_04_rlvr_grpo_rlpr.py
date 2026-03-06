import numpy as np


def verifier_math(prompt: str, answer: str) -> int:
    try:
        lhs, rhs = prompt.split("=")
        expected = eval(lhs.strip())
        return int(float(answer.strip()) == float(expected))
    except Exception:
        return 0


def rlvr_score(prompts, answers):
    return np.array([verifier_math(p, a) for p, a in zip(prompts, answers)], dtype=np.float64)


def grpo_advantages(group_rewards):
    mu = np.mean(group_rewards)
    std = np.std(group_rewards) + 1e-8
    return (group_rewards - mu) / std


def rlpr_intrinsic_reward(logp_final, logp_steps):
    baseline = np.mean(logp_steps, axis=1, keepdims=True)
    debiased = logp_steps - baseline
    return np.mean(debiased, axis=1) + 0.5 * logp_final


def main():
    prompts = ["2+3 =", "5*4 =", "10-7 =", "9/3 ="]
    answers = ["5", "19", "3", "3"]
    r = rlvr_score(prompts, answers)

    rng = np.random.default_rng(42)
    group_rewards = rng.integers(0, 2, size=8).astype(np.float64)
    adv = grpo_advantages(group_rewards)

    logp_final = rng.normal(-1.0, 0.3, size=8)
    logp_steps = rng.normal(-1.2, 0.4, size=(8, 5))
    intrinsic = rlpr_intrinsic_reward(logp_final, logp_steps)

    print("\nSeason 7 / Ep 04 - RLVR / GRPO / RLPR (toy)")
    print("RLVR verifier rewards:", r.astype(int))
    print("GRPO normalized advantages:", np.round(adv, 4))
    print("RLPR intrinsic rewards:", np.round(intrinsic, 4))


if __name__ == "__main__":
    main()
