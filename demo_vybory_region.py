import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
# Пользователь должен ввести ссылку на сводную таблицу результатов выборов по региону
url =  input ("Введите ссылку на страницу с результами выборов")
page = requests.get(url)
soup = BeautifulSoup(page.text)
def pars():
    table = soup.findAll('table', 
                     {'style': 'width:100%;border-color:#000000'})[0]
     # выберем из длинного списка выше таблицу с индексом 1
     # здесь данные по всей ТИК

    first = pd.read_html(str(table))[1]
    
    # транспонируем, чтобы по столбцам шли названия показателей

    part1 = pd.read_html(str(table))[1].T
    
    pd.read_html(str(table))[2]
   
    part2 = pd.read_html(str(table))[2].T
 # склеиваем две части
    final = pd.concat([part1, part2])
    final

 # убираем строку 0
    final = final.iloc[1:, :]
    final

 # новую строку 0 используем как названия столбцов 
    final.columns = final.iloc[0, :]
    final

 # вместо nan называем первый столбец УИК
    final.rename(columns = {np.nan: 'tik'}, inplace=True)
    final
    final = final.reset_index()
    final
  
 # убираем строку 0
    final = final.iloc[1:, :]
    left = final.iloc[:, 0]
    right = final.iloc[:, 1:]
    result = pd.concat([left, right], axis=1)
    return result
result = pars()
result = pd.DataFrame(result)
pd.options.display.max_rows = 100
result.head()


# In[3]:


#выбираем название выборов
name_election = soup.select("tr:nth-of-type(2) .headers b")
name_elect = str(name_election[0].text)
name_elect


# In[6]:


#расчитываем явку на выборах
o = int(final_df.loc[1,'Число недействительных бюллетеней']) + int(final_df.loc[1,'Число действительных бюллетеней'])
a = int(final_df.loc[1,'Число избирателей, внесенных в список на момент окончания голосования'])
yavka = o/a
yavka = yavka *100
yavka = round(yavka,2)
print(yavka)


# In[63]:


hero1 = input("Введите ФИО первого кандидата:")
name1_df = result[hero1].str.split(expand=True)
name1_df.columns=['hero1_values','hero1_procent']
name1_df= pd.DataFrame(name1_df)
name1_df
hero2 = input("Введите ФИО второго кандидата:")
name2_df = result[hero2].str.split(expand=True)
name2_df.columns = ['hero2_values','hero2_procent']
name2_df = pd.DataFrame(name2_df)
name2_df
name1_df['hero1_values']= name1_df['hero1_values'].astype(int)
name2_df['hero2_values']= name2_df['hero2_values'].astype(int)
name1_df['hero1_procent']= name1_df['hero1_procent'].str.strip("%").astype(float)
name2_df['hero2_procent']= name2_df['hero2_procent'].str.strip("%").astype(float)
final_df = pd.concat([result,name1_df,name2_df],axis=1)


# In[64]:


# достаем переменные из датафрэйма
# результаты первого и второго кандидатов, находит минимальные и максимальные значения для проигравшего и выигравшего кандидатов
procent1 = final_df.loc[1,'hero1_procent']
procent2 = final_df.loc[1,'hero2_procent']
hero1_min = final_df.hero1_procent.min()
hero1_max = final_df.hero1_procent.max()
hero2_min = final_df.hero2_procent.min()
hero2_max = final_df.hero2_procent.max()
#Находим значения индексов и названия регионов с наихудшим и наилучшим результатом для кандидатов
def heroi1():
    index_min1 = final_df.index[final_df['hero1_procent'] == hero1_min][0]
    index_min1 = index_min1 - 1
    pl_min1 = final_df.iloc[index_min1,1]
    index_max1 = final_df.index[final_df['hero1_procent'] == hero1_max][0]
    index_max1 = index_max1 - 1
    pl_max1 = final_df.iloc[index_max1,1]
    return pl_max1,hero1_max, pl_min1,hero1_min
pl_max1,hero1_max, pl_min1,hero1_min = heroi1()
def heroi2():
    index_min2= final_df.index[final_df['hero2_procent'] == hero2_min][0]
    index_min2 = index_min2 - 1
    pl_min2 = final_df.iloc[index_min2,1]
    #print(pl_min2)
    index_max2 = final_df.index[final_df['hero2_procent'] == hero2_max][0]
    index_max2 = index_max2 - 1
    pl_max2 = final_df.iloc[index_max2,1]
    #print(pl_max2)
    return pl_max2,hero2_max, pl_min2,hero2_min
