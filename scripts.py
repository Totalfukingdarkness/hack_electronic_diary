from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
from random import choice

PRAISES = [
    'Молодец',
    'Отлично',
    'Хорошо',
    'Гораздо лучше, чем я ожидал',
    'Ты меня приятно удивил',
    'Великолепно',
    'Прекрасно',
    'Ты меня очень обрадовал',
    'Именно этого я давно ждал от тебя',
    'Сказано здорово – просто и ясно',
    'Ты, как всегда, точен',
    'Очень хороший ответ',
    'Талантливо',
    'Ты сегодня прыгнул выше головы',
    'Я поражен',
    'Уже существенно лучше',
    'Потрясающе',
    'Замечательно',
    'Прекрасное начало',
    'Так держать',
    'Ты на верном пути',
    'Здорово',
    'Это как раз то, что нужно',
    'Я тобой горжусь',
    'С каждым разом у тебя получается всё лучше',
    'Мы с тобой не зря поработали',
    'Я вижу, как ты стараешься',
    'Ты растешь над собой',
    'Ты многое сделал, я это вижу',
    'Теперь у тебя точно все получится',
]


def fix_marks(schoolkid_name):
    schoolkid = checks_pupil(schoolkid_name)
    if schoolkid:
        marks_kid = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
        marks_kid.update(points=5)


def remove_chastisements(schoolkid_name):
    schoolkid = checks_pupil(schoolkid_name)
    if schoolkid:
        chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
        chastisement.delete()


def create_commendation(schoolkid_name, subject):
    schoolkid = checks_pupil(schoolkid_name)
    if schoolkid:
        lesson = Lesson.objects.filter(
            subject__title=subject, year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter).order_by('subject').first()
        if lesson:
            commendation = Commendation.objects.create(
                text=choice(PRAISES), created=lesson.date,
                schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
        else:
            print('Этот предмет у данного ученика не преподается')


def checks_pupil(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name, year_of_study=6, group_letter='А')
        return schoolkid
    except Schoolkid.MultipleObjectsReturned:
        print('С этим именем есть несколько учеников')
    except Schoolkid.DoesNotExist:
        print('В этом классе, ученика с таким именем нет')
