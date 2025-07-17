# students/forms.py

from django import forms
from .models import Student, Group ,Grade




class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'group', 'photo', 'phone', 'email', 'telegram', 'note']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telegram': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}), # Changed for consistency
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    ### REMOVE THE OLD clean() METHOD ###
    # def clean(self):
    #     ... (delete this entire method) ...

    ### ADD THIS NEW METHOD ###
    def clean_full_name(self):
        """
        Check if a student with this name already exists in the selected group.
        """
        full_name = self.cleaned_data.get('full_name')
        group = self.cleaned_data.get('group')

        if full_name and group:
            # Build the query to check for duplicates
            queryset = Student.objects.filter(full_name__iexact=full_name, group=group)
            
            # If we are editing an existing student, we must exclude them from the check.
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)

            # If the queryset still finds a student, a duplicate exists.
            if queryset.exists():
                # Raise an error that will be attached to the 'full_name' field.
                raise forms.ValidationError("A student with this name already exists in this group.")
        
        # Always return the cleaned data for the field.
        return full_name

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Grade
        # +++ ADD 'submission_text' TO THE FIELDS LIST +++
        fields = ['submission_file', 'submission_text']
        widgets = {
            'submission_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            # +++ ADD A WIDGET FOR THE TEXT AREA +++
            'submission_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Type your response here...'}),
        }