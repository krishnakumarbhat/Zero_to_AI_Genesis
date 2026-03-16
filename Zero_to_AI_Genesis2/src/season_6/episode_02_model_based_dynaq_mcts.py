from collections import defaultdict

import numpy as np

from rl_utils import GridWorld, epsilon_greedy


def dyna_q(env: GridWorld, episodes: int = 250, alpha: float = 0.1, gamma: float = 0.95, planning_steps: int = 20):
    rng = np.random.default_rng(42)
    Q = np.zeros((env.n_states, env.n_actions))
    model = {}
    seen = []

    for _ in range(episodes):
        s = env.reset()
        done = False

        while not done:
            a = epsilon_greedy(Q[s], 0.1, rng)
            s2, r, done = env.step(a)

            Q[s, a] += alpha * (r + gamma * np.max(Q[s2]) - Q[s, a])

            model[(s, a)] = (s2, r)
            seen.append((s, a))

            for _ in range(planning_steps):
                sp, ap = seen[int(rng.integers(0, len(seen)))]
                sp2, rp = model[(sp, ap)]
                Q[sp, ap] += alpha * (rp + gamma * np.max(Q[sp2]) - Q[sp, ap])
            s = s2
    return Q


class TinyTreeEnv:
    def __init__(self):
        self.transitions = {
            "root": {0: ("left", 0.0), 1: ("right", 0.0)},
            "left": {0: ("terminal", 2.0), 1: ("terminal", 1.0)},
            "right": {0: ("terminal", 0.2), 1: ("terminal", 3.0)},
        }

    def step(self, state, action):
        return self.transitions[state][action]


def mcts_ucb(env: TinyTreeEnv, simulations: int = 200, c: float = 1.2):
    n = defaultdict(int)
    w = defaultdict(float)

    def ucb(state, action, t):
        key = (state, action)
        if n[key] == 0:
            return np.inf
        q = w[key] / n[key]
        return q + c * np.sqrt(np.log(t + 1) / n[key])

    for t in range(1, simulations + 1):
        s = "root"
        a_root = int(np.argmax([ucb(s, 0, t), ucb(s, 1, t)]))
        s2, r0 = env.step(s, a_root)

        a2 = int(np.argmax([ucb(s2, 0, t), ucb(s2, 1, t)]))
        _, r1 = env.step(s2, a2)
        ret = r0 + r1

        n[("root", a_root)] += 1
        w[("root", a_root)] += ret
        n[(s2, a2)] += 1
        w[(s2, a2)] += r1

    q_root = [w[("root", a)] / max(n[("root", a)], 1) for a in [0, 1]]
    return int(np.argmax(q_root)), q_root


def main():
    env = GridWorld(size=5)
    Q = dyna_q(env)
    start = env.state_to_idx(env.start)
    greedy = int(np.argmax(Q[start]))

    mcts_action, mcts_q = mcts_ucb(TinyTreeEnv())

    print("\nSeason 6 / Ep 02 - Model-Based RL")
    print("Dyna-Q greedy start action (0/1/2/3):", greedy)
    print("MCTS root action (0=left,1=right):", mcts_action)
    print("MCTS root action values:", np.round(mcts_q, 4))


if __name__ == "__main__":
    main()
