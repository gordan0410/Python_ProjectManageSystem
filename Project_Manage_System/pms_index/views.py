from django.shortcuts import render, redirect
from django.views import View
from .forms import ProjectForm, RegisterForm, LoginForm
from .models import Projects, ProjectMembers, VisibilityAttribute, WorkspaceList, ListCard
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json


@login_required(login_url="Login")
def pms_index(request):
    my_projects = []
    projects_list_include_myself_as_owner = ProjectMembers.objects.filter(member_id=request.user).filter(member_status='Owner')
    for projects in projects_list_include_myself_as_owner:
        projects_list_private = Projects.objects.filter(id=projects.project_id_id).filter(visibility_id=1).filter(status='active').values()
        if projects_list_private:
            my_projects.append({'id': projects_list_private[0]['id'], 'name': projects_list_private[0]['name']})

    group_projects = []
    projects_list_include_myself = ProjectMembers.objects.filter(member_id=request.user)
    for projects in projects_list_include_myself:
        projects_list_group = Projects.objects.filter(id=projects.project_id_id).filter(visibility_id=3).filter(status='active').values()
        if projects_list_group:
            group_projects.append({'id': projects_list_group[0]['id'], 'name': projects_list_group[0]['name']})

    public_projects = Projects.objects.filter(visibility_id=2).filter(status='active').values()

    all_users = User.objects.exclude(username=request.user)
    new_project_form = ProjectForm()
    visibility_label = VisibilityAttribute.objects.values_list('visibility', flat=True)
    return render(request, "index.html", locals())


@login_required(login_url="Login")
def create_workspace(request):
    if request.method == "POST":
        new_project_form = ProjectForm(request.POST)
        current_user = request.user
        if new_project_form.is_valid():
            npfform = new_project_form.save(commit=False)
            npfform.status = "active"
            npfform.save()
            member_model = ProjectMembers()
            member_model.project_id = npfform
            member_model.member_status = "Owner"
            member = User.objects.filter(id=current_user.id).first()
            member_model.member_id = member
            member_model.save()
            messages.success(request, "成功新增工作區", extra_tags="Workspace")
            return redirect("/")
        else:
            messages.error(request, "新增工作區失敗", extra_tags="Workspace")
            return redirect("/")


def sign_in(request):

    login_form = LoginForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")

    return render(request, "login.html", locals())


def log_out(request):

    logout(request)

    return redirect('/login')


def register(request):
    register_form = RegisterForm()
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, "註冊成功，請重新登入", extra_tags="Login")
            return redirect("/login")
        else:
            errs = dict(register_form.errors)
            errfields = []
            for errfield in errs.keys():
                errfields.append(errfield)
            messages.error(request, "註冊失敗，請重新輸入", extra_tags="Login")

    return render(request, "register.html", locals())


@login_required(login_url="Login")
def workspace(request, pk):
    workspace_title = Projects.objects.get(id=pk)
    workspace_lists = WorkspaceList.objects.filter(workspace=pk).exclude(status="close").values().order_by('position')
    list_cards = ListCard.objects.all()
    all_lists_cards = {}
    for list_items in workspace_lists:
        card_ids = []
        list_cards = ListCard.objects.filter(list_id=list_items["id"]).exclude(status="close").values().order_by('position')
        for card_items in list_cards:
            card_ids.append(card_items)
            all_lists_cards[list_items["id"]] = card_ids

    return render(request, "workspace.html", locals())


def workspace_list_add(request):
    input_list_name = request.POST.get('add_list_name')
    workspace_id = request.POST.get('workspace_id')
    workspace_obj = Projects.objects.get(id=workspace_id)
    workspace_list_total = WorkspaceList.objects.filter(workspace=workspace_id).exclude(status="close").count()
    workspacelist_model = WorkspaceList()
    workspacelist_model.workspace_id = workspace_obj.id
    workspacelist_model.list_name = input_list_name
    workspacelist_model.position = workspace_list_total + 1
    try:
        workspacelist_model.save()
        data = {"result": "success", "list_name": input_list_name, "list_id": workspacelist_model.id}
        return JsonResponse(data, safe=False)
    except:
        error_message = {"result": "fail"}
        return JsonResponse(error_message, safe=False)


def workspace_card_add(request):
    input_project_name = request.POST.get('add_project_name')
    list_id = request.POST.get('list_id')
    list_obj = WorkspaceList.objects.get(id=list_id)
    list_card_total = ListCard.objects.filter(list=list_id).exclude(status="close").count()
    listcard_model = ListCard()
    listcard_model.list_id = list_obj.id
    listcard_model.card_name = input_project_name
    listcard_model.position = list_card_total + 1
    try:
        listcard_model.save()
        data = {"result": "success", "card_name": input_project_name, "card_id": listcard_model.id}
        return JsonResponse(data, safe=False)

    except:
        error_message = {"result": "fail"}
        return JsonResponse(error_message, safe=False)


def workspace_list_switch(request):
    workspace_id = request.POST.get("workspace_id")
    list_of_all_position_raw = request.POST.get("list_of_all_position").split(",")
    list_of_all_position = [int(i) for i in list_of_all_position_raw]
    original_position_obj = WorkspaceList.objects.filter(workspace=workspace_id).exclude(status="close").order_by('position').values_list('id', flat=True)
    list_of_origin_position = list(original_position_obj)
    for index, value in enumerate(list_of_all_position):
        if list_of_origin_position[index] != value:
            WorkspaceList.objects.filter(id=value).update(position=index+1)
    return JsonResponse(list_of_all_position, safe=False)


