from rest_framework.serializers import ModelSerializer, ValidationError, DictField, FloatField
from .models import Calculator, History
from .parser import evaluate_as_programmer_expr, evaluate_as_standard_expr


class CalculatorSerializer(ModelSerializer):
    class Meta:
        model = Calculator
        fields = ['id', 'mode', 'created_time']
        read_only_fields = ['created_time']

    def validate_mode(self, value):
        if self.instance and value != self.instance.mode:
            raise ValidationError("'mode' should not be changed.")
        return value

    def create(self, validated_data):
        calculator = Calculator(**validated_data, owner=self.context['request'].user)
        calculator.save()
        return calculator


class HistorySerializer(ModelSerializer):
    variables = DictField(child=FloatField(), write_only=True, default={})

    class Meta:
        model = History
        fields = ['id', 'calculator', 'expr', 'result', 'variables']
        read_only_fields = ['result']

    def validate_expr(self, value):
        if self.instance and value != self.instance.expr:
            raise ValidationError("'expr' should not be changed.")
        return value

    def validate_calculator(self, value):
        if self.instance:
            if value != self.instance.calculator:
                raise ValidationError("'calculator' should not be changed.")
        elif self.context['request'].user != value.owner:
            raise ValidationError("No permissions to evaluate expr for this calculator.")
        return value

    def validate(self, data):
        if self.context['request'].method == 'POST':
            res, error = try_to_evaluate_expr(data)
            if error:
                raise ValidationError(error)
            else:
                data['result'] = res
                # pop variables as it has been used only for result calculation
                data.pop('variables')
                return data
        return data

    def create(self, validated_data):
        history = History(**validated_data)
        history.save()
        return history


def try_to_evaluate_expr(data):
    mode = data['calculator'].mode
    variables = data['variables']
    if mode == 'S':
        return evaluate_as_standard_expr(data['expr'], variables)
    elif mode == 'P':
        return evaluate_as_programmer_expr(data['expr'], variables)
