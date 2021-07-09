from django.views.generic.edit import FormView
from django import forms
from django.contrib import messages
from django.urls import reverse_lazy
from kafka_test.producer import produce_example_message
from kafka_test.models import ExampleValue
import uuid
import logging

LOGGER = logging.getLogger(__name__)


class TestForm(forms.ModelForm):
    class Meta:
        model = ExampleValue
        fields = ['value']


class IndexView(FormView):
    template_name = 'kafka_test/index.html'
    form_class = TestForm
    success_url = reverse_lazy('kafka-test')

    def form_valid(self, form):
        try:
            value = form.cleaned_data.get('value')
            produce_example_message(value)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                "Added to queue: '%s'" % value,
            )
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            messages.add_message(
                self.request,
                messages.ERROR,
                "Uh oh! %s" % e,
            )
        return super().form_valid(form)
