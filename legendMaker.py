######
# So this labelMaker uses a legend from the tags on files from image classification and creates a binary array
#
# Just input a list of file names 
#
######

import re

f = open('multiIDList.txt', 'a')

g = open('extractedLabels.txt', 'a')

h = open('mixedList.txt', 'a')

csvLabelsFile = open('csvLabels.csv', 'a')


myl_1_0 = '1' 
rob_2_1 =  '2' 
elo_3_2 =  '3' 
rich_4_3 =  '4' 
crisp_5_4 =  '5' 
amp_6_5 = '6' 
grami_7_6 =  '7'      ##### sort grami-zost prob   i think all grami are zost
utri_8_7 = '8' 
sparg_9_8=  '9' 
cera_a_9 = 'a' 
erio_b_10 = 'b' 
valli_c_11 =  'c' 
het_d_12 = 'd' 
cal_e_13 = 'e' 
nuph_h_14 = 'h' 
stuck_l_15 =  'l' 
chara_j_16 =  'j' 
sagi_k_17 = 'k' 
prael_m_18 =  'm' 
zost_n_19 = 'n' 
niet_i_20 = 'i' 
blur_o_21 = 'f' 
other_g_22 =  'g' 
#mix = 'h' 

legend = [myl_1_0,rob_2_1, elo_3_2, rich_4_3, crisp_5_4, amp_6_5,grami_7_6,utri_8_7,sparg_9_8,cera_a_9,erio_b_10,valli_c_11, het_d_12,cal_e_13,nuph_h_14,stuck_l_15, chara_j_16,sagi_k_17,prael_m_18, zost_n_19,niet_i_20,blur_o_21,other_g_22] 


fileName3 = 'Beauchamp_Day17_2022-09-12_00-14-13_picNo_855_M45.491917103333336_N-75.620316615_T04-18-58.800000_P1_P4_Uub2'

fileName = 'Beauchamp_Day16_2022-09-10_21-29-54_picNo_489_M45.48808531666667_N-75.62312744333333_T01-32-37.400000_Pf_P2_Uub1_P1_Uub2_P3_Uub3.png'


fileName1 = 'Brompton_Day8_2022-07-05_07-35-44_picNo_397_45.4008011_-72.144508_3_76_Pi_Uub1_P7_Uub1.png'

files = [fileName, fileName1, fileName3]
# print(fileName.count('_U'))

def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1 #change to k += len(sub) to not search overlapping results
    return result

for file in files:
    multiUsers = False
    mixed = False
    matchesU = find_all(file, '_U')
    idArr = []
    if len(matchesU) > 1:
        multiUsers = True
    matchesP = find_all(file, '_P')

    for i in range(len(matchesU)):
        print(matchesU)
        mixCount = 0

        for match_P in matchesP:
            # print(file)
            if len(matchesU) > 1:
                if i < 1:
                    if (match_P < matchesU[i]):
                        id = file[match_P + 2]
                        mixCount = mixCount + 1
                        idArr.append(id)
                    else:
                        pass

                if (i > 0 and i < len(matchesU)):
                    if (match_P > matchesU[i-1] and match_P < matchesU[i]):
                        id = file[match_P + 2] 
                        mixCount = mixCount + 1 
                        idArr.append(id)        
                    else:
                        pass
                if (i == len(matchesU)):
                    if (match_P > matchesU[i-1] and match_P < matchesU[len(matchesU)-1]):
                        id = file[match_P + 2] 
                        mixCount = mixCount + 1
                        idArr.append(id)
                    else:
                        pass

            else: 
                id = file[match_P + 2]
                mixCount = mixCount + 1
                idArr.append(id)
            if mixCount > 1:
                mixed = True
            
            user = file[matchesU[i]+2: matchesU[i]+5]     
        ######
        #csv

        myl = 0
        rob = 0
        elo = 0
        rich = 0
        crisp = 0
        amp = 0
        grami = 0
        utri = 0
        sparg = 0
        cera = 0
        erio = 0
        valli = 0
        het = 0
        cal = 0
        nuph = 0
        stuck = 0
        chara = 0
        sagi = 0
        prael = 0
        zost = 0
        niet = 0
        blur = 0
        other = 0
        # labelLegend = [myl,rob,elo,rich,crisp,amp,grami,utri,sparg,cera,erio,valli,het,cal,nuph,stuck,chara,sagi,prael,zost,niet,blur,other]
    
        # labelList1 = '_Pi_P1_P4'

        fileID = file #file[0]
        csvFile = [fileID,myl,rob,elo,rich,crisp,amp,grami,utri,sparg,cera,erio,valli,het,cal,nuph,stuck,chara,sagi,prael,zost,niet,blur,other]

        for id in idArr:#file[1]:
            for i in range(len(legend)):
                if id == legend[i]:
                    # labelLegend[i] = 1
                    csvFile[i+2] = 1
        # print(csvLegend)
        csvFileStr = str(csvFile)
        c = csvFileStr.replace('[', '')
        d =c.replace(']', '')
        print(str(d))
        csvLabelsFile.write(d + '\n')
        


        ###########
        stringF = str(file) + ' ; ' + str(idArr) + ' ; ' + str(user) + ' ; ' + 'multiUsers: '+ str(multiUsers) + ' ; ' + 'iterationsCount: ' + str(len(matchesU)) + ' ; '  + 'mixed: ' + str(mixed)
        if (multiUsers):
            f.write(stringF+ '\n')
        g.write(stringF + '\n')

        if(mixed):
            h.write(stringF + '\n')
        idArr = []

