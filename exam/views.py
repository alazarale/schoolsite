from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.http import Http404, JsonResponse, HttpResponse, FileResponse
from django.urls.resolvers import re
from .models import ExamQuestion, Exam, ExamTaken
from accyear.models import AccadamicYear
from course.models import Module, Course
from django.utils import timezone
from datetime import datetime 
import xml.etree.ElementTree as ET
import pytz
import json


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def exams(request):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'
    
    exams = Exam.objects.filter(owner=request.user)
    print(exams)

    return render(request, 'exam/exams.html', {'w': 'Te', 'yr': yr, 'exams': exams})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def exam_questions(request, pk):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'
    
    exam = Exam.objects.get(id=pk)
    print(exam.exam_questions.all())

    return render(request, 'exam/exam_question.html', {'w': 'Te', 'yr': yr, 'exam': exam})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def exam_questions_add(request, pk):
    if request.is_ajax() and request.method == 'POST':
        exam = Exam.objects.get(id=pk)
        files = request.FILES.getlist('files[]', None)
        f = files[0]
        mytree = ET.parse(f)
        myroot = mytree.getroot()
        for ques in myroot[1:]:
            question = ques.find('questiontext').find('text').text.lstrip().rstrip()
            anss = ques.findall('answer')
            choice = []
            for ans in anss:
                new_c = {}
                new_c['choice'] = ans.find('text').text.lstrip().rstrip()
                if ans.attrib['fraction'] == "100.000":
                    new_c['ans'] = True
                else:
                    new_c['ans'] = False
                choice.append(new_c)
            
            ans = ''
            choice_a = choice[0]['choice']
            if choice[0]['ans'] == True:
                ans = 'choice_a'
            choice_b = choice[1]['choice']
            if choice[1]['ans'] == True:
                ans = 'choice_b'
            choice_c = choice[2]['choice']
            if choice[2]['ans'] == True:
                ans = 'choice_c'
            choice_d = choice[3]['choice']
            if choice[3]['ans'] == True:
                ans = 'choice_d'
            new_ques = ExamQuestion.objects.create(exam=exam, question=question, choice_a=choice_a, choice_b=choice_b, choice_c=choice_c, choice_d=choice_d, answer=ans)
            print(new_ques)
    return JsonResponse({"subject": ''})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def exam_questions_add_modules(request, pk):
    try:
        yr = AccadamicYear.objects.filter(status="Active")[0]
    except:
        yr = 'no'
    
    exam = Exam.objects.get(id=pk)
    f_course = Course.objects.filter(owner=request.user)
    courses = []
    for e in exam.grade_association.all():
        if f_course.filter(grade__grades=e.grade).count() > 0:
            courses.append(f_course.filter(grade__grades=e.grade))
    modules = []
    print(courses)
    for course in courses:
        for i in course:
            if i.modules.count() > 0:
                modules.append(i.modules.all())
    
    f_modules = []
    for m in modules:
        for e in m:
            f_modules.append(e)

    return render(request, 'exam/exam_question_modules.html', {'w': 'Te', 'yr': yr, 'exam': exam, 'modules': f_modules})


@user_passes_test(lambda u: u.groups.filter(name='teacher').exists())
def exam_questions_add_modules_add(request, pk):
    if request.is_ajax() and request.method == 'POST':
        data = json.loads(request.POST.get('data[]'))
        for i in data.keys():
            exam_q = ExamQuestion.objects.get(id=int(i))
            print(exam_q)
            module = Module.objects.get(id=int(data[i]))
            print(module)
            exam_q.module = module
            exam_q.save()
       
    
    return JsonResponse({"stat": 'success'})


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='admin').count() > 0, login_url='/accounts/login/')
# def round_select(request):
#     rounds = ExamRound.objects.all()
#     if request.method == 'POST':
#         form = ExamRoundForm(request.POST)
#         print(form)
#         if form.is_valid():
#             cd = form.cleaned_data
#             print(cd)
#     form = ExamRoundForm()
#     return render(request, 'exam/rounds.html', {'rounds': rounds, 'form': form})


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='admin').count() > 0, login_url='/accounts/login/')
# def exam_list(request, pk):
#     round_s = ExamRound.objects.get(id=pk)
#     exams = round_s.exams.all()
#     return render(request, 'exam/list.html', {'round_s': round_s, 'exams': exams})
    


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='admin').count() > 0, login_url='/accounts/login/')
# def exam_list_sp(request, pk, exam_pk):
#     round_s = ExamRound.objects.get(id=pk)
#     exams = round_s.exams.all()
#     exam = Exam.objects.get(id=exam_pk)
#     subject = Subject.objects.all()
#     return render(request, 'exam/list.html', {'exams': exams, 'exam': exam, 'subject': subject, 'round_s': round_s})


# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='admin').count() > 0, login_url='/accounts/login/')
# def exam_list_sp_res(request, pk, exam_pk):
#     round_s = ExamRound.objects.get(id=pk)
#     exams = round_s.exams.all()
#     exam = Exam.objects.get(id=exam_pk)
#     results = exam.taken.all()
#     print(results)
#     subject = Subject.objects.all()
#     return render(request, 'exam/list_result.html', {'exams': exams, 'exam': exam, 'subject': subject, 'round_s': round_s, 'results': results})



# @login_required
# def exam_statup(request, pk):
#     if request.is_ajax() and request.method == 'POST':
#         exam = Exam.objects.get(id=pk)
#         st = request.POST.get('status')
#         print(st)
#         exam.status = st
#         exam.save()
#         return HttpResponse()


# @login_required
# def exam_ques_add(request, pk):
#     if request.is_ajax() and request.method == 'POST':
#         ans = request.POST.get('answer')
#         ans = 'choice_' + ans
#         question = request.POST.get('question')
#         choice_a = request.POST.get('choice_a')
#         choice_b = request.POST.get('choice_b')
#         choice_c = request.POST.get('choice_c')
#         choice_d = request.POST.get('choice_d')
#         exam = Exam.objects.get(id=pk)
#         new_quest = ExamQuestion(exam=exam, question=question, choice_a=choice_a, choice_b=choice_b, choice_c=choice_c, choice_d=choice_d, answer=ans )
#         new_quest.save()
#         return HttpResponse()


# @login_required
# def stud_exam_list(request):
#     try:
#         subjects = Subject.objects.all()
#         sgr = request.user.student.grade
#     except:
#         raise Http404('the user is not a student')
    
#     ex_ass = sgr.exam_association.all()
#     r_list = []
#     for i in ex_ass:
#         if i.exam.exam_round.id in r_list:
#             pass
#         else:
#             r_list.append(i.exam.exam_round.id)
#     round_list = []
#     for i in r_list:
#         e_round = ExamRound.objects.get(id=i)
#         if e_round.status == 'Show':
#             round_list.append(e_round)
#     print(round_list)
#     return render(request, 'exam/stud_list.html', { 'subjects': subjects, 'rounds': round_list})
    


# @login_required
# def stud_exam_list_sub(request, pk):
#     try:
#         sgr = request.user.student.grade
#     except:
#         raise Http404('the user is not a student')
    
#     exam_round = ExamRound.objects.get(id=pk)
#     exams = exam_round.exams.all()
#     exams = exams.filter(grade_association__grade=sgr)
#     exams = exams.exclude(taken__user=request.user)

#     ex_ass = sgr.exam_association.all()
#     r_list = []
#     for i in ex_ass:
#         if i.exam.exam_round.id in r_list:
#             pass
#         else:
#             r_list.append(i.exam.exam_round.id)
#     round_list = []
#     for i in r_list:
#         e_round = ExamRound.objects.get(id=i)
#         if e_round.status == 'Show':
#             round_list.append(e_round)
#     IST = pytz.timezone('Africa/Addis_Ababa')        
#     now_time = datetime.now(IST)
#     print(now_time.date)

#     return render(request, 'exam/stud_list.html', {'exams': exams, 'rounds': round_list, 'round': exam_round, 'now_time': now_time})
    


# @login_required
# def exam_take_detail(request, pk):
#     try:
#         stud = request.user.student
#     except:
#         raise Http404('not student')

#     IST = pytz.timezone('Africa/Addis_Ababa')        
#     now_time = datetime.now(IST)
#     exam = Exam.objects.get(id=pk)
#     if not exam.taken.filter(user=request.user).exists():  
#         if exam.grade_association.filter(grade=request.user.student.grade).exists():
#             if exam.starting_time <= now_time <= exam.end_time:
#                 up_finish = exam.end_time - now_time
#                 up_finish = up_finish.total_seconds()
#                 t_given = exam.time * 60

