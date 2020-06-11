import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
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


# In[18]:


result.to_excel("vybory_rus.xlsx")


# In[158]:


#выбираем название выборов и разбираем его на запчасти
name_election = soup.select("tr:nth-of-type(2) .headers b")
name_elect = str(name_election[0].text)
name_elect = name_elect.split()
name_first = name_elect[0]
name_second = name_elect[1].lower()
print(name_second)


# In[3]:


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
final_df.head()


# In[169]:


# достаем переменные из датафрэйма
# результаты первого и второго кандидатов, находит минимальные и максимальные значения для проигравшего и выигравшего кандидатов
#Находим значения индексов и названия регионов с наихудшим и наилучшим результатом для кандидатов
procent1 = final_df.loc[1,'hero1_procent']
procent2 = final_df.loc[1,'hero2_procent']
hero1_min = final_df.hero1_procent.min()
hero1_max = final_df.hero1_procent.max()
hero2_min = final_df.hero2_procent.min()
hero2_max = final_df.hero2_procent.max()
def heroi1():
    index_min1 = final_df.index[final_df['hero1_procent'] == hero1_min][0]
    index_min1 = index_min1 - 1
    pl_min1 = final_df.iloc[index_min1,1]
    procent_max1 = hero1_max
    index_max1 = final_df.index[final_df['hero1_procent'] == hero1_max][0]
    index_max1 = index_max1 - 1
    pl_max1 = final_df.iloc[index_max1,1]
    return pl_max1,hero1_max, pl_min1,hero1_min
pl_max1,hero1_max,pl_min1,hero1_min = heroi1()
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
    procent1 = final_df.loc[1,'hero1_procent']
    procent2 = final_df.loc[1,'hero2_procent']
    hero1_min = final_df.hero1_procent.min()
    hero1_max = final_df.hero1_procent.max()
    hero2_min = final_df.hero2_procent.min()
    hero2_max = final_df.hero2_procent.max()
    loser = heroi2()
    winner = heroi1()
else:
    procent1 = final_df.loc[1,'hero1_procent']
    procent2 = final_df.loc[1,'hero2_procent']
    hero1_min = final_df.hero1_procent.min()
    hero1_max = final_df.hero1_procent.max()
    hero2_min = final_df.hero2_procent.min()
    hero2_max = final_df.hero2_procent.max()
    procent3 = procent2
    procent2 = procent1
    procent1 = procent3
    hero3=hero2
    hero2=hero1
    hero1=hero3
    loser = heroi1()
    winner = heroi2()
print("Побеждает: ", hero1,procent1,winner)
print("Проигравает: ",hero2,procent2,loser)
#находим общее число недействительных бюллетеней
nb = final_df.loc[1,'Число недействительных избирательных бюллетеней']
print("Общее число недействительных избирательных бюллетеней: ", nb)
print(pl_max2, pl_min2,pl_max1,pl_min1)


# In[149]:


o = int(final_df.loc[1,'Число недействительных избирательных бюллетеней']) + int(final_df.loc[1,'Число действительных избирательных бюллетеней'])
a = int(final_df.loc[1,'Число избирателей, включенных в список избирателей'])
yavka = o/a
yavka = yavka *100
yavka = round(yavka,2)
print(yavka)


# In[154]:


pip install pymorphy2


# In[150]:


import pymorphy2 as pm2
morph = pm2.MorphAnalyzer()


# In[151]:


p = morph.parse(pl_min1)[0]
p
if 'masc' in p.tag:
    region = p.inflect({'loct','masc'})[0]
else:
    region = p.inflect({'loct','femn'})[0]
print(region)


# In[152]:


region = region.title()
region


# In[161]:


def names(hero2):
    name2 = hero2.split()
    names2 = name2[1]+" "+name2[0]
    return names2
names2 = names(hero2)
names02 = names(hero2)
names2 = names2.split()
imya = names2[0]
family = names2[1]
familia = family
print(familia)
imya = morph.parse(imya)[0]
family = morph.parse(family)[0]
if {'masc'} in imya.tag:
    imya = imya.inflect({'accs','masc'})[0]
    family = family.inflect({'accs','masc'})[0]
elif {'femn'} in imya.tag:
    imya = imya.inflect({'accs','femn'})[0]
    print(imya)
    family = family.inflect({'accs','femn'})[0]
imya = imya.title()
family = family.title()
names2 = imya +" "+ family
names2


# In[162]:


names1 = names(hero1)
names01 = names(hero1)
print(names01)
names1 = names1.split()
imya1 = names1[0]
family1 = names1[1]
familia1 = family1


# In[163]:


name_first = morph.parse(name_first)[0]
name_first = name_first.inflect({'loct'})[0]
name_first
elect = name_first + " " + name_second
elect


# In[171]:


itog = '{0} опережает {1} на {2}. После подсчёта всех протоколов избирательных комиссий {3} получает {4}% голосов избирателей. Самое маленькое число голосов {5}% {6} набирает в {7}.'.format(names01,names2,elect,familia1,procent1,hero2_min,familia,pl_min2)
itog


# In[172]:


itog2 = 'На {0} {1} опережает {2}. После подсчета 100% протоколов избирательных комиссий результат составляет {3}% голосов избирателей. Больше всего голосов за {4} было отдано в {5}. Худший результат в {6}. Общее количество недействительных бюллетеней на выборах составило {7} штук. Явка на выборах – {8}%.'.format(elect,names01,names2,procent1,familia1,pl_max1,pl_min1,nb,yavka)
itog2
