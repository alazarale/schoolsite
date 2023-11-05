from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse, HttpResponse, FileResponse
from .forms import AccadamicYearForm
from .models import AccadamicYear, Grade, Subject, GradeSubject, GradeStudent, ExcelStud
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from acctype.models import Student
from adminpanel.models import PreviousGrade
from django.core.files import File
import unicodedata
import xlsxwriter
import io
import json
import string

# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
def acc_yr_setup(request):
    if request.method == 'POST':
        form = AccadamicYearForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ec = cd['name_EC']
            gc = str(int(ec) + 7)+'/'+str(int(ec) + 8)
            new_acc = AccadamicYear(name_EC=ec, name_GC=gc, status='Creating')
            new_acc.save()
            return redirect('acc_year:yr_setup_grade', new_acc.id)
    form = AccadamicYearForm()
    return render(request, 'comps/acc_yr.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def yr_setup_grades(request, pk):
    yr = AccadamicYear.objects.get(id=pk)
    return render(request, 'comps/acc_yr_grade.html', {'yr': yr})

@user_passes_test(lambda u: u.is_superuser)
def add_grades_json(request, pk):
    if request.is_ajax() and request.method == 'POST':
        acc = AccadamicYear.objects.get(id=pk)
        grade = request.POST.get('grade')
        section = request.POST.get('section')
        section = section.replace(" ", "")
        sections = section.split(',')
        sec = ''
        for i in sections:
            
            if i == '':
                pass
            else:
                new_gr = Grade(acc_yr=acc, grade_num=int(grade), section=i.upper())
                new_gr.save()
                sec += grade+i.upper()+', '
        
        return JsonResponse({"grade": grade, "section": sec})

@user_passes_test(lambda u: u.is_superuser)
def yr_setup_subjects(request, pk):
    yr = AccadamicYear.objects.get(id=pk)
    grades = Grade.objects.filter(acc_yr=yr)
    gr_list = []
    for i in grades:
        val = str(i.grade_num)
        if val not in gr_list:
            gr_list.append(val)

    return render(request, 'comps/acc_yr_subject.html', {'yr': yr, 'gr_list': gr_list})

@user_passes_test(lambda u: u.is_superuser)
def add_subjects_json(request, pk):
    if request.is_ajax() and request.method == 'POST':
        yr = AccadamicYear.objects.get(id=pk)
        subject = request.POST.get('subject')
        grades_list = request.POST.getlist('grades[]')
        gr_json = ''
        new_sub = Subject(name=subject)
        new_sub.save()
        for i in grades_list:
            gr_json+=i+', '
            grades = Grade.objects.filter(acc_yr=yr, grade_num=int(i))
            for gr in grades:
                print(gr)
                gr_sub = GradeSubject(subject=new_sub, grade=gr)
                gr_sub.save()

        return JsonResponse({"subject": subject, 'gr': gr_json})

@user_passes_test(lambda u: u.is_superuser)
def yr_setup_students(request, pk):
    yr = AccadamicYear.objects.get(id=pk)
    lst_yr = AccadamicYear.objects.filter(status="Active")
    if len(lst_yr) == 0:
        yr.status = "Active"
        yr.save()
    return render(request, 'comps/acc_yr_students.html', {'yr': yr})

@user_passes_test(lambda u: u.is_superuser)
def add_students_json(request, pk):
    if request.is_ajax() and request.method == 'POST':
        acc_yr = AccadamicYear.objects.get(id=pk)
        files = request.FILES.getlist('files[]', None)
        f = files[0]
        stud_data = json.load(f)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        cell_format = workbook.add_format({'bold': True, 'italic': True})
        for sec in stud_data:
            grade = Grade.objects.filter(acc_yr=acc_yr, grade_num=int(sec[:-1]), section=sec[-1])[0]
            e_grade = stud_data[sec]
            worksheet = workbook.add_worksheet(sec)
            worksheet.set_column(0, 0, 16)
            worksheet.set_column(1, 3, 30)
            worksheet.write(0, 0, 'ID', cell_format)
            worksheet.write(0, 1, 'Full Name', cell_format)
            worksheet.write(0, 2, 'Username', cell_format)
            worksheet.write(0, 3, 'Password', cell_format)
            row = 1
            for stud in e_grade:
                username = (stud['ID']).replace('/', '')
                password = BaseUserManager().make_random_password(8, string.ascii_uppercase)
                f_name = (stud['Full Name']).split(' ')[0]
                l_name = stud['Full Name'][len(f_name):]
                usr = User.objects.create(username=username, first_name=f_name, last_name=l_name)
                usr.set_password(password)
                usr.save()  
                student = Student(user=usr, stud_id=stud['ID'], gender=stud['Gender'], phone=stud['Phone'])
                student.save()
                gr_stud = GradeStudent(grade=grade, student=student)
                gr_stud.save()
                pre_sc = PreviousGrade.objects.create(student=student, score=float(stud['Previous Score']))
                worksheet.write(row, 0, stud['ID'])
                worksheet.write(row, 1, stud['Full Name'])
                worksheet.write(row, 2, username)
                worksheet.write(row, 3, password)
                
                row+=1 
        workbook.close()
        output.seek(0)
        excl = ExcelStud()
        fl_tt = "Grade " + sec[:-1] + " Students user info.xlsx"
        excl.fl.save(fl_tt, File(output))
        return JsonResponse({"fl_url": excl.fl.url, "fl_title": fl_tt})

        
    return JsonResponse({"subject": ''})

