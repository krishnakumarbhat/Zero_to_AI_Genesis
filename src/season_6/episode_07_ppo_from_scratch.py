import numpy as np


class LineWorld:
    def __init__(self, n_states: int = 5, max_steps: int = 25):
        self.n_states = n_states
        self.max_steps = max_steps
        self.start_state = 0
        self.goal_state = n_states - 1
        self.reset()

    @property
    def n_actions(self):
        return 2  # 0=left, 1=right

    def reset(self):
        self.state = self.start_state
        self.steps = 0
        return self.state

    def step(self, action: int):
        if action == 0:
            self.state = max(0, self.state - 1)
        else:
            self.state = min(self.n_states - 1, self.state + 1)
        self.steps += 1

        done = self.state == self.goal_state or self.steps >= self.max_steps
        reward = 1.0 if self.state == self.goal_state else -0.02
        return self.state, reward, done


def softmax(x):
    z = x - np.max(x)
    e = np.exp(z)
    return e / e.sum()


def sample_action(probs: np.ndarray, rng: np.random.Generator):
    return int(rng.choice(len(probs), p=probs))


def collect_rollouts(env, logits, values, batch_episodes=20, gamma=0.99, lam=0.95, seed=42):
    rng = np.random.default_rng(seed)
    trajectories = []
    episode_returns = []

    for _ in range(batch_episodes):
        s = env.reset()
        done = False
        states, actions, rewards, old_logps, vals = [], [], [], [], []

        while not done:
            probs = softmax(logits[s])
            a = sample_action(probs, rng)
            logp = np.log(probs[a] + 1e-12)

            s2, r, done = env.step(a)

            states.append(s)
            actions.append(a)
            rewards.append(r)
            old_logps.append(logp)
            vals.append(values[s])
            s = s2

        vals.append(values[s])
        episode_returns.append(sum(rewards))

        adv = np.zeros(len(rewards))
        gae = 0.0
        for t in reversed(range(len(rewards))):
            delta = rewards[t] + gamma * vals[t + 1] - vals[t]
            gae = delta + gamma * lam * gae
            adv[t] = gae
        ret = adv + np.array(vals[:-1])

        trajectories.append(
            {
                "states": np.array(states, dtype=np.int64),
                "actions": np.array(actions, dtype=np.int64),
                "rewards": np.array(rewards, dtype=np.float64),
                "old_logps": np.array(old_logps, dtype=np.float64),
                "advantages": adv,
                "returns": ret,
            }
        )

    return trajectories, float(np.mean(episode_returns))


def ppo_update(logits, values, trajectories, clip_eps=0.2, lr_policy=0.06, lr_value=0.08, epochs=6):
    data = {
        k: np.concatenate([tr[k] for tr in trajectories])
        for k in ["states", "actions", "old_logps", "advantages", "returns"]
    }

    adv = data["advantages"]
    adv = (adv - adv.mean()) / (adv.std() + 1e-8)

    for _ in range(epochs):
        for s, a, old_logp, a_hat, ret in zip(data["states"], data["actions"], data["old_logps"], adv, data["returns"]):
            probs = softmax(logits[s])
            logp = np.log(probs[a] + 1e-12)
            ratio = np.exp(logp - old_logp)

            clipped_high = ratio > (1 + clip_eps) and a_hat > 0
            clipped_low = ratio < (1 - clip_eps) and a_hat < 0

            if not (clipped_high or clipped_low):
                grad_logp = -probs
                grad_logp[a] += 1.0
                logits[s] += lr_policy * (a_hat * ratio) * grad_logp

            values[s] += lr_value * (ret - values[s])

    return logits, values


def evaluate_policy(env, logits, episodes=40, seed=7):
    rng = np.random.default_rng(seed)
    returns = []
    for _ in range(episodes):
        s = env.reset()
        done = False
        total = 0.0
        while not done:
            probs = softmax(logits[s])
            a = int(rng.choice(len(probs), p=probs))
            s, r, done = env.step(a)
            total += r
        returns.append(total)
    return float(np.mean(returns))


def main():
    env = LineWorld(n_states=5, max_steps=25)
    logits = np.zeros((env.n_states, env.n_actions))
    values = np.zeros(env.n_states)

    before = evaluate_policy(env, logits)
    for it in range(45):
        traj, batch_ret = collect_rollouts(env, logits, values, batch_episodes=20, seed=42 + it)
        logits, values = ppo_update(logits, values, traj)
        if (it + 1) % 15 == 0:
            print(f"iter {it+1:02d} | batch return={batch_ret:.4f}")

    after = evaluate_policy(env, logits)
    start_probs = softmax(logits[0])

    print("\nSeason 6 / Ep 07 - PPO from Scratch")
    print("Start-state policy probs [left,right]:", np.round(start_probs, 4))
    print(f"Average return before training: {before:.4f}")
    print(f"Average return after training:  {after:.4f}")


if __name__ == "__main__":
    main()
