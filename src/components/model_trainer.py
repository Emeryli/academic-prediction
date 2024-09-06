# import
import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

# config class
@dataclass
class DataTrainerConfig:
    train_model_file_path = os.path.join('artifacts', 'model.pkl')

# trainer class
class DataTrainer:
    def __init__(self):
        # attribute
        self.model_trainer_config = DataTrainerConfig()

    # initialize
    def initial_model_trainer(self, train_array, test_array):
        try:
            # X, y train and test
            X_train = train_array[:,:-1]
            X_test = test_array[:,:-1]
            y_train = train_array[:,-1]
            y_test = test_array[:,-1]
            logging.info("Created X, y train and test arrays")
            # models: dict
            models = {
                "Random Forest":RandomForestRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Classifier":KNeighborsRegressor(),
                "XGBClassifier":XGBRegressor(),
                "CatBoosting Classifier":CatBoostRegressor(verbose=False),
                "AdaBoost Classifier":AdaBoostRegressor()
            }
            # use dict to store the result of evaluating models
            results = evaluate_models(X_train, y_train, X_test, y_test, models)
            logging.info("Models have been evaluated")
            # get the best model score
            best_model_score = max(results.values())
            # get the name of the model
            max_key = max(results, key=results.get)
            # raise exception if the the best score is below 0.6
            if best_model_score < 0.6:
                logging.info("All models' r2 scores are below 0.6")
                raise CustomException("No best model found")
            else:
                logging.info(f"Best model is {max_key}, which has a score of {best_model_score}")
            
            save_object(file_path=self.model_trainer_config.train_model_file_path,
                        obj=max_key)
            return best_model_score            
        except Exception as e:
            raise CustomException(e, sys)
