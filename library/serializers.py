from rest_framework import serializers

from library.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(max_length=100)
    # last_name = serializers.CharField(max_length=100)
    # birth_date = serializers.DateField(allow_null=True)
    # country = serializers.CharField(max_length=100)
    #
    class Meta:
        model = Author
        # fields = ['first_name', 'last_name', 'birth_date', 'country']
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer()  # توجه به نام صحیح فیلد (author به جای authors)

    class Meta:
        model = Book  # تعریف مدل مرتبط
        # fields = ['title', 'publish_date', 'pages_count', 'author']  # فیلدهای مورد نظر
        fields = '__all__'

    def validate_pages_count(self, pages_count):
        if pages_count < 5:
            raise serializers.ValidationError('Pages count must be at least 5')
        return pages_count

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.publish_date = validated_data.get('publish_date', instance.publish_date)
        instance.pages_count = validated_data.get('pages_count', instance.pages_count)
        instance.save()
        return instance
