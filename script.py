import argparse
import os
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()
from datacenter.models import Teacher, Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject


def get_pupil(name):
    try:
        pupil = Schoolkid.objects.get(full_name__icontains=name)
        print("\nОценки исправлены, замечания удалены")
        return pupil
    except Schoolkid.DoesNotExist:
        print("Такого ученика нет! Для справки используйте -h")
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено несколько учеников, введите ФИО полностью!\n")


def correct_points(pupil):
    marks = Mark.objects.filter(schoolkid=pupil, points__lte=3)
    for mark_to_correct in marks:
        mark_to_correct.points = 5
        mark_to_correct.save()


def remove_chastisements(pupil):
    chastisements = Chastisement.objects.filter(schoolkid=pupil)
    chastisements.delete()


def create_commendation(commendation_subject, pupil):
    commendations = [
        "Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!", "Великолепно!", "Прекрасно!", "Ты меня очень обрадовал!",
        "Именно этого я давно ждал от тебя!", "Сказано здорово – просто и ясно!",
        "Ты, как всегда, точен!", "Очень хороший ответ!", "Талантливо!",
        "Ты сегодня прыгнул выше головы!", "Я поражен!", "Уже существенно лучше!",
    ]
    try:
        subject = Subject.objects.get(year_of_study=pupil.year_of_study,
                                      title=commendation_subject)
    except Subject.DoesNotExist:
        pass

    pupils_subject = Lesson.objects.filter(
        year_of_study=pupil.year_of_study,
        group_letter=pupil.group_letter,
        subject=subject).order_by("?").only("date", "teacher").first()
    teacher_id = Teacher.objects.get(full_name=pupils_subject.teacher)
    commendation = Commendation.objects.filter(
        subject=subject,
        schoolkid=pupil,
        created=pupils_subject.date
    )
    commendation.create(
        text=random.choice(commendations),
        created=pupils_subject.date,
        schoolkid=pupil,
        teacher=teacher_id,
        subject=subject
    )


def choice_subject():
    subjects = [
        "Краеведение", "География", "Математика", "Музыка", "Физкультура",
        "Изобразительное искусство", "Технология", "Русский язык", "Литература",
        "Обществознание", "Иностранный язык", "Биология", "История",
        "Основы безопасности жизнедеятельности (ОБЖ)"
    ]
    subjects_collection = []
    for subject in subjects:
        subjects_collection.append({"name": f"{subject}", "code": subject})
    print("\nВыберите название предмета из списка: \n")
    list_subjects = []
    for code, lesson in enumerate(subjects_collection, start=1):
        list_subjects.append(code)
        print(code, lesson["name"], sep=": ")
    input_choice = int(input("\nВведите номер предмета: "))
    try:
        return subjects_collection[input_choice - 1]["code"]
    except IndexError as exc:
        print(exc)


def get_arguments():
    parser = argparse.ArgumentParser(
        description='The code corrects teachers grades and comments.'
    )
    parser.add_argument(
        '-n', '--name', help="-Чтобы исправить оценки используйте аргумент: -n или '--name' и введите: 'фамилию имя'"
                   " в кавычках через пробел"
    )
    parser.add_argument(
        '-s', '--subject', help="-Чтобы добавить похвалу учителя используйте аргумент: -s=True или --subject=True"
    )

    args = parser.parse_args()
    return args.s, args.y


if __name__ == "__main__":
    only_marks, praise = get_arguments()
    pupil = get_pupil(name=only_marks)
    correct_points(pupil)
    remove_chastisements(pupil)
    choice_args = get_arguments()
    commendation_subject = choice_subject()
    if commendation_subject:
        try:
            print(f"\nДобавлена похвала: \nпредмет: {commendation_subject}")
            create_commendation(commendation_subject, pupil)
        except UnboundLocalError as exc:
            print(exc)
