
from keras.layers.embeddings import Embedding
from keras.layers.core import Dense, Dropout, Activation, Reshape, Flatten
from keras.models import Sequential
import numpy as np
from keras.layers.recurrent import LSTM
from keras.layers.core import TimeDistributedDense

np.random.seed(1989)

emb_out = 50  #Dimension of the dense embedding.
lstm_size_1 = 5
lstm_size_2 = 10
in_dim = 1000 #Size of the vocabulary + 1
out_dim = 1

input = np.array(
    [
        [               # 1st sent
            1,        # index of 1st word in Voc
            2,        # index of 2nd word in Voc
            3,        # index of 3rd word in Voc
            4,        # index of 4th word in Voc
            5         # index of 5th word in Voc
        ],
        [               # 2nd sent
            3, 4, 1, 6, 7
        ],
        [               # 3rd sent
            7, 6, 7, 6, 7
        ]
    ]
)

input = np.random.random_integers(5, size=(500.,20.))

nof_inst = input.shape[0]
in_len = input.shape[-1]

lstm_size_3 = 1

model = Sequential() # or Graph or whatever

# model.add(Embedding(output_dim=rnn_dim, input_dim=n_symbols + 1, mask_zero=True, weights=[embedding_weights])) # note you have to put embedding weights in a list by convention

model.add(Embedding(input_dim = in_dim, output_dim = emb_out, input_length= in_len))

print(model.layers[-1].input_shape)
print(model.layers[-1].output_shape)

model.add(LSTM(lstm_size_1, return_sequences=True, activation='relu'))

print(model.layers[-1].input_shape)
print(model.layers[-1].output_shape)

model.add(Dropout(0.5))
model.add(LSTM( lstm_size_2, return_sequences=True, activation='relu'))

print(model.layers[-1].input_shape)
print(model.layers[-1].output_shape)

model.add(Dropout(0.5))
model.add(LSTM( lstm_size_3, return_sequences=True, activation='linear'))

print(model.layers[-1].input_shape)
print(model.layers[-1].output_shape)

#model.add(Reshape((nof_inst, in_len)))
model.add(Flatten())

print(model.layers[-1].input_shape)
print(model.layers[-1].output_shape)

model.compile(loss='mse', optimizer='sgd')

model.fit(input , input)

# model.fit(X_train, Y_train, nb_epoch=10, batch_size=BATCH_SIZE, verbose=1, show_accuracy=True, validation_split=0.1)




























