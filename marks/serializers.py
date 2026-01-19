from rest_framework import serializers
from .models import StudentMark


class StudentMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMark
        fields = [
            'id',
            'student',
            'subject',
            'exam_name',
            'marks_obtained',
            'total_marks',
        ]

    def validate(self, data):
        if data['marks_obtained'] > data['total_marks']:
            raise serializers.ValidationError(
                "Obtained marks total marks se zyada nahi ho sakte"
            )
        return data
