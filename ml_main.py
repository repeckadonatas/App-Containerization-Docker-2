import source.ml_model as mlm
import source.logger as log
from source.constants import *

ml_train_logger = log.app_logger(__name__)

try:
    model = mlm.Model(COMMODITIES, 12, 1)
    for col in TRAINING_DATA_COLUMNS:
        model.train(col)
        model.save(f"model_{col}")
        
except Exception as e:
    ml_train_logger.error('An error occured while training the model: {}'.format(e))

