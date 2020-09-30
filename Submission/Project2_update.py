# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 12:12:50 2019

@author: User
"""
from __future__ import print_function
import kivy
kivy.require("1.9.2")
import pypmml as pyml
import pandas as pd
import numpy as np
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
# from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.bubble import Bubble
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label

# from kivy.clock import mainthread
from kivy.animation import Animation
import pandas as pd
import string
sm = ScreenManager()
# result
home_province_choices = ['Gauteng', 'Mpumalanga', 'Limpopo', 'Eastern Cape', 'Kwazulu Natal', 'Northern Cape',
                                'Free State', 'Western Cape', 'North West', "N/A"]
school_setting_choices = ["Rural", "Urban", "N/A"]
school_quintile_choices = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', "N/A"]
nationality_choices = ["South African", "International"]
plan_choices = ['Biochemistry and Cell Biology', 'Geography', 'Genetics & Development Biology',
                'Applied & Experimental Physiology', 'Advanced Earth Sciences', 'Chemistry',
                'Ecology Environment and Conservation', 'Computational and Applied Mathematics', 'Human Physiology',
                'Computer Science', 'Applied Chemistry', 'Archaeology','Animal Plant and Environmental Sciences', 'Actuarial Science',
                'Biological Sciences', 'Geology', 'Microbiology and Biotechnology',
                'Nuclear Sciences and Engineering', 'Chemistry with Chemical Engineering', 'Applied Bioinformatics',
                'Economic Science', 'Mathematics', 'Astronomy Astrophysics', 'Investment and Corporate Finance',
                'Plant Sciences','Applied Computing', 'Medical Cell Biology', 'Materials Science', 'Information Systems',
                'Geography and Archaeology Sciences', 'Human Biology', 'Economic Theory', 'Material Science with Metallurgy', 'Physics',
                'Physical Science', 'Mathematics of Finance',
                'Mathematical Sciences A']
data = []
plan_choices = sorted(plan_choices)
Builder.load_string("""
<DisclaimerWindow>:
    FloatLayout:
        cols:1
        Label:
            size_hint: .25, .35
            pos_hint: {"x":.05,"y":.7}
            canvas.before:
                Rectangle:
                    pos: self.center_x - 50, self.center_y - 50 # default size is 100x100
                    source: 'logo.PNG'
        Label:
            size_hint: .3, .4
            pos_hint: {"x":.35,"y":.7}
            text: "DISCLAIMER"
            font_size: 35
            color: 1,1,0,1
        Label:
            size_hint: .3, .4
            pos_hint: {"x":.35,"y":.4}
            text: "This system is designed to show you an estimate of your academic trajectory for your chosen Plan."
            font_size: 25

        Label:
            size_hint: .3, .4
            pos_hint: {"x":.35,"y":.3}
            text: "Keep in mind that the model used is 70% accurate. Accuracy decreases the less information you provide"
            font_size: 25

        NormalButton:
            id: accept
            size_hint: .2, .1
            pos_hint: {"x":.4,"y":.15}
            allow_stretch: False
            keep_ratio: True
            source: "yellowbetter.png"
            on_release:
                app.root.current = "second"
                root.manager.transition.direction = "left"
            Label:
                center: accept.center
                color: 0,0,0,1
                text: "I understand and accept"
<NormalButton@ButtonBehavior+Image>
<quintile>
    size_hint: (None, None)
    size: (520, 93)
    background_color: 0,0,1,1
    pos_hint: {"center_x":.18,"center_y":.43}
    BubbleButton:
        font_size: 12
        color: 1,1,0,1
        text:"Quintile: \\n A ranking of your high school according to the income level of the surrounding neighbourhood. \\n Q1-Q3: Little to no fees \\n Q4: Model C and schools that charge higher fees \\n Q5: Private schools"
        on_press:
            print(" ")
<SecondWindow>:
    FloatLayout:
        Label:
            size_hint: .25, .35
            pos_hint: {"x":.001,"y":.7}
            canvas.before:
                Rectangle:
                    pos: self.center_x - 50, self.center_y - 50 # default size is 100x100
                    source: 'logo.PNG'
        NormalButton:
            id: back
            size_hint: .1, .08
            pos_hint: {"x":.45,"y":.045}
            allow_stretch: False
            keep_ratio: True
            source: "yellowbetter.png"
            on_release:
                app.root.current = "DISCLAIMER"
                root.manager.transition.direction = "right"
            Label:
                center: back.center
                text: "Go back to disclaimer"
                color: 0,0,0,1
        NormalButton:
            id: calculate
            size_hint: .1, .08
            pos_hint: {"x":.45,"y":.12}
            allow_stretch: False
            keep_ratio: True
            source: "yellowbetter.png"
            on_release:
                root.pressed()
            Label:
                center: calculate.center
                text: "Calculate Trajectory"
                color: 0,0,0,1
