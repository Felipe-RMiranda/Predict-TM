from rest_framework import serializers
from .models import Diagnosis
from .services import ImgService, IImgService

class DiagnosisSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Diagnosis
        fields = ['name', 'age', 'gender', 'img', 'probability', 'status', 'result', 'created_at']

    @staticmethod
    def get_img(obj, service: IImgService = ImgService()):
        return service.toBase64(obj.img)

class DiagnosisRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    gender = serializers.ChoiceField(choices=["Masculino", "Feminino", "Outro"], required=True)
    img = serializers.ImageField(required=True)