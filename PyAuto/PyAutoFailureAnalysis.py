import json
# from failureanalyzer import DataCreation, ModelCreation, UploadJson, Vectorization
import pandas as pd
import re
import nltk
from nltk.stem.porter import PorterStemmer
import logging
import joblib
import os
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import LinearSVC
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
from jinja2 import Template
import webbrowser

# logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logging = logging.getLogger(__name__)

stop_word_list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", 
                  "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
                  'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                  'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 
                  'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
                  'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 
                  'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
                  'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
                  'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
                  'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
                  'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 
                  'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 
                  'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 
                  'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
                  "won't", 'wouldn', "wouldn't"]


class DataCreation:

    def __init__(self, train_dir):
        logging.info("Initializing Data Training")
        self.train_dir = train_dir
        self.ps = PorterStemmer()
        self.all_stopwords = stop_word_list

    def get_dataset(self):
        logging.info("Preparing to read Training Data")
        try:
            dataset = pd.read_csv(self.train_dir, engine='python')
            dataset['clean_log'] = dataset['Failure_Log'].apply(self.clean_up)

            logging.info("Data Trained Successfully")
        except Exception as e:
            logging.error("Error while reading the Training Data csv", e.__cause__)

        return dataset

    def get_retrain_dataset(self, df_retrain):
        logging.info("Preparing to Retraining  Data")
        try:
            df_retrain['clean_log'] = df_retrain['failureLog'].apply(self.clean_up)
            logging.info("Retrain Data cleaned")
        except Exception as e:
            logging.error("Error while cleaning retrain data", e.__cause__)
        return df_retrain

    def clean_up(self, logtext):
        logtext = str(logtext)
        logtext = re.sub('[^a-zA-Z]', ' ', logtext)
        logtext = logtext.lower()
        logtext = logtext.split()
        logtext = [self.ps.stem(word) for word in logtext if not word in set(self.all_stopwords)]
        logtext = ' '.join(logtext)
        return logtext

    def is_text_nlp_data(self, text):
        found = False
        nlp_data = joblib.load("../../resources/nlpdata.pkl")
        split_text = text.split()
        for eachData in nlp_data:
            trainEachData = eachData.split()
            common = set(split_text).intersection(set(trainEachData))
            if len(common) != 0:
                found = True
                break
        return found

class ModelCreation:

    def __init__(self):
        self.classifier = None
        self.classifier_path = "../../resource/classifier.pkl"

    def train(self, X_train, y_train):
        logging.info("Training the machine learning model started")
        try:
            self.classifier = LinearSVC(class_weight='balanced', random_state=0)
            self.classifier.fit(X_train, y_train)
            joblib.dump(self.classifier, self.classifier_path)
            logging.info("Model Trained Successfully")
        except Exception as e:
            logging.error("Failed to train the model", e.__cause__)

    def predict(self, X_test):
        logging.info("Predicting the model")
        classifier = joblib.load(self.classifier_path)
        y_pred = classifier.predict(X_test)
        return y_pred

    def accuracy(self, y_test, y_pred):
        logging.info("Predicting the accuracy")
        cm = confusion_matrix(y_test, y_pred)
        print(accuracy_score(y_test, y_pred))
        pd.crosstab(y_test, y_pred)
        return cm
    
    
