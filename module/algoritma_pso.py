# -*- coding: utf-8 -*-
"""Tugas Akhir_Algoritma PSO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PphkapyKSxI2bo24-1PWdN8rXjcpu3Wz

**IMPORT LIBRARY**
"""

import numpy as np
import pandas as pd
import random as rd
import itertools,random
import math
from math import floor
from random import randint,random,uniform
from operator import add
from functools import reduce 
import matplotlib.pyplot as plt
import pymysql

"""**MENENTUKAN PARAMETER**"""
class algoritma_pso:
  def connect(self):
    return pymysql.connect(host="localhost", user="root", password="", database="AI", charset='utf8mb4')
  def algoritma(self,data):
    con = algoritma_pso.connect(self)
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

    print("Masukkan Jumlah Partikel Yang Diinginkan : ")
    solutions_per_pop = banyak_device
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
        
    print("Masukkan Jumlah Maksimal iterasi Yang Diinginkan : ")
    num_iterations = 20
    print(num_iterations)
    print("\n")

    print("Jumlah Maksimal KWH perhari : ")
    knapsack_threshold = kwh_perhari
    print(knapsack_threshold, "\n")

    print("Nilai r1 : ")
    nilai_r1 = uniform(0, 1)
    #print(nilai_r1)
    print("\n")

    print("Nilai r2 : ")
    nilai_r2 = uniform(0,1)
    #print(nilai_r2)
    print("\n")

    print("Nilai c1 : ")
    nilai_c1 = randint(0,4)
    #print(nilai_c1)
    print("\n")

    print("Nilai c2 : ")
    nilai_c2 = randint(0,4)
    #print(nilai_c2)
    print("\n")

    print('Initial population: ')
    for i in range(len(initial_population)):
      print(initial_population[i])
    print("\n")
    print('Value population: ')
    for i in range(len(value_population)):
      print(value_population[i])

    """**EVALUASI PARTIKEL**"""

    sumArray = []

    for i in range(len(value_population[0])):
      sum = 0
      for j in range(len(value_population)):
        sum += value_population[j][i]
      sumArray.append(round(sum,3))

    print(sumArray)

    total_value_eval = []
    value_population_eval = []
    initial_population_eval = []

    finish_var = 1
    while (finish_var != 0):
      print("initial population BEFORE : ")
      for i in range(len(initial_population)):
        print(initial_population[i])

      print("===========================================")
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

      print("temp sumArray : ",sumArray)
      x = 0
      for i in range(len(sumArray)):
        if (sumArray[i] > knapsack_threshold):
          x = 1
      finish_var = x

    """**Algoritma Particle Swarm Optimization**"""

    fitness_terbaik = []
    partikel_terbaik = []

    for l in range(num_iterations):
      l += 1

      #Menentukan Pbest
      print("Menentukan Pbest Pada Iterasi -", l)

      gbesthigh = []
      gbestmid = []
      gbestlow = []

      pbest = initial_population
      for i in range(len(pbest[0])):
        gbest_high = []
        gbest_mid = []
        gbest_low = []
        for j in range(len(pbest)):
          if pbest[j][i] >= 17 and pbest[j][i] <= 24:
            gbest_high.append(pbest[j][i])
          elif pbest[j][i] >= 9 and pbest[j][i] <= 16:
            gbest_mid.append(pbest[j][i])
          elif pbest[j][i] >= 1 and pbest[j][i] <= 8:
            gbest_low.append(pbest[j][i])
          print(pbest[j][i], end =" ")
        print("")

        if(len(gbest_high) != 0):
          I = np.max(gbest_high)
          gbesthigh.append(I)
          print("gbest high : ", max(gbest_high))
        if(len(gbest_mid) != 0):
          I = np.max(gbest_mid)
          gbestmid.append(I)
          print("gbest mid : ", max(gbest_mid))
        if(len(gbest_low) != 0):
          I = np.max(gbest_low)
          gbestlow.append(I)
          print("gbest low : ", max(gbest_low))
          print("==================")

      print("Hasil array gbest high : ", gbesthigh)
      print("Hasil array gbest mid  : ", gbestmid)
      print("Hasil array gbest low : ", gbestlow)

      v0 = 0
      v1 = []
      x1 = []
      x0 = pbest
      print("pbest[0] : "+str(len(pbest[0])))
      for i in range(len(pbest[0])):
        for j in range(len(pbest)):
          if (Kelas[i]=="High"):
            value_c1_r1 =  (float(nilai_c1) * nilai_r1)
            value_pbest_x0 = (pbest[i][j] - x0[i][j])
            value_c2_r2 = (float(nilai_c2) * nilai_r2)
            value_gbest_x0 = (gbesthigh[j] - x0[i][j])
            V1 = v0 + (value_c1_r1*value_pbest_x0) + (value_c2_r2 * value_gbest_x0)
            v1.append(V1)
          if (Kelas[i]=="Mid"):
            value_c1_r1 =  (float(nilai_c1) * nilai_r1)
            value_pbest_x0 = (pbest[i][j] - x0[i][j])
            value_c2_r2 = (float(nilai_c2) * nilai_r2)
            value_gbest_x0 = (gbestmid[j] - x0[i][j])
            V1 = v0 + (value_c1_r1*value_pbest_x0) + (value_c2_r2 * value_gbest_x0)
            v1.append(V1)
          if (Kelas[i]=="Low"):
            value_c1_r1 =  (float(nilai_c1) * nilai_r1)
            value_pbest_x0 = (pbest[i][j] - x0[i][j])
            value_c2_r2 = (float(nilai_c2) * nilai_r2)
            value_gbest_x0 = (gbestlow[j] - x0[i][j])
            V1 = v0 + (value_c1_r1*value_pbest_x0) + (value_c2_r2 * value_gbest_x0)
            v1.append(V1)

      x1 = []
      k = 0 
      for i in range(len(pbest[0])):
        arrays = []
        for j in range(len(pbest)):
          print(v1[i+j+k] + pbest[i][j], end = " ")
          array = floor(v1[i+j+k] + pbest[i][j])
          arrays.append(array)
        x1.append(arrays)
        k += j
        print("")
        print("==============================")

      for arr in x1:
        print(arr)

      #EVALUASI NILAI FUNGSI
      #Menghitung kembali KWH/device
      print("Evaluasi Nilai Fungsi Iterasi -", l)
      initial_population = []
      initial_population = x1
      print("Partikel baru:")
      for i in initial_population:
        print(i)
      print("============================")
      print("Value population: ")
      value_populations = []
      for i in range(len(initial_population[0])):
        group_populations = []
        for j in range(len(initial_population)):
          group_populations.append(KWH[i]*jmlh_device[i]*initial_population[i][j]/1000)
        value_populations.append(group_populations)
      for i in value_populations:
        print(i)

      sum_Arrays = []

      for i in range(len(value_populations[0])):
        sum = 0
        for j in range(len(value_populations)):
          sum += value_populations[j][i]
        sum_Arrays.append(round(sum,3))
      print("Total Fitness: ")
      print(sum_Arrays)

      #Mengevaluasi hasil nilai fungsi
      finish_var = 1
      while (finish_var != 0):
        print("initial population BEFORE : ")
        for i in range(len(initial_population)):
          print(initial_population[i])

        print("=========================")
        print("knapsack threshold ",knapsack_threshold)
        for i in range(len(sum_Arrays)):
          if (sum_Arrays[i] > knapsack_threshold):
            print(sum_Arrays[i], " > ", knapsack_threshold)
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
        
        valuepopulationn = []
        for i in range(len(initial_population[0])):
          grouppopulations = []
          for j in range(len(initial_population)):
            grouppopulations.append(KWH[i]*jmlh_device[i]*initial_population[i][j]/1000)
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

        print("temp sumArrays : ",sum_Arrayy)
        x = 0
        for i in range(len(sum_Arrayy)):
          if (sum_Arrayy[i] > knapsack_threshold):
            x = 1
        finish_var = x

      #CEK KONVERGEN
      print("Partikel Iterasi -", l, ":")
      for i in range(len(initial_population)):
        print(initial_population[i])
      print("========================")
      initialpopulations = []
      for i in range(len(initial_population)):
        group = []
        for j in range(len(initial_population[i])):
          group.append(initial_population[j][i])
        initialpopulations.append(group)
      for i in range(len(initialpopulations)):
        print(initialpopulations[i])
      for i in range(len(initialpopulations)):
        if sum_Arrayy[i] == max(sum_Arrayy):
          fitness_terbaik.append(max(sum_Arrayy))
          partikel_terbaik.append(initialpopulations[i])

    """**ITERASI**"""

    Biaya = []
    for l in range(num_iterations):
      m = l + 1
      biaya = fitness_terbaik[l] * golongan
      print(jumlah_tagihan)
      print(golongan)
      Biaya.append(biaya)
      #print("Total Nilai fitness terbaik generasi ke-",m,":", fitness_terbaik[l])
      #print("Total Biaya terbaik generasi ke-",m,":", Biaya[l])
      #print("Partikel terbaik generasi ke-",m,":", partikel_terbaik[l])
      if fitness_terbaik[l] == max(fitness_terbaik):
        print("Total Nilai fitness terbaik generasi ke-",m,":", fitness_terbaik[l])
        print("Total Biaya terbaik generasi ke-",m,":", Biaya[l])
        print("partikel terbaik generasi ke-",m,":", partikel_terbaik[l])
        return partikel_terbaik[l],round(Biaya[l]),nama_device
    """**GRAFIK HASIL**"""

    fitness_history_mean = [np.mean(fitness) for fitness in fitness_terbaik]
    fitness_history_max = [np.max(fitness) for fitness in fitness_terbaik]
    plt.plot(list(range(num_iterations)), fitness_history_mean, label = 'Mean Fitness')
    plt.plot(list(range(num_iterations)), fitness_history_max, label = 'Max Fitness')
    plt.legend()
    plt.title('Fitness through the Iterations')
    plt.xlabel('Iterations')
    plt.ylabel('Fitness')
    plt.show()
    print(np.asarray(fitness_terbaik).shape)
