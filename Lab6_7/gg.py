import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
import matplotlib.pyplot as plt


def prepare_data():
    column_names = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"]
    data = pd.read_csv('/Lab6_7\\seeds_dataset.txt', sep="\s+", names=column_names)
    x = data.iloc[:, :-1].values  # scot ultima coloană din date
    y = data.iloc[:, -1].values - 1  # ultima coloană - rezultatul

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=13)

    # incercam sa aducem la medie zero si o deviatie standard de 1
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test


def initialize_parameters(input_size, hidden_size, output_size):
    weights_input_hidden = np.random.uniform(low=-0.1, high=0.1, size=(input_size, hidden_size))
    weights_hidden_output = np.random.uniform(low=-0.1, high=0.1, size=(hidden_size, output_size))

    bias_input_hidden = np.zeros(shape=(1, hidden_size))
    bias_hidden_output = np.zeros(shape=(1, output_size))

    return weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output


def forward_propagation(X, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output):
    hidden_input = np.dot(X, weights_input_hidden) + bias_input_hidden
    hidden_output = np.tanh(hidden_input)

    output_input = np.dot(hidden_output, weights_hidden_output) + bias_hidden_output
    output = softmax(output_input)

    return hidden_output, output


def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


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
    return -np.sum(y_true * np.log(y_pred + epsilon)) / len(y_true)


def backward_propagation(X, y, hidden_output, output, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output, learning_rate):
    m = len(X)

    output_error = output - np.eye(output.shape[1])[y]  # one-hot encoding pentru y
    output_delta = output_error / m

    hidden_error = output_delta.dot(weights_hidden_output.T)
    hidden_delta = hidden_error * tanh_derivative(hidden_output)

    weights_hidden_output -= hidden_output.T.dot(output_delta) * learning_rate
    bias_hidden_output -= np.sum(output_delta, axis=0, keepdims=True) * learning_rate

    weights_input_hidden -= X.T.dot(hidden_delta) * learning_rate
    bias_input_hidden -= np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate


def train_neural_network(X_train, y_train, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output, learning_rate, epochs):
    errors_train = []
    errors_test = []

    for epoch in range(epochs):
        hidden_output, output = forward_propagation(X_train, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output)
        backward_propagation(X_train, y_train, hidden_output, output, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output, learning_rate)

        # eroare pentru fiecare epoca
        _, train_output = forward_propagation(X_train, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output)
        loss_train = categorical_crossentropy(np.eye(output_size)[y_train], train_output)
        errors_train.append(loss_train)

        _, test_output = forward_propagation(X_test, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output)
        loss_test = categorical_crossentropy(np.eye(output_size)[y_test], test_output)
        errors_test.append(loss_test)

        # acuratetea pe setul de antrenare
        train_predictions = predict(X_train, weights_input_hidden, bias_input_hidden, weights_hidden_output,
                                    bias_hidden_output)
        train_accuracy = accuracy_score(y_train, train_predictions)

        if epoch % 100 == 0:  # Afisam eroarea si acuratetea o data la fiecare 100 de epoci
            print(f'Epoca {epoch}, Eroare: {loss_train}, Acuratețe pe antrenare: {train_accuracy}')

    plot_convergence(errors_train, errors_test)


def predict(X, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output):
    _, output = forward_propagation(X, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output)
    return np.argmax(output, axis=1)


def plot_convergence(errors_train, errors_test):
    plt.figure(figsize=(10, 6))
    plt.plot(errors_train, label='Antrenare')
    plt.plot(errors_test, label='Testare')
    plt.title('Convergenta modelului')
    plt.xlabel('Epoca')
    plt.ylabel('Eroare')
    plt.legend()
    plt.show()


def plot_misclassified_points(X, y_true, y_pred):
    misclassified_points = X[y_true != y_pred]

    plt.figure(figsize=(10, 6))
    plt.scatter(X[:, 0], X[:, 1], c=y_true, cmap=plt.cm.Spectral, marker='o', label='Corect clasificate')
    plt.scatter(misclassified_points[:, 0], misclassified_points[:, 1], c='red', marker='x', label='Eronat clasificate')
    plt.title('Puncte clasificate eronat')
    plt.xlabel('Caracteristica 1')
    plt.ylabel('Caracteristica 2')
    plt.legend()
    plt.show()

input_size = 7
hidden_size = 5
output_size = 3
learning_rate = 0.01
epochs = 1000

# Initializam ponderile si biasele
weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output = initialize_parameters(input_size, hidden_size, output_size)

# Pregatim datele
X_train, X_test, y_train, y_test = prepare_data()

# Antrenam rețeaua
train_neural_network(X_train, y_train, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output, learning_rate, epochs)

# Realizam predictii pe setul de testare
y_pred = predict(X_test, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output)


_, train_output = forward_propagation(X_train, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output)
final_loss = categorical_crossentropy(np.eye(output_size)[y_train], train_output)
print(f'Eroare finală: {final_loss}')

# Evaluam performanta
acc = accuracy_score(y_test, y_pred)
print("Acuratete pe setul de testare:", acc)

precision = precision_score(y_test, y_pred, average='weighted')
print("Precizie pe setul de testare:", precision)

# Afisam si punctele clasificate eronat
plot_misclassified_points(X_test, y_test, y_pred)