class UploadJson:

    def __init__(self, jsondata, train_dir):
        self.jsondata = jsondata
        self.train_dir = train_dir

    def append_data_csv(self):
        logging.info("Updating the train data set")
        try:
            with open(self.train_dir, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for item in self.jsondata['trainingInformation']:
                    writer.writerow([item['failureLog'], item['failureType']])
        except Exception as e:
            logging.error("Error while updating the training Data set", e.__cause__)



class Vectorization:

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.path = "../../resources/vectorized.pkl"

    def create_vectors(self, x_data):
        fitted_obj = self.vectorizer.fit(x_data)
        joblib.dump(self.vectorizer, self.path)
        vectors = fitted_obj.transform(x_data)
        return vectors

    def do_transform(self, x_data):
        fitted_obj = joblib.load(self.path)
        vectors = fitted_obj.transform([x_data])
        return vectors


# def predict_failure(failure_analysis_path):
#     analyzed_data = {}
#     if os.path.isfile(failure_analysis_path+ "/failures.json"):
#         with open(failure_analysis_path+ "/failures.json", 'r') as file:
#             failed_test_json = json.load(file)
#     else: 
#         return None
#     for test_name_details, (reason_for_failure, now_time) in failed_test_json.items():
#         classifier = joblib.load("../../resources/classifier.pkl")
#         dset = DataCreation(None)
#         vec_obj = Vectorization()
#         text_stemmed = dset.clean_up(reason_for_failure)
#         predict_vector = vec_obj.do_transform([text_stemmed])
#         predict_str = str(classifier.predict(predict_vector))
#         # print(predict_str)
#         match_predict = re.findall(r"'(.*?)'", predict_str, re.DOTALL)
#         # print(match_predict)
#         test_suite_split = test_name_details.split("::")
#         test_suite = test_suite_split[0]
#         test_name_split = test_suite_split[1].split("[")
#         test_name = test_name_split[0]
#         if len(test_name_split) == 2:
#             test_data = test_name_split[1][:-1]
#         else:
#             test_data = None
#         match_predict_split = match_predict[0].split('_')
#         if analyzed_data.get(match_predict_split[0], None):
#             analyzed_data[match_predict_split[0]].append((match_predict_split[1],test_name, test_suite, 
#                                                           test_data, reason_for_failure, now_time))
#         else:
#             analyzed_data[match_predict_split[0]] = [(match_predict_split[1], test_name, test_suite, 
#                                                       test_data, reason_for_failure, now_time)]
#         # if analyzed_data.get(match_predict[0], None):
#         #     analyzed_data[match_predict[0]].append((test_name, test_suite, test_data, reason_for_failure))
#         # else:
#         #     analyzed_data[match_predict[0]] = [(test_name, test_suite, test_data, reason_for_failure)]
#         # analyzed_data[test_name] = [reason_for_failure, match_predict]
#     with open(failure_analysis_path+"/analysis.json", 'w') as file:
#         json.dump(analyzed_data, file, indent=4)
# 
#     with open("../../resources/failure_report.html", "r") as html_file:
#         data = html_file.read()
#         t = Template(data)
#     failure_name = list(analyzed_data.keys())
#     count = []
#     for i in analyzed_data.keys():
#         count.append(len(analyzed_data[i]))
#     output = t.render(Title="Failed Test Report", my_list=failure_name, 
#                       analyzed_data = analyzed_data,
#                       graph_count=count)
#     with open(failure_analysis_path + '/failed.html', 'w') as file:
#         file.write(output)
#     webbrowser.open(failure_analysis_path + '/failed.html')



def predict_failure(failure_analysis_path):
    analyzed_data = {}
    if os.path.isfile(failure_analysis_path+ "/failures.json"):
        with open(failure_analysis_path+ "/failures.json", 'r') as file:
            failed_test_json = json.load(file)
    else: 
        return None
    for test_name_details, (reason_for_failure, now_time) in failed_test_json.items():
        classifier = joblib.load("../../resources/classifier.pkl")
        dset = DataCreation(None)
        vec_obj = Vectorization()
        text_stemmed = dset.clean_up(reason_for_failure)
        if dset.is_text_nlp_data(text_stemmed):
            predict_vector = vec_obj.do_transform(text_stemmed)
            print(classifier.predict(predict_vector))
            predict_str = str(classifier.predict(predict_vector))
            match_predict = re.findall(r"'(.*?)'", predict_str, re.DOTALL)
        else:
            match_predict = ["Others"]
        # print(predict_str)
        
        # print(match_predict)
        test_suite_split = test_name_details.split("::")
        test_suite = test_suite_split[0]
        test_name_split = test_suite_split[1].split("[")
        test_name = test_name_split[0]
        if len(test_name_split) == 2:
            test_data = test_name_split[1][:-1]
        else:
            test_data = None
        # match_predict_split = match_predict[0].split('_')
        if analyzed_data.get(match_predict[0], None):
            analyzed_data[match_predict[0]].append((test_name, test_suite, 
                                                          test_data, reason_for_failure, now_time))
        else:
            analyzed_data[match_predict[0]] = [(test_name, test_suite, 
                                                      test_data, reason_for_failure, now_time)]
        # if analyzed_data.get(match_predict[0], None):
        #     analyzed_data[match_predict[0]].append((test_name, test_suite, test_data, reason_for_failure))
        # else:
        #     analyzed_data[match_predict[0]] = [(test_name, test_suite, test_data, reason_for_failure)]
        # analyzed_data[test_name] = [reason_for_failure, match_predict]
    with open(failure_analysis_path+"/analysis.json", 'w') as file:
        json.dump(analyzed_data, file, indent=4)

    with open("../../resources/Failure_Report_New.html", "r") as html_file:
        data = html_file.read()
        t = Template(data)
    graph_data = []
    for key, value in analyzed_data.items():
        graph_data.append([key,len(value)])
    output = t.render(analyzed_data = analyzed_data, graph_data = graph_data)
    with open(failure_analysis_path + '/failed.html', 'w') as file:
        file.write(output)
    webbrowser.open(failure_analysis_path + '/failed.html')


