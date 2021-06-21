from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.files import File

import requests
import json
from . import validate
        
def request_api(sub_url,payload=None,method="POST"):
    url = "http://127.0.0.1:8000/api/"+sub_url

    headers = {'Content-Type': 'application/json'}

    response = requests.request(method, url, headers=headers, data=payload)

    return response

def request_api_file(box_id,file_name,store_file_name):
    url = "http://127.0.0.1:8000/api/files_create/"
    payload={'sect_box_id': box_id,
            'file_name': file_name}
    files=[
  ('file_url',(f'{store_file_name}',open(f'media\\junk\\{store_file_name}','rb')))
    ]
    headers = {
  'Cookie': 'csrftoken=O55ihKVFEVHqVeRhocJmav7jS55E4FnPsZAmcse6mI1waGNqEPQ69JJnKwD0V8lk'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response

# Create your views here.
def index(request):

    if request.method == "GET":
        if request.session.has_key('id'):
            return redirect(home)
        return render(request,'index.html')

    elif request.method == "POST":
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        payload = json.dumps({
            "user_name": user_name,
            "password": password
        })
        response = request_api("login/",payload)

        if response.ok:
            response_json = json.loads(response.text)
            request.session['id'] = response_json['user_id']
            request.session['holder'] = True

            return redirect(home)
        else:
            messages.error(request,'Wrong credentials')
    
        return render(request,'index.html')

def code_login(request):
    if request.method=="POST":
        code = request.POST.get('code')
        response = request_api(f'code_login/{code}/',payload=None,method="GET")

        if response.ok:
            response_json = json.loads(response.text)
            request.session['id'] = response_json['user_id'] 
            request.session['holder'] = False           

            return redirect(home)
        else:
            messages.error(request,"No such code exists")
            return redirect(index)

def register(request):
    if request.method == "GET":
        return render(request,'register.html')
    else:
        
        name = request.POST.get('name')
        user_name = request.POST.get('user-name')
        email = request.POST.get('email') 
        password = request.POST.get('password')
        password2 = request.POST.get('re_password')

        payload = json.dumps({
        "name": name,
        "user_name": user_name,
        "password": password,
        "email": email
        })

        if password==password2:
            error = validate.validate_register(request,user_name,email)
            if not error:
                response = request_api("register/",payload)
                if response.ok:
                    messages.success(request,"Account created successfully!!!\nLogin to continue")
                    return redirect(index)
        else:
            messages.error(request,"re-password didn't match the password")

        return render(request,'register.html')


def home(request,holder=False):
    if request.method == "GET":

        all_section={}

        if request.session.has_key('id'):
            user_id = request.session['id']
            holder = request.session['holder']

            response = request_api(f"sections/{user_id}/",payload=None,method="GET")
            sections = json.loads(response.text)
        
            all_section = []
            for section in sections:

                sect_name = section['section_name']
                sect_id = section['section_id']

                response = request_api(f"boxes/{sect_id}/",payload=None,method="GET")
                boxes = json.loads(response.text)
                sect_boxes = []
                for box in boxes:
                    box_id = box['sect_box_id']
                    box_name = box['box_name']
                    sect_boxes.append([box_id,box_name])
                # sort as data from json is unordered
                sect_boxes.sort(key=lambda x:x[0])

                all_details = [sect_id,sect_name,sect_boxes]
                all_section.append(all_details)
            # sort all_section[]
            all_section.sort(key=lambda x:x[0])

            # get user data
            response = request_api(f"users/{user_id}/",payload=None,method="GET")
            user = json.loads(response.text)
            return render(request,'home.html',{'user':user,'sections':all_section,'holder':holder})
        else:
            return redirect(index)
    else:
        return redirect(index)

def section_create(request):
    if request.method == "POST":
        payload = json.dumps({
            "section_name":request.POST.get('section'),
            "user_id" : request.session['id']
        })
        response = request_api("sections_create/",payload)
        response_json = json.loads(response.text)
        if not response.ok:
            messages.warning(request,response_json["message"])
        else:
            messages.success(request,"Section created successfully")
        return redirect(home)

def section_edit(request,section_id):
    if request.method == "POST":
        payload = json.dumps({
            "section_name":request.POST['section'],
            "section_id":section_id,
            "user_id":request.session['id']
        })
        response = request_api("sections_edit/",payload,method="POST")
        response_json = json.loads(response.text)
        if not response.ok:
            messages.warning(request,response_json["message"])
        else:
            messages.success(request,"Section edited successfully")
        return redirect(home)

def section_delete(request,section_id):
        
        response = request_api(f"sections_delete/{section_id}/",payload=None)
        response_json = json.loads(response.text)
        if not response.ok:
            messages.warning(request,response_json["message"])
        else:
            messages.success(request,"Section deleted successfully")
        return redirect(home)

def box_create(request,section_id):
    if request.method == "POST":
        payload = json.dumps({
            "box_name":request.POST.get('box'),
            "section_id" : section_id
        })
        response = request_api("boxes_create/",payload)
        response_json = json.loads(response.text)
        if not response.ok:
            messages.warning(request,response_json["message"])
            pass
        else:
            messages.success(request,"Box created successfully")
        return redirect(home)
        
def box_edit(request,box_id):
    if request.method == "POST":
        payload = json.dumps({
            "box_name":request.POST.get('box'),
            "sect_box_id":box_id,
            "section_id":request.POST.get('sect_id')
        })
        response = request_api("boxes_edit/",payload,method="POST")
        response_json = json.loads(response.text)
        if not response.ok:
            messages.warning(request,response_json["message"])
        else:
            messages.success(request,"Box edited successfully")
        return redirect(home)

def box_delete(request,box_id):
        
        response = request_api(f"boxes_delete/{box_id}/",payload=None)
        response_json = json.loads(response.text)
        if not response.ok:
            messages.warning(request,response_json["message"])
        else:
            messages.success(request,"Box deleted successfully")
        return redirect(home)


def view(request,box_id):
    if request.method == "GET":
        if request.session.has_key('id'):
            
            response = request_api(f'files/{box_id}/',payload=None,method="GET")
            file_detail = json.loads(response.text)
            holder = request.session['holder']

            def sort_file(ele):
                value = list(ele.values())
                return value[0]

            file_detail.sort(key=sort_file)
            # get sect and box name
            response = request_api(f'boxes_detail/{box_id}',method="GET")
            name = json.loads(response.text)
            return render(request,'view.html',{'files':file_detail,'box_id':box_id,'name':name,'holder':holder})
        else:
            return redirect(index)

def file_create(request,box_id):
    if request.method == "POST":
        file_name = request.POST.get('file')
        files = request.FILES.getlist('files')
        fs = FileSystemStorage(location='media/junk')
        print("len:",len(files))
        for file_ in files:
            if(len(file_name)==0):
                file_name = file_.name
            # file_exist = fs.exists(file_name)
            # if file_exist:
            #     file_name = fs.get_available_name(file_name,max_length=15)
            #     messages.warning(request,"File name already exists so saved as: "+file_name)

            store_file_name = fs.save(file_.name,file_)
            print("file_name:",file_name)
            print("store_file_name:",store_file_name)
            print("file_.name:",file_.name)
            
            response = request_api_file(box_id,file_name,store_file_name)
            response_json = json.loads(response.text)
            if not response.ok:
                messages.warning(request,response_json["message"])

            else:
                messages.success(request,"File addedd successfully")
            file_name=""
        return redirect(view,box_id=box_id)

def file_edit(request,box_id,file_id):
    if request.method == "POST":
       
        payload = json.dumps({
            "file_name":request.POST.get('file_name'),
            "file_id":file_id,
            "sect_box_id":box_id,
        })
        response = request_api("files_edit/",payload,method="POST")
        response_json = json.loads(response.text)
        if not response.ok:
            messages.warning(request,response_json["message"])
        else:
            messages.success(request,"Box edited successfully")
        return redirect(view,box_id=box_id)

def file_delete(request,box_id,file_id):
    response = request_api(f"files_delete/{file_id}/",payload=None)
    response_json = json.loads(response.text)
    if not response.ok:
        messages.warning(request,response_json["message"])
    else:
        messages.success(request,"File deleted successfully")
    return redirect(view,box_id=box_id)

def logout(request):
    try:
        del request.session['id']
        del request.session['holder']
    except:
        pass

    return redirect(index)
    