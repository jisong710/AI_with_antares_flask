import numpy as np
import pandas as pd
import random as rd
import itertools,random
import math
from math import floor
from random import randint,random,uniform,choice
from operator import add
from functools import reduce 
import matplotlib.pyplot as plt
import pymysql
import requests
import json

class algoritma_genetik:
  def connect(self):
    return pymysql.connect(host="localhost", user="root", password="", database="AI", charset='utf8mb4')
  def algoritma(self,data):
    con = algoritma_genetik.connect(self)
    cursor = con.cursor()
    tagihan = cursor.execute("SELECT golongan_daya FROM gedung where id = "+data['gedung']+"")
    daya = cursor.fetchone()
    jumlah_tagihan =  int(data['budget'])
    golongan = float(daya[0])
    tagihan_perhari = jumlah_tagihan/float(data['durasi'])
    kwh_perhari = round(tagihan_perhari/golongan)
    print("kWh perhari yang dapat digunakan = ", kwh_perhari)
    banyak = cursor.execute("SELECT nama_device,besar_daya,prioritas,jumlah FROM device where id_gedung = "+data['gedung']+"")
    banyak_data = cursor.fetchall()
    #Input Jumlah Device dan KWH
    banyak_device = cursor.rowcount
    jmlh_device = []
    nama_device = []
    KWH = []
    value = []
    Jam = []
    Kelas = []
    k = 1
    while k <= banyak_device:
        nama_dvc = str(banyak_data[k-1][0])
        jmlh_dvc = int(banyak_data[k-1][3]) 
        kwh = int(banyak_data[k-1][1])
        kelas = str(banyak_data[k-1][2])
        nama_device.append(nama_dvc)
        jmlh_device.append(jmlh_dvc)
        KWH.append(kwh)
        Kelas.append(kelas)
        k += 1

    print('The list is as follows:')
    print('Item No. \t Device \t Jumlah Device \t KWH \t Kelas')
    for i in range(len(KWH)):
        print("   {0} \t\t {1} \t\t {2} \t\t {3} \t {4}\n".format(i+1, nama_device[i], jmlh_device[i], KWH[i], Kelas[i]))
    print(cursor.rowcount)
    """**INISIALISASI POPULASI**"""

    print("Masukkan Jumlah Kromosom Yang Diinginkan : ")
    solutions_per_pop = 12
    print("\n")
    pop_size = (solutions_per_pop, banyak_device)
    print('Population size = {}'.format(pop_size))
    print("\n")
    initial_population = []
    for i in range(len(KWH)):   
      if (Kelas[i] == "High"):         
        initial_population.append(np.random.randint(17,25, size = solutions_per_pop))
      if (Kelas[i] == "Mid"):
        initial_population.append(np.random.randint(9,17, size = solutions_per_pop))
      if (Kelas[i] == "Low"):
        initial_population.append(np.random.randint(1,9, size = solutions_per_pop))
    value_population = []
    for i in range(len(KWH)):
        value_population.append(KWH[i]*jmlh_device[i]*initial_population[i]/1000)

    print("Masukkan Jumlah Maksimal Generasi Yang Diinginkan : ")
    num_generations = 20
    print(num_generations)
    print("\n")

    print("Jumlah Maksimal KWH perhari : ")
    knapsack_threshold = kwh_perhari
    print(knapsack_threshold, "\n")

    print("Nilai Crossover Rate : ")
    nilai_pc = round(uniform(0.5,0.95),2)
    #print(nilai_pc)
    print("\n")

    print("Nilai Mutation Rate : ")
    nilai_pm = round(uniform(0,0.3),2)
    #print(nilai_pm)
    print("\n")
    print('Initial population: ')
    for i in range(len(initial_population)):
      print(initial_population[i])
    print("\n")
    print('Value population: ')
    for i in range(len(value_population)):
      print(value_population[i])

    """**EVALUASI KROMOSOM**"""

    sumArray = []

    for i in range(len(value_population[0])):
      sum = 0
      for j in range(len(value_population)):
        sum += value_population[j][i]
      sumArray.append(round(sum,3))

    print(sumArray)

    finish_var = 1
    while (finish_var != 0):
      print("initial population BEFORE : ")
      for i in range(len(initial_population)):
        print(initial_population[i])

      print("========================")
      print("knapsack threshold ",knapsack_threshold)
      for i in range(len(sumArray)):
        if (sumArray[i] > knapsack_threshold):
          print(sumArray[i], " > ", knapsack_threshold)
          for j in range(len(initial_population)):
            if (Kelas[j].lower()=="high"):
              if (initial_population[j][i] == 17):
                initial_population[j][i] = initial_population[j][i]
              else:
                initial_population[j][i] = initial_population[j][i] - floor(initial_population[j][i] * 0.1)
            if(Kelas[j].lower()=="mid"):
              if (initial_population[j][i] == 9):
                initial_population[j][i] = initial_population[j][i]
              else:
                initial_population[j][i] = initial_population[j][i] - floor(initial_population[j][i] * 0.1)
            if(Kelas[j].lower()=="low"):
              if (initial_population[j][i] == 1):
                initial_population[j][i] = initial_population[j][i]
              else:
                initial_population[j][i] = initial_population[j][i] - floor(initial_population[j][i] * 0.1)

      print("initial population AFTER : ")
      for i in range(len(initial_population)):
        print(initial_population[i])
      
      value_population = []
      for i in range(len(KWH)):
        value_population.append(KWH[i]*jmlh_device[i]*initial_population[i]/1000)

      print("Value Population :")
      for i in value_population:
        print(i)

      sumArray = []

      for i in range(len(value_population[0])):
        sum = 0
        for j in range(len(value_population)):
          sum += value_population[j][i]
        sumArray.append(round(sum,3))

      print("========================")
      print("Total KWH : ")
      print(sumArray)
      x = 0
      for i in range(len(sumArray)):
        if (sumArray[i] > knapsack_threshold):
          x = 1
      finish_var = x

    """**ALGORITMA GENETIKA**"""

    fitnessterbaik = []
    kromosomterbaik = []
    for l in range(num_generations):
      l += 1
      
      #SELEKSI KROMOSOM
      #Menghitung nilai fitness relatif fan fitness comulative
      print("Seleksi kromosom generasi -", l)
      total_fitness = 0
      for i in sumArray:
        total_fitness += i
      print ('Total Fitness: ', round(total_fitness,3))
      fitness_r = []
      for i in sumArray:
        fitnessr = i/total_fitness
        fitness_r.append(round(fitnessr,3))
      print('Fitness Relative: ', fitness_r)
      fitness_c = []
      fitnessc = 0
      for i in fitness_r:
        fitnessc += i
        fitness_c.append(round(fitnessc,3))
      print('Fitness Comulative: ', fitness_c)
      roulate_sk=[]
      k = 1
      while k <= solutions_per_pop:
        rlt_sk = round(uniform(0,1),2)
        roulate_sk.append(rlt_sk)
        k +=1
      print('Roulate Wheel yang digunakan: ', roulate_sk)

      temp_initial_population = initial_population

      print("initial population BEFORE : ")
      for arr in temp_initial_population:
        print(arr)

      print("Fitness Comulative : ", fitness_c)
      print('Roulate Wheel : ', roulate_sk)

      route = []

      for i in range(len(roulate_sk)):
        next = False
        j = 0
        while next != True and j < len(fitness_c):
          print("roulate ",i, " : ", roulate_sk[i])
          print("fitness c ",j," : ", fitness_c[j])
          if (roulate_sk[i] <= fitness_c[j] and j not in route):
            route.append(i)
            for k in range(len(temp_initial_population)):
              print("route :",route)
              print("initial_population K-",k, " I-", i, " : ",temp_initial_population[k][i])
              print("initial_population K-",k, " J-", j, " : ",temp_initial_population[k][j])
              temp = temp_initial_population[k][i]
              temp_initial_population[k][i] = temp_initial_population[k][j]
              temp_initial_population[k][j] = temp
            next = True
            for x in range(len(temp_initial_population)):
              print(temp_initial_population[x])
          print("===================================================")
          j += 1
        

      #CROSSOVER
      #Membuat kelompok
      print("Crossover generasi -", l)
      all_group_kromosom = []
      exists_value = []
      n = 0
      length_initial_population = len(initial_population[0]) - 1
      exist = False
      length_group = int(len(initial_population[0]) / 2)
      print('Initial population: ')
      for i in range(len(initial_population)):
        print(initial_population[i])
      print("====================")

      for i in range(length_group):
        group_kromosom = []
        for j in range(2):
          while exist==False:
            n =  randint(0, length_initial_population)
            if(n not in exists_value):
              exists_value.append(n)
              exist = True
        
          exist = False
          
          kromosom = []
          k = 0
          for k in range(len(initial_population)):
            kromosom.append(initial_population[k][n])
          print("kromosom-",n, " : ",kromosom)
          group_kromosom.append(kromosom)
        
        print("===============================================")
        all_group_kromosom.append(group_kromosom)

      for x in all_group_kromosom:
        print(x)

      roulate_co=[]
      k = 1
      while k <= solutions_per_pop/2:
        rlt_co = round(uniform(0,1),2)
        roulate_co.append(rlt_co)
        k +=1
      print('Roulate Wheel yang digunakan: ', roulate_co)

      temp_all_group_kromosom = all_group_kromosom
      print("=================================================================")
      for x in all_group_kromosom:
        print(x)

      print("roulate co : ")
      print(roulate_co)

      for i in range(len(roulate_co)):
        if roulate_co[i] < nilai_pc:
          for j in range(len(temp_all_group_kromosom[i])):
            print("TEMP ALL GROUP KROMOSOM KE-", i," : ",temp_all_group_kromosom[i])
            count = 0
            length = len(temp_all_group_kromosom[i][0]) - 1
            print("length : ",length)
            while count <= 3 :
              temp = temp_all_group_kromosom[i][0][length - count]
              temp_all_group_kromosom[i][0][length - count] = temp_all_group_kromosom[i][1][length - count]
              temp_all_group_kromosom[i][1][length - count] = temp
              count+=1

      print("=================================================================")
      for x in temp_all_group_kromosom:
        print(x)

      #Menghitung kembali KWH/device
      initialpopulation = []
      for i in range(len(roulate_co)):
        initialpopulation.append(all_group_kromosom[i][0])
        initialpopulation.append(all_group_kromosom[i][1])
      print("Kromosom baru:")
      for i in initialpopulation:
        print(i)
      print("===================================")
      print("Value population: ")
      valuepopulation = []
      for i in range(len(initialpopulation[0])):
        group_population = []
        for j in range(len(initialpopulation)):
          group_population.append(KWH[i]*jmlh_device[i]*initialpopulation[j][i]/1000)
        valuepopulation.append(group_population)
      for i in valuepopulation:
        print(i)

      sum_Array = []

      for i in range(len(valuepopulation[0])):
        sum = 0
        for j in range(len(valuepopulation)):
          sum += valuepopulation[j][i]
        sum_Array.append(round(sum,3))
      print("===================================")
      print("Total KWH: ")
      print(sum_Array)

      #Mengevaluasi hasil Crossover
      print("Total KWH: ")
      print(sum_Array)
      print("=================================")
      finish_var = 1
      while (finish_var != 0):
        print("initial population BEFORE : ")
        for i in range(len(initialpopulation)):
          print(initialpopulation[i])

        print("===========================================")
        print("knapsack threshold ",knapsack_threshold)
        for i in range(len(initialpopulation)):
          if (sumArray[i] > knapsack_threshold):
            print(sumArray[i], " > ", knapsack_threshold)
            for j in range(len(initialpopulation[i])):
              if (Kelas[j].lower()=="high"):
                if (initialpopulation[i][j] == 17):
                  initialpopulation[i][j] = initialpopulation[i][j]
                else:
                  initialpopulation[i][j] = initialpopulation[i][j] - floor(initialpopulation[i][j] * 0.1)
              if(Kelas[j].lower()=="mid"):
                if (initialpopulation[i][j] == 9):
                  initialpopulation[i][j] = initialpopulation[i][j]
                else:
                  initialpopulation[i][j] = initialpopulation[i][j] - floor(initialpopulation[i][j] * 0.1)
              if(Kelas[j].lower()=="low"):
                if (initial_population[i][j] == 1):
                  initialpopulation[i][j] = initialpopulation[i][j]
                else:
                  initialpopulation[i][j] = initialpopulation[i][j] - floor(initialpopulation[i][j] * 0.1)

        print("initial population AFTER : ")
        for i in range(len(initialpopulation)):
          print(initialpopulation[i])
      
        valuepopulations = []
        for i in range(len(initialpopulation[0])):
          group_population = []
          for j in range(len(initialpopulation)):
            group_population.append(KWH[i]*jmlh_device[i]*initialpopulation[j][i]/1000)
          valuepopulations.append(group_population)
        print("Value Population :")
        for i in valuepopulations:
          print(i)

        sum_Arrays = []

        for i in range(len(valuepopulations[0])):
          sum = 0
          for j in range(len(valuepopulations)):
            sum += valuepopulations[j][i]
          sum_Arrays.append(round(sum,3))

        print("temp sumArrays : ",sum_Arrays)
        x = 0
        for i in range(len(sum_Arrays)):
          if (sum_Arrays[i] > knapsack_threshold):
            x = 1
        finish_var = x


      #MUTASI
      print("Mutasi generasi -", l)
      roulate_m=[]
      k = 1
      while k <= solutions_per_pop:
        rlt_m = round(uniform(0,1),2)
        roulate_m.append(rlt_m)
        k +=1
      print('Roulate Wheel yang digunakan: ', roulate_m)

      print("initial BEFORE")
      for i in range(len(initialpopulation)):
        print(initialpopulation[i])
      print("===============================") 
      temp = 0
      temp1 = 0
      for i in range(len(initialpopulation)):
        if roulate_m[i] < nilai_pm:
          temp = initialpopulation[i][0] 
          initialpopulation[i][0] = initialpopulation[i][3]
          initialpopulation[i][3] = temp
          temp1 = initialpopulation[i][1] 
          initialpopulation[i][1] = initialpopulation[i][2]
          initialpopulation[i][2] = temp1
      print("initial AFTER")               
      for i in range(len(initialpopulation)):
        print(initialpopulation[i])

      #Menghitung kembali KWH/device
      initialpopulations = []
      for i in range(len(roulate_co)):
        initialpopulations.append(all_group_kromosom[i][0])
        initialpopulations.append(all_group_kromosom[i][1])
      print("Kromosom baru:")
      for i in initialpopulations:
        print(i)
      print("=================================")
      print("Value population: ")
      value_populations = []
      for i in range(len(initialpopulations[0])):
        group_populations = []
        for j in range(len(initialpopulations)):
          group_populations.append(KWH[i]*jmlh_device[i]*initialpopulations[j][i]/1000)
        value_populations.append(group_populations)
      for i in value_populations:
        print(i)

      sum_Arrayy = []

      for i in range(len(value_populations[0])):
        sum = 0
        for j in range(len(value_populations)):
          sum += value_populations[j][i]
        sum_Arrayy.append(round(sum,3))
      print("=================================")
      print("Total KWH: ")
      print(sum_Arrayy)

      #Mengevaluasi hasil Mutasi
      print("Total KWH: ")
      print(sum_Arrayy)
      print("=================================")
      finish_var = 1
      while (finish_var != 0):
        print("initial population BEFORE : ")
        for i in range(len(initialpopulations)):
          print(initialpopulations[i])

        print("==================================")
        print("knapsack threshold ",knapsack_threshold)
        for i in range(len(initialpopulations)):
          if (sum_Arrayy[i] > knapsack_threshold):
            print(sum_Arrayy[i], " > ", knapsack_threshold)
            for j in range(len(initialpopulations[i])):
              if (Kelas[j].lower()=="high"):
                if (initialpopulations[i][j] == 17):
                  initialpopulations[i][j] = initialpopulations[i][j]
                else:
                  initialpopulations[i][j] = initialpopulations[i][j] - floor(initialpopulations[i][j] * 0.1)
              if(Kelas[j].lower()=="mid"):
                if (initialpopulations[i][j] == 9):
                  initialpopulations[i][j] = initialpopulations[i][j]
                else:
                  initialpopulations[i][j] = initialpopulations[i][j] - floor(initialpopulations[i][j] * 0.1)
              if(Kelas[j].lower()=="low"):
                if (initialpopulations[i][j] == 1):
                  initialpopulations[i][j] = initialpopulations[i][j]
                else:
                  initialpopulations[i][j] = initialpopulations[i][j] - floor(initialpopulations[i][j] * 0.1)

        print("initial population AFTER : ")
        for i in range(len(initialpopulations)):
          print(initialpopulations[i])
      
        valuepopulationn = []
        for i in range(len(initialpopulations[0])):
          grouppopulations = []
          for j in range(len(initialpopulations)):
            grouppopulations.append(KWH[i]*jmlh_device[i]*initialpopulations[j][i]/1000)
          valuepopulationn.append(grouppopulations)
        print("Value Population :")
        for i in valuepopulationn:
          print(i)

        sum_Arrayy = []

        for i in range(len(valuepopulationn[0])):
          sum = 0
          for j in range(len(valuepopulationn)):
            sum += valuepopulationn[j][i]
          sum_Arrayy.append(round(sum,3))

        print("==================================")
        print("Total KWH: ")
        print(sum_Arrayy)
        x = 0
        for i in range(len(sum_Arrayy)):
          if (sum_Arrayy[i] > knapsack_threshold):
            x = 1
        finish_var = x

      
      #OPTIMASI
      print("Kromdomsom Generasi ke-", l, ": ")
      for i in range(len(initialpopulations)):
        print(initialpopulations[i])
      print("=================================")
      for i in range(len(initialpopulations)):
        if sum_Arrayy[i] == max(sum_Arrayy):
          print(max(sum_Arrayy))
          fitnessterbaik.append(max(sum_Arrayy))
          print(initialpopulations[i])
          print("=================================")
          kromosomterbaik.append(initialpopulations[i])
      initial_population = []
      for i in range(len(initialpopulations[0])):
        group = []
        for j in range(len(initialpopulations)):
          group.append(initialpopulations[j][i])
        initial_population.append(group)
      for i in range(len(initial_population)):
        print(initial_population[i])

    """**GENERASI**"""

    Biaya = []
    for l in range(num_generations):
      m = l + 1
      biaya = fitnessterbaik[l] * 1444.7
      Biaya.append(biaya)
      #print("Total Nilai fitness terbaik generasi ke-",m,":", fitnessterbaik[l])
      #print("Total Biaya terbaik generasi ke-",m,":", Biaya[l])
      #print("Kromosom terbaik generasi ke-",m,":", kromosomterbaik[l])
      if fitnessterbaik[l] == max(fitnessterbaik):
        print("Total Nilai fitness terbaik generasi ke-",m,":", fitnessterbaik[l])
        print("Total Biaya terbaik generasi ke-",m,":", Biaya[l])
        print("Kromosom terbaik generasi ke-",m,":", kromosomterbaik[l])
        for i in range nama_device:
          
        return kromosomterbaik[l],round(Biaya[l]),nama_device

    """**GRAFIK**"""

    fitness_history_max = [np.max(fitness) for fitness in Biaya]
    plt.plot(list(range(num_generations)), fitness_history_max, label = 'Max Fitness')
    plt.legend()
    plt.title('Fitness through the generations')
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.show()
    print(np.asarray(Biaya).shape)
