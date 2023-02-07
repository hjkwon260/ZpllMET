import tensorflow as tf

class Seq(tf.keras.Model):
    """build customed sequential model"""
    def __init__(self, input_dim, inter_dim, output_dim, output_activation, drop_rate=0.1, **kwargs):
        super(Seq, self).__init__()
        self.dense_input = tf.keras.layers.Dense(input_dim, input_dim=input_dim, activation=tf.nn.relu)
        self.dense1 = tf.keras.layers.Dense(inter_dim, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(inter_dim, activation=tf.nn.relu)
        self.dense3 = tf.keras.layers.Dense(inter_dim, activation=tf.nn.relu)
        self.dense4 = tf.keras.layers.Dense(inter_dim, activation=tf.nn.relu)
        self.dense_output = tf.keras.layers.Dense(output_dim, activation=output_activation)
        self.dropout = tf.keras.layers.Dropout(drop_rate)

    def call(self, inputs, training=None):
        x = self.dense_input(inputs)
        x = self.dense1(x)
        if training:
            x = self.dropout(x, training=training)
        x = self.dense2(x)
        if training:
            x = self.dropout(x, training=training)
        x = self.dense3(x)
        x = self.dense4(x)
        return self.dense_output(x)