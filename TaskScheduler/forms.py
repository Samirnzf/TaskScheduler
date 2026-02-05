from django import forms
from .models import Task, Location

class TaskForm(forms.ModelForm):
    # We redefine these to ensure they don't have default labels in the HTML flow if we manually place them
    new_location_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input-field'}))
    new_location_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'input-field'}))
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        empty_label="Select a Location...",  # <--- THIS FIXES THE "------"
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})  # Add a class for styling
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'category']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 bg-white/50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all placeholder-gray-400',
                'placeholder': 'What needs to be done?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 bg-white/50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all placeholder-gray-400',
                'rows': 4,
                'placeholder': 'Add details...'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 bg-white/50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all',
                'type': 'datetime-local'
            }),
            # 2. Add styling for the Priority Dropdown
            'priority': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-white/50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all cursor-pointer'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-white/50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all cursor-pointer'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_loc_name = self.cleaned_data.get('new_location_name')
        if new_loc_name:
            loc, created = Location.objects.get_or_create(
                name=new_loc_name,
                defaults={'address': self.cleaned_data.get('new_location_address')}
            )
            instance.location = loc
        if commit:
            instance.save()
        return instance