from django.views.generic.edit import FormView
from django import forms
from django.contrib import messages
from django.urls import reverse_lazy
from kafka_test.kafka.producer import produce_example_message
from kafka_test.models import ExampleValue
import logging

LOGGER = logging.getLogger(__name__)


class TestForm(forms.ModelForm):
    """
    Form for the ExampleValue
    """
    class Meta:
        model = ExampleValue
        fields = ['value']


class IndexView(FormView):
    """
    It's a form with one field, the value to send
    """
    template_name = 'kafka_test/index.html'
    form_class = TestForm
    # When done, redirect back to this page
    success_url = reverse_lazy('kafka-test')

    def form_valid(self, form):
        """
        The form itself is good, try sending it as a message
        """
        try:
            value = form.cleaned_data.get('value')
            produce_example_message(value)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                "Added to queue: '%s'" % value,
            )
            LOGGER.debug("Added to queue: %s", value)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            messages.add_message(
                self.request,
                messages.ERROR,
                "Uh oh! %s" % e,
            )
        # Those operations set a message in the response
        # but the response itself is always the form looking ok
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add data to the template context
        """
        context = super().get_context_data(**kwargs)
        # Include the last few processed items
        context['recent'] = ExampleValue.objects.order_by('-created_date')[:20]
        return context
