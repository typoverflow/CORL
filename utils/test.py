from algorithms import iql, cql, td3_bc
import torch
import os
import argparse
import copy
# parser = argparse.ArgumentParser()
# parser.add_argument("--algo", type=str, required=True)
# parser.add_argument("--path", type=str, required=True)
# parser.add_argument("--env", type=str, default="halfcheetah-medium-v2")
# args = parser.parse_args()

all_module = {
    "cql": cql, 
    "iql": iql, 
    "td3_bc": td3_bc
}
all_cls = {
    "cql": cql.ContinuousCQL, 
    "iql": iql.ImplicitQLearning, 
    "td3_bc": td3_bc.TD3_BC
}


from utils.eval import eval_actor
from UtilsRL.env.wrapper.mujoco_wrapper import MujocoParamOverWrite
import gym

def get_env(env, type, amp):
    env = gym.make(env)
    return MujocoParamOverWrite(env, {type: amp}, do_scale=True)

def test_one_actor(trainer, path, env):
    # module = all_module[algo]
    # cls = all_cls[algo]
    # config = module.TrainConfig.__dict__
    # config = {_key:_value for _key, _value in config.items() if not _key.startswith("__")}

    # actor = cls(**config)
    trainer.load_state_dict(torch.load(path, map_location="cpu"))
    amp_range = {
        "gravity": [0.5, 0.8, 1.0, 1.2, 1.5], 
        "dof_damping": [0.5, 0.8, 1.0, 1.2, 1.5], 
        "dens": [0.5, 0.8, 1.0, 1.2, 1.5], 
        "fric": [0.5, 0.8, 1.0, 1.2, 1.5]
    }
    for perturb_type in ["gravity", "dof_damping"]:
        for perturb_amp in amp_range[perturb_type]:
            # print(f"env: {env.unwrapped.model.opt.gravity}")
            perturb_env = copy.deepcopy(env)
            perturb_env = MujocoParamOverWrite(perturb_env, {perturb_type: perturb_amp}, do_scale=True)
            # print(f"penv: {env.unwrapped.model.opt.gravity}")
            eval_dict = eval_actor(perturb_env, trainer.actor, device="cuda", n_episodes=10, seed=0, raw_env=env)
            print(f"{perturb_type}\t{perturb_amp}: {eval_dict['normalized_score_mean']}")

if __name__ == "__main__":
    algos = ["cql"]
    envs = ["halfcheetah-medium-v2"]
    for algo in algos:
        for env in envs:
            for run in os.listdir(f"./log/{algo}/{env}"):
                ckpt = os.path.join("./log", algo, env, run, "checkpoints", "checkpoint_1000000.pt")
                test_one_actor(algo, ckpt, env)