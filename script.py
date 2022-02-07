import random
import shlex, subprocess

from datacenter.models import Teacher, Chastisement, Commendation, Lesson, Mark, Schoolkid, Subject


def get_pupil(name):
    try:
        pupil = Schoolkid.objects.get(full_name__icontains=name)
        return pupil
    except Schoolkid.DoesNotExist:
        print("Такого ученика нет!")
        main()
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено несколько учеников, введите ФИО полностью!")
        exit("Конец!")


def correct_points(pupil):
    marks = Mark.objects.filter(schoolkid=pupil, points__lte=3)
    for mark_to_correct in marks:
        mark_to_correct.points = 5
        mark_to_correct.save()
    print("\nОценки исправлены, замечания удалены")


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
    while True:
        input_choice = int(input("\nВведите номер предмета: "))
        try:
            return subjects_collection[input_choice - 1]["code"]
        except IndexError:
            print("Вы ввели не корректный номер предмета!")


def get_name(command):
    dialog = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
    name, errors = dialog.communicate()
    return name


def dialog_name(command):
    name = get_name(command)
    pupil = get_pupil(name.strip())
    correct_points(pupil)
    remove_chastisements(pupil)
    return pupil


def dialog_praise(choice_args, pupil):
    if choice_args.strip() == "y":
        try:
            commendation_subject = choice_subject()
            create_commendation(commendation_subject, pupil)
            print(f"\nДобавлена похвала: \nпредмет: {commendation_subject}")
            response = input("Еще махинации? y/n: ")
            if response == "y".lower():
                print("-" * 50, "\n")
                main()
            else:
                exit("Конец!")
        except UnboundLocalError:
            pass
    elif choice_args.strip() == "n":
        exit("Конец!")


def main():
    command = shlex.split("./dialog.sh name")
    pupil = dialog_name(command)

    command = shlex.split("./dialog.sh praise")
    choice_args = get_name(command)
    dialog_praise(choice_args, pupil)


main()




