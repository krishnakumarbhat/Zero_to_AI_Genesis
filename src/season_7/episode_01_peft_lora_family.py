import numpy as np


def quantize_int4(w: np.ndarray):
    w_min, w_max = w.min(), w.max()
    scale = (w_max - w_min) / 15.0 + 1e-12
    q = np.clip(np.round((w - w_min) / scale), 0, 15)
    return q.astype(np.int8), w_min, scale


def dequantize_int4(q: np.ndarray, w_min: float, scale: float):
    return q.astype(np.float32) * scale + w_min


def train_lora(X, Y, rank=2, epochs=400, lr=0.05, seed=42, use_quantized_base=False):
    rng = np.random.default_rng(seed)
    d_in, d_out = X.shape[1], Y.shape[1]

    W0 = rng.normal(0, 0.5, size=(d_in, d_out))
    if use_quantized_base:
        q, w_min, scale = quantize_int4(W0)
        W0 = dequantize_int4(q, w_min, scale)

    U, S, Vt = np.linalg.svd(W0, full_matrices=False)
    B = U[:, :rank] * np.sqrt(S[:rank])[None, :]
    A = np.sqrt(S[:rank])[:, None] * Vt[:rank, :]

    mag = np.linalg.norm(W0, axis=0, keepdims=True) + 1e-12
    dir_base = W0 / mag

    for _ in range(epochs):
        delta = B @ A
        W = mag * dir_base + delta
        pred = X @ W
        err = pred - Y

        grad_W = (X.T @ err) / len(X)
        grad_B = grad_W @ A.T
        grad_A = B.T @ grad_W
        grad_mag = np.sum(grad_W * dir_base, axis=0, keepdims=True)

        B -= lr * grad_B
        A -= lr * grad_A
        mag -= lr * grad_mag

    final = mag * dir_base + B @ A
    mse = np.mean((X @ final - Y) ** 2)
    return mse


def main():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(300, 8))
    W_true = rng.normal(size=(8, 6))
    Y = X @ W_true + 0.05 * rng.normal(size=(300, 6))

    mse_lora = train_lora(X, Y, rank=2, use_quantized_base=False)
    mse_qlora = train_lora(X, Y, rank=2, use_quantized_base=True)

    print("\nSeason 7 / Ep 01 - PEFT (LoRA family, toy)")
    print("LoRA: W = W0 + B@A, with rank r << d")
    print("QLoRA (toy): frozen base quantized to 4-bit + train LoRA adapters")
    print("DoRA/PiSSA-inspired init included (magnitude-direction + SVD init)")
    print("Final MSE (LoRA):", round(float(mse_lora), 6))
    print("Final MSE (QLoRA-style):", round(float(mse_qlora), 6))


if __name__ == "__main__":
    main()
