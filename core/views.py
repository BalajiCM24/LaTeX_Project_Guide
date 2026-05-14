from django.shortcuts import render
from django.http import HttpResponse
import os
import subprocess

def home_view(request):
    return render(request, 'core/base.html', {'is_home': True})

def latex2docx_view(request):
    return render(request, 'core/latex2docx.html')

def uppreedit_view(request):
    return render(request, 'core/uppreedit.html')

def uptypeset_view(request):
    return render(request, 'core/uptypeset.html')

def olhtypeset_view(request):
    return render(request, 'core/olhtypeset.html')

def latextoxml_view(request):
    return render(request, 'core/latextoxml.html')

def open_folder(request):
    folder_path = r'\\192.168.1.2\latextoxml\TeX2Docx\Input'
    try:
        # On Windows, os.startfile opens the folder in File Explorer
        os.startfile(folder_path)
        return HttpResponse("Folder opened successfully")
    except Exception as e:
        return HttpResponse(f"Error opening folder: {str(e)}", status=500)
