import gym
from gym import Wrapper
from gym import error, version
import os, json, logging, numpy as np, six

FILE_PREFIX = 'openaigym'
MANIFEST_PREFIX = FILE_PREFIX + '.manifest'

class FeatureInverter(Wrapper):
    """
    This wrapper is used to change the order of features in the state representation of an environment
    It has no effect on the dynamics of the environment
    It is mainly used for visualisation: if an environment has more than 2 state features,
    it makes it possible to choose which of the features are the first two, because only the
    first two will be visualized with a portrait visualization.
    A concrete example is CartPole: we would like to visualize position and pole angle, and pole angle
    is only the third feature.
    We specify the rank of two features to be inverted and their place is exchanged in the observation
    vector output at each step, including reset.
    """
    def __init__(self, env, f1, f2):
        """
        :param env: the environment to be wrapped
        :param f1: the rank of the first feature to be inverted
        :param f2:  the rank of the second feature to be inverted
        """
        super(FeatureInverter, self).__init__(env)
        self.f1 = f1
        self.f2 = f2

        low_space = env.observation_space.low
        high_space = env.observation_space.high
        tmp = low_space[self.f1]
        low_space[self.f1] = low_space[self.f2]
        low_space[self.f2] = tmp
        tmp = high_space[self.f1]
        high_space[self.f1] = high_space[self.f2]
        high_space[self.f2] = tmp
        self.observation_space.low = low_space
        self.observation_space.high = high_space

    def _step(self, action):
        observation, reward, done, info = self.env.step(action)
        tmp = observation[self.f1]
        observation[self.f1] = observation[self.f2]
        observation[self.f2] = tmp
        return observation, reward, done, info

    def _reset(self, **kwargs):
        observation = self.env.reset(**kwargs)
        tmp = observation[self.f1]
        observation[self.f1] = observation[self.f2]
        observation[self.f2] = tmp
        return observation

    def _env_info(self):
        env_info = {
            'gym_version': version.VERSION,
        }
        if self.env.spec:
            env_info['env_id'] = self.env.spec.id
        return env_info