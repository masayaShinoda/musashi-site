from django import forms
from .models import LinkPageDescription
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


class LinkPageDescriptionAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs=TINYMCE_COMMON_ATTRS))

    class Meta:
        model = LinkPageDescription
        fields = "__all__"
