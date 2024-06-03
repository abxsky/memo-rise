from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_kb = 1000

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Le fichiers ne doit pas dépasser {max_size_kb} Kilobytes!')