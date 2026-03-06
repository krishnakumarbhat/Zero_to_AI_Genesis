import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def dpo_loss(logp_w, logp_l, logp_ref_w, logp_ref_l, beta=0.1):
    z = beta * ((logp_w - logp_ref_w) - (logp_l - logp_ref_l))
    return -np.mean(np.log(sigmoid(z) + 1e-12))


def kto_loss(logp, labels, beta=0.1):
    util = np.where(labels == 1, logp, -logp)
    return -np.mean(np.log(sigmoid(beta * util) + 1e-12))


def orpo_loss(logp_target, logp_reject, lam=0.2):
    sft_term = -np.mean(logp_target)
    odds_term = np.mean(np.log(1 + np.exp(logp_reject - logp_target)))
    return sft_term + lam * odds_term


def main():
    rng = np.random.default_rng(42)
    logp_w = rng.normal(-1.2, 0.4, size=128)
    logp_l = rng.normal(-2.0, 0.4, size=128)
    logp_ref_w = rng.normal(-1.5, 0.4, size=128)
    logp_ref_l = rng.normal(-1.7, 0.4, size=128)

    labels = rng.integers(0, 2, size=128)
    single_logp = rng.normal(-1.4, 0.5, size=128)

    dpo = dpo_loss(logp_w, logp_l, logp_ref_w, logp_ref_l, beta=0.2)
    kto = kto_loss(single_logp, labels, beta=0.15)
    orpo = orpo_loss(logp_w, logp_l, lam=0.3)

    print("\nSeason 7 / Ep 03 - DPO / KTO / ORPO (toy)")
    print("DPO loss:", round(float(dpo), 6))
    print("KTO loss:", round(float(kto), 6))
    print("ORPO loss:", round(float(orpo), 6))


if __name__ == "__main__":
    main()
