import numpy as np
from unittest.mock import patch, MagicMock
from django.test import TestCase
from ..services.AIService import IAIService, AIService

class TestAIService(TestCase):
    def setUp(self):
        self.service: IAIService = AIService()
        # mocka load_model para não carregar o modelo real
        with patch("diagnostics.services.AIService.load_model") as mock_load_model:
            mock_model = MagicMock()
            # retorna probabilidade controlada
            mock_model.predict.return_value = np.array([[0.8]])
            mock_load_model.return_value = mock_model
            self.service.model = mock_model

    def test_img_process_ok(self):
        # cria uma imagem fake em bytes (quadrado preto 128x128)
        import cv2
        img = np.zeros((128, 128), dtype=np.uint8)
        _, img_bytes = cv2.imencode(".jpg", img)

        processed = self.service._img_process(img_bytes.tobytes())
        assert processed.shape == (1, 128, 128, 1)
        assert processed.max() <= 1.0

    def test_img_process_invalid(self):
        with self.assertRaises(ValueError):
            self.service._img_process(b"not_an_image")

    def test_predict_tumor(self):
        # mock retorna 0.8 (>= 0.5 → tumor detectado)
        self.service.model.predict.return_value = np.array([[0.8]])
        prob, msg, title = self.service.img_predict(b"fake_bytes")
        assert prob >= 0.5
        assert "tumor" in msg.lower()
        assert "TM" in title

    def test_predict_healthy(self):
        self.service.model.predict.return_value = np.array([[0.2]])  # < 0.5
        prob, msg, title = self.service.img_predict(b"fake_bytes")
        assert prob < 0.5
        assert "saudável" in msg.lower()
        assert "Cerebro saudável" in title