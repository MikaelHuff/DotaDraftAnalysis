import PySimpleGUI as sg

import dataComp
import draftAnalyser as analys

# The file that shows the actual GUI that is used.

# Takes the random heroes created in draftAnalyser.py and updates the drop down menus to have
# the selected choices
def randomHeroes():
    draft = analys.randomise(len(heroes))
    for i in range(10):
        team = 'A' if (i < 5) else 'B'
        number = str(i % 5+1)
        string = '_'+team+number+'_'
        window[string].update(heroes[draft[i]])

# Takes a draft, and updates the 10 hero images to be the new images.
def updateImages(draft):
    for i in range(5):
        window['_imageA'+str(i)+'_'].update('Images\\'+draft[2*i]+'.png')
        window['_imageB'+str(i)+'_'].update('Images\\'+draft[2*i+1]+'.png')


# The GUI settings
data = dataComp.data()
heroes = data.getHeroList()
sg.theme('DarkBrown4')
rows = 7
cols = 7

# Making the table used in the top half of the GUI
column_layout = [[sg.Text(str(i+j), size=(15, 3), justification='center', key=(i, j),text_color='white') for j in range(cols)] for i in range(rows)]

column_layout[0][0] = sg.Text('Heroes', text_color='white', size=(15, 3),justification='center')
for i in range(5):
    column_layout[i + 1][0] = sg.Image('Images\\default.png', key='_imageA'+str(i)+'_')
    column_layout[0][i + 1] = sg.Image('Images\\default.png', key='_imageB'+str(i)+'_')
column_layout[6][0] = sg.Text('Totals', text_color='green', size=(15, 5),justification='center')
column_layout[0][6] = sg.Text('Totals', text_color='red', size=(15, 3),justification='center')

# Layout for the entire GUI
layout = [[sg.Col(column_layout, size=(1000, 650))],
          [sg.Text('Choose the Heroes for each Team'), sg.Text(size=(15,1))],
          [sg.Text('Team 1'), sg.Push(), sg.Text('Team 2')],
          [sg.Text('Hero 1'), sg.Combo(heroes, key = '_A1_'), sg.Push(), sg.Text('Hero 1'), sg.Combo(heroes, key = '_B1_')],
          [sg.Text('Hero 2'), sg.Combo(heroes, key = '_A2_'), sg.Push(), sg.Text('Hero 2'), sg.Combo(heroes, key = '_B2_')],
          [sg.Text('Hero 3'), sg.Combo(heroes, key = '_A3_'), sg.Push(), sg.Text('Hero 3'), sg.Combo(heroes, key = '_B3_')],
          [sg.Text('Hero 4'), sg.Combo(heroes, key = '_A4_'), sg.Push(), sg.Text('Hero 4'), sg.Combo(heroes, key = '_B4_')],
          [sg.Text('Hero 5'), sg.Combo(heroes, key = '_A5_'), sg.Push(), sg.Text('Hero 5'), sg.Combo(heroes, key = '_B5_')],
          [sg.Push(), sg.Text('Calculation type'), sg.Combo(['weighted', 'raw winrate'], key='_weights_', default_value='raw winrate'), sg.Button('Randomize'),  sg.Button('Update Results')]]

window = sg.Window('Draft Analyser', layout)

# Depending on which button is hit, decides which functions should be called
while True:  # Event Loop
    event, values = window.read()
    if event == 'Randomize':
        randomHeroes()
    if event == 'Update Results':
        draft = list(values.values())[0:10]
        calcType = list(values.values())[10]
        updateImages(draft)
        results = analys.findRatings(draft, calcType)
        [[window[i+1,j+1].update(str(round(10*results[i,j],3)),text_color=['green' if results[i,j]>0 else 'red' if results[i,j]<0 else'white']) for i in range(6)] for j in range(6)]
    if event == sg.WIN_CLOSED or event == 'Exit':
        break


window.close()

# values = {'_A1_': 'drow_ranger', '_B1_': 'troll_warlord', '_A2_': 'primal_beast', '_B2_': 'nyx_assassin', '_A3_':
# 'naga_siren', '_B3_': 'meepo', '_A4_': 'gyrocopter', '_B4_': 'skywrath_mage', '_A5_': 'huskar', '_B5_': 'spectre'}