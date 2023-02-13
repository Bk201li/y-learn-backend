from rest_framework import serializers
from .models import MyUser, Budget, Categorie, Exercice


class BudgetSerializer(serializers.ModelSerializer):
    categorie_name = serializers.SerializerMethodField('get_category_name')

    def get_category_name(self, obj):
        if obj.categorie_id:
            return obj.categorie.nom

    class Meta:
        model = Budget
        fields = ["id", "short_description", "montant", "type", "date", "categorie", "categorie_name", "utilisateur"]


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = [
            "id",
            "email",
            "password",
            "password2"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = MyUser(
            email=self.validated_data["email"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError({"current_password": "Does not match"})
        return value
        

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'label']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_active', 'total_amount', 'is_admin']

class ExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercice
        fields = ['id', 'label', 'answer', 'doneBy', 'createdBy', 'category']