import abc
from abc import ABC, abstractmethod
from diagnostics.models import Diagnosis
import logging

logger = logging.getLogger("django")

class IDiagnosisRepository(ABC):
    @abstractmethod
    def save(self, name, age, gender, img_bytes, probability, status_c, resul):
        pass
    @abstractmethod
    def get_by_name(self, name):
        pass
    @abstractmethod
    def get_last(self):
        pass

class DiagnosisRepository(IDiagnosisRepository):
    def save(self, name, age, gender, img_bytes, probability, status_c, result):
        try:
            diag, _ = Diagnosis.objects.update_or_create(
                name=name,
                defaults={
                    'age': int(age),
                    'gender': gender,
                    'img': img_bytes,
                    'probability': probability,
                    'status': status_c,
                    'result': result
                }
            )
            return diag
        except Exception as e:
            logger.error(f"DiagnosisRepository error: {e}")
            return None

    def get_by_name(self, name):
        try: return Diagnosis.objects.get(name=name)
        except Diagnosis.DoesNotExist:
            return None

    def get_last(self):
        try: return Diagnosis.objects.last()
        except Diagnosis.DoesNotExist:
            return None