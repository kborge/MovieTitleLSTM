import os, pickle, tflearn
from tflearn.data_utils import *

path = "movie_titles.txt"
char_idx_file = 'char_idx.pickle'

#set some variables
maxlen = 25
learning_rate = 0.001
max_epochs = 30
batch_size = 128

#load pickle
char_idx = None
if os.path.isfile(char_idx_file):
    print("Loading previous char_idx")
    char_idx = pickle.load(open(char_idx_file, 'rb'))


#vectorize sequence
X, Y, char_idx = textfile_to_semi_redundant_sequences(path, seq_maxlen=maxlen, redun_step=3)

pickle.dump(char_idx, open(char_idx_file, 'wb'))

#create lstm
g = tflearn.input_data(shape=[None, maxlen, len(char_idx)])
g = tflearn.lstm(g, 512, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 512, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 512)
g = tflearn.dropout(g, 0.5)
g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy', learning_rate=learning_rate)

#generate sequence
m = tflearn.SequenceGenerator(g, dictionary=char_idx, seq_maxlen=maxlen, clip_gradients=5.0, checkpoint_path='model_movie_titles')

#training
for i in range(max_epochs):
    seed = random_sequence_from_textfile(path, maxlen)
    m.fit(X, Y, validation_set=0.1, batch_size=batch_size, snapshot_epoch=False, show_metric=True, n_epoch=1, run_id='movie_titles')
    print("-- Testing --")
    print("-- Temp of 1.0 --")
    print(m.generate(100, temperature=1.0, seq_seed=seed))
    print("-- Temp of 0.5 --")
    print(m.generate(100, temperature=0.5, seq_seed=seed))

#final output
seed = random_sequence_from_textfile(path, maxlen)
print("-- Final Movie Titles --")
print("-- Temp of 1.0 --")
print(m.generate(100, temperature=1.0, seq_seed=seed))
print("-- Temp of 0.5 --")
print(m.generate(100, temperature=0.5, seq_seed=seed))
