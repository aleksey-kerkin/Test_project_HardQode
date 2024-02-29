from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Group


@receiver(m2m_changed, sender=Group.students.through)
def reallocate_students(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        # Перераспределение пользователей по группам
        reallocate_groups(instance)


def reallocate_groups(group):
    # Получаем все студенты в группе
    students = group.students.all()
    # Получаем все группы продукта, к которому принадлежит текущая группа
    product_groups = group.product.groups.all()

    # Сортируем группы по количеству студентов
    sorted_groups = sorted(product_groups, key=lambda g: g.students.count())

    # Перераспределяем студентов по группам
    for student in students:
        # Проверяем, что студент еще не в другой группе продукта
        if not student.student_groups.exclude(pk=group.pk).exists():
            # Ищем группу с наименьшим количеством студентов, которой не принадлежит студент
            for target_group in sorted_groups:
                if target_group.students.count() < target_group.max_users and student not in target_group.students.all():
                    target_group.students.add(student)
                    break
