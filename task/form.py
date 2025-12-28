from django import forms
from task.models import Event,Category,Participant

class Maxin:

    basestyle='border rounded-lg p-2 mb-2 '
    def apply_style(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':f"{self.basestyle} w-2/6  ",
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':f"{self.basestyle} w-4/6",
                     'placeholder':f"Enter {field.label.lower()}"
                })
            else:
                 field.widget.attrs.update({
                 })


class CategoryForm(Maxin,forms.ModelForm):
    class Meta:
        model=Category
        fields=['Event_Categorys','description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()


class EventForm(Maxin,forms.ModelForm):
    class Meta:
        model=Event
        fields=['Event_Name','description','data','time','location']
        widgets = {
                    'data': forms.SelectDateWidget(
                    attrs={
                        'class': 'border rounded-lg p-2 mb-2'

                        }),
                    'time': forms.TimeInput(
                        format='%H:%M',
                        attrs={
                            'type': 'time',
                            'class': 'rounded border-2 border-gray-300 mt-2 mb-3 w-full px-2 py-1'
                        })
                        
                    }
        labels = {
            'data': 'Event Date',
            'time': 'Event Time',
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()
    


class ParticipantForm(Maxin,forms.ModelForm):
    class Meta:
        model=Participant
        fields=['Participant','description','Event']
        widgets = {
            'Event': forms.CheckboxSelectMultiple
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()

    


