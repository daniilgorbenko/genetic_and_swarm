import random as rnd
from all_functions import *

import matplotlib.pyplot as plt
import imageio
import os

class Individ():
    """ Класс одного индивида в популяции"""
    def __init__(self, start, end, mutationSteps, function):
        # пределы поиска минимума
        self.start = start
        self.end = end
        # позиция индивида по Х (первый раз определяется случайно)
        self.x = rnd.triangular(self.start, self.end)
        # позиция индивида по Y (первый раз определяется случайно)
        self.y = rnd.triangular(self.start, self.end)
        # значение функции, которую реализует индивид
        self.score = 0
        # передаем функцию для оптимизации
        self.function = function
        # количество шагов мутации
        self.mutationSteps = mutationSteps
        # считаем сразу значение функции
        self.calculateFunction()


    def calculateFunction(self):
        """ Функция для пересчета значения значение в индивиде"""
        self.score = self.function(self.x, self.y)

    def mutate(self):
        """ Функция для мутации индивида"""
        # задаем отклонение по Х
        delta = 0
        for i in range(1, self.mutationSteps+1):
            if rnd.random() < 1 / self.mutationSteps:
                delta += 1 / (2 ** i)
        if rnd.randint(0, 1):
            delta = self.end * delta
        else:
            delta = self.start * delta
        self.x += delta
        # ограничим наших индивидом по Х
        if self.x < 0:
            self.x = max(self.x, self.start)
        else:
            self.x = min(self.x, self.end)
        # отклонение по У
        delta = 0
        for i in range(1, self.mutationSteps+1):
            if rnd.random() < 1 / self.mutationSteps:
                delta += 1 / (2 ** i)
        if rnd.randint(0, 1):
            delta = self.end * delta
        else:
            delta = self.start * delta
        self.y += delta
        # ограничим наших индивидом по У
        if self.y < 0:
            self.y = max(self.y, self.start)
        else:
            self.y = min(self.y, self.end)



class Genetic:
    """ Класс, отвечающий за реализацию генетического алгоритма"""
    def __init__(self,
                 numberOfIndividums,
                 crossoverRate,
                 mutationSteps,
                 chanceMutations,
                 numberLives,
                 function,
                 start,
                 end):
        # размер популяции
        self.numberOfIndividums = numberOfIndividums
        # какая часть популяции должна производить потомство (в % соотношении)
        self.crossoverRate = crossoverRate
        # количество шагов мутации
        self.mutationSteps = mutationSteps
        # шанс мутации особи
        self.chanceMutations = chanceMutations
        # сколько раз будет появляться новое поколение (сколько раз будет выполняться алгоритм)
        self.numberLives = numberLives
        # функция для поиска минимума
        self.function = function

        # самое минимальное значение, которое было в нашей популяции
        self.bestScore = float('inf')
        # точка Х, У, где нашли минимальное значение
        self.xy = [float('inf'), float('inf')]
        # область поиска
        self.start = start
        self.end = end



    def crossover(self, parent1:Individ, parent2:Individ):
        """ Функция для скрещивания двух родителей

        :return: 2 потомка, полученных путем скрещивания
        """
        # создаем 2х новых детей
        child1 = Individ(self.start, self.end, self.mutationSteps, self.function)
        child2 = Individ(self.start, self.end, self.mutationSteps, self.function)
        # создаем новые координаты для детей
        alpha = rnd.uniform(0.01, 1)
        child1.x = parent1.x + alpha * (parent2.x - parent1.x)

        alpha = rnd.uniform(0.01, 1)
        child1.y = parent1.y + alpha * (parent2.y - parent1.y)

        alpha = rnd.uniform(0.01, 1)
        child2.x = parent1.x + alpha * (parent1.x - parent2.x)

        alpha = rnd.uniform(0.01, 1)
        child2.y = parent1.y + alpha * (parent1.y - parent2.y)
        return child1, child2


    def startGenetic(self):
        # будем собирать данные для gif
        dataForGIF = []

        # создаем стартовую популяцию
        pack = [self.start, self.end, self.mutationSteps,self.function]
        population = [Individ(*pack) for _ in range(self.numberOfIndividums)]

        # запускаем алгоритм
        for _ in range(self.numberLives):
            # сортируем популяцию по значению score
            population = sorted(population, key=lambda item: item.score)
            # данные для отрисовки GIF
            oneStepDataX = [individ.x for individ in population]
            oneStepDataY = [individ.y for individ in population]
            dataForGIF.append([oneStepDataX, oneStepDataY])

            # берем ту часть лучших индивидов, которых будем скрещивать между собой
            bestPopulation = population[:int(self.numberOfIndividums*self.crossoverRate)]
            # теперь проводим скрещивание столько раз, сколько было задано по коэффициенту кроссовера
            childs = []
            for individ1 in bestPopulation:
                # находим случайную пару для каждого индивида и скрещиваем
                individ2 = rnd.choice(bestPopulation)
                while individ1 == individ2:
                    individ2 = rnd.choice(bestPopulation)
                child1, child2 = self.crossover(individ1, individ2)
                childs.append(child1)
                childs.append(child2)
            # добавляем всех новых потомков в нашу популяцию
            population.extend(childs)

            for individ in population:
                # проводим мутации для каждого индивида
                individ.mutate()
                # пересчитываем значение функции для каждого индивида
                individ.calculateFunction()
            # отбираем лучших индивидов
            population = sorted(population, key=lambda item: item.score)
            population = population[:self.numberOfIndividums]
            # теперь проверим значение функции лучшего индивида на наилучшее значение экстремума
            if population[0].score < self.bestScore:
                self.bestScore = population[0].score
                self.xy = [population[0].x, population[0].y]

        # print("ОПТИМИЗИРОВАННОЕ ЗНАЧЕНИЕ ФУНКЦИИ:", self.xy, self.bestScore)

        # рисуем gif
        fnames = []
        i = 0
        for x, y in dataForGIF:
            i += 1
            fname = f"g{i}.png"
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.suptitle(f"Итерация: {i}")
            ax2.plot(x, y, 'bo')
            ax2.set_xlim(self.start, self.end)
            ax2.set_ylim(self.start, self.end)
            ax1.plot(x, y, 'bo')
            fig.savefig(fname)
            plt.close()

            fnames.append(fname)

        with imageio.get_writer('genetic.gif', mode='I') as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)

a = Genetic(numberOfIndividums=500, crossoverRate=0.5, mutationSteps=15, chanceMutations=0.4,
            numberLives=200, function=Ackley, start=-5, end=5)
a.startGenetic()
print("ОПТИМИЗИРОВАННОЕ ЗНАЧЕНИЕ ФУНКЦИИ:", a.xy, a.bestScore)

