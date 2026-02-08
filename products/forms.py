from django import forms
from .models import Product, ProductInstruction, Order
from tinymce.widgets import TinyMCE

TINYMCE_COMMON_ATTRS = {
    "plugins": "image link code lists table color",
    "toolbar": (
        "undo redo | styles | bold italic underline forecolor backcolor | "
        "alignleft aligncenter alignright | bullist numlist outdent indent | "
        "link image | code"
    ),
    "images_upload_url": "/admin/tinymce-upload/",
    "relative_urls": False,
    "remove_script_host": False,
    "content_style": "body { font-family: Poppins, Helvetica, Arial, sans-serif; font-size: 14px }",
}


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs=TINYMCE_COMMON_ATTRS))
    standards_and_approval = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs=TINYMCE_COMMON_ATTRS))

    class Meta:
        model = Product
        fields = "__all__"


class ProductInstructionAdminForm(forms.ModelForm):
    instruction_steps = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs=TINYMCE_COMMON_ATTRS))

    class Meta:
        model = ProductInstruction
        fields = "__all__"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'remarks']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-brand focus:border-brand', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-brand focus:border-brand', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-brand focus:border-brand', 'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-brand focus:border-brand', 'placeholder': '+1 234 567 890'}),
            'remarks': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-brand focus:border-brand', 'rows': 3, 'placeholder': 'Any special requests?'}),
        }
