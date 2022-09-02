from typing import Optional

import tensorflow as tf
import tensorflow.keras as k

from dqn_trainer import DQNTrainer
from dqn_hyperparams import DQNHyperparams


class DQNModel:
    nn: k.Sequential
    num_actions: int
    trainable: bool

    def __init__(
            self,
            num_actions: int,
            trainable: bool = False,
            hyperparams: Optional[DQNHyperparams] = None):
        self.nn = k.Sequential()
        self.num_actions = num_actions
        self.trainable = trainable
        self.hyperparams = hyperparams if hyperparams else DQNHyperparams()
        self.trainer = DQNTrainer(self.nn, self.hyperparams)

    def build(self):
        self.nn.add(k.layers.Input(shape=(84, 84, 4,), name="x"))
        self.nn.add(k.layers.Conv2D(32, 8, strides=4, activation="relu", name="h1_conv"))
        self.nn.add(k.layers.Conv2D(64, 4, strides=2, activation="relu", name="h2_conv"))
        self.nn.add(k.layers.Conv2D(64, 3, strides=1, activation="relu", name="h3_conv"))
        self.nn.add(k.layers.Flatten(name="h4_flat"))
        self.nn.add(k.layers.Dense(512, activation="relu", name="h5_dense"))
        self.nn.add(k.layers.Dense(self.num_actions, activation="linear", name="y_hat"))

    def summary(self):
        self.nn_live.summary()

    def predict(self, x: tf.Tensor) -> tf.Tensor:
        return self.nn_live(x)

    def __call__(self, x: tf.Tensor) -> tf.Tensor:
        return self.predict(x)

    def train(self, x: tf.Tensor) -> None:
        assert self.trainable
        self.trainer.feed(x)
        
