from djng.forms import NgModelFormMixin, NgModelForm


class QModelForm(NgModelFormMixin, NgModelForm):
    class Meta:
        abstract = True

    @property
    def is_new(self):
        return self.instance.pk is None

    @property
    def is_existing(self):
        return not self.is_new()