pl_max2,hero2_max, pl_min2,hero2_min = heroi2()
#находим регионы в таблице в зависимости от того, кто из двух кандидатов, выбранных пользователем является победителем, а кто проигравшим
if procent1>procent2:
    loser = heroi2()
    winner = heroi1()
    procent1_min = hero1_min
    procent2_min = hero2_min
    region2_min = pl_min2
    region1_min = pl_min1
else: 
    hero1,hero2 = hero2,hero1
    procent1,procent2 = procent2,procent1
    loser = heroi1()
    winner = heroi2()
    region2_min = pl_min1
    region1_min = pl_min2
    procent1_min = hero2_min
    procent2_min = hero1_min
print("Побеждает: ", hero1,procent1,winner)
print("Проигравает: ",hero2,procent2,loser)
#находим общее число недействительных бюллетеней
nb = final_df.loc[1,'Число недействительных бюллетеней']
print("Общее число недействительных избирательных бюллетеней: ", nb)
print(procent2_min)


# In[49]:


pip install pymorphy2


# In[65]:


#Импортируем модуль Pymorphy2 и ставим фамилии кандидатов в нужные формы. Преобразуем названия ТИК в названия районов.
import pymorphy2 as pm2
morph = pm2.MorphAnalyzer()

p = morph.parse(region2_min)[0]
region2 = p.inflect({'loct','masc'})[0]
region2 = region2.title()
region2


# In[121]:


def names(hero2):
    name2 = hero2.split()
    names2 = name2[1]+" "+name2[0]
    return names2
names2 = names(hero2)
names02 = names(hero2)
names2 = names2.split()
imya2 = names2[0]
family2 = names2[1]
familia2 = family2
imya2 = morph.parse(imya2)[0]
family2 = morph.parse(family2)[0]
if {'masc'} in imya2.tag:
    imya2 = imya2.inflect({'accs','masc'})[0]
    family2 = family2.inflect({'accs','masc'})[0]
elif {'femn'} in imya2.tag:
    imya2 = imya2.inflect({'accs','femn'})[0]
    family2 = family2.inflect({'accs','femn'})[0]
imyav2 = morph.parse(imya2)[0]
familyv2 = morph.parse(family2)[0]
if {'masc'} in imyav2.tag:
    imyav2 = imyav2.inflect({'gent','masc'})[0]
    familyv2 = familyv2.inflect({'gent','masc'})[0]
elif {'femn'} in imyav2.tag:
    imyav2 = imyav2.inflect({'gent','femn'})[0]
    familyv2 = familyv2.inflect({'gent','femn'})[0]
imya2 = imya2.title()
family2 = family2.title()
names2 = imya2 +" "+ family2
names2
imyav2 = imyav2.title()
familyv2 = familyv2.title()
namesv2 = imyav2 +" "+ familyv2
namesv2


# In[21]:


#Переменные для шаблонов
#yavka - общая явка на выборах
#name_elect - название выборов в Им.пад
#names01 - имя первого кандидата(в формате имя, фамилия), Им.пад
#names02 - имя второго кандидата(в формате имя, фамилия), Им.пад
#familia2 - фамилия второго кандидата, Им. пад
#family2 - фамилия второго кандидата, В. пад
#region1 - название района с минимальным результатом для первого кандидата, Предл.пад
#region2 - название района с минимальным результатом для второго кандидата, Предл. пад
#procent1 - общий процент голосов, набранный первым кандидатом
#procent2 - общий процент голосов, набранный вторым кандидатом
#procent1_min - минимальный процент голосов, набранный первым кандидатом
#procent2_min - минимальный процент голосов, набранный вторым кандидатом
#procent1_max - максимальный процент голосов, набранный первым кандидатом
#procent2_max - максимальный процент голосов, набранный вторым кандидатом


# In[67]:


#Итоговый генератор. Возможен как данный вариант, так и подгрузка шаблона в переменную
itog = '{0}. {1} опережает {2}. После подсчёта всех протоколов избирательных комиссий {3} получает {4}% голосов избирателей. Самое маленькое число голосов {5}% – {6} набирает в {7} районе.'.format(name_elect,names1,names2,names1,procent1,procent2_min,familia2,region2)
itog


# In[122]:


itogi2 = "{0} набирает в {1} районе {2}% голосов избирателей.{3} обгоняет {4} на {5} c результатом {6}%. {7} получает {8}% голосов избирателей. При этом худший результат {9} в {10} районе. Явка на этих выборах составила {11}%."
itogi2.format(names02,region2,procent2_min,names1,names2,name_elect,procent1,familia2,procent2,familyv2,region2,yavka)


# In[ ]:
