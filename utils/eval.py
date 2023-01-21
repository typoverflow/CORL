import torch
import torch.nn as nn
import numpy as np
import gym

@torch.no_grad()
def eval_actor(
    env: gym.Env, actor: nn.Module, device: str, n_episodes: int, seed: int, raw_env=None
) -> np.ndarray:
    if raw_env is None:
        raw_env = env
    env.seed(seed)
    actor.eval()
    actor.to(device)
    episode_lengths = []
    episode_rewards = []
    for _ in range(n_episodes):
        state, done = env.reset(), False
        episode_reward = 0.0
        episode_length = 0.0
        while not done:
            action = actor.act(state, device)
            state, reward, done, _ = env.step(action)
            episode_reward += reward
            episode_length += 1
        episode_rewards.append(raw_env.get_normalized_score(episode_reward)*100)
        episode_lengths.append(episode_length)

    actor.train()
    episode_rewards = np.asarray(episode_rewards)
    episode_lengths = np.asarray(episode_lengths)
    return {
        "normalized_score_mean": episode_rewards.mean(), 
        "normalized_score_std": episode_rewards.std(), 
        "length_mean": episode_lengths.mean(), 
        "length_std": episode_lengths.std()
    }