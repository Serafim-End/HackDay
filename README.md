# HackDay

Прошел хакатон 
Тема хакатона: кино и телевидение 
Идея проекта: 
на основе комментариев к фильмам и купленных пользователем билетов в кино предлагать подходящее кино для просмотра. 
По сути говоря - рекомендовать пользователю фильм, который ему погравится. 

Очевидно, что задача поставлена не просто. 
Использовалось lsi (латентно семантический анализ)
Использовалось lda (латентное распределение Дирихле) 
корпус - это подвид словаря - подготовленные для обучения данные был сделан так,
чтобы можно было использовать как в lsi, так и в lda

Написано обучение на комментариях кинопоиска + ... (основное это кинопоиск)
Использовалось статическое api кинохода

lsi lda in hack day
