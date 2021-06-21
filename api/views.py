from django.shortcuts import render,redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.core.files import File


from .models import user,section,box,files
from .serializer import UserSerializer,SectionSerializer,BoxSerializer,FileSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser

import json

from .password_manage import encrypt,check_password
# Create your views here.


@api_view(["GET","POST"])
def login(request):
    # if request.method == "POST":
        user_name = request.data['user_name']
        password = request.data['password']

        login_user = user.objects.filter(user_name=user_name)

        if login_user.exists():
            login_user = user.objects.get(user_name=user_name)
            auth = check_password(login_user.password,password)
            if auth:
                user_id = user.objects.get(user_name=user_name).user_id
                data = {'message':'Login Authorized','user_id':user_id}
                return Response(data,status=status.HTTP_200_OK)
        
        return Response({'message':'Wrong credentials'},status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def code_login(request,code):
    if user.objects.filter(code=code).exists():
        user_id = user.objects.get(code=code).user_id
        data = {'message':'Code Login Authorized','user_id':user_id}
        return Response(data,status=status.HTTP_200_OK)
    else:
        return Response({'message':'No such code exists'},status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def register(request):
    if request.method=="POST":
        request.data['password'] = encrypt(request.data['password'])        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'success'},status=status.HTTP_201_CREATED)
        
        return Response({'message':'Data not accepted'},status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def users(request,user_id=None):
    if user_id is None:
        user_ = user.objects.all()
        serializer = UserSerializer(user_,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        if user.objects.filter(user_id=user_id).exists():
            user_ = user.objects.get(user_id=user_id)
            serializer = UserSerializer(user_)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"message":"User_id not present"},status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def sections(request,user_id=None):
    
    if request.method=="GET":
        if user_id is None:
            all_section = section.objects.all()
            serializer = SectionSerializer(all_section,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            if user.objects.filter(user_id=user_id).exists():
                section_ = section.objects.filter(user_id=user_id)
                serializer = SectionSerializer(section_,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'message':'User not found'},status=status.HTTP_404_NOT_FOUND)

@api_view(["POST","PUT"])
def sections_create(request):
    if request.method == "POST":
        user_id = request.data['user_id']
        sect_name = request.data['section_name']
        if user.objects.filter(user_id=user_id).exists():
            if not section.objects.filter(user_id=user_id,section_name=sect_name).exists():
                serializer = SectionSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message":"Section create successful"},status=status.HTTP_202_ACCEPTED)
                else:
                    msg = "Data not valid"+" [ maximum length is 25 ]"
                    return Response({"message":msg},status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"message":"Section alreasy exists"},status=status.HTTP_403_FORBIDDEN)               
        else:
            return Response({"message":"User doesn't exist"},status=status.HTTP_404_NOT_FOUND)
    

@api_view(["POST"])
def sections_edit(request):
    if request.method == "POST":
        section_id = request.data['section_id']
        section_name = request.data['section_name']
        user_id = request.data['user_id']

        if section.objects.filter(section_id=section_id).exists():
            if not section.objects.filter(user_id=user_id,section_name=section_name).exists():
                section_ = section.objects.get(section_id=section_id)
                serializer = SectionSerializer(instance=section_,data=request.data)
                if serializer.is_valid():
                    serializer.save(update_fields=['section_name'])
                    return Response({"message":"Section edit successful"},status=status.HTTP_202_ACCEPTED)
                else:
                    msg = "Data not valid"+" [ maximum length is 25 ]"
                    return Response({"message":msg},status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"message":"Section alreasy exists"},status=status.HTTP_403_FORBIDDEN)               
        else:
            return Response({"message":"Section doesn't exist"},status=status.HTTP_404_NOT_FOUND)
   
