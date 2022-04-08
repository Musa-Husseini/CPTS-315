from random import shuffle

STOP_LIST = 'stoplist.txt'
TRAIN_DATA = 'traindata.txt'
TRAIN_LABELS = 'trainlabels.txt'
TEST_DATA = 'testdata.txt'
TEST_LABELS = 'testlabels.txt'

OUT_FILE = 'output2.txt'


# Read in the file
def read_input(file):
    # reading in data
    with open(file, "r") as text_file:
        all_lines = text_file.read().splitlines()

    return all_lines


# file dumping
def dump_output(training_results, test_results):
    # First block of required output
    with open(OUT_FILE, "w") as text_file:
        test_accuracy = test_results["accuracy"]

        for iteration, data in training_results.items():
            text_file.write(f"Iteration{iteration + 1} {data['incorrect']}\n")

        text_file.write("\n")

        for iteration, data in training_results.items():
            text_file.write(f"Iteration{iteration + 1} {data['accuracy']} {test_accuracy}\n")

    return


def build_vocabulary(training_lines, stop_list):
    # create a set of all the words in the fortune cookies that are not stop words
    print("Cleaning vocabulary")
    vocabulary = sorted(
        list(set([word for sentence in training_lines for word in sentence.split() if word not in stop_list])))
    print("done")

    return vocabulary


def create_feature_vectors(training_lines, vocabulary, stop_list):
    feature_vectors = []

    # split the training lines to a list of lists of strings
    split_lines = [line.split() for line in training_lines]

    for line in split_lines:

        current_vector = []

        # if the current word in the vocab is in the current line, append a 1, if not, append a zero
        # this produces a vector of size len(vocab), where the ith index of the vector will be a 1 if the ith word in
        # vocab is present in the current line
        for word in vocabulary:
            current_vector.append(1) if word in line else current_vector.append(0)

        feature_vectors.append(current_vector)

    # return the fruits of our labor
    return feature_vectors


def binary_classifier_algorithm(feature_vectors, training_labels, number_of_iterations):
    # initialize the weight vector + bias
    w = [0] * len(feature_vectors[0])
    b = 0
    results = {}

    # start training
    for iteration in range(number_of_iterations):

        correct_answers = 0
        mistakes = 0

        # generate the order of training examples that we'll be iterating over
        r = list(range(len(feature_vectors)))
        shuffle(r)

        for i in r:

            # compute the activation
            a = compute_activation(weight_vector=w, feature_vector=feature_vectors[i], bias=b)

            # pull the correct answer from the training labels list
            correct_answer = int(training_labels[i]) if int(training_labels[i]) == 1 else -1

            if correct_answer * a <= 0:
                w = update_weights(weight_vector=w, feature_vector=feature_vectors[i], correct_answer=correct_answer)
                b += correct_answer
                mistakes += 1
            else:
                correct_answers += 1

        results[iteration] = {"correct": correct_answers,
                              "incorrect": mistakes,
                              "accuracy": correct_answers / (correct_answers + mistakes)}

    return w, b, results


def compute_activation(weight_vector, feature_vector, bias):
    vector_summation = 0

    for i in range(len(feature_vector)):
        vector_summation += (weight_vector[i] * feature_vector[i])

    vector_summation += bias

    return vector_summation


def update_weights(weight_vector, feature_vector, correct_answer):
    new_weight_vector = [0] * len(weight_vector)

    for i in range(len(weight_vector)):
        new_weight_vector[i] = weight_vector[i] + (feature_vector[i] * correct_answer)

    return new_weight_vector


def perceptron_tests(weight_vector, bias, test_lines, test_labels, number_of_iterations):
    # generate the order of training examples that we'll be iterating over
    r = list(range(len(test_lines)))

    # start training

    correct_answers = 0
    mistakes = 0

    for i in r:
        # compute the activation
        a = compute_activation(weight_vector=weight_vector, feature_vector=test_lines[i], bias=bias)

        if a <= 0:
            a = 0
        else:
            a = 1

        correct_answer = int(test_labels[i])

        if a == correct_answer:
            correct_answers += 1
        else:
            mistakes += 1

    return {"correct": correct_answers,
            "incorrect": mistakes,
            "accuracy": correct_answers / (correct_answers + mistakes)}


def main():
    # Fortune Cookie classification

    # Pre-process steps
    # ********************************************************
    # Read in the training data
    print("Reading training data")
    training_lines = read_input(TRAIN_DATA)
    print("Done")

    # Read in the training labels
    print("Reading training labels")
    training_labels = read_input(TRAIN_LABELS)
    print("Done")

    # Read in the stop list
    print("Reading stop list")
    stop_list = read_input(STOP_LIST)
    print("Done")

    print("Building vocabulary")
    vocabulary = build_vocabulary(training_lines, stop_list)
    print("Done building vocabulary")

    # Create training feature vectors
    print("Creating training feature vectors")
    training_feature_vectors = create_feature_vectors(training_lines=training_lines, vocabulary=vocabulary,
                                                      stop_list=stop_list)
    print("Done")

    # Read in test data
    print("Reading test data")
    test_lines = read_input(TEST_DATA)
    print("Done")

    # Read in the test labels
    print("Reading test labels")
    test_labels = read_input(TEST_LABELS)
    print("Done")

    # Create test feature vectors
    print("Creating test feature vectors")
    test_feature_vectors = create_feature_vectors(training_lines=test_lines, vocabulary=vocabulary, stop_list=stop_list)
    print("Done")

    # Train with provided examples
    print("Training..")
    weight_vector, bias, training_results = binary_classifier_algorithm(training_feature_vectors, training_labels, 20)
    print("Done")

    # Run perceptron tests
    print("Running perceptron tests")
    perceptron_test_results = perceptron_tests(weight_vector=weight_vector, bias=bias, test_lines=test_feature_vectors,
                                               test_labels=test_labels, number_of_iterations=20)
    print("done")

    dump_output(training_results, perceptron_test_results)
    print(f"Results data written! Please see {OUT_FILE} for results.")


if __name__ == '__main__':
    main()