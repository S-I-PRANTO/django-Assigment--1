from django.shortcuts import render


def No_permission(request):
    return render(request,'No_permission.html')
