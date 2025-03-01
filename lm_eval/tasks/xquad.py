from .squad import SQuAD2
from math import exp
from functools import partial
import datasets
from lm_eval.base import rf


def _squad_metric(predictions, references):
    squad_metric = datasets.load_metric("squad")
    return squad_metric.compute(predictions=predictions, references=references)


def _squad_agg(key, items):
    predictions, references = zip(*items)
    for prediction in predictions:
        if isinstance(prediction["prediction_text"], list):
            prediction["prediction_text"] = prediction["prediction_text"][0]
    return _squad_metric(predictions=predictions, references=references)[key]


class XQuADBase(SQuAD2):
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = None
    BACKGROUND = "Background:"
    QUESTION = "Question:"
    ANSWER = "Answer:"

    def has_training_docs(self):
        return False

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.
        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        continuation = rf.greedy_until(ctx, {"until": ["\n"]})
        return continuation

    def doc_to_text(self, doc):
        text = (
            self.BACKGROUND
            + "\n\n"
            + doc["context"]
            + "\n\n"
            + self.QUESTION
            + doc["question"]
            + "\n\n"
            + self.ANSWER
        )
        return text

    def process_results(self, doc, results):
        """Take a single document and the LM results and evaluates, returning a
        dict where keys are the names of submetrics and values are the values of
        the metric for that one document
        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param results:
            The results of the requests created in construct_requests.
        """
        continuation = results

        predictions = {
            "id": doc["id"],
            "prediction_text": continuation,
        }

        references = {
            "id": doc["id"],
            "answers": doc["answers"],
        }

        return {
            "exact_match": (
                predictions,
                references,
            ),  # Exact match (the normalized answer exactly match the gold answer)
            "f1": (
                predictions,
                references,
            ),  # The F-score of predicted tokens versus the gold answer
        }

    def aggregation(self):
        """
        :returns: {str: [float] -> float}
            A dictionary where keys are the names of submetrics and values are
            functions that aggregate a list of metrics
        """
        return {
            "exact_match": partial(
                _squad_agg, "exact_match"
            ),  # Exact match (the normalized answer exactly match the gold answer)
            "f1": partial(
                _squad_agg, "f1"
            ),  # The F-score of predicted tokens versus the gold answer
        }

    def higher_is_better(self):
        """
        :returns: {str: bool}
            A dictionary where keys are the names of submetrics and values are
            whether a higher value of the submetric is better
        """
        return {
            "exact_match": True,  # Exact match (the normalized answer exactly match the gold answer)
            "f1": True,  # The F-score of predicted tokens versus the gold answer
        }


class XQuADAr(XQuADBase):  # arabic
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.ar"
    BACKGROUND = ":معرفتي"
    QUESTION = ":سؤال"
    ANSWER = ":إجابه"


class XQuADDe(XQuADBase):  # german
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.de"
    BACKGROUND = "Hintergrund:"
    QUESTION = "Frage:"
    ANSWER = "Antwort:"


class XQuADZh(XQuADBase):  # chinese
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.zh"
    BACKGROUND = "背景:"
    QUESTION = "問題:"
    ANSWER = "答案:"


class XQuADVi(XQuADBase):  # vietnamese
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.vi"
    BACKGROUND = "lý lịch:"
    QUESTION = "câu hỏi:"
    ANSWER = "câu trả lời:"


class XQuADEn(XQuADBase):  # english
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.en"


class XQuADEs(XQuADBase):  # spanish
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.es"
    BACKGROUND = "antecedentes:"
    QUESTION = "pregunta:"
    ANSWER = "respuesta:"


class XQuADHi(XQuADBase):  # hindi
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.hi"
    BACKGROUND = "पृष्ठभूमि:"
    QUESTION = "सवाल:"
    ANSWER = "उत्तर:"


class XQuADEl(XQuADBase):  # greek
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.el"
    BACKGROUND = "Πληροφορίες ιστορικού:"
    QUESTION = "Ερώτηση:"
    ANSWER = "Απάντηση:"


class XQuADTh(XQuADBase):  # thai
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.th"
    BACKGROUND = "พื้นหลัง:"
    QUESTION = "คำถาม:"
    ANSWER = "ตอบ:"


class XQuADTr(XQuADBase):  # turkish
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.tr"
    BACKGROUND = "arka fon:"
    QUESTION = "soru:"
    ANSWER = "Cevap:"


class XQuADRu(XQuADBase):  # russian
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.ru"
    BACKGROUND = "задний план:"
    QUESTION = "вопрос:"
    ANSWER = "отвечать:"


class XQuADRo(XQuADBase):  # romanian
    VERSION = 0
    DATASET_PATH = "xquad"
    DATASET_NAME = "xquad.ro"
    BACKGROUND = "fundal:"
    QUESTION = "întrebare:"
    ANSWER = "Răspuns:"
