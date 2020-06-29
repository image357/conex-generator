import tensorflow as tf


class LabelMerger(tf.keras.layers.Layer):

    def __init__(self, numparticle=6, expscale=False, epsilon=1e-25, **kwargs):
        super().__init__(**kwargs)
        self._numparticle = numparticle

        self.expscale = expscale
        self.epsilon = epsilon

    @tf.function
    def call(self, inputs, training=False):
        # normalize inputs
        particle = tf.cast(inputs[:,0], tf.int32)
        particle_oh = tf.cast(tf.one_hot(particle, self._numparticle),
                              tf.float32)
        energy = inputs[:,1] / 1e10
        theta = inputs[:,2] / 90.0
        phi = inputs[:,3] / 180.0

        if self.expscale:
            energy = tf.math.log(tf.math.abs(energy) + self.epsilon)

        # merge
        tensor = tf.concat(
            [
                particle_oh,
                tf.expand_dims(energy, -1),
                tf.expand_dims(theta, -1),
                tf.expand_dims(phi, -1),
            ],
            -1
        )

        return tensor