<P>:
    Label:
        text: "Please choose a Plan"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}

<AFY>:
    Label:
        text: "Please input your age during your first year"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<HP>:
    Label:
        text: "Please input your Home Province"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<SQ>:
    Label:
        text: "Please input your School Quintile"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<QualMin>:
    Label:
        text: "You have a high chance of qualifying \\n in minimum time i.e. 3 years"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<Qual>:
    Label:
        text: "You have a high chance of qualifying, however, \\n not in 3 years. You may repeat years along the way. \\n Be mindful of time management and work ethics "
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<Fail>:
    Label:
        text: "You may find it difficult to pass this course. \\n Perhaps consider an alternate course or take bridging \\n courses in certain subjects that may better your chances"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<Math>:
    Label:
        text: "Please input a Mathematics mark"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<Eng>:
    Label:
        text: "Please input an English mark"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<LO>:
    Label:
        text: "Please input a Life Orientation mark"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<Core>:
    Label:
        text: "Please input your core Matric subject marks \\n i.e. an English, Mathematics and Life Orientation mark"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
<Numb>:
    Label:
        text: "Please make sure all typed values are \\n numbers between 0-100"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top": 1}
""")

class P(FloatLayout):
    pass

class AFY(FloatLayout):
    pass

class HP(FloatLayout):
    pass

class SQ(FloatLayout):
    pass

class QualMin(FloatLayout):
    pass

class Qual(FloatLayout):
    pass

class Fail(FloatLayout):
    pass

class Math(FloatLayout):
    pass

class Eng(FloatLayout):
    pass

class LO(FloatLayout):
    pass

class Core(FloatLayout):
    pass

class Numb(FloatLayout):
    pass

def show_popupP():
    show = P()
    popup_window = Popup(title="Error Message", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupAFY():
    show = AFY()
    popup_window = Popup(title="Error Message", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupHP():
    show = HP()
    popup_window = Popup(title="Error Message", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupSQ():
    show = SQ()
    popup_window = Popup(title="Error Message", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupQM():
    show = QualMin()
    popup_window = Popup(title="Your Result. Click outside of box to exit", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupQ():
    show = Qual()
    popup_window = Popup(title="Your Result. Click outside of box to exit", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupF():
    show = Fail()
    popup_window = Popup(title="Your Result. Click outside of box to exit", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupMath():
    show = Math()
    popup_window = Popup(title="Error Message", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupEng():
    show = Eng()
    popup_window = Popup(title="Error Message", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupLO():
    show = LO()
    popup_window = Popup(title="Error Message", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupCore():
    show = Core()
    popup_window = Popup(title="Error Message", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()

def show_popupNumb():
    show = Numb()
    popup_window = Popup(title="Error Message", content=show, size_hint=(None, None), size=(400,400))
    popup_window.open()


class DisclaimerWindow(Screen):
    pass

class quintile(Bubble):
    pass

class SecondWindow(Screen):
    def popP(self):
        show_popupP()

    def popAFY(self):
        show_popupAFY()

    def popHP(self):
        show_popupHP()

    def popSQ(self):
        show_popupSQ()

    def popQualMin(self):
        show_popupQM()

    def popQual(self):
        show_popupQ()

    def popFail(self):
        show_popupF()

    def popMath(self):
        show_popupMath()

    def popEng(self):
        show_popupEng()

    def popLO(self):
        show_popupLO()

    def popCore(self):
        show_popupCore()

    def popNumb(self):
        show_popupNumb()


    def show_bubble(self, *l):
        if not hasattr(self, 'bubb'):
            self.bubb = bubb = quintile()
            self.add_widget(bubb)
        else:
            values = ('left_mid')
            index = values.index(self.bubb.arrow_pos)
            self.bubb.arrow_pos = values[(index + 1) % len(values)]

    def remove_bubble(self, bubb):
        self.remove_widget(bubb)

    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        # self.cols=6
        Color(rgba=(.5, .5, .5))
        # Rectangle(size=self.size, pos=self.pos)
        self.add_widget(Label(text='Fill in the fields below. If a field does not apply, leave it blank.', font_size=35, pos_hint={"center_x":.5,"center_y":.9}))
        self.add_widget(Label(text = '*This field must be filled in.', font_size=25, pos_hint={"center_x":.5,"center_y":.85}, color=[1,1,0,1]))
        self.add_widget(Label(text = 'Please fill in Matric core subjects i.e. Mathematics Core/Literacy mark, an English mark and Life Orientation mark.', font_size=21, pos_hint={"center_x":.5,"center_y":.8}, color=[1,1,0,1]))


        self.add_widget(Label(text = '*', font_size= 20, pos_hint={"center_x":.05,"center_y":.7}, color=[1,1,0,1]))
        self.add_widget(Label(text='Home Province', font_size= 20, pos_hint={"center_x":.1,"center_y":.7}))
        self.dropdownHP = DropDown()
        for i in range(len(home_province_choices)):
            btn = Button(text = home_province_choices[i],  size_hint_y=None, height=20, background_color=[1,1,0,1])
            btn.bind(on_release = lambda btn: self.dropdownHP.select(btn.text))
            self.dropdownHP.add_widget(btn)
        self.mainbutton1 = Button(text ='-Select-', size_hint=(.075, .035), pos_hint={"center_x":.19,"center_y":.7}, background_color=[1,1,0,1])
        self.mainbutton1.bind(on_release = self.dropdownHP.open)
        self.dropdownHP.bind(on_select = lambda instance, x: setattr(self.mainbutton1, 'text', x))
        self.add_widget(self.mainbutton1)

        self.but_bubble = Button(text='i', pos_hint={"center_x":.24,"center_y":.65}, size_hint=(.02, .03), background_color=[0,0,1,1])
        # text="Hellloooo"
        self.but_bubble.bind(on_release=self.show_bubble)
        self.add_widget(self.but_bubble)
        p = 1
        if (p == 1):
            self.but_bubble.bind(on_release=self.remove_bubble)
            p = 0


        self.add_widget(Label(text='School Quintile', font_size= 20, pos_hint={"center_x":.1,"center_y":.65}))
        self.add_widget(Label(text = '*', font_size= 20, pos_hint={"center_x":.05,"center_y":.65}, color=[1,1,0,1]))
        dropdownSQ = DropDown()
        for i in range(len(school_quintile_choices)):
            btn = Button(text = school_quintile_choices[i],  size_hint_y=None, height=20, background_color=[1,1,0,1])
            btn.bind(on_release = lambda btn: dropdownSQ.select(btn.text))
            dropdownSQ.add_widget(btn)
        self.mainbutton2 = Button(text ='-Select-', pos_hint={"center_x":.19,"center_y":.65}, size_hint=(.075, .035), background_color=[1,1,0,1])
        self.mainbutton2.bind(on_release = dropdownSQ.open)
        dropdownSQ.bind(on_select = lambda instance, x: setattr(self.mainbutton2, 'text', x))
        self.add_widget(self.mainbutton2)

        self.add_widget(Label(text='School Setting', font_size= 20, pos_hint={"center_x":.1,"center_y":.6}))
        dropdownSS = DropDown()
        for i in range(len(school_setting_choices)):
            btn = Button(text = school_setting_choices[i],  size_hint_y=None, height=20, background_color=[1,1,0,1])
            btn.bind(on_release = lambda btn: dropdownSS.select(btn.text))
            dropdownSS.add_widget(btn)
        self.mainbutton3 = Button(text ='-Select-', pos_hint={"center_x":.19,"center_y":.6}, size_hint=(.075, .035), background_color=[1,1,0,1])
        self.mainbutton3.bind(on_release = dropdownSS.open)
        dropdownSS.bind(on_select = lambda instance, x: setattr(self.mainbutton3, 'text', x))
        self.add_widget(self.mainbutton3)

        self.add_widget(Label(text='Nationality', font_size= 20, pos_hint={"center_x":.1,"center_y":.55}))
        dropdownN = DropDown()
        for i in range(len(nationality_choices)):
            btn = Button(text = nationality_choices[i],  size_hint_y=None, height=20, background_color=[1,1,0,1])
            btn.bind(on_release = lambda btn: dropdownN.select(btn.text))
            dropdownN.add_widget(btn)
        self.mainbutton4 = Button(text ='-Select-', pos_hint={"center_x":.19,"center_y":.55}, size_hint=(.075, .035), background_color=[1,1,0,1])
        self.mainbutton4.bind(on_release = dropdownN.open)
        dropdownN.bind(on_select = lambda instance, x: setattr(self.mainbutton4, 'text', x))
        self.add_widget(self.mainbutton4)

        self.add_widget(Label(text='Age at First Year', font_size= 20, pos_hint={"center_x":.1,"center_y":.5}))
        self.AFY= TextInput(multiline=False, pos_hint={"center_x":.19,"center_y":.5}, size_hint=(.075, .035))
        self.add_widget(self.AFY)
        self.add_widget(Label(text = '*', font_size= 20, pos_hint={"center_x":.05,"center_y":.5}, color=[1,1,0,1]))

# #######################

        self.add_widget(Label(text='NBTAL', font_size= 20, pos_hint={"center_x":.4,"center_y":.7}))
        self.NBTAL= TextInput(multiline=False, pos_hint={"center_x":.49,"center_y":.7}, size_hint=(.075, .035))
        self.add_widget(self.NBTAL)

        self.add_widget(Label(text='NBTMA', font_size= 20, pos_hint={"center_x":.4,"center_y":.65}))
        self.NBTMA= TextInput(multiline=False, pos_hint={"center_x":.49,"center_y":.65}, size_hint=(.075, .035))
        self.add_widget(self.NBTMA)

        self.add_widget(Label(text='NBTQL', font_size= 20, pos_hint={"center_x":.4,"center_y":.6}))
        self.NBTQL= TextInput(multiline=False, pos_hint={"center_x":.49,"center_y":.6}, size_hint=(.075, .035))
        self.add_widget(self.NBTQL)
# #######################
        self.add_widget(Label(text='Core Mathematics', font_size= 20, pos_hint={"center_x":.75,"center_y":.7}))
        self.CM= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.7}, size_hint=(.075, .035))
        self.add_widget(self.CM)

        self.add_widget(Label(text='Mathematics Literacy', font_size= 20, pos_hint={"center_x":.75,"center_y":.65}))
        self.ML= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.65}, size_hint=(.075, .035))
        self.add_widget(self.ML)

        self.add_widget(Label(text='Additional Mathematics', font_size= 20, pos_hint={"center_x": .75,"center_y":.6}))
        self.AM= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.6}, size_hint=(.075, .035))
        self.add_widget(self.AM)

        self.add_widget(Label(text='English Home Language', font_size= 20, pos_hint={"center_x":.75,"center_y":.55}))
        self.EHL= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.55}, size_hint=(.075, .035))
        self.add_widget(self.EHL)

        self.add_widget(Label(text='English First Additional Language', font_size= 20, pos_hint={"center_x":.73,"center_y":.5}))
        self.EFAL= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.5}, size_hint=(.075, .035))
        self.add_widget(self.EFAL)

        self.add_widget(Label(text='Computer Studies', font_size= 20, pos_hint={"center_x":.75,"center_y":.45}))
        self.CS= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.45}, size_hint=(.075, .035))
        self.add_widget(self.CS)

        self.add_widget(Label(text='Physical Sciences', font_size= 20, pos_hint={"center_x":.75,"center_y":.4}))
        self.PS= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.4}, size_hint=(.075, .035))
        self.add_widget(self.PS)

        self.add_widget(Label(text='Life Sciences', font_size= 20, pos_hint={"center_x":.75,"center_y":.35}))
        self.LS= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.35}, size_hint=(.075, .035))
        self.add_widget(self.LS)

        self.add_widget(Label(text='Geography', font_size= 20, pos_hint={"center_x":.75,"center_y":.3}))
        self.GEOG= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.3}, size_hint=(.075, .035))
        self.add_widget(self.GEOG)

        self.add_widget(Label(text='Life Orientation', font_size= 20, pos_hint={"center_x":.75,"center_y":.25}))
        self.LO= TextInput(multiline=False, pos_hint={"center_x":.87,"center_y":.25}, size_hint=(.075, .035))
        self.add_widget(self.LO)

        self.add_widget(Label(text='Choose a Plan Description', font_size= 20, pos_hint={"center_x":.3,"center_y":.35}))
        self.add_widget(Label(text = '*', font_size= 20, pos_hint={"center_x":.215,"center_y":.35}, color=[1,1,0,1]))
        dropdownPD = DropDown()
        for i in range(len(plan_choices)):
            btn = Button(text = plan_choices[i],  size_hint_y=None, height=20, background_color=[1,1,0,1])
            btn.bind(on_release = lambda btn: dropdownPD.select(btn.text))
            dropdownPD.add_widget(btn)
        self.mainbutton5 = Button(text ='-Select-', pos_hint={"center_x":.5,"center_y":.35}, size_hint=(.185, .035), background_color=[1,1,0,1])
        self.mainbutton5.bind(on_release = dropdownPD.open)
        dropdownPD.bind(on_select = lambda instance, x: setattr(self.mainbutton5, 'text', x))
        self.add_widget(self.mainbutton5)

        HP_Data = self.mainbutton1.text
        SS_Data = self.mainbutton3.text
        SQ_Data = self.mainbutton2.text
        Nat_Data = self.mainbutton4.text
        AFY_Data = self.AFY.text
        NBTAL_Data = self.NBTAL.text
        NBTQL_Data= self.NBTQL.text
        NBTMA_Data = self.NBTMA.text
        CM_Data = self.CM.text
        ML_Data = self.ML.text
        AM_Data = self.AM.text
        EHL_Data = self.EHL.text
        EFAL_Data = self.EFAL.text
        CS_Data = self.CS.text
        PS_Data = self.PS.text
        LS_Data = self.LS.text
        GEOG_Data = self.GEOG.text
        LO_Data =self.LO.text
        Plan_Data = self.mainbutton5.text

    def numb(self, str):
        if (str == ''):
            return True
        else:
            try:
                int(str)
                if (int(str) < 101 and int(str) >= 0):
                    return True
            except ValueError:
                return False

    # def bigNumb(self, str):


    def pressed(self):
        del data[:]
        data.append(self.mainbutton1.text)  #0
        data.append(self.mainbutton2.text) #1
        data.append(self.mainbutton3.text) #2
        data.append(self.mainbutton4.text) #3
        data.append(self.AFY.text) #4
        data.append(self.NBTAL.text) #5
        data.append(self.NBTQL.text) #6
        data.append(self.NBTMA.text) #7
        data.append(self.CM.text) #8
        data.append(self.ML.text) #9
        data.append(self.AM.text) #10
        data.append(self.EHL.text) #11
        data.append(self.EFAL.text) #12
        data.append(self.CS.text) #13
        data.append(self.PS.text) #14
        data.append(self.LS.text) #15
        data.append(self.GEOG.text) #16
        data.append(self.LO.text) #17
        data.append(self.mainbutton5.text) #18

        if (data[0] == 'Gauteng') :
            data[0] = 'GA'
        elif (data[0] ==  'Mpumalanga'):
            data[0] = 'MP'
        elif (data[0] == 'Limpopo'):
            data[0] = 'LP'
        elif (data[0] == 'Estern Cape'):
            data[0] = 'EC'
        elif (data[0] == 'Kwazulu Natal'):
            data[0] = 'KZ'
        elif (data[0] == 'Northern Cape'):
            data[0] = 'NC'
        elif (data[0] == 'Free State'):
            data[0] = 'FS'
        elif (data[0] == 'Western Cape'):
            data[0] = 'WC'
        elif (data[0] == 'North West'):
            data[0] = 'NW'
        elif (data[0] == 'N/A'):
            data[0] = np.nan

        if (data[2] == 'Urban'):
            data[2] = 'URBAN'
        elif (data[2] == 'Rural'):
            data[2] = 'RURAL'
        elif ((data[2] == "N/A") or (data[2] == '-Select-')):
            data[2] = np.nan

        if ((data[1] == 'N/A')):
            data[1] = np.nan
        if (data[3] == "International"):
            data[3] = "IS"
        elif (data[3] == "South African"):
            data[3] = "ZAF"

        model = pyml.Model.fromFile('DTModelUpdate.pmml')
        running = True
        if (data[4] == ''):  #Age
            running = False
            self.popAFY()
            return
        # else:
        #     data[4] = int(data[4])

        if (data[1] == '-Select-'):  #SQ
            running = False
            self.popSQ()
            return

        if (data[0] == '-Select-'):  #HP
            running = False
            self.popHP()
            return
        mark_run = True
        if ((data[11] == '') and (data[12] == '') and (data[9] == '') and
            (data[8] == '') and  (data[17] == '')):
            running = False
            mark_run = False
            self.popCore()
            return

        if (mark_run):
            if ((data[9] == '') and (data[8] == '')):
                running = False
                self.popMath()
                return

            if ((data[11] == '') and (data[12] == '')):
                running = False
                self.popEng()
                return
            if (((data[11] != '') or (data[12] != '')) and ((data[9] != '') or
            (data[8] != '')) and  (data[17] == '')):
                running = False
                self.popLO()
                return
        if (not self.numb(data[4]) or not self.numb(data[5]) or not self.numb(data[6]) or not self.numb(data[7]) or not self.numb(data[8]) or not self.numb(data[9])
            or not self.numb(data[10]) or not self.numb(data[11]) or not self.numb(data[12]) or not self.numb(data[15]) or not self.numb(data[14]) or not self.numb(data[15])
            or not self.numb(data[16]) or not self.numb(data[17])):
            running = False
            self.popNumb()
            return

        else:
            if (data[8] != ''):
                data[8] = int(data[8])
            if (data[9] != ''):
                data[9] = int(data[9])
            if (data[12] != ''):
                data[12] = int(data[12])
            if (data[11] != ''):
                data[11] = int(data[11])
            if (data[17] != ''):
                data[17] = int(data[17])
            if (data[5] == ''):
                data[5] = np.nan
            else:
                data[5] = int(data[5])

            if (data[7] == ''):
                data[7] = np.nan
            else:
                data[7] = int(data[7])

            if (data[6] == ''):
                data[6] = np.nan
            else:
                data[6] = int(data[6])

            if (data[10] == ''):
                data[10] = np.nan
            else:
                data[10] = int(data[10])

            if (data[13] == ''):
                data[13] = np.nan
            else:
                data[13] = int(data[13])
            if (data[14] == ''):
                data[14] = np.nan
            else:
                data[14] = int(data[14])
            if (data[15] == ''):
                data[15] = np.nan
            else:
                data[15] = int(data[15])
            if (data[16] == ''):
                data[16] = np.nan
            else:
                data[16] = int(data[16])
        if (data[18] == '-Select-'):
            running = False
            self.popP()
            return

        # if((data[8] == '') or (data[8] < 70)):
        #     data[4] = 32
        # if ((data[5] == '') or (data[6] == '')):
        #     data[4] = 29
        # if ((data[8] != '') and (data[8] > 75) and (data[14] > 75)):
        #     data[4] = 20
        # if (((data[8] == np.nan) and (data[9] < 85)) or (data[14] == np.nan) or (data[14] < 70)):
        #     data[4] = 2016
        if ((data[18] != '-Select-') and (running == True)):
            prediction = model.predict(pd.Series({'PlanDescription' : data[18],
                                     'Homeprovince' : data[0],
                                     'AgeatFirstYear' : data[4],
                                     'SchoolQuintile' : data[1],
                                     'isRuralorUrban' : data[2],
                                     'LifeOrientation' : data[17],
                                     'MathematicsMatricMajor' : data[8],
                                     'MathematicsMatricLit' : data[9],
                                     'AdditionalMathematics' : data[10],
                                     'EnglishFirstLang' : data[11],
                                     'EnglishFirstAdditional' : data[12],
                                     'ComputerStudies' : data[13],
                                     'NBTAL' : data[5],
                                     'NBTMA' : data[7],
                                     'NBTQL' : data[6],
                                     'PhysicsChem' : data[14],
                                     'Geography' : data[16],
                                     'LifeSciences' : data[15],
                                     'International' : data[3]}))
            # result = DecisionTree(model_input)
            result = prediction[1]
            if (((data[5] != np.nan) and (data[5] >= 75))  or ((data[6] != np.nan) and (data[6] >= 75))):
                result = "Qualified"

            if (result == None):
                self.popFail()
            elif(result == 'QualMin'):
                self.popQualMin()
            elif(result == 'Qualified'):
                self.popQual()
            elif(result == 'Failed'):
                self.popFail()

    pass
sm.add_widget(DisclaimerWindow(name='DISCLAIMER'))
sm.add_widget(SecondWindow(name='second'))


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        self.transition = SlideTransition(direction = 'left')

def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
