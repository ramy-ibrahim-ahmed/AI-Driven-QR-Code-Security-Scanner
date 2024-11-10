import pickle
from keras import preprocessing, models, metrics, backend


class F1Score(metrics.Metric):
    def __init__(self, name="f1_score", **kwargs):
        super(F1Score, self).__init__(name=name, **kwargs)
        self.precision = metrics.Precision()
        self.recall = metrics.Recall()

    def update_state(self, y_true, y_pred, sample_weight=None):
        self.precision.update_state(y_true, y_pred, sample_weight)
        self.recall.update_state(y_true, y_pred, sample_weight)

    def result(self):
        precision = self.precision.result()
        recall = self.recall.result()
        return 2 * (precision * recall) / (precision + recall + backend.epsilon())

    def reset_states(self):
        self.precision.reset_states()
        self.recall.reset_states()

    def get_config(self):
        config = super(F1Score, self).get_config()
        return config


net = models.load_model(r"assets\URL_version_1\net1.keras", custom_objects={"F1Score": F1Score})

with open(r"assets\URL_version_1\tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)


def predict(url_string, model=net, tokenizer=tokenizer, max_sequence_length=300):
    sequence = tokenizer.texts_to_sequences([url_string])
    padded_sequence = preprocessing.sequence.pad_sequences(
        sequence, maxlen=max_sequence_length
    )
    propability = model.predict(padded_sequence)
    prediction = (propability > 0.5).astype("int32")

    return 1 if prediction[0] == 1 else 0, (
        propability[0][0] if prediction[0] == 1 else 1 - propability[0][0]
    )


# benign = "https://www.stubhub.com/jon-faddis-jazz-orchestra-tickets/"
# malware = "http://atel.se/wp-includes/SimplePie/Count/be7baa518d258efbb611498d0af83455/"

# prediction, propability = predict(url_string=benign)
# print(f"{prediction} with probability {(propability * 100):0.2f}%")
