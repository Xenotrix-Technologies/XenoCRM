import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def health_check(request):
    return HttpResponse("OK")

@csrf_exempt
def cloudinary_test_view(request):
    if request.method == 'POST' and request.FILES.get('test_file'):
        file = request.FILES['test_file']
        # Save file using default_storage (Cloudinary)
        path = default_storage.save(f"test_uploads/{file.name}", ContentFile(file.read()))
        # Retrieve public URL
        file_url = default_storage.url(path)
        
        return HttpResponse(f"""
            <h3>Upload Successful!</h3>
            <p>File saved at path: {path}</p>
            <p>Cloudinary URL: <a href="{file_url}" target="_blank">{file_url}</a></p>
            <img src="{file_url}" style="max-width: 300px; margin-top: 20px;" />
            <br/><br/><a href="/cloudinary-test/">Upload another</a>
        """)
        
    return HttpResponse("""
        <h2>Cloudinary Storage Test</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="test_file" required>
            <button type="submit">Upload to Cloudinary</button>
        </form>
    """)
