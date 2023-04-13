import io
import os

import docx
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import MaskerForm
from .utils import mask_text


def masker(request):
    if request.method == 'POST':
        form = MaskerForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            file = request.FILES.get('file', None)

            if file:
                # If a file was uploaded, read its contents and mask the text
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                filepath = os.path.join(settings.MEDIA_ROOT, filename)

                # Determine the file extension and read the file contents
                _, ext = os.path.splitext(filepath)
                if ext == '.txt':
                    with open(filepath, 'r', encoding='utf-8') as f:
                        file_text = f.read()

                    # Mask the file text
                    file_text = mask_text(file_text)
                elif ext == '.docx':
                    # Load the DOC file using python-docx
                    doc = docx.Document(filepath)

                    # Iterate over all paragraphs in the document
                    for para in doc.paragraphs:
                        # Mask the text in each paragraph
                        para.text = mask_text(para.text)

                    # Iterate over all tables in the document
                    for table in doc.tables:
                        # Iterate over all cells in each table
                        for row in table.rows:
                            for cell in row.cells:
                                # Mask the text in each cell
                                cell.text = mask_text(cell.text)

                    # Save the modified document
                    doc.save(filepath)

                    # Read the modified file contents
                    with open(filepath, 'rb') as f:
                        file_text = f.read()
                else:
                    return HttpResponse('Unsupported file type')

                # Return the file in the appropriate format
                if ext == '.txt':
                    response = HttpResponse(file_text, content_type='text/plain')
                    response['Content-Disposition'] = f'attachment; filename="{filename}'
                elif ext == '.docx':
                    response = HttpResponse(file_text, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                else:
                    return HttpResponse('Unsupported file type')

                return response
            else:
                # If no file was uploaded, mask the entered text and display it on the page
                masked_text = mask_text(text)
                return render(request, 'masker.html', {'form': form, 'masked_text': masked_text, 'text': text})
    else:
        form = MaskerForm()
        return render(request, 'masker.html', {'form': form})
    
def aboutus(request):
    return render(request, 'aboutus.html')