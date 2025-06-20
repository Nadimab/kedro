from keras.layers import (
    LSTM,
    Activation,
    BatchNormalization,
    Conv1D,
    Dense,
    Dropout,
    GlobalAveragePooling1D,
    Input,
    Layer,
    Masking,
    Reshape,
    concatenate,
    multiply,
)
from keras.models import Model


def lstm_fcn_maze_classifier(
    nb_vars: int = 2, x1000_sequence_max_length: int = 30, nb_classes: int = 2
):
    model_input = Input(shape=(int(x1000_sequence_max_length * 1000), nb_vars))

    lstm = Masking()(model_input)
    lstm = LSTM(8)(lstm)
    lstm = Dropout(0.8)(lstm)

    # layer_1 = Permute((2, 1))(model_input)
    layer_1 = Conv1D(128, 8, padding="same", kernel_initializer="he_uniform")(
        model_input
    )
    layer_1 = BatchNormalization()(layer_1)
    layer_1 = Activation("relu")(layer_1)
    layer_1 = squeeze_excite_block(layer_1)

    layer_2 = Conv1D(256, 5, padding="same", kernel_initializer="he_uniform")(
        layer_1
    )
    layer_2 = BatchNormalization()(layer_2)
    layer_2 = Activation("relu")(layer_2)
    layer_2 = squeeze_excite_block(layer_2)

    layer_3 = Conv1D(128, 3, padding="same", kernel_initializer="he_uniform")(
        layer_2
    )
    layer_3 = BatchNormalization()(layer_3)
    layer_3 = Activation("relu")(layer_3)

    pooling = GlobalAveragePooling1D()(layer_3)

    network = concatenate([lstm, pooling])

    output = Dense(nb_classes, activation="softmax")(network)

    model = Model(model_input, output)
    return model


def squeeze_excite_block(input_layer: Layer):
    """Create a squeeze-excite block
    Args:
        input_layer: input
    Returns: a keras tensor
    """
    filters = input_layer.shape[-1]  # channel_axis = -1 for TF

    squeeze_excite_layer = GlobalAveragePooling1D()(input_layer)
    squeeze_excite_layer = Reshape((1, filters))(squeeze_excite_layer)
    squeeze_excite_layer = Dense(
        filters // 16,
        activation="relu",
        kernel_initializer="he_normal",
        use_bias=False,
    )(squeeze_excite_layer)
    squeeze_excite_layer = Dense(
        filters,
        activation="sigmoid",
        kernel_initializer="he_normal",
        use_bias=False,
    )(squeeze_excite_layer)
    squeeze_excite_layer = multiply([input_layer, squeeze_excite_layer])
    return squeeze_excite_layer
