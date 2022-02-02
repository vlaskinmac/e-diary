import random

from datacenter.models import Teacher, Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject


def get_pupil(name):
    try:
        pupil = Schoolkid.objects.get(full_name__icontains=name)
        return pupil
    except Schoolkid.DoesNotExist:
        print("Такого ученика нет!")
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено несколько учеников, введите ФИО полностью!")
        exit("Конец!")


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
        print("Такого предмета нет!")
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
        subjects_collection.append({'name': f'{subject}', 'code': subject})
    print('\nВыберите название предмета из списка: \n')
    list_subjects = []
    for code, lesson in enumerate(subjects_collection, start=1):
        list_subjects.append(code)
        print(code, lesson['name'], sep=': ')
    input_choice = int(input('\nВведите номер предмета: '))
    try:
        return subjects_collection[input_choice - 1]['code']
    except IndexError:
        print('Вы ввели не корректный номер предмета'
              '\nВведите номер предмета: ')


name = None
pupil = None
commendation_subject = None
while not pupil:
    name = input("Введите, фамилию и имя через пробел: ")
    pupil = get_pupil(name)
correct_points(pupil)
remove_chastisements(pupil)
print("\nОценки исправлены, замечания удалены")
while True:
    choice = input("\nДобавить похвалу учителя? Да/Нет?: ").lower()
    if choice == "да":
        while not commendation_subject:
            commendation_subject = choice_subject()
            try:
                print(f"\nДобавлена похвала: \nпредмет: {commendation_subject}")
                create_commendation(commendation_subject, pupil)
            except UnboundLocalError:
                pass
    elif choice not in ("да", "нет"):
        print("Введите: Да/Нет")
    elif choice == "нет":
        exit("Конец!")
