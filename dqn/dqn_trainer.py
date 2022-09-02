from typing import List
from copy import deepcopy

import tensorflow as tf
import tensorflow.keras as k


from dqn_history import DQNEntry
from dqn_hyperparams import DQNHyperparams

class DQNTrainer:
    nn_live: k.Sequential
    nn_dash: k.Sequential
    buffer: List[List[List[str]]]
    history: List[DQNEntry]

    def __init__(
            self,
            nn: k.Sequential,
            hyperparams: DQNHyperparams) -> None:
        self.nn_live = nn
        self.nn_dash = k.models.clone_model(nn)
        self.history = []
        self.hyperparams = hyperparams

    def feed(
            self,
            s: List[List[int]],
            a: int,
            r: float,
            s_prime: List[List[int]],
            d: bool) -> None:
        
        self.buffer.append(s)
        if self.buffer and len(self.buffer) % self.self.n_frames == 0:
            frames = deepcopy(self.buffer)
            self.buffer.clear()
            self.history.append(DQNEntry(
                state=frames,
                action=a,
                total_reward=r,
                next_state=s_prime,
                ended=d
            ))
        if self._should_retrain_live():
            yhat_prime = tf.reduce_max(self.nn_live(s_prime), axis=1)
            yhat = tf.reduce_max(self.nn_live(s))
            loss = r + (self.hyperparams.gamma * yhat_prime) - (yhat)
            
