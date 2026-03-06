# Zero to AI Genesis 🧠🔬

[![CI](https://github.com/krishnakumarbhat/Zero_to_AI_Genesis/actions/workflows/ci.yml/badge.svg)](https://github.com/krishnakumarbhat/Zero_to_AI_Genesis/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

An educational **from-scratch AI learning repository** spanning 7+ seasons — from classic ML to LLM alignment. Each season builds on the previous, with explicit equations and lightweight implementations designed to teach internals, not just usage.

## 🏗️ Learning Roadmap

```mermaid
flowchart LR
    S0[Season 0\nClassic ML\nNumPy-first] --> S1[Season 1\nDeep Learning\n& Vision]
    S1 --> S2[Season 2\nGOFAI\nSearch & Logic]
    S2 --> S3[Season 3\nRetrieval\nRAG]
    S3 --> S4[Season 4\nDL Foundations\nCourse Modules]
    S4 --> S5[Season 5\nAgentic\nWorkflows]
    S5 --> S6[Season 6\nReinforcement\nLearning]
    S6 --> S7[Season 7\nLLM Fine-tuning\n& Alignment]

    style S0 fill:#4CAF50,color:#fff
    style S1 fill:#2196F3,color:#fff
    style S2 fill:#FF9800,color:#fff
    style S3 fill:#9C27B0,color:#fff
    style S4 fill:#F44336,color:#fff
    style S5 fill:#00BCD4,color:#fff
    style S6 fill:#FF5722,color:#fff
    style S7 fill:#673AB7,color:#fff
```

## 🔬 Season 6 — Reinforcement Learning Deep Dive

```mermaid
flowchart TD
    subgraph Foundations["Foundations"]
        E0[Ep 0: Exploration\nε-greedy, UCB]
        E1[Ep 1: Bellman\nn-step, Q-learning]
        E2[Ep 2: Model-based\nDyna-Q, MCTS]
    end

    subgraph Advanced["Advanced Methods"]
        E3[Ep 3: Rainbow\nPER, NoisyNet]
        E4[Ep 4: Policy Gradient\nTRPO-style]
        E5[Ep 5: Continuous\nDDPG, SAC]
    end

    subgraph Applied["Applied RL"]
        E6[Ep 6: Imitation\nBC, GAIL, CQL]
        E7[Ep 7: PPO\nFrom Scratch]
    end

    E0 --> E1 --> E2 --> E3 --> E4 --> E5 --> E6 --> E7
```

## 🔬 Season 7 — LLM Fine-Tuning & Alignment

```mermaid
flowchart TD
    subgraph FT["Fine-Tuning"]
        F0[Ep 0: SFT\nSupervised]
        F1[Ep 1: LoRA/QLoRA\nDoRA/PiSSA]
    end

    subgraph Align["Alignment"]
        F2[Ep 2: RLHF\nReward Model + PPO]
        F3[Ep 3: DPO/KTO/ORPO\nDirect Preference]
    end

    subgraph Verify["Verifiable RL"]
        F4[Ep 4: RLVR/GRPO\nGroup Advantage]
        F5[Ep 5: DPO Trainer\nEnd-to-End]
    end

    F0 --> F1 --> F2 --> F3 --> F4 --> F5
```

## 🛠️ Tech Stack

| Component     | Technology                             |
| ------------- | -------------------------------------- |
| Core          | NumPy, Python 3.10+                    |
| Deep Learning | PyTorch (minimal)                      |
| Math          | LaTeX equations inline                 |
| Design        | From-scratch, no high-level frameworks |

## 📦 Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/data/make_dummy_data.py
```

## ▶️ Running Episodes

```bash
# Season 6 — RL
python3 src/season_6/episode_00_exploration_foundations.py
python3 src/season_6/episode_07_ppo_from_scratch.py

# Season 7 — LLM Alignment
python3 src/season_7/episode_00_sft.py
python3 src/season_7/episode_05_dpo_trainer_from_scratch.py
```

## 📁 Project Structure

```
Zero_to_AI_Genesis/
├── src/
│   ├── season_0/         # Classic ML (NumPy)
│   ├── season_1/         # Deep Learning & Vision
│   ├── season_2/         # GOFAI (Search/Logic)
│   ├── season_3/         # Retrieval / RAG
│   ├── season_4/         # DL Foundations
│   ├── season_5/         # Agentic Workflows
│   ├── season_6/         # Reinforcement Learning
│   ├── season_7/         # LLM Fine-Tuning & Alignment
│   └── data/             # Dummy data generation
├── requirements.txt
├── .github/workflows/    # CI/CD pipeline
├── .gitignore
└── README.md
```

## 📖 Key Equations

<details>
<summary><b>RL Core (Season 6)</b></summary>

**Expected Return:** $G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$

**Bellman Optimality:** $V^*(s) = \max_a \sum_{s',r}P(s',r|s,a)\left[r + \gamma V^*(s')\right]$

**PPO Clipped Surrogate:** $L^{CLIP}(\theta) = \hat{\mathbb{E}}_t\left[\min\left(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right)\right]$

</details>

<details>
<summary><b>LLM Alignment (Season 7)</b></summary>

**DPO:** $\mathcal{L}_{DPO}=-\mathbb{E}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)}-\beta\log\frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}\right)\right]$

**LoRA:** $W=W_0+\Delta W=W_0+BA,\quad r\ll d,k$

**GRPO:** $\hat{A}_i=\frac{r_i-\text{mean}(r_1,\dots,r_G)}{\text{std}(r_1,\dots,r_G)}$

</details>

## ⚠️ Scope

These are **teaching implementations** on dummy/synthetic data. For production-grade training, use distributed systems and robust ML frameworks.

## 📝 License

Apache 2.0 License