def workspace_card_switch(request):
    card_id = request.POST.get("target_id")
    target_list = request.POST.get("target_to_list")
    target_list_card_position_raw = request.POST.getlist("target_to_list_card_order[]")
    previous_list_id = request.POST.get("origin_list_id")
    previous_list_card_position_raw = request.POST.getlist("origin_list_card_order[]")

    previous_list_card_position = [int(i) for i in previous_list_card_position_raw]
    target_list_card_position = [int(i) for i in target_list_card_position_raw]
    target_list_origin = ListCard.objects.get(id=card_id).list_id
    target_list_origin_card_position_raw = ListCard.objects.filter(list=target_list).exclude(status="close").values_list('id', flat=True).order_by('position')
    target_list_origin_card_position = list(target_list_origin_card_position_raw)
    if int(target_list_origin) == int(target_list):
        for index, value in enumerate(target_list_card_position):
            if target_list_origin_card_position[index] != value:
                ListCard.objects.filter(id=value).update(position=index+1)
        return JsonResponse(target_list_origin, safe=False)

    else:
        origin_list_card_position_raw = ListCard.objects.filter(list_id=previous_list_id).exclude(status="close").values_list('id', flat=True).order_by('position')
        origin_list_card_position = list(origin_list_card_position_raw)
        origin_card_obj = ListCard.objects.get(id=card_id)
        origin_card_position = int(origin_card_obj.position)

        target_list_origin_card_position.append(0)
        list_obj = WorkspaceList.objects.get(id=target_list)
        target_list_total_cards = ListCard.objects.filter(list=target_list).exclude(status="close").count()
        try:
            origin_card_obj.list = list_obj
            origin_card_obj.position = target_list_total_cards+1
            origin_card_obj.save()
        except WorkspaceList.DoesNotExist:
            print("error")

        for index, value in enumerate(target_list_card_position):
            if target_list_origin_card_position[index] != value:
                ListCard.objects.filter(id=value).update(position=index+1)

        for index, value in enumerate(origin_list_card_position):
            if index+1 == origin_card_position:
                continue
            elif index+1 > origin_card_position:
                ListCard.objects.filter(id=value).update(position=index)
        return JsonResponse(previous_list_card_position, safe=False)


def workspace_list_delete(request):
    # 前端位置(以list_id排序)比對資料庫位置後, 不相稱則修改
    list_id = request.POST.get('list_id')
    list_position_raw = request.POST.getlist('workspace_list_order[]')
    list_position = [int(i) for i in list_position_raw]
    workspace_list_obj = WorkspaceList.objects.get(id=list_id)
    workspace_id = workspace_list_obj.workspace
    list_position_origin_raw = WorkspaceList.objects.filter(workspace=workspace_id).exclude(status="close").order_by(
        'position').values_list("id", flat=True)
    list_position_origin = list(list_position_origin_raw)
    for index, value in enumerate(list_position):
        if list_position_origin[index] != value:
            WorkspaceList.objects.filter(id=value).update(position=index+1)

    # 判斷列表內是否有剩餘card, 若有則修改card狀態
    list_card_exist = request.POST.get('list_card_exist')
    if list_card_exist == "true":
        list_card_obj = ListCard.objects.filter(list=list_id).exclude(status='close')
        for card in list_card_obj:
            card.position = 0
            card.status = 'close'
            card.save()

    # 修改刪除項目狀態並儲存
    workspace_list_obj.status = "close"
    workspace_list_obj.position = 0
    try:
        workspace_list_obj.save()
        data = {"result": "success"}
        return JsonResponse(data, safe=False)
    except SyntaxError:
        error_message = {"result": "fail"}
        return JsonResponse(error_message, safe=False)


def workspace_card_delete(request):
    # 前端位置(以card_id排序)比對後端位置後, 不相稱則修改
    card_id = request.POST.get('card_id')
    card_position_raw = request.POST.getlist('list_card_order[]')
    card_position = [int(i) for i in card_position_raw]
    list_card_obj = ListCard.objects.get(id=card_id)
    list_id = list_card_obj.list
    card_position_origin_raw = ListCard.objects.filter(list=list_id).exclude(status="close").order_by('position').values_list("id", flat=True)
    card_position_origin = list(card_position_origin_raw)
    for index, value in enumerate(card_position):
        if card_position_origin[index] != value:
            ListCard.objects.filter(id=value).update(position=index+1)

    # 修改刪除項目狀態並儲存, 回傳list_id以利前端辨識重整區塊
    list_card_obj.status = "close"
    list_card_obj.position = 0
    try:
        list_card_obj.save()
        data = {"result": "success", "list_id": list_card_obj.list_id}
        return JsonResponse(data, safe=False)
    except SyntaxError:
        error_message = {"result": "fail"}
        return JsonResponse(error_message, safe=False)


def workspace_card_edit(request):
    if request.method == "GET":
        card_id = request.GET.get('card_id')
        try:
            list_card_obj = ListCard.objects.get(id=card_id)
            data = {"result": "success", "card_content": list_card_obj.card_content}
            return JsonResponse(data, safe=False)
        except:
            data = {"result": "fail"}
            return JsonResponse(data, safe=False)

    elif request.method == "POST":
        card_id = request.POST.get('card_id')
        card_title = request.POST.get('card_title')
        card_content = request.POST.get('card_content')
        list_card_obj = ListCard.objects.get(id=card_id)
        if card_title != list_card_obj.card_name or card_content != list_card_obj.card_content:
            list_card_obj.card_name = card_title
            list_card_obj.card_content = card_content
            list_card_obj.save()
            data = {"result": "success"}
            return JsonResponse(data, safe=False)
        elif card_title == list_card_obj.card_name and card_content == list_card_obj.card_content:
            data = {"result": "no_change"}
            return JsonResponse(data, safe=False)
        else:
            data = {"result": "fail"}
            return JsonResponse(data, safe=False)
