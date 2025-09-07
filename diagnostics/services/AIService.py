import logging
import os
from abc import ABC, abstractmethod
import cv2
import numpy as np
from tensorflow.keras.models import load_model

logger = logging.getLogger("django")

class IAIService(ABC):
    @abstractmethod
    def img_predict(self, img_bytes):
        pass

class AIService(IAIService):
    def __init__(self):
        try:
            model_path = os.path.join('diagnostics', 'cnn_tumor_model.h5')
            self.model = load_model(model_path)
            logger.info("✅ Modelo carregado com sucesso.")
        except Exception as e:
            logger.info(f"❌ Modelo não encontrado em: {model_path}\n[ERROR]: {e}")
            #raise FileNotFoundError(f"❌ Modelo não encontrado em: {model_path}")

    @staticmethod
    def _img_process(img):
        img_bytes = np.asarray(bytearray(img), dtype=np.uint8)
        img_cv2 = cv2.imdecode(img_bytes, cv2.IMREAD_GRAYSCALE)
        if img_cv2 is None:
            raise ValueError("❌ Erro ao carregar imagem!")

        img_cv2 = cv2.resize(img_cv2, (128, 128))
        img_cv2 = img_cv2.astype('float32') / 255.0
        img_cv2 = img_cv2.reshape(1, 128, 128, 1)
        return img_cv2

    def img_predict(self, img_bytes):
        logger.info(f"🔎 Analisando imagem...")
        prob = None
        try:
            prob = self.model.predict(self._img_process(img_bytes))[0][0]
        except Exception as e:
            logger.error(f"predict error: {e}")
        if prob >= 0.5:
            logger.info("🚨 Indício de tumor detectado!")
            return prob, " • Possível presença de tumor (TM). Recomenda-se a apresentação deste documento ao especialista responsável.", "Possível TM detectado"
        else:
            logger.info("✅ Cérebro saudável detectado.")
            return prob, " • Não foi encontrado alterações relevantes.", "Cerebro saudável."