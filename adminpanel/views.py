import unicodedata
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accyear.models import AccadamicYear, Grade, GradeStudent, GradeSubject, HomeRoomTeacher, Subject, GrSubTeacher
from acctype.models import Student, Teacher, Parent, TeacherPassword, ParentPassword, StudentParent
from .models import Result, StudentResult, Attendance, FinalScore
from .forms import ParentForm
from django.http import Http404, JsonResponse
from django.utils.dateparse import parse_date
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
import string
from datetime import date, timedelta


def generate_username(full_name):
    full_name = full_name.lower()
    name = full_name.split(' ')
    lastname = name[-1]
    firstname = name[0]

    username = '%s%s' % (firstname[0], lastname)
    if User.objects.filter(username=username).count() > 0:

        username = '%s%s' % (firstname, lastname[0])
        if User.objects.filter(username=username).count() > 0:

            users = User.objects.filter(
                username__regex=r'^%s[1-9]{1,}$' % firstname).order_by('username').values('username')
            if len(users) > 0:
                last_number_used = list(
                    map(lambda x: int(x['username'].replace(firstname, '')), users))

                last_number_used.sort()
                last_number_used = last_number_used[-1]
                number = last_number_used + 1
                username = '%s%s' % (firstname, number)
            else:
                username = '%s%s' % (firstname, 1)

    return username


# Create your views here.
@login_required
def adminpanel(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':

        grades = Grade.objects.filter(acc_yr=yr)
        stud_num = 0
        for grade in grades:
            stud_num += GradeStudent.objects.filter(grade=grade).count()

        teacher = Teacher.objects.all().count()
        parent = Parent.objects.all().count()

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'admin_index.html', {'w': 'dash', 'yr': yr, 'stud': stud_num, 'teacher': teacher, 'parent': parent})


