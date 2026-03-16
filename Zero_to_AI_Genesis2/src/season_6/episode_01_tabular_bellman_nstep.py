import numpy as np

from rl_utils import GridWorld, epsilon_greedy


def value_iteration(env: GridWorld, gamma: float = 0.95, tol: float = 1e-6):
    v = np.zeros(env.n_states)
    while True:
        old = v.copy()
        for s in range(env.n_states):
            if s == env.state_to_idx(env.goal):
                continue
            q_vals = []
            for a in range(env.n_actions):
                row, col = env.idx_to_state(s)
                env.state = (row, col)
                s2, r, done = env.step(a)
                q_vals.append(r if done else r + gamma * old[s2])
            v[s] = np.max(q_vals)
        if np.max(np.abs(v - old)) < tol:
            break
    return v


def q_learning_n_step(env: GridWorld, n_step: int = 3, episodes: int = 400, alpha: float = 0.1, gamma: float = 0.95):
    rng = np.random.default_rng(42)
    Q = np.zeros((env.n_states, env.n_actions))

    for _ in range(episodes):
        s = env.reset()
        done = False
        trajectory = []

        while not done:
            a = epsilon_greedy(Q[s], epsilon=0.1, rng=rng)
            s2, r, done = env.step(a)
            trajectory.append((s, a, r))

            if len(trajectory) >= n_step:
                g = 0.0
                for i in range(n_step):
                    g += (gamma**i) * trajectory[i][2]
                if not done:
                    g += (gamma**n_step) * np.max(Q[s2])
                s_upd, a_upd, _ = trajectory.pop(0)
                Q[s_upd, a_upd] += alpha * (g - Q[s_upd, a_upd])

            s = s2

        while trajectory:
            g = 0.0
            for i, (_, _, rr) in enumerate(trajectory):
                g += (gamma**i) * rr
            s_upd, a_upd, _ = trajectory.pop(0)
            Q[s_upd, a_upd] += alpha * (g - Q[s_upd, a_upd])
    return Q


def main():
    env = GridWorld(size=5, max_steps=50)
    v_star = value_iteration(env)
    q = q_learning_n_step(env, n_step=3)

    start = env.state_to_idx(env.start)
    print("\nSeason 6 / Ep 01 - Bellman + N-step")
    print("V*(start) from value iteration:", round(float(v_star[start]), 4))
    print("Q(start, :) from learned 3-step Q-learning:", np.round(q[start], 4))
    print("Greedy action at start (0=up,1=down,2=left,3=right):", int(np.argmax(q[start])))


if __name__ == "__main__":
    main()
