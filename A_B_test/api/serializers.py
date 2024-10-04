from rest_framework import serializers
from A_B_test.models import User, Item


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']

    def to_representation(self, obj):
        # Get the original representation
        ret = super(UserSerializer, self).to_representation(obj)

        # Remove email and password before retrieving it
        ret.pop('email')
        ret.pop('password')

        return ret


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