#                 if up_finish > t_given:
#                     f_time = t_given
#                 else:
#                     f_time = up_finish
#                 print(f_time)
#                 return render(request, 'exam/exam_detail.html', {'exam': exam, 'f_time': f_time})
#             else:
#                 raise Http404('Not the time yet')
#         else:
#             raise Http404('Not the time yet')
#     else:
#         raise Http404('Already Taken')
    



# @login_required
# def exam_submit(request, pk):
#     if request.is_ajax() and request.method == 'POST':
#         answers = request.POST.getlist('answers[]')
#         un_answer = request.POST.getlist('un_answer[]')
#         print(answers)
#         print(un_answer)
#         exam = Exam.objects.get(id=pk)
#         if not exam.taken.filter(user=request.user).exists():
#             ans_count = 0
#             wrong = ''
#             un_ans = ''
#             for i in range(len(answers)):
#                 elem = answers[i]
#                 elem_ans = elem[-1]
#                 elem_q = elem[:-1]
#                 eq = exam.exam_questions.get(pk=int(elem_q))
#                 if eq.answer == 'choice_'+elem_ans.lower():
#                     ans_count += 1
#                 else:
#                     if i == len(answers) - 1:
#                         wrong += elem
#                     else:
#                         wrong += elem+', '
#             for i in range(len(un_answer)):
#                 res = un_answer[i]
#                 if i == len(un_answer)-1:
#                     un_ans += res
#                 else:
#                     un_ans += res+', '

#             score = ans_count
#             new_exam_taken = ExamTaken(exam=exam, user=request.user, score=score, wrong=wrong, unanswered=un_ans)
#             new_exam_taken.save()
#             loc = 'result3244353'+str(new_exam_taken.exam.exam_round.id)+'4646456'

#             return HttpResponse(loc)
#         else:
#             return HttpResponse('not-fooled')


# @login_required
# def exam_result(request, pk):
#     round_t = ExamRound.objects.get(id=pk)
#     return render(request, 'exam/result.html', {'round_t': round_t})


# @login_required
# def not_fooled(request):
#     return render(request, 'exam/finished.html', {})


# @login_required
# def res_rounds(request):
#     exam_taken = ExamTaken.objects.filter(user=request.user)
#     rounds_id = []
#     rounds = []
#     for i in exam_taken:
#         r = i.exam.exam_round
#         if r.id not in rounds_id:
#             rounds.append(r)
#             rounds_id.append(r.id)
    
#     IST = pytz.timezone('Africa/Addis_Ababa')        
#     now_time = datetime.now(IST)

#     return render(request, 'exam/round_res.html', {'rounds': rounds, 'now_time': now_time})


# @login_required
# def res_rounds_exam(request, pk):
#     s_round = ExamRound.objects.get(id=pk)
#     exams = ExamTaken.objects.filter(user=request.user, exam__exam_round=s_round)
#     print(exams)
#     return render(request, 'exam/round_res_exam.html', {'exams': exams})


# @login_required
# def res_rounds_exam_det(request, exam_pk):
#     exam_t = ExamTaken.objects.get(id=exam_pk)
#     try:
#         wrong = exam_t.wrong.split(', ')
#     except:
#         wrong = []
#     try: 
#         unans = exam_t.unanswered.split(', ')
#     except:
#         unans = []
#     wrong_list = []
#     wrong_c = len(wrong)
#     unans_c = len(unans)
#     wrong_ques = []

#     for i in wrong:
#         e = {}
#         q_id = int(i[0:-1])     
#         ques = ExamQuestion.objects.get(id=q_id)
#         e['ques'] = ques
#         e['y_ans'] = i[-1]
#         ans = ques.answer[-1].upper()
#         e['ans'] = ans
#         wrong_ques.append(e)
#         e = {}
    
#     unans_ques = []
#     for i in unans:
#         e  = {}
#         ques = ExamQuestion.objects.get(id=int(i))
#         e['ques'] = ques
#         ans = ques.answer[-1].upper()
#         e['ans'] = ans
#         unans_ques.append(e)
#         e = {}


#     per_score = exam_t.score * 100 / len(exam_t.exam.exam_questions.all())
#     per_score = format(per_score, ".2f")
  

#     return render(request, 'exam/round_res_detail.html', {'exam_t': exam_t, 'wrong_c': wrong_c, 'unans_c': unans_c, 'wrong_ques': wrong_ques, 'per_score': per_score, 'unans_ques': unans_ques})
