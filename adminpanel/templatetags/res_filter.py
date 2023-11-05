from django import template
from acctype.models import Student
from accyear.models import GradeSubject, Subject
from adminpanel.models import StudentResult

register = template.Library()

@register.filter
def flt(result, student):
    stud = Student.objects.get(stud_id=student)
    if result.result.filter(student=stud).count() > 0:
        return (result.result.filter(student=stud)[0]).score
    else:
        return '-'

@register.filter
def flt_att(attendances, date):
    return attendances.filter(att_date=date)

@register.filter
def flt_att_st(attendances, stud):
    return (attendances.filter(student=stud)[0]).stat

@register.filter
def flt_res(results, student):
    stud = Student.objects.get(stud_id=student)
    return results.filter(gr_stud__student=stud)[0]

@register.filter
def flt_res_sub(results, sub):
    sub = Subject.objects.get(id=sub)
    try:
        return results.filter(subject=sub)[0]
    except:
        return False

@register.filter
def flt_add(results, res):
    return res.first_50 + res.second_50

@register.filter
def flt_add_pp(res):
    return res.first_50 + res.second_50

@register.filter
def flt_gr_sub(grade, sub):
    s = Subject.objects.get(id=sub)
    return GradeSubject.objects.filter(grade=grade, subject=s.id)[0]

@register.filter
def flt_res_stud(gr_sub, stud):
    return StudentResult.objects.filter(result__gr_sub=gr_sub, student=stud)

@register.filter
def flt_spres(res, sub):
    try:
        return res.filter(subject=sub.subject)[0]
    except:
        return ''

@register.filter
def flt_st_add(res, stat):
    if stat == '1':
        if res.first_50 != None and res.second_50 != None:
            return float(res.first_50) + float(res.second_50)
        else:
            return '-'
    elif stat == '2':
        if res.third_50 != None and res.forth_50 != None:
            return float(res.third_50) + float(res.forth_50)
        else:
            return '-'