@api_view(["POST","DELETE"])
def sections_delete(request,section_id):
    if request.method == "POST" or True:
        if section.objects.filter(section_id=section_id).exists():
            section_ = section.objects.get(section_id=section_id)
            section_.delete()
            return Response({'message':'Section deleted'},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Section doesn't exist"},status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def boxes(request,section_id=None):
    
    if request.method=="GET":
        if section_id is None:
            all_box = box.objects.all()
            serializer = BoxSerializer(all_box,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            if section.objects.filter(section_id=section_id).exists():
                box_ = box.objects.filter(section_id=section_id)
                serializer = BoxSerializer(box_,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"message":"Section doens't exist"},status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def boxes_create(request):
    if request.method =="POST":
        section_id = request.data['section_id']
        box_name = request.data['box_name']
        if section.objects.filter(section_id=section_id).exists():
            if not box.objects.filter(section_id=section_id,box_name=box_name).exists():
                serializer = BoxSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    msg = "Data not valid"+" [ maximum length is 25 ]"
                    return Response({"message":msg},status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"message":"Box already exists"},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message":"Section doesn't exist"},status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def boxes_edit(request):
    if request.method == "POST":
        box_name = request.data['box_name']
        sect_box_id = request.data['sect_box_id']
        section_id = request.data['section_id']

        if box.objects.filter(sect_box_id=sect_box_id).exists():
            if not box.objects.filter(section_id=section_id,box_name=box_name).exists():
                box_ = box.objects.get(sect_box_id=sect_box_id)
                serializer = BoxSerializer(instance=box_,data=request.data)
                if serializer.is_valid():
                    serializer.save(update_fields=['box_name'])
                    return Response({"message":"Box name edit successful"},status=status.HTTP_202_ACCEPTED)
                else:
                    msg = "Data not valid"+" [ maximum length is 25 ]"
                    return Response({"message":msg},status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"message":"Box already exists"},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message":"Box doesn't exist"},status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def boxes_delete(request,sect_box_id):
    if request.method == "POST":
        if box.objects.filter(sect_box_id=sect_box_id).exists():
            box_ = box.objects.get(sect_box_id=sect_box_id)
            box_.delete()
            return Response({'message':'Box deleted'},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Box doesn't exist"},status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def boxes_detail(request,sect_box_id):
    if request.method=="GET":
        if box.objects.filter(sect_box_id=sect_box_id).exists():
            box_ = box.objects.get(sect_box_id=sect_box_id)
            print(box_.section_id)
            box_name = box_.box_name
            section_ = box_.section_id
            sect_name = section.objects.get(section_id=section_.section_id).section_name
            return Response({'box':box_name,'section':sect_name},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Box doesn't exist"},status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def filesdoc(request,box_id=None):
    
    if request.method=="GET":
        if box_id is None:
            all_files = files.objects.all()
            serializer = FileSerializer(all_files,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            if box.objects.filter(sect_box_id=box_id).exists():
                files_ = files.objects.filter(sect_box_id=box_id)
                serializer = FileSerializer(files_,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"message":"Box doens't exist"},status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def files_create(request):
    if request.method =="POST":
        sect_box_id = request.data['sect_box_id']
        
        if box.objects.filter(sect_box_id=sect_box_id).exists():
            serializer = FileSerializer(data=request.data,context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"message":"Data not valid"},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message":"Box doesn't exist"},status=status.HTTP_226_IM_USED)

@api_view(["POST"])
def files_edit(request):
    if request.method == "POST":
        file_name = request.data['file_name']
        file_id = request.data['file_id']

        if files.objects.filter(file_id=file_id).exists():
            file_ = files.objects.get(file_id=file_id)
            serializer = FileSerializer(instance=file_,data=request.data)
            if serializer.is_valid():
                serializer.save(update_fields=['file_name'])
                return Response({"message":"File name edit successful"},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message":"Data not valid"},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message":"File doesn't exist"},status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def files_delete(request,file_id):
    if request.method == "POST":
        if files.objects.filter(file_id=file_id).exists():
            file_ = files.objects.get(file_id=file_id)
            file_.delete()
            return Response({'message':'file deleted'},status=status.HTTP_200_OK)
        else:
            return Response({"message":"file doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        