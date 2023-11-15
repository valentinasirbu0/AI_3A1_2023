import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# X_train   pe care ne antrenam
# X_test    pe care testam
# y_train   rezultatele care ar trebui sa fie
# y_test    rezultatele obtinute de noi
# 0.3 din date pentru testare

#functia sigmoidala - strat ascuns
#softmax - strat iesire


def prepare_data():
    column_names = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"]
    data = pd.read_csv('C:\\Users\\Valea\\Desktop\\ai\\Lab6\\seeds_dataset.txt', sep="\s+", names=column_names)
    x = data.iloc[:, :-1].values  # scot ultima coloana din date
    y = data.iloc[:, -1].values - 1  # ultima coloana - rezultatul
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    # incercam sa aducem la medie zero și o deviație standard de 1
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test


def initialize_parameters(input_size, hidden_size, output_size):
    np.random.seed(42)
    weights_input_hidden = np.random.uniform(low=-1, high=1, size=(input_size, hidden_size))
    weights_hidden_output = np.random.uniform(low=-1, high=1, size=(hidden_size, output_size))
    return weights_input_hidden, weights_hidden_output


def forward_propagation(X, weights_input_hidden, weights_hidden_output):
    hidden_input = np.dot(X, weights_input_hidden)
    hidden_output = sigmoid(hidden_input)

    output_input = np.dot(hidden_output, weights_hidden_output)
    output = softmax(output_input)

    return hidden_output, output


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


def error_function(y_true, y_pred):
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.sum(y_true * np.log(y_pred)) / len(y_true)









X_train, X_test, y_train, y_test = prepare_data()
learning_rate = 0.01

weights_input_hidden, weights_hidden_output = initialize_parameters(input_size=7, hidden_size=5, output_size=3)

for epoch in range(1000):  # range prea mare se poate produce overfitting

    hidden_output, output = forward_propagation(X_train, weights_input_hidden, weights_hidden_output)
    loss = error_function(np.eye(3)[y_train], output)
    output_error = output - np.eye(3)[y_train]
    hidden_error = np.dot(output_error, weights_hidden_output.T) * sigmoid_derivative(hidden_output)
    weights_hidden_output -= learning_rate * np.dot(hidden_output.T, output_error)
    weights_input_hidden -= learning_rate * np.dot(X_train.T, hidden_error)

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss}")


_, test_output = forward_propagation(X_test, weights_input_hidden, weights_hidden_output)
predicted_labels = np.argmax(test_output, axis=1)


# Evaluate accuracy
accuracy = accuracy_score(y_test, predicted_labels)
print(f"Accuracy on test set: {accuracy}")

# Print additional metrics
print("Classification Report:\n", classification_report(y_test, predicted_labels))
print("Confusion Matrix:\n", confusion_matrix(y_test, predicted_labels))