f.close()
g.close()
h.close()
csvLabelsFile.close()


##########################
#plant_label_arrayPosition
f = open('labelCSV.csv', 'a')
g = open('labelCSV_headless.csv', 'a')


myl_1_0 = '1' 
rob_2_1 =  '2' 
elo_3_2 =  '3' 
rich_4_3 =  '4' 
crisp_5_4 =  '5' 
amp_6_5 = '6' 
grami_7_6 =  '7'      ##### sort grami-zost prob   i think all grami are zost
utri_8_7 = '8' 
sparg_9_8=  '9' 
cera_a_9 = 'a' 
erio_b_10 = 'b' 
valli_c_11 =  'c' 
het_d_12 = 'd' 
cal_e_13 = 'e' 
nuph_h_14 = 'h' 
stuck_l_15 =  'l' 
chara_j_16 =  'j' 
sagi_k_17 = 'k' 
prael_m_18 =  'm' 
zost_n_19 = 'n' 
niet_i_20 = 'i' 
blur_o_21 = 'f' 
other_g_22 =  'g' 
#mix = 'h' 

fileID = ''
labelList = ''
myl = 0
rob = 0
elo = 0
rich = 0
crisp = 0
amp = 0
grami = 0
utri = 0
sparg = 0
cera = 0
erio = 0
valli = 0
het = 0
cal = 0
nuph = 0
stuck = 0
chara = 0
sagi = 0
prael = 0
zost = 0
niet = 0
blur = 0
other = 0

legend = [myl_1_0,rob_2_1, elo_3_2, rich_4_3, crisp_5_4, amp_6_5,grami_7_6,utri_8_7,sparg_9_8,cera_a_9,erio_b_10,valli_c_11, het_d_12,cal_e_13,nuph_h_14,stuck_l_15, chara_j_16,sagi_k_17,prael_m_18, zost_n_19,niet_i_20,blur_o_21,other_g_22] 
legendString = ['myl_1','rob_2', 'elo_3', 'rich_4', 'crisp_5', 'amp_6','grami_7','utri_8','sparg_9','cera_a','erio_b','valli_c', 'het_d','cal_e','nuph_h','stuck_l_', 'chara_j','sagi_k','prael_m', 'zost_n','niet_i','blur_o','other_g'] 
labelLegendString = ['myl','rob','elo','rich','crisp','amp','grami','utri','sparg','cera','erio','valli','het','cal','nuph','stuck','chara','sagi','prael','zost','niet','blur','other']
csvLegendString = ['fileID','labelList','myl','rob','elo','rich','crisp','amp','grami','utri','sparg','cera','erio','valli','het','cal','nuph','stuck','chara','sagi','prael','zost','niet','blur','other']


# label = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
######################



fileWithLabel = ['example_Pi_P1_P4.png', ['i','1','4']]
fileWithLabel2 = ['example2_Pj_P3_P4.png', ['j','3','4']]

l = str(csvLegendString)
a = l.replace('[', '')
csvLegend =a.replace(']', '')
f.write(csvLegend + '\n')


files = [fileWithLabel, fileWithLabel2]

for file in files:
    myl = 0
    rob = 0
    elo = 0
    rich = 0
    crisp = 0
    amp = 0
    grami = 0
    utri = 0
    sparg = 0
    cera = 0
    erio = 0
    valli = 0
    het = 0
    cal = 0
    nuph = 0
    stuck = 0
    chara = 0
    sagi = 0
    prael = 0
    zost = 0
    niet = 0
    blur = 0
    other = 0
    labelLegend = [myl,rob,elo,rich,crisp,amp,grami,utri,sparg,cera,erio,valli,het,cal,nuph,stuck,chara,sagi,prael,zost,niet,blur,other]
   
    labelList1 = '_Pi_P1_P4'
    labelList2 = '_Pj_P3_P4'
    fileID = file[0]
    csvFile = [fileID,labelList1,myl,rob,elo,rich,crisp,amp,grami,utri,sparg,cera,erio,valli,het,cal,nuph,stuck,chara,sagi,prael,zost,niet,blur,other]

    for id in file[1]:
        for i in range(len(legend)):
            if id == legend[i]:
                labelLegend[i] = 1
                csvFile[i+2] = 1
    print(csvLegend)
    csvFileStr = str(csvFile)
    c = csvFileStr.replace('[', '')
    d =c.replace(']', '')
    print(str(d))
    f.write(d + '\n')
    g.write(d + '\n')

f.close()










#######################
#myl2Btn = '_P1' 
# rob2Btn =  '_P2' 
# eloBtn =  '_P3' 
# richBtn =  '_P4' 
# crispBtn =  '_P5' 
# ampBtn = '_P6' 
# gramiBtn =  '_P7' 
# utriBtn = '_P8' 
# spargBtn =  '_P9' 
# ceraBtn = '_Pa' 
# erioBtn = '_Pb' 
# valliBtn =  '_Pc' 
# hetBtn = _Pd' 
# calBtn = _Pe' 
# nuphBtn = '_Ph' 

# ####added
# stuckBtn =  '_Pl' 
# charaBtn =  '_Pj' 
# sagiBtn = '_Pk' 
# praelBtn =  '_Pm' 
# zostBtn = '_Pn' 

# ####

# blurBtn = '_Pf' 
# otherBtn =  '_Pg' 
# #  mixBtn = '_Ph' 
# nietBtn = '_Pi' 

