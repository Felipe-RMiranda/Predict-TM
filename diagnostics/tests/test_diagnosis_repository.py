from django.test import TestCase
from ..repositorys import DiagnosisRepository, IDiagnosisRepository
from ..models import Diagnosis

class TestDiagnosisRepository(TestCase):
    def setUp(self):
        self.repo: IDiagnosisRepository = DiagnosisRepository()

    def test_save_creates_new_diagnosis(self):
        diag = self.repo.save(
            name="João",
            age=30,
            gender="M",
            img_bytes=b"fakeimg",
            probability=0.95,
            status_c="OK",
            result="Negativo"
        )
        self.assertIsNotNone(diag)
        self.assertEqual(Diagnosis.objects.count(), 1)
        self.assertEqual(diag.name, "João")

    def test_save_updates_existing_diagnosis(self):
        # cria inicial
        self.repo.save("Maria", 25, "F", b"img1", 0.80, "OK", "Positivo")
        # atualiza
        updated = self.repo.save("Maria", 26, "F", b"img2", 0.85, "OK", "Negativo")

        self.assertEqual(Diagnosis.objects.count(), 1)
        self.assertEqual(updated.age, 26)
        self.assertEqual(updated.result, "Negativo")

    def test_get_by_name_returns_diagnosis(self):
        self.repo.save("Carlos", 40, "M", b"img", 0.70, "OK", "Positivo")
        diag = self.repo.get_by_name("Carlos")
        self.assertIsNotNone(diag)
        self.assertEqual(diag.name, "Carlos")

    def test_get_by_name_returns_none_if_not_found(self):
        diag = self.repo.get_by_name("Inexistente")
        self.assertIsNone(diag)

    def test_get_last_returns_last_diagnosis(self):
        self.repo.save("A", 20, "F", b"img1", 0.60, "OK", "Positivo")
        self.repo.save("B", 22, "M", b"img2", 0.65, "OK", "Negativo")

        last = self.repo.get_last()
        self.assertIsNotNone(last)
        self.assertEqual(last.name, "B")

    def test_get_last_returns_none_if_no_records(self):
        last = self.repo.get_last()
        self.assertIsNone(last)