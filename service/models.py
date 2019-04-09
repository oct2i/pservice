from django.db import models
import jsonfield


class Candidate(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=25)
    age = models.IntegerField(verbose_name='Возраст', default=0)
    email = models.CharField(verbose_name='Email', max_length=25)
    residence_planet = models.ForeignKey('Planet',
                                         verbose_name='Планета проживания',
                                         related_name='candidates',
                                         on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Jedi(models.Model):
    name = models.CharField(verbose_name='Имя джежая', max_length=25)
    learning_planet = models.ForeignKey('Planet',
                                        verbose_name='Планета обучения',
                                        related_name='jedis',
                                        on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Planet(models.Model):
    title = models.CharField(verbose_name='Название планеты', max_length=35)

    def __str__(self):
        return self.title


class Orden(models.Model):
    name = models.CharField(verbose_name='Название ордена', max_length=35)
    planet = models.OneToOneField('Planet',
                                  verbose_name='Планета',
                                  related_name='ordens',
                                  on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Test(models.Model):
    orden = models.OneToOneField('Orden',
                                 verbose_name='Орден',
                                 related_name='tests',
                                 on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)


class Question(models.Model):
    test = models.ForeignKey('Test',
                             verbose_name='Тест',
                             related_name='questions',
                             on_delete=models.PROTECT)
    question = models.CharField(verbose_name='Текст вопроса', max_length=256)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answers = jsonfield.JSONField()