@user_passes_test(lambda u: u.is_superuser)
def admingrade(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        grades = Grade.objects.filter(acc_yr=yr)

        # page_num = request.GET.get('page', 1)
        # paginator = Paginator(grades, 10)
        # try:
        #     page_obj = paginator.page(page_num)
        # except PageNotAnInteger:
        #     # if page is not an integer, deliver the first page
        #     page_obj = paginator.page(1)
        # except EmptyPage:
        #     # if the page is out of range, deliver the last page
        #     page_obj = paginator.page(paginator.num_pages)

        stud_num = 0
        for grade in grades:
            stud_num += GradeStudent.objects.filter(grade=grade).count()
    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/admin_grade.html', {'w': 'Gg', 'yr': yr, 'grades': grades, 'stud': stud_num, })


@user_passes_test(lambda u: u.is_superuser)
def admingrade_edit(request, pk):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        grade = Grade.objects.get(id=pk)
    
    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/admin_grade_edit.html', {'w': 'Gg', 'yr': yr, 'grade': grade})


@user_passes_test(lambda u: u.is_superuser)
def admingrade_edit_ajax(request, pk):
    if request.is_ajax() and request.method == 'POST':
        grade_num = request.POST.get('grade_num')
        section = request.POST.get('section')
        grade = Grade.objects.get(id=pk)
        grade.grade_num = grade_num
        grade.section = section.upper()
        grade.save()

        return JsonResponse({"stat": 'success'})


@user_passes_test(lambda u: u.is_superuser)
def adminstudent(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        grades = Grade.objects.filter(acc_yr=yr)
        studs = []
        for grade in grades:
            studs += GradeStudent.objects.filter(grade=grade)
        studs = list(sorted(
            studs, key=lambda obj: obj.student.user.first_name+'     '+obj.student.user.last_name))

        # page_num = request.GET.get('page', 1)
        # paginator = Paginator(studs, 10)
        # try:
        #     page_obj = paginator.page(page_num)
        # except PageNotAnInteger:
        #     # if page is not an integer, deliver the first page
        #     page_obj = paginator.page(1)
        # except EmptyPage:
        #     # if the page is out of range, deliver the last page
        #     page_obj = paginator.page(paginator.num_pages)
    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/admin_students.html', {'w': 'As', 'yr': yr, 'studs': studs})


@user_passes_test(lambda u: u.is_superuser)
def adminstudent_profile(request, pk):
    grade_stud = GradeStudent.objects.get(id=pk)
    yr = grade_stud.grade.acc_yr
    subjects = grade_stud.grade.subjects.all()
    try:
        res = grade_stud.final_score.all()
    except:
        res = None

    return render(request, 'pages/admin_student_profile_scores.html', {'w': 'As', 'yr': yr, 'ps': 'sc', 'res': res, 'grade_stud': grade_stud, 'subjects': subjects})


@user_passes_test(lambda u: u.is_superuser)
def adminstudent_profile_att(request, pk):
    grade_stud = GradeStudent.objects.get(id=pk)
    yr = grade_stud.grade.acc_yr
    atts = Attendance.objects.filter(student=grade_stud.student, att_date__year__range=[
                                     (yr.name_GC).split('/')[0], (yr.name_GC).split('/')[1]])

    return render(request, 'pages/admin_stud_profile_att.html', {'w': 'As', 'yr': yr, 'ps': 'att', 'grade_stud': grade_stud, 'atts': atts})


@user_passes_test(lambda u: u.is_superuser)
def adminteacher(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        teachers = Teacher.objects.all()
    
    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/admin_teacher.html', {'w': 'At', 'yr': yr, 'teachers': teachers})


@user_passes_test(lambda u: u.is_superuser)
def adminteacher_add(request):
    return render(request, 'pages/admin_teacher_add.html', {})


@user_passes_test(lambda u: u.is_superuser)
def adminteacher_add_json(request):
    if request.is_ajax() and request.method == 'POST':
        f_name = request.POST.get('f_name')
        last_name = request.POST.get(
            'm_name') + ' ' + request.POST.get('l_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        bd = parse_date(request.POST.get('bd'))
        hd = parse_date(request.POST.get('hd'))
        print(hd.strftime('%Y'))

        new_teach = Teacher(phone=phone, birth_date=bd,
                            hired_date=hd, status='Active')
        new_teach.save()
        last_id = new_teach.id
        zs = ''
        if 4-len(str(last_id)) > 0:
            for i in range(4-len(str(last_id))):
                zs += '0'
            zs = zs+str(last_id+1)
        teacher_id = 'T/'+zs+'/'+str(hd.strftime('%Y'))[2:]
        username = "t"+zs+str(hd.strftime('%Y'))[2:]
        password = BaseUserManager().make_random_password(8, string.ascii_uppercase)
        usr = User.objects.create(
            username=username, first_name=f_name, last_name=last_name, email=email)
        usr.set_password(password)
        usr.save()
        new_teach.user = usr
        new_teach.teacher_id = teacher_id
        new_teach.save()
        teach_pass = TeacherPassword(teacher=new_teach, pass_w=password)
        teach_pass.save()

        return JsonResponse({"pk": new_teach.id})


@user_passes_test(lambda u: u.is_superuser)
def adminteacher_profile(request, pk):
    yr = AccadamicYear.objects.filter(status="Active")[0]
    teacher = Teacher.objects.get(id=pk)
    sub_list = []
    for s in teacher.subjects.all():
        if s.gr_sub.subject.name not in sub_list:
            sub_list.append(s.gr_sub.subject.name)

    grades_p = Grade.objects.filter(acc_yr=yr)
    grades = []
    for grade in grades_p:
        if grade.home_room.count() == 0:
            grades.append(grade)
    subjects = Subject.objects.all()

    return render(request, 'pages/teacher_profile_subject.html', {'w': 'At', 'teacher': teacher, 'grades': grades, 'subjects': subjects, 'yr': yr, 'sub_l': sub_list})


@user_passes_test(lambda u: u.is_superuser)
def adminteacher_profile_home(request, pk):
    if request.is_ajax() and request.method == 'POST':
        grade = Grade.objects.get(id=int(request.POST.get('grade')))
        teacher = Teacher.objects.get(id=pk)
        stat = ''

        if teacher.home_room.count() == 0 and grade.home_room.count() == 0:
            new_home = HomeRoomTeacher.objects.create(
                grade=grade, teacher=teacher)
            stat = 'success'
        else:
            stat = 'fail'

        return JsonResponse({"stat": stat})


@user_passes_test(lambda u: u.is_superuser)
def adminteacher_get(request, pk):
    if request.is_ajax() and request.method == 'GET':
        sub = Subject.objects.get(id=int(request.GET.get('subject')))
        gr_sub = GradeSubject.objects.filter(subject=sub)
        grades = []
        for gs in gr_sub:
            print(GrSubTeacher.objects.filter(gr_sub=gs))
            if not GrSubTeacher.objects.filter(gr_sub=gs).exists():
                grades.append(str(gs.grade.grade_num)+gs.grade.section)
        if len(grades) == 0:
            stat = 'nog'
        else:
            stat = 'success'

        return JsonResponse({"grades": grades, 'stat': stat})


@user_passes_test(lambda u: u.is_superuser)
def adminteacher_subadd(request, pk):
    if request.is_ajax() and request.method == 'POST':
        grades = request.POST.getlist('grades[]')
        acc_yr = AccadamicYear.objects.filter(status="Active")[0]
        subject = Subject.objects.get(id=int(request.POST.get('subject')))
        teacher = Teacher.objects.get(id=pk)
        gr_su = []
        for grade in grades:
            gr_su.append(GradeSubject.objects.filter(grade=Grade.objects.filter(grade_num=int(
                grade[:-1]), section=grade[-1], acc_yr=acc_yr)[0], subject=subject)[0])

        for i in gr_su:
            if GrSubTeacher.objects.filter(gr_sub=i, teacher=teacher).count() == 0:
                GrSubTeacher.objects.create(gr_sub=i, teacher=teacher)

        return JsonResponse({"stat": 'success'})


@user_passes_test(lambda u: u.is_superuser)
def adminparent(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        parents = Parent.objects.all()
    
    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/parents/admin-parent.html', {'w': 'Ap', 'yr': yr, 'parents': parents})


@user_passes_test(lambda u: u.is_superuser)
def adminparent_add(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        if request.method == 'POST':
            form = ParentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                username = generate_username(
                    cd['first_name'] + ' ' + cd['last_name'])
                password = BaseUserManager().make_random_password(8, string.ascii_uppercase)
                usr = User.objects.create(
                    username=username, first_name=cd['first_name'], last_name=cd['last_name'])
                usr.set_password(password)
                usr.save()
                new_parent = Parent.objects.create(
                    user=usr, phone=cd['phone'], job=cd['job'], address=cd['address'], relation_ship=cd['relation_ship'])
                ParentPassword.objects.create(
                    parent=new_parent, pass_w=password)
                p_group = Group.objects.get(name='parent')
                p_group.user_set.add(usr)

                return redirect('ad_panel:admin_parent_add_link', new_parent.id)

        form = ParentForm()

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/parents/admin-parent-create.html', {'w': 'Ap', 'yr': yr, 'form': form})


@user_passes_test(lambda u: u.is_superuser)
def adminparent_add_link(request, pk):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        parent = Parent.objects.get(id=pk)
    
    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/parents/admin-parent-link.html', {'w': 'Ap', 'yr': yr, 'parent': parent})


@user_passes_test(lambda u: u.is_superuser)
def adminparent_add_link_get(request, pk):
    if request.is_ajax() and request.method == 'GET':
        stud_id = request.GET.get('stud')
        parent = Parent.objects.get(id=pk)
        try:
            stud = Student.objects.filter(stud_id='SMI/'+stud_id)[0]
            if StudentParent.objects.filter(student=stud, parent=parent).exists():
                return JsonResponse({"stat": 'fail', 'desc': 'This student is already linked to this parent'})
            else:
                if stud.profile_pic:
                    pp = stud.profile_pic
                else:
                    pp = None
                return JsonResponse({"stat": 'success', 'id': stud.id, 'name': stud.user.first_name+' '+stud.user.last_name, 'pp': pp, 'stud_id': stud.stud_id, 'grade': str((stud.grade.all()[0]).grade.grade_num)+(stud.grade.all()[0]).grade.section})

        except:
            return JsonResponse({"stat": 'fail', "desc": 'No User. Check the id again'})


@user_passes_test(lambda u: u.is_superuser)
def adminparent_add_link_add(request, pk):
    if request.is_ajax() and request.method == 'POST':
        stud_id = request.POST.get('stud_id')
        stud = Student.objects.get(id=stud_id)
        parent = Parent.objects.get(id=pk)
        if StudentParent.objects.filter(student=stud, parent=parent).exists():
            return JsonResponse({"stat": 'fail', 'desc': 'This student is already linked to this parent'})
        else:
            StudentParent.objects.create(parent=parent, student=stud)
            if stud.profile_pic:
                pp = stud.profile_pic
            else:
                pp = None
            return JsonResponse({"stat": 'success', 'id': stud.id, 'name': stud.user.first_name+' '+stud.user.last_name, 'pp': pp, 'stud_id': stud.stud_id, 'grade': str((stud.grade.all()[0]).grade.grade_num)+(stud.grade.all()[0]).grade.section})


@user_passes_test(lambda u: u.is_superuser)
def adminsubjects(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        subjects = Subject.objects.all()
        teachers = Teacher.objects.filter(status="Active")
        grades = Grade.objects.filter(acc_yr=yr)
        gr_list = []
        for i in grades:
            val = str(i.grade_num)
            if val not in gr_list:
                gr_list.append(val)

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/admin_subjects.html', {'w': 'Gsu', 'subjects': subjects, 'teachers': teachers, 'yr': yr, 'gr_list': gr_list})


@user_passes_test(lambda u: u.is_superuser)
def adminsubjects_add(request):
    if request.is_ajax() and request.method == 'POST':
        yr = AccadamicYear.objects.filter(status="Active")[0]
        grade = (request.POST.get('grade')).strip('Grade ')
        subject = Subject.objects.filter(name=request.POST.get('subject'))[0]
        teacher = Teacher.objects.get(id=int(request.POST.get('teacher')))
        grade = Grade.objects.filter(
            grade_num=grade[:-1], section=grade[-1], acc_yr=yr)[0]
        gr_sub = GradeSubject.objects.filter(grade=grade, subject=subject)[0]

        if GrSubTeacher.objects.filter(gr_sub=gr_sub, teacher=teacher).count() == 0:
            GrSubTeacher.objects.create(gr_sub=gr_sub, teacher=teacher)

        return JsonResponse({"stat": 'success'})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def teaching_list(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        teaching_grades = (request.user.teacher.all())[0].subjects.all()

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/teacher/list.html', {'w': 'Tl', 'yr': yr, 'teaching_grades': teaching_grades})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def teaching_sub_see_all(request, sub, pk):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        try:
            gr_sub = GradeSubject.objects.filter(subject=Subject.objects.filter(name=sub)[
                                                 0], grade=Grade.objects.get(id=int(pk)))[0]
            gr_sub_t = GrSubTeacher.objects.filter(
                gr_sub=gr_sub, teacher=(request.user.teacher.all())[0])[0]
            students = gr_sub_t.gr_sub.grade.students.all()
            print('df')
            if Result.objects.filter(gr_sub=gr_sub).count() > 0:
                results = Result.objects.filter(gr_sub=gr_sub)
                r = results[0]
            else:
                results = []

        except:
            return HttpResponse('<h1>Page Not found</h1>')

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/teacher/sub_see_all.html', {'w': 'Tl', 'yr': yr, 'gr_sub_t': gr_sub_t, 'students': students, 'rp': 'all', 'results': results, "gr_sub": gr_sub})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def teaching_sub_add(request, sub, pk):
    if request.is_ajax() and request.method == 'POST':
        privacy = request.POST.get('privacy')
        if privacy == '1':
            privacy = 'Student'
        elif privacy == '2':
            privacy = 'All'
        else:
            return JsonResponse({"stat": 'error'})

        desc = request.POST.get('desc')
        out_of = request.POST.get('out_of')
        try:
            gr_sub = GradeSubject.objects.filter(subject=Subject.objects.filter(name=sub)[
                                                 0], grade=Grade.objects.get(id=int(pk)))[0]
            gr_sub_t = GrSubTeacher.objects.filter(
                gr_sub=gr_sub, teacher=(request.user.teacher.all())[0])[0]
            new_result = Result.objects.create(
                gr_sub=gr_sub, description=desc, out_of=out_of, privacy=privacy)
            return JsonResponse({"stat": 'success', "id": new_result.id})

        except:
            return HttpResponse('<h1>Page Not found</h1>')


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def teaching_sub_res_fill(request, sub, pk, pk2):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        try:
            gr_sub = GradeSubject.objects.filter(subject=Subject.objects.filter(name=sub)[
                                                 0], grade=Grade.objects.get(id=int(pk)))[0]
            gr_sub_t = GrSubTeacher.objects.filter(
                gr_sub=gr_sub, teacher=(request.user.teacher.all())[0])[0]
            students = gr_sub_t.gr_sub.grade.students.all()
            result = Result.objects.get(id=pk2)

        except:
            return HttpResponse('<h1>Page Not found</h1>')

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/teacher/sub_fill_res.html', {'w': 'Tl', 'students': students, 'yr': yr, 'result': result})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def teaching_sub_res_fill_json(request, sub, pk, pk2):
    if request.is_ajax() and request.method == 'POST':
        data = request.POST.get('data')
        data = data.split('&')
        result = Result.objects.get(id=pk2)
        for d in data:
            d = d.split('=')
            student = Student.objects.filter(
                user=User.objects.get(username=d[0]))[0]
            if d[1] != '':
                new_res_stud = StudentResult.objects.create(
                    result=result, student=student, score=float(d[1]))
            else:
                new_res_stud = StudentResult.objects.create(
                    result=result, student=student)

        return JsonResponse({"stat": 'success'})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def homeclass_attendance(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        teacher = request.user.teacher.all()[0]

        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=4)
        dates = []

        for i in range(5):
            dates.append(start + timedelta(days=i))

        attendances = Attendance.objects.filter(
            student__grade__grade=teacher.home_room.all()[0].grade)
        grade = teacher.home_room.all()[0].grade
        at = attendances.filter(att_date=today)

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/teacher/attendance-main.html', {'w': 'Hc', 'yr': yr, 'dates': dates, 'attendances': attendances, 'at': at, 'grade': grade})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def attendance_take(request, pk):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        grade = Grade.objects.get(id=pk)
        today = date.today()

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/teacher/attendance-take.html', {'w': 'Hc', 'yr': yr, 'grade': grade, 'today': today})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def attendance_take_add(request, pk):
    if request.is_ajax() and request.method == 'POST':
        data = request.POST.get('data')
        data = data.split('&')
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=4)

        for d in data:
            el = d.split('=')
            stud = Student.objects.get(id=el[0])
            Attendance.objects.create(student=stud, stat=el[1], att_date=today)

        return JsonResponse({"stat": 'success'})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def submitted_grades_self(request, sub, pk):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        try:
            gr_sub = GradeSubject.objects.filter(subject=Subject.objects.filter(name=sub)[
                                                 0], grade=Grade.objects.get(id=int(pk)))[0]
            gr_sub_t = GrSubTeacher.objects.filter(
                gr_sub=gr_sub, teacher=(request.user.teacher.all())[0])[0]
            students = gr_sub_t.gr_sub.grade.students.all()
            final_scores = FinalScore.objects.filter(
                gr_stud__grade=gr_sub.grade, subject=gr_sub.subject)

            try:
                f = final_scores.all()[0]
                print(f.first_50)
                if f.forth_50 != None:
                    t = '4'
                elif f.third_50 != None:
                    t = '3'
                elif f.second_50 != None:
                    t = '2'
                elif f.first_50 != None:
                    t = '1'
            except:
                t = '0'

        except:
            return HttpResponse('<h1>Page Not found</h1>')

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/teacher/sub_see_submitted.html', {'w': 'Tl', 'yr': yr, 't': t, 'rp': 'submitted', 'gr_sub': gr_sub, 'students': students, 'final_scores': final_scores})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def submitted_grades_self_add(request, sub, pk, numb):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        try:
            gr_sub = GradeSubject.objects.filter(subject=Subject.objects.filter(name=sub)[
                                                 0], grade=Grade.objects.get(id=int(pk)))[0]
            gr_sub_t = GrSubTeacher.objects.filter(
                gr_sub=gr_sub, teacher=(request.user.teacher.all())[0])[0]
            students = gr_sub_t.gr_sub.grade.students.all()

        except:
            return HttpResponse('<h1>Page Not found</h1>')
    
    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/teacher/sub_see_subm_fill.html', {'w': 'Tl', 'yr': yr, 'numb': numb, 'gr_sub': gr_sub, 'students': students})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def submitted_grades_self_json(request, sub, pk, numb):
    if request.is_ajax() and request.method == 'POST':
        data = request.POST.get('data')
        desc = request.POST.get('desc')
        data = data.split('&')
        gr_sub = GradeSubject.objects.filter(subject=Subject.objects.filter(name=sub)[
                                             0], grade=Grade.objects.get(id=int(pk)))[0]
        gr_sub_t = GrSubTeacher.objects.filter(
            gr_sub=gr_sub, teacher=(request.user.teacher.all())[0])[0]
        students = gr_sub_t.gr_sub.grade.students.all()
        final_scores = FinalScore.objects.filter(gr_stud=students)
        for d in data:
            d = d.split('=')
            stud = Student.objects.get(user__username=d[0])
            gr_stud = students.filter(student=stud)[0]
            print(gr_stud)
            if numb == '1':
                if d[1] == '':
                    FinalScore.objects.create(
                        gr_stud=gr_stud, subject=gr_sub.subject, first_desc=desc, first_50=0.0)
                else:
                    FinalScore.objects.create(
                        gr_stud=gr_stud, subject=gr_sub.subject, first_desc=desc, first_50=float(d[1]))
            elif numb == '2':
                if d[1] == '':
                    res = FinalScore.objects.filter(
                        gr_stud=gr_stud, subject=gr_sub.subject)[0]
                    res.second_desc = desc
                    res.second_50 = 0.0
                    res.save()
                else:
                    res = FinalScore.objects.filter(
                        gr_stud=gr_stud, subject=gr_sub.subject)[0]
                    res.second_desc = desc
                    res.second_50 = float(d[1])
                    res.save()

        return JsonResponse({"stat": 'success'})


@user_passes_test(lambda u: u.groups.filter(name='student').exists())
def results_all(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        subjects = request.user.student.all()[0].grade.all()[
            0].grade.subjects.all()

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/students/results-all.html', {'rp': 'all', 'w': 'AIr', 'yr': yr, 'subjects': subjects})


@user_passes_test(lambda u: u.groups.filter(name='student').exists())
def results_submitted(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'

    if yr != 'no':
        gr_stud = request.user.student.all()[0].grade.all()[0]
        gr_sub = GradeSubject.objects.filter(grade=gr_stud.grade)
        res_sub = FinalScore.objects.filter(gr_stud=gr_stud)

    else:
        return redirect("acc_year:yr_setup")

    return render(request, 'pages/students/results-sub.html', {'rp': 'submitted', 'w': 'AIr', 'yr': yr, 'gr_sub': gr_sub, 'res_sub': res_sub})
