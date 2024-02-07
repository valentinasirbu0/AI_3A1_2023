import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# X_train   pe care ne antrenam
# X_test    pe care testam
# y_train   rezultatele care ar trebui sa fie
# y_test    rezultatele obtinute de noi
# 0.3 din date pentru testare


def prepare_data():
    column_names = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"]
    data = pd.read_csv('/Lab6_7\\seeds_dataset.txt', sep="\s+", names=column_names)
    x = data.iloc[:, :-1].values  # scot ultima coloana din date
    y = data.iloc[:, -1].values - 1  # ultima coloana - rezultatul

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=13)

    # incercam sa aducem la medie zero și o deviație standard de 1
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test


def initialize_parameters(input_size, hidden_size, output_size):
    weights_input_hidden = np.random.uniform(low=-1, high=1, size=(input_size, hidden_size))
    weights_hidden_output = np.random.uniform(low=-1, high=1, size=(hidden_size, output_size))

    bias_input_hidden = np.zeros(shape=(1, hidden_size))
    bias_hidden_output = np.zeros(shape=(1, output_size))

    return weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output


def forward_propagation(X, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output):
    hidden_input = np.dot(X, weights_input_hidden) + bias_input_hidden
    hidden_output = np.tanh(hidden_input)

    output_input = np.dot(hidden_output, weights_hidden_output) + bias_hidden_output
    output = sigmoid(output_input)

    return hidden_output, output


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


def tanh(x):
    return np.tanh(x)


def tanh_derivative(x):
    return 1 - np.tanh(x) ** 2


def categorical_crossentropy(y_true, y_pred):
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.sum(y_true * np.log(y_pred)) / len(y_true)









X_train, X_test, y_train, y_test = prepare_data()

weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output = initialize_parameters(input_size = 7, hidden_size = 5, output_size = 3)

hidden_output, output = forward_propagation(X_train, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output)
print("Hidden : ", hidden_output)
print("Output : ", output)
