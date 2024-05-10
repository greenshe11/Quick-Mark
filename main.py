# LIBRARIES
import numpy as np
import threading
from datetime import datetime
import shutil
import os
import time
import matplotlib.pyplot as plt
import logging
import matplotlib
matplotlib.use('agg') 
# Disable debug messages from Matplotlib
logging.getLogger('matplotlib').setLevel(logging.WARNING)

try:
    on_android = True
    from android.storage import primary_external_storage_path
    android_storage = primary_external_storage_path()
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    from jnius import cast

    autoclass = autoclass
    python_activity = autoclass('org.kivy.android.PythonActivity')
    context = autoclass('android.content.Context')
    activity = python_activity.mActivity
    vibrator = activity.getSystemService(context.VIBRATOR_SERVICE)

except Exception as e:
    on_android = False

def vibrate(pattern):
        if on_android:
            vibrator.vibrate(pattern)

# LOCAL FILES/MODULES
from utilities.misc.util4image import fit_score,stich_all_image as stitch_sheet, fit_score
from utilities.misc.filesystem import *
from utilities.misc.searchsystem import SearchSystem
from utilities.misc.image2pdf import generate as generate_pdf
from screens.camera import CameraWidget
import utilities.misc.feedback_sheet as feedback

# KIVY/KIVYMD IMPORTS
#kivymd misc
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivymd.toast import toast
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.image import Image as CoreImage


#kivymd.uix

from kivymd.uix.list import IconLeftWidget, IconLeftWidgetWithoutTouch, IconRightWidgetWithoutTouch
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, FadeTransition
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton,MDRaisedButton, MDRectangleFlatButton, MDRoundFlatButton, MDFillRoundFlatButton
from kivymd.uix.card import MDSeparator
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, TwoLineListItem, TwoLineIconListItem, TwoLineAvatarIconListItem, OneLineAvatarIconListItem, ThreeLineAvatarIconListItem
from kivy.uix.image import Image
#kivy.uix
from kivy.uix.boxlayout import BoxLayout



KV = '''
CustomScreenManager:

    HomeScreen:
    NameScreen:
    CheckScreen:
    MCScreen:
    IDScreen:
    TFScreen:
    AnalysisScreen:
    AnswerSheetScreen:
    OneCheckScreen:
    NameScreenExpanded:
    KeyScreen:
    MCQAnalysisScreen:
    TFAnalysis:
    KeyScreenIDTF:
    IDAnalysis:

<NextDisplay@Image>:
    
    source: 'assets/next.png'
    size_hint: (1,1)
    pos_hint: {'center_x':0.5,'center_y':0.5}
    opacity: 0

<PreviousDisplay@Image>:
    
    source: 'assets/previous.png'
    size_hint: (1,1)
    pos_hint: {'center_x':0.5,'center_y':0.5}
    opacity: 0

<PreviewImage@PreviewImage>:

<KeyScreen>:
    name: 'keyscreen'
    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            right_action_items: [["cog-outline", lambda x: print(setattr(root.manager, 'current', 'name'),root.add_new_sheet(),'hello world')]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                id: pos_nav_label
                text: "Home > Sheet > "
                font_size: dp(10)
                pos_hint: {'center_x':0}
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.5,0.5,1,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                id: page_num_label
                text: "Page Number: 1 of 10"
                font_size: dp(10)
                halign: 'left'
                pos_hint: {'center_x':0}
            MDLabel:
                id: total_items_label
                text: "Total Items: 25"
                halign: 'right'
                font_size: dp(10)
                pos_hint: {'center_x':0}
        BoxLayout:
            size_hint: 1,None
            height: dp(30)
        ScrollView:
            id: scroll_view
            size_hint: (1, 1)  # Changed from (1, None)
            on_scroll_move: root.scroll_nav()
            
            MDList:
                id: saved_list
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1,1,1,1)
                padding: 0  # Set padding to 0
                spacing: 0 
                
                CustomListItem:
                CustomListItem:
                CustomListItem:
                CustomListItem:
                CustomListItem:
                CustomListItem:
                CustomListItem:
                CustomListItem:
                CustomListItem:
                CustomListItem:
        
                
    MDBoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 0.1
        md_bg_color: (0.8,0.8,0.8,1)
        #MDIconButton:
         #   id: previous
          #  icon: "skip-previous"
           # line_color: 0, 0, 0, 0
            ##theme_icon_color: "Custom"
            #icon_color: 'black'
            #pos_hint: {"center_x": .5, "center_y": .5}
            #on_release: root.previous()
            #size_hint: 0.35,1
           
        MDRectangleFlatButton:
            id: jump
            text: "JUMP"
            text_color: 'black'
            line_color: 0, 0, 0, 0
            on_release: root.jump()
            pos_hint: {"center_x": .5, "center_y": .5}
            size_hint: 0.35,1
        #MDIconButton:
         #   id: next
          #  icon: 'skip-next'
           # theme_icon_color: "Custom"
           # icon_color: 'black'
           # on_release: root.next()
            #size_hint: 0.35,1
    NextDisplay:
        id: next_display
    PreviousDisplay:
        id: previous_display

<KeyScreenIDTF>:
    name: 'keyscreenidtf'
    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            right_action_items: [["cog-outline", lambda x: print(setattr(root.manager, 'current', 'name'),root.add_new_sheet(),'hello world')]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                id: pos_nav_label
                text: "Home > Sheet > "
                font_size: dp(10)
                pos_hint: {'center_x':0}
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.5,0.5,1,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                id: page_num_label
                text: "Page Number: 1 of 10"
                font_size: dp(10)
                halign: 'left'
                pos_hint: {'center_x':0}
            MDLabel:
                id: total_items_label
                text: "Total Items: 25"
                halign: 'right'
                font_size: dp(10)
                pos_hint: {'center_x':0}
        BoxLayout:
            size_hint: 1,None
            height: dp(30)
        ScrollView:
            id: scroll_view
            size_hint: (1, 1)  # Changed from (1, None)
            on_scroll_move: root.scroll_nav()
            
            MDList:
                id: saved_list
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1,1,1,1)
                padding: 0  # Set padding to 0
                spacing: 0

                MDStackLayout:
                    id: idtf_items
                    size_hint: 1,None
                    spacing: 10
                    height: dp(400)  # Adjust the height as needed
                    orientation: 'tb-lr'
                    padding: 40,40
                    spacing: 20

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: (1,None)
                        height: dp(48)
                        
                        
                        MDLabel:
                            id: _1
                            text: '1.'
                            size_hint_x: 0.2
                        
                        MDTextField:
                            id: _1_field
                            mode: "fill"
                            hint_text: '(max: 15 characters)'
                            size_hint_x: 0.8
                            font_size: '18dp'
                            max_text_length: 15
                            on_text: (lambda *args: root.autovalidate_item(1))()

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: (1,None)
                        height: dp(48)
                        
                        
                        MDLabel:
                            id: _2
                            text: '2.'
                            size_hint_x: 0.2 
                        
                        MDTextField:
                            id: _2_field
                            mode: "fill"
                            opacity: 1
                            hint_text: '(max: 15 characters)'
                            size_hint_x: 0.8
                            font_size: '18dp'
                            max_text_length: 15
                            on_text: (lambda *args: root.autovalidate_item(2))()

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: (1,None)
                        height: dp(48)
                    
                        
                        MDLabel:
                            id: _3
                            text: '3.'
                            size_hint_x: 0.2 
                        
                        MDTextField:
                            id: _3_field
                            mode: "fill"
                            hint_text: '(max: 15 characters)'
                            size_hint_x: 0.8
                            font_size: '18dp'
                            max_text_length: 15
                            on_text: (lambda *args: root.autovalidate_item(3))()

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: (1,None)
                        height: dp(48)
                        
                        
                        MDLabel:
                            id: _4
                            text: '4.'
                            size_hint_x: 0.2
                        
                        MDTextField:
                            id: _4_field
                            mode: "fill"
                            #width: "240dp" 
                            font_size: '18dp'
                            hint_text: '(max: 15 characters)'
                            size_hint_x: 0.8
                            max_text_length: 15
                            on_text: (lambda *args: root.autovalidate_item(4))()

                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: (1,None)
                        height: dp(48)
                        
                        MDLabel:
                            id: _5
                            text: '5'
                            size_hint_x: 0.2
                        
                        MDTextField:
                            id: _5_field
                            hint_text: '(max: 15 characters)'
                            mode: "fill"
                            size_hint_x: 0.8
                            font_size: '18dp'
                            max_text_length: 15
                            on_text: (lambda *args: root.autovalidate_item(5))()

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 0.1
        md_bg_color: (0.8,0.8,0.8,1)
        #MDIconButton:
         #   id: previous
          #  icon: "skip-previous"
           # line_color: 0, 0, 0, 0
            ##theme_icon_color: "Custom"
            #icon_color: 'black'
            #pos_hint: {"center_x": .5, "center_y": .5}
            #on_release: root.previous()
            #size_hint: 0.35,1

        MDRectangleFlatButton:
            id: jump
            text: "JUMP"
            text_color: 'black'
            line_color: 0, 0, 0, 0
            on_release: root.jump()
            pos_hint: {"center_x": .5, "center_y": .5}
            size_hint: 0.35,1
        #MDIconButton:
         #   id: next
          #  icon: 'skip-next'
           # theme_icon_color: "Custom"
           # icon_color: 'black'
           # on_release: root.next()
            #size_hint: 0.35,1
    NextDisplay:
        id: next_display
    PreviousDisplay:
        id: previous_display

    


    

<CustomListItem@MDStackLayout>:
    
    size_hint: 1,None
    height: dp(48)  # Adjust the height as needed
    orientation: 'lr-tb'
    padding: 20,20
    
    
    MDLabel:
        text: "Custom Item"
        halign: 'center'
        size_hint_x: 0.2  # Adjust the width ratio as needed
        theme_text_color: "Custom"
        text_color: (0.5,0.5,1,1)
        size_hint_y: 1

    MDIconButton:
        icon: 'alpha-a'
        size_hint_x: 0.2  # Adjust the width ratio as needed
        size_hint_y: 1
        on_release: root.choice_click(self,app)
    MDIconButton:
        icon: 'alpha-b'
        size_hint_y: 1
        size_hint_x: 0.2  # Adjust the width ratio as needed
        on_release: root.choice_click(self,app)
    MDIconButton:
        icon: 'alpha-c'
        size_hint_x: 0.2  # Adjust the width ratio as needed
        size_hint_y: 1
        on_release: root.choice_click(self,app)
    MDIconButton:
        icon: 'alpha-d'
        size_hint_x: 0.2  # Adjust the width ratio as needed
        size_hint_y: 1
        on_release: root.choice_click(self,app)
    
<HomeScreen>:
    
    name: 'home'

    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # White color
        Rectangle:
            size: self.size
            pos: self.pos
    
    MDTopAppBar:
        title: "QuickMark"
        pos_hint: {"top": 1,}
        left_action_items: [['menu', lambda x: app.screen_manager_func()]]
        right_action_items: [["e", ""]]
        elevation: 0


    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['close-box', lambda x: app.screen_manager_func()]]
            right_action_items: [["",""]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                id: pos_nav_label
                text: "Home > "
                font_size: dp(10)
                pos_hint: {'center_x':0}
                

        BoxLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(80)
            padding: (20,10)
            size_hint: (0.95,None)
            
            MDTextField:
                id: search
                md_bg_color: (1,1,1,1)
                icon_left: 'magnify'
                hint_text: "Search..."
                height: dp(20)
                padding: (40, 40)
                size_hint: (0.9,None)
                on_text: root.word_search(*args)

                
        BoxLayout:
            id: box_label
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], dp(10)
            size_hint: (None,None)
            orientation: 'horizontal'
            
            size_hint: (1,None)
            height: 100
            MDLabel:
                id: empty_label
                text: ""
                halign:"center"  # Center the text horizontally
                theme_text_color:"Secondary" # Set the color to gray
                size_hint_y: None
                height:20
                padding:(20, 10)  # Add padding around the label
                pos_hint:{"center_y": 0.5} 
        
        ScrollView:
            id: scroll_view
            size_hint: (1, None)
            height: dp(400)

            MDList:
                id: saved_list 
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1,1,1,1)
                padding: 0  # Set padding to 0
                spacing: 0 
    
    MDFloatingActionButton:
        icon: 'import'
        on_release:  root.import_sheet() #Call add_new_sheet method from CheckScreen        
        pos_hint: {'center_x': .85, 'top': .22}
        elevation: 0

    MDFloatingActionButton:
        id: plus_button
        icon: 'file-document-plus-outline'
        on_release: root.add_new_sheet()          
        pos_hint: {'center_x': .85, 'top': .12}
        elevation: 0
    NextDisplay:
        id: next_display
    PreviousDisplay:
        id: previous_display
    
                                 
<NameScreen>:
    name: 'name'

    MDLabel:
        id: display_label
        text: ""
        halign: "center"
        pos_hint: {"top": 1.33}
    
    MDStackLayout:
        md_bg_color: (1,1,1,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            right_action_items: [["", ""]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                text: "Home > Sheet > "
                font_size: dp(10)
                pos_hint: {'center_x':0}
        
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'vertical'
            height: dp(100)
            padding: (20,20)
            size_hint: (0.95,None)
                
    
            BoxLayout:
                size_hint: 1,None
                padding: (25,25)
                spacing: dp(10)
                orientation: 'horizontal'
                MDTextField:
                    id: text_field
                    mode: "fill"
                    multiline: False
                    size_hint_y: None
                    size_hint_x: None
                    height: dp(20)
                    width: "250dp"
                    pos_hint: {"center_y":0.5, "center_x": .5}
                    hint_text: "Sheet Name"
                    on_text_validate: root.rename()
                    on_text: root.capitalize(*args)
            
                MDIconButton:
                    id: save_button
                    icon: 'square-edit-outline'
                    pos_hint:{"center_y":.5}
                    on_release: root.rename()
                    elevation: 0

            MDLabel:
                id: date_label
                text: 'Date Created: YYYY-MM-DD'
                color: (0.5,0.5,0.5,1)
                pos_hint: {'center_x':0.5}
                font_size: dp(10)
        BoxLayout:
            id: box_label
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], dp(10)
            size_hint: (None,None)
            orientation: 'horizontal'
            
            size_hint: (1,None)
            height: dp(10)

        ScrollView:
            id: scroll_view
            size_hint: (1, 1)

            MDList:
                id: saved_list
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1,1,1,1)
                padding: 0  # Set padding to 0
                spacing: 0 
                
                TwoLineAvatarIconListItem:
                    text: 'Check Papers'
                    secondary_text: 'Review and record student marks.'
                    secondary_font_style: 'Caption'
                    on_release: root.manager.change_screen('onecheck')
                    IconLeftWidgetWithoutTouch:
                        icon: "paperclip-check"
                    IconRightWidgetWithoutTouch:
                        icon: "chevron-right"

                TwoLineAvatarIconListItem:
                    text: 'Analysis'
                    secondary_text: 'Conduct item analysis.'
                    secondary_font_style: 'Caption'
                    on_release: root.manager.change_screen('analysis')
                    IconLeftWidgetWithoutTouch:
                        icon: "google-analytics"
                    IconRightWidgetWithoutTouch:
                        icon: "chevron-right"

                TwoLineAvatarIconListItem:
                    text: 'Sheet Settings'
                   
                    secondary_text: 'View and edit answer sheet.'
                    secondary_font_style: 'Caption'
                    on_release: print(root.prepare_answer_sheet(),root.manager.change_screen('answer_sheet'))
                    IconLeftWidgetWithoutTouch:
                        icon: "view-dashboard-edit-outline"
                    IconRightWidgetWithoutTouch:
                        id: btn_key_right
                        icon: "chevron-right"
                TwoLineAvatarIconListItem:
                    text: 'Answer Key'
                    id: btn_key
                    secondary_text: 'View or change answer keys.'
                    secondary_font_style: 'Caption'
                    on_release: root.expand_keys()
                    IconLeftWidgetWithoutTouch:
                        icon: "key-outline"
                    IconRightWidgetWithoutTouch:
                        id: btn_answer_key_icon
                        icon: "chevron-right"
                OneLineAvatarIconListItem:
                    id: mc
                    text: 'Multiple Choice'
                    opacity: 0
                    disabled: True
                    font_style: 'Body2'
                    on_release: root.manager.change_screen('keyscreen',test_type='mc')
                    IconRightWidgetWithoutTouch:
                        id: btn_key_right
                        icon: "chevron-right"
                OneLineAvatarIconListItem:
                    id: tf
                    text: 'True or False'
                    opacity: 0
                    disabled: True
                    font_style: 'Body2'
                    on_release: root.manager.change_screen('keyscreen',test_type='tf')
                    IconRightWidgetWithoutTouch:
                        id: btn_key_right
                        icon: "chevron-right"
                OneLineAvatarIconListItem:
                    id: idtf
                    text: 'Identification'
                    font_style: 'Body2'
                    opacity: 0
                    disabled: True
                    on_release: root.manager.change_screen('keyscreenidtf')
                    IconRightWidgetWithoutTouch:
                        id: btn_key_right
                        icon: "chevron-right"
    MDFloatingActionButton:
        icon: 'share-variant-outline'
        on_release:  root.share_sheet() #Call add_new_sheet method from CheckScreen        
        pos_hint: {'center_x': .85, 'top': .32}
        elevation: 0

    MDFloatingActionButton:
        icon: 'export'
        on_release:  root.export_sheet() #Call add_new_sheet method from CheckScreen        
        pos_hint: {'center_x': .85, 'top': .22}
        elevation: 0

    MDFloatingActionButton:
        icon: 'trash-can-outline'
        on_release:  root.delete_sheet() #Call add_new_sheet method from CheckScreen        
        pos_hint: {'center_x': .85, 'top': .12}
        elevation: 0
        md_bg_color: 'red'

<NameScreenExpanded>:
    name: 'name_expanded'

    MDLabel:
        id: display_label
        text: ""
        halign: "center"
        pos_hint: {"top": 1.33}
    
    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            right_action_items: [["", ""]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                text: "Home > Sheet > "
                font_size: dp(10)
                pos_hint: {'center_x':0}
        
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'vertical'
            height: dp(100)
            padding: (20,20)
            size_hint: (0.95,None)
                
    
            BoxLayout:
                size_hint: 1,None
                padding: (25,25)
                spacing: dp(10)
                orientation: 'horizontal'
                MDTextField:
                    id: text_field
                    mode: "fill"
                    multiline: False
                    size_hint_y: None
                    size_hint_x: None
                    height: dp(20)
                    width: "250dp"
                    pos_hint: {"center_y":0.5, "center_x": .5}
                    hint_text: "Sheet Name"
                    on_text_validate: root.rename()
                    on_text: root.capitalize(*args)
            
                MDIconButton:
                    id: save_button
                    icon: 'square-edit-outline'
                    pos_hint:{"center_y":.5}
                    on_release: root.rename()
                    elevation: 0

            MDLabel:
                id: date_label
                text: 'Date Created: YYYY-MM-DD'
                color: (0.5,0.5,0.5,1)
                pos_hint: {'center_x':0.5}
                font_size: dp(10)
        BoxLayout:
            id: box_label
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], dp(10)
            size_hint: (None,None)
            orientation: 'horizontal'
            
            size_hint: (1,None)
            height: dp(10)

        ScrollView:
            id: scroll_view
            size_hint: (1, 1)

            MDList:
                id: saved_list
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1,1,1,1)
                padding: 0  # Set padding to 0
                spacing: 0 
                
                TwoLineAvatarIconListItem:
                    text: 'Check Papers'
                    secondary_text: 'Review and record student marks.'
                    secondary_font_style: 'Caption'
                    on_release: root.manager.change_screen('onecheck')
                    IconLeftWidgetWithoutTouch:
                        icon: "paperclip-check"
                    IconRightWidgetWithoutTouch:
                        icon: "chevron-right"

                TwoLineAvatarIconListItem:
                    text: 'Analysis'
                    secondary_text: 'Conduct item analysis.'
                    secondary_font_style: 'Caption'
                    on_release: root.manager.change_screen('analysis')
                    IconLeftWidgetWithoutTouch:
                        icon: "google-analytics"
                    IconRightWidgetWithoutTouch:
                        icon: "chevron-right"

                TwoLineAvatarIconListItem:
                    text: 'Sheet Settings'
                   
                    secondary_text: 'View and edit answer sheet.'
                    secondary_font_style: 'Caption'
                    on_release: print(root.prepare_answer_sheet(),root.manager.change_screen('answer_sheet'))
                    IconLeftWidgetWithoutTouch:
                        icon: "view-dashboard-edit-outline"
                    IconRightWidgetWithoutTouch:
                        id: btn_key_right
                        icon: "chevron-right"
                TwoLineAvatarIconListItem:
                    text: 'Answer Key'
                    id: btn_key
                    secondary_text: 'View or change answer keys.'
                    secondary_font_style: 'Caption'
                    
                    on_release: root.manager.change_screen('name')
                    IconLeftWidgetWithoutTouch:
                        icon: "key-outline"
                    IconRightWidgetWithoutTouch:
                        id: btn_key_right
                        icon: "chevron-down"
                OneLineAvatarIconListItem:
                    text: 'Multiple Choice'
                    
                    on_release: root.manager.change_screen('keyscreen',test_type='mc')
                    IconRightWidgetWithoutTouch:
                        id: btn_key_right
                        icon: "chevron-right"
                OneLineAvatarIconListItem:
                    text: 'True or False'
                    
                    on_release: root.manager.change_screen('keyscreen',test_type='tf')
                    IconRightWidgetWithoutTouch:
                        id: btn_key_right
                        icon: "chevron-right"
                OneLineAvatarIconListItem:
                    text: 'Identification'
                    
                    on_release: print(root.manager.change_screen('ID'))
                    IconRightWidgetWithoutTouch:
                        id: btn_key_right
                        icon: "chevron-right"
    MDFloatingActionButton:
        icon: 'trash-can-outline'
        on_release:  root.manager.get_screen('name').delete_sheet() #Call add_new_sheet method from CheckScreen        
        pos_hint: {'center_x': .85, 'top': .12}
        elevation: 0
        md_bg_color: 'red'
            
<AnswerSheetScreen>:
    name: 'answer_sheet'
    orientation: 'vertical'
    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            right_action_items: [["",""]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                text: "Home > Sheet > Sheet Settings"
                font_size: dp(10)
                pos_hint: {'center_x':0}
        
        MDGridLayout:
            cols: 2
            spacing: dp(10)
            size_hint: None, None
            pos_hint: {'center_x':0.15}

            MDGridLayout:
                cols: 2
                size_hint: None, None
                width: dp(200) 
                height: dp(50)
                
                MDCheckbox:
                    id: mcq_checkbox
                    size_hint: None, None
                    size: dp(48), dp(48)
                    on_active: root.show_text_field(self.active, 'mcq');root.get_fit()

                MDLabel:
                    text: "Multiple Choice"
                    size_hint: None, None
                    halign: 'left'
                    size: dp(200), dp(48)


            MDTextField:
                id: mcq_textfield
                hint_text: "(max: 100)"
                input_filter: 'int'
                mode: "fill"
                size_hint: None, None
                width: dp(400) 
                height: dp(48)
                multiline: False
                disabled: not mcq_checkbox.active
                on_text: root.get_fit()
                on_text_validate: root.apply_count()

            MDGridLayout:
                cols: 2
                spacing: dp(10)

                MDGridLayout:
                    cols: 2
                    size_hint: None, None
                    width: dp(200) 
                    height: dp(50)
                    
                    MDCheckbox:
                        id: tf_checkbox
                        size_hint: None, None
                        size: dp(48), dp(48)
                        on_active: root.show_text_field(self.active, 'tf');root.get_fit()

                    MDLabel:
                        text: "True or False"
                        size_hint: None, None
                        halign: 'left'
                        size: dp(200), dp(48)


                MDTextField:
                    id: tf_textfield
                    hint_text: "(max: 175)"
                    input_filter: 'int'
                    mode: "fill"
                    size_hint: None, None
                    width: dp(400) 
                    height: dp(48)
                    multiline: False
                    disabled: not tf_checkbox.active
                    on_text: root.get_fit()
                    on_text_validate: root.apply_count()

                MDGridLayout:
                    cols: 2
                    size_hint: None, None
                    width: dp(200) 
                    height: dp(50)
                    
                    MDCheckbox:
                        id: ident_checkbox
                        size_hint: None, None
                        size: dp(48), dp(48)
                        on_active: root.show_text_field(self.active, 'ident');root.get_fit()

                    MDLabel:
                        text: "Identification"
                        size_hint: None, None
                        halign: 'left'
                        size: dp(200), dp(48)


                MDTextField:
                    id: ident_textfield
                    hint_text: "(max: 10)"
                    input_filter: 'int'
                    mode: "fill"
                    size_hint: None, None
                    width: dp(400) 
                    height: dp(48)
                    multiline: False
                    disabled: not ident_checkbox.active
                    on_text: root.get_fit()
                    on_text_validate: root.apply_count()

    Widget:
        size_hint_y: None
        height: dp(48)

    #MDRectangleFlatButton:
     #   id: apply_btn
      #  text: "APPLY"
      #  size_hint: None, None
       # size: dp(200), dp(48)
       # pos_hint: {'top':0.52,'center_x': 0.5}
        
        #on_release: root.apply_count()

    PreviewImage:
        id: generated_image
        size_hint: 1, None
        height: dp(210)  # Set the height of the image as needed
        pos_hint: {'top':0.5,'center_x': 0.5}
        on_release: root.max_image()
    
    
    
    MDLabel:
        id: fit_label
        text: 'Fit: 0.0%'
        size_hint: 1, None
        height: dp(210)  # Set the height of the image as needed
        pos_hint: {'top':0.30,'center_x': 0.5}
        theme_text_color: 'Custom'
        text_color: (0,0,1,0.7)
        font_size: dp(28)
        halign: 'center'
        valign: 'bottom'

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 0.1
        md_bg_color: (0.8,0.8,0.8,1)
        MDIconButton:
            id: export
            icon: "file-export-outline"
            line_color: 0, 0, 0, 0
            theme_icon_color: "Custom"
            icon_color: 'black'
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release: root.open_file_manager()
            size_hint: 0.35,1
           
        MDIconButton:
            id: apply
            icon: 'content-save'
            theme_icon_color: "Custom"
            icon_color: 'black'
            on_release: root.apply_count()
            size_hint: 0.35,1
        MDIconButton:
            id: share
            icon: 'share-variant-outline'
            theme_icon_color: "Custom"
            icon_color: 'black'
            on_release: root.share()
            size_hint: 0.35,1

    #MDBoxLayout:
      #  orientation: 'horizontal'
       # size_hint: None, 1
        #pos_hint: {'center_x': 0.4}
        #padding: dp(20)
        #spacing: dp(10)

        #MDRectangleFlatButton:
        #    id: download
        #    text: "Export"
        #    size_hint: 1, None
         #   size: dp(200), dp(36)
          #  pos_hint: {'center_x': 0.5}
           # on_release: root.open_file_manager()

       # MDRectangleFlatButton:
        #    id: download
         #   text: "Share"
          #  size_hint: 1, None
           # size: dp(200), dp(36)
          #  pos_hint: {'center_x': 0.5}
          #  on_release: root.share()
    
<CheckScreen>:
    name: 'check'

    
    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            right_action_items: [["", ""]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                text: "Home > Sheet > Sessions > Check Screen"
                font_size: dp(10)
                pos_hint: {'center_x':0}

        BoxLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'vertical'
            height: dp(100)
            padding: (20,20)
            size_hint: (0.95,None)
                
    
            BoxLayout:
                size_hint: 1,None
                padding: (25,25)
                spacing: dp(10)
                orientation: 'horizontal'
                MDTextField:
                    id: check_text_field
                    mode: "fill"
                    multiline: False
                    size_hint_y: None
                    size_hint_x: None
                    height: dp(20)
                    width: "250dp"
                    pos_hint: {"center_y":0.5, "center_x": .5}
                    hint_text: "Recipient"
                    on_text_validate: root.rename()
                    #on_text: root.capitalize(*args)
            
                MDIconButton:
                    id: save_button
                    icon: 'square-edit-outline'
                    pos_hint:{"center_y":.5}
                    on_release: root.rename()
                    elevation: 0

            MDLabel:
                id: date_label
                text: 'Date Created: YYYY-MM-DD'
                color: (0.5,0.5,0.5,1)
                pos_hint: {'center_x':0.5}
                font_size: dp(10)
        BoxLayout:
            id: box_label
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], dp(10)
            size_hint: (None,None)
            orientation: 'horizontal'
            
            size_hint: (1,None)
            height: dp(10)

        BoxLayout:
            id: img_box
            size_hint: (1,0.5)
            pos_hint: {'center_x':0.5, 'center_y':0.5}
            BoxLayout:
                size_hint:(0.15,1)
            PreviewImage:
                id: feedback_img
                source: 'assets/loading.jpg'
                size_hint: (0.7,1)
                #pos_hint: {'top': 0.8, 'center_x': 0.5}
                allow_stretch: True
                keep_ratio: True
                on_release: root.max_image()
            BoxLayout:
                size_hint:(0.15,1)

        MDStackLayout:
            id: stack_layout
            spacing: dp(5)
            pos_hint: {'top':0.2, 'center_x': 0.5}
            size_hint: 1,None
            height: dp(500)
            padding: 20
                
            MDLabel:
                text: 'Scores'
                theme_text_color: 'Primary'
                font_size: dp(15)
                size_hint_y: None
                size_hint_x: None
                height: dp(10)

            MDLabel:
                id: mc_indicator
                text: 'Multiple Choice: '
                theme_text_color: 'Secondary'
                font_size: dp(12)
                size_hint_y: None
                height: dp(10)

            MDLabel:
                id: tf_indicator
                text: 'True or False: '
                theme_text_color: 'Secondary'
                font_size: dp(12)
                size_hint_y: None
                height: dp(10)

            MDLabel:
                id: idtf_indicator
                text: 'Identification: '
                theme_text_color: 'Secondary'
                font_size: dp(12)
                size_hint_y: None
                height: dp(10)
    
    MDFloatingActionButton:
        id: plus_button
        icon: 'account-plus'
        on_release: app.root.get_screen('onecheck').add_new_sheet()  # Call add_new_sheet method from CheckScreen        
        pos_hint: {'center_x': .85, 'top': .22}
        elevation: 0

    

    MDFloatingActionButton:
        icon: 'trash-can-outline'
        on_release:  root.delete_session() #Call add_new_sheet method from CheckScreen        
        pos_hint: {'center_x': .85, 'top': .32}
        elevation: 0
        md_bg_color: 'red'
    
    MDBoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 0.1
        md_bg_color: (0.8,0.8,0.8,1)
        MDIconButton:
            id: export
            icon: "file-export-outline"
            line_color: 0, 0, 0, 0
            theme_icon_color: "Custom"
            icon_color: 'black'
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release: root.open_file_manager()
            size_hint: 0.35,1
           
        MDIconButton:
            id: cam_button
            icon: 'camera'
            theme_icon_color: "Custom"
            icon_color: 'black'
            
            on_release: root.switch_cam()
            size_hint: 0.35,1
        MDIconButton:
            id: share
            icon: 'share-variant-outline'
            theme_icon_color: "Custom"
            icon_color: 'black'
            on_release: root.share()
            size_hint: 0.35,1

<MCScreen>:
    name: 'MC'
    
    
    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'top': 1}  # Align to the top
        spacing: dp(10)

        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["",""]]
            elevation: 0
        ScrollView:
            id: mc_scroll_view
            size_hint: (1, None)
            MDList:
                id: mc_box_all
                size_hint_y: None
                height: self.minimum_height
         
<TFScreen>:
    name: 'TF'

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'top': 1}  # Align to the top
        spacing: dp(10)

        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [["",""]]
            elevation: 0
        ScrollView:
            id: tf_scroll_view
            size_hint: (1, None)
            MDList:
                id: tf_box_all
                size_hint_y: None
                height: self.minimum_height
        
<AnalysisScreen>:
    name: 'analysis'

    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            right_action_items: [["", ""]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                text: "Home > Sheet > Analysis"
                font_size: dp(10)
                pos_hint: {'center_x':0}

        MDBoxLayout:
            padding: dp(10)
            size_hint_y: None
            height: self.minimum_height
            pos_hint: {"center_y": 0.5}
            orientation: 'vertical'

            MDCard:
                size_hint: None, None
                size: 0.9 * root.width, "100dp"
                padding: "12dp"
                elevation: 0.5
                pos_hint: {"center_x": 0.5}
                MDBoxLayout:
                    spacing: dp(15)
                    orientation: 'vertical'
                    MDLabel:
                        text: 'Overall Statistics'
                        halign: 'center'
                    MDLabel:
                        id: mean_label
                        text: 'Average Score:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
                    MDLabel:
                        id: min_label
                        text: 'Min. Score:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
                    MDLabel:
                        id: max_label
                        text: 'Max Score:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
                    MDLabel:
                        id: std_label
                        text: 'Std. Dev:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                size_hint_x: 0.6
                size_hint_y: None
                height: dp(300)
                pos_hint: {"center_y": 0.5, 'center_x': 0.5}  # Adjusted position
                MDLabel:
                    text: "Item Analysis"
                    halign: 'center'
                    size_hint: (1,1)
                MDRaisedButton:
                    text: "Multiple Choice"
                    size_hint: (1,1)
                    pos_hint: {'center_x': 0.5}
                    on_release: root.manager.change_screen('mcqanalysis',test_type='mc' )
                MDRaisedButton:
                    text: "True or False"
                    size_hint: (1,1)
                    pos_hint: {'center_x': 0.5}
                    on_release: root.manager.change_screen('mcqanalysis',test_type='tf' )
                MDRaisedButton:
                    size_hint: (1,1)
                    text: "Identification"
                    pos_hint: {'center_x': 0.5}
                    on_release: root.manager.change_screen('mcqanalysis',test_type='idtf' )
<MCQAnalysisScreen>:
    name: 'mcqanalysis'
    
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: (1,1,1,1)
        
        MDStackLayout:
            md_bg_color: (0.95,0.95,0.95,1)
            height: self.minimum_height
            pos_hint: {'center_x': 0.5}
            MDTopAppBar:
                title: "QuickMark"
                left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
                right_action_items: [["", ""]]
                elevation: 0
            BoxLayout:
                canvas.before:
                    Color:
                        rgba: 0.95,0.95,0.95,1 # Set the background color here
                    Rectangle:
                        pos: self.pos
                        size: root.size[0], self.size[1]
                size_hint: (None,None)
                orientation: 'horizontal'
                height: dp(25)
                padding: (20,10)
                size_hint: (0.95,None)

                MDLabel:
                    text: "Home > Sheet > Analysis"
                    font_size: dp(10)
                    pos_hint: {'center_x':0}
            BoxLayout:
                canvas.before:
                    Color:
                        rgba: 0.5,0.5,1,1 # Set the background color here
                    Rectangle:
                        pos: self.pos
                        size: root.size[0], self.size[1]
                size_hint: (None,None)
                orientation: 'horizontal'
                height: dp(25)
                padding: (20,10)
                size_hint: (0.95,None)

                MDLabel:
                    id: page_num_label
                    text: "Page Number: 1 of 10"
                    font_size: dp(10)
                    halign: 'left'
                    pos_hint: {'center_x':0}
                MDLabel:
                    id: total_items_label
                    text: "Total Items: 25"
                    halign: 'right'
                    font_size: dp(10)
                    pos_hint: {'center_x':0}

         
            MDBoxLayout:
                padding: dp(10)
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_y": 0.5,'center_x':0.5}
                orientation: 'vertical'
                md_bg_color: (1,1,1,1)
                MDCard:
                    size_hint: None, None
                    size: 0.9 * root.width, "100dp"
                    padding: "12dp"
                    pos_hint: {'center_x': 0.5}
                    elevation: 0.5
                    MDBoxLayout:
                        spacing: dp(15)
                        orientation: 'vertical'
                        MDLabel:
                            id: title
                            text: 'Multiple Choice Statistics'
                            halign: 'center'
                        MDLabel:
                            id: mean_label
                            text: 'Average Score:'
                            halign: 'left'
                            font_style: 'Subtitle1'
                            font_size: dp(12)
                        MDLabel:
                            id: min_label
                            text: 'Min. Score:'
                            halign: 'left'
                            font_style: 'Subtitle1'
                            font_size: dp(12)
                        MDLabel:
                            id: max_label
                            text: 'Max Score:'
                            halign: 'left'
                            font_style: 'Subtitle1'
                            font_size: dp(12)
                        MDLabel:
                            id: std_label
                            text: 'Std. Dev:'
                            halign: 'left'
                            font_style: 'Subtitle1'
                            font_size: dp(12)
                    
            ScrollView:
                
                id: scroll_view
                size_hint: (1, 1) 
                on_scroll_move: root.scroll_nav()
                
                MDList:
                    padding: 10
                    md_bg_color: (1,1,1,1)
                    id: mcqlist
                    size_hint_y: None
                    height: self.minimum_height
                    
                    Image:
                        size_hint_y: None
                        size_hint_x: 1
                        height: dp(100)
                        allow_stretch: True
                        
                
                    Image:
                        size_hint_y: None
                        size_hint_x: 1
                        height: dp(100)
                        allow_stretch: 100
                    Image:
                        size_hint_y: None
                        size_hint_x: 1
                        height: dp(100)
                        allow_stretch: 100
                    Image:
                        size_hint_y: None
                        size_hint_x: 1
                        height: dp(100)
                        allow_stretch: 100
          
    

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint: {0.99999999, 0.1}
            pos_hint: {"center_x": 0.5, "top": 0.9}
            md_bg_color: (0.8,0.8,0.8,1)
            
            MDIconButton:
                id: export
                icon: "file-export-outline"
                line_color: 0, 0, 0, 0
                theme_icon_color: "Custom"
                icon_color: 'black'
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.open_file_manager()
                size_hint: 0.35,1
            
            MDRectangleFlatButton:
                id: jump
                text: "JUMP"
                text_color: 'black'
                line_color: 0, 0, 0, 0
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: 0.35,1
                on_release: root.jump()
            MDIconButton:
                id: share
                icon: 'share-variant-outline'
                theme_icon_color: "Custom"
                icon_color: 'black'
                on_release: root.share()
                size_hint: 0.35,1

    MDStackLayout:
        id: loading
        size_hint: (1, 1)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        opacity: 0
        spacing: 10
        orientation: 'tb-lr'

        canvas.before:
            Color:
                rgba: 0, 0, 0, 1  # Black color
            Rectangle:
                pos: self.pos
                size: self.size
        Image:
            size_hint: (1, 1)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            source: 'assets/loading.jpg'
        Label:
            id: loading_text
            text: ''
            size_hint: (1, 1)
            font_size: dp(24)
            color: (1, 1, 1, 1)  # White text color

    NextDisplay:
        id: next_display
    PreviousDisplay:
        id: previous_display
    

<TFAnalysis>:
    name: 'tfanalysis'
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "QuickMark"
            pos_hint: {'center':0.5}
            elevation: 0

        MDBoxLayout:
            size_hint_y: None
            height: dp(130)
            padding: dp(10)
            pos_hint: {"center_x": 0.535}
            orientation: 'vertical'

            MDCard:
                size_hint: None, None
                size: 0.9 * root.width, "100dp"
                padding: "12dp"
                elevation: 0.5
                MDBoxLayout:
                    spacing: dp(15)
                    orientation: 'vertical'
                    MDLabel:
                        text: 'Multiple Choice Statistics'
                        halign: 'center'
                    MDLabel:
                        id: mean_label
                        text: 'Average Score:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
                    MDLabel:
                        id: min_label
                        text: 'Min. Score:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
                    MDLabel:
                        id: max_label
                        text: 'Max Score:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
                    MDLabel:
                        id: max_label
                        text: 'Std. Dev:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
        MDLabel:
            text: 'Item Analysis'
            halign: 'center'
            size_hint_y: None
            height: dp(20)
        ScrollView:
            MDList:
                id: mcqlist
                size_hint_y: 3
                Image:
                    id: img1
                    height: dp(200)
                    source:''
                Image:
                    id: img2
                    height: dp(100)
                    source:''
                Image:
                    id: img3
                    height: dp(100)
                    source:''
                Image:
                    id: img4
                    height: dp(100)
                    source:''
                Image:
                    id: img5
                    height: dp(100)
                    source:''
                Image:
                    id: img6
                    height: dp(100)
                    source:''
                Image:
                    id: img7
                    height: dp(100)
                    source:''
                Image:
                    id: img8
                    height: dp(100)
                    source:''
                Image:
                    id: img9
                    height: dp(100)
                    source:''
                Image:
                    id: img10
                    height: dp(100)
                    source:''

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint: {0.75, 0.15}
            pos_hint: {"center_x": 0.5, "top": 0.9}
            md_bg_color: (0.8,0.8,0.8,1)
            
            MDRectangleFlatButton:
                id: jump
                text: "JUMP"
                text_color: 'black'
                line_color: 0, 0, 0, 0
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: 0.35,1
        

<IDAnalysis>:
    name: 'idanalysis'
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "QuickMark"
            pos_hint: {'center':0.5}
            elevation: 0

        MDBoxLayout:
            size_hint_y: None
            height: dp(130)
            padding: dp(10)
            pos_hint: {"center_x": 0.535}
            orientation: 'vertical'

            MDCard:
                size_hint: None, None
                size: 0.9 * root.width, "100dp"
                padding: "12dp"
                elevation: 0.5
                MDBoxLayout:
                    spacing: dp(15)
                    orientation: 'vertical'
                    MDLabel:
                        text: 'Multiple Choice Statistics'
                        halign: 'center'
                    MDLabel:
                        id: mean_label
                        text: 'Average Score:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
                    MDLabel:
                        id: min_label
                        text: 'Min. Score:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
                    MDLabel:
                        id: max_label
                        text: 'Max Score:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
                    MDLabel:
                        id: max_label
                        text: 'Std. Dev:'
                        halign: 'left'
                        font_style: 'Subtitle1'
                        font_size: dp(12)
        MDLabel:
            text: 'Item Analysis'
            halign: 'center'
            size_hint_y: None
            height: dp(20)
        ScrollView:
            MDList:
                id: mcqlist
                size_hint_y: 3
                Image:
                    id: img1
                    height: dp(200)
                    source:''
                Image:
                    id: img2
                    height: dp(100)
                    source:''
                Image:
                    id: img3
                    height: dp(100)
                    source:''
                Image:
                    id: img4
                    height: dp(100)
                    source:''
                Image:
                    id: img5
                    height: dp(100)
                    source:''
                Image:
                    id: img6
                    height: dp(100)
                    source:''
                Image:
                    id: img7
                    height: dp(100)
                    source:''
                Image:
                    id: img8
                    height: dp(100)
                    source:''
                Image:
                    id: img9
                    height: dp(100)
                    source:''
                Image:
                    id: img10
                    height: dp(100)
                    source:''

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint: {0.75, 0.15}
            pos_hint: {"center_x": 0.5, "top": 0.9}
            md_bg_color: (0.8,0.8,0.8,1)
            
            MDRectangleFlatButton:
                id: jump
                text: "JUMP"
                text_color: 'black'
                line_color: 0, 0, 0, 0
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint: 0.35,1

<IDScreen>:
    name: 'ID'
    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            right_action_items: [["cog-outline", lambda x: print(setattr(root.manager, 'current', 'name'),root.add_new_sheet(),'hello world')]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                id: pos_nav_label
                text: "Home > Sheet > Answer Keys (Identification)"
                font_size: dp(10)
                pos_hint: {'center_x':0}
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.5,0.5,1,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                id: page_num_label
                text: "Page Number: 1 of 10"
                font_size: dp(10)
                halign: 'left'
                pos_hint: {'center_x':0}
            MDLabel:
                id: total_items_label
                text: "Total Items: 25"
                halign: 'right'
                font_size: dp(10)
                pos_hint: {'center_x':0}
        
        BoxLayout:
            size_hint: (1, .7)
            pos_hint: {'center_y': 0.7}
            orientation: 'vertical'

        
            BoxLayout:
                orientation: 'horizontal'
                size_hint: (.5,None)
                height: dp(88)
                
                MDLabel:
                    text: '1.'
                    adaptive_width: True 
                
                MDTextField:
                    mode: "rectangle"
                    width: "240dp" 
                    font_size: '18dp'
                    max_text_length: 15

            BoxLayout:
                orientation: 'horizontal'
                size_hint: (.5,None)
                height: dp(88)
                
                
                MDLabel:
                    text: '2.'
                    adaptive_width: True 
                
                MDTextField:
                    mode: "rectangle"
                    opacity: 1
                    width: "240dp" 
                    font_size: '18dp'
                    max_text_length: 15

            BoxLayout:
                orientation: 'horizontal'
                size_hint: (.5,None)
                height: dp(88)
                
                
                MDLabel:
                    text: '3.'
                    adaptive_width: True 
                
                MDTextField:
                    mode: "rectangle"
                    width: "240dp" 
                    font_size: '18dp'
                    max_text_length: 15

            BoxLayout:
                orientation: 'horizontal'
                size_hint: (.5,None)
                height: dp(88)
                
                
                MDLabel:
                    text: '4.'
                    adaptive_width: True 
                
                MDTextField:
                    mode: "rectangle"
                    width: "240dp" 
                    font_size: '18dp'
                    max_text_length: 15

            BoxLayout:
                orientation: 'horizontal'
                size_hint: (.5,None)
                height: dp(88)
                
                
                MDLabel:
                    text: '5.'
                    adaptive_width: True 
                
                MDTextField:
                    mode: "rectangle"
                    width: "240dp" 
                    font_size: '18dp'
                    max_text_length: 15


        
        
                
    MDBoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 0.1
        md_bg_color: (0.8,0.8,0.8,1)
        
           
        MDRectangleFlatButton:
            id: jump
            text: "JUMP"
            text_color: 'black'
            line_color: 0, 0, 0, 0
            on_release: root.jump()
            pos_hint: {"center_x": .5, "center_y": .5}
            size_hint: 0.35,1
        
    
            
<OneCheckScreen>
    name: 'onecheck'


    MDStackLayout:
        md_bg_color: (0.95,0.95,0.95,1)
        height: self.minimum_height
        pos_hint: {'center_x': 0.5}
        MDTopAppBar:
            title: "QuickMark"
            right_action_items: [['']]
            left_action_items: [['chevron-left', lambda x: app.screen_manager_func()]]
            elevation: 0
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(25)
            padding: (20,10)
            size_hint: (0.95,None)

            MDLabel:
                text: "Home > Sheet > Check Papers "
                font_size: dp(10)
                pos_hint: {'center_x':0}

        BoxLayout:
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1  # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], self.size[1]
            size_hint: (None,None)
            orientation: 'horizontal'
            height: dp(80)
            padding: (20,10)
            size_hint: (0.95,None)
            
            MDTextField:
                id: search
                md_bg_color: (1,1,1,1)
                icon_left: 'magnify'
                hint_text: "Search..."
                height: dp(20)
                padding: (40, 40)
                size_hint: (0.9,None)
                on_text: root.word_search(*args)

        BoxLayout:
            id: box_label
            canvas.before:
                Color:
                    rgba: 0.95,0.95,0.95,1 # Set the background color here
                Rectangle:
                    pos: self.pos
                    size: root.size[0], dp(1)
            size_hint: (0,None)
            orientation: 'horizontal'
            
            size_hint: (1,None)
            height: 15
            MDLabel:
                id: empty_label
                text: ""
                halign:"center"  # Center the text horizontally
                theme_text_color:"Secondary" # Set the color to gray
                height:5
                pos_hint:{"center_y": 0.5} 
                
        ScrollView:
            id: scroll_view
            size_hint: (1, None)
            height: dp(500)

            MDList:
                id: onecheck_list 
                size_hint_y: None
                height: self.minimum_height
                md_bg_color: (1,1,1,1)
                padding: 0  # Set padding to 0
                spacing: 0 


    MDFloatingActionButton:
        id: plus_button
        icon: 'account-plus'
        on_release: app.root.get_screen('onecheck').add_new_sheet()        
        pos_hint: {'center_x': .85, 'top': .12}
        elevation: 0
'''

def msg(text, *args, **kwargs):
    if on_android:
        toast(text, y=Window.height*0.4, x=0) # toast appears on center; use gravity to put below.
    else:
        toast(text) # gravity is only supported on android.
        
class OneCheckScreen(Screen):
    def __init__(self, **kwargs):
        super(OneCheckScreen, self).__init__(**kwargs)
        self.instances = [] # list contains widgets for the list items
        

    def refresh_list_gui(self, session_list_basis=None):
        
        if session_list_basis is None:
            session_list =fs.get_sessions() # returns lists of sessins
        else:
            #session_list,indices = session_list_basis
            session_list = [x[0] for x in session_list_basis]
            indices = [x[1] for x in session_list_basis]
        gui_list = self.ids.onecheck_list.children # refernce to list widget childrens
        i=0 # initialize;readability purposes
        for session,i in zip(session_list,range(len(session_list))): # gets each session object paired with its index
            # binds widget info to session details
            gui_list[i].text = session_list[i].name
            gui_list[i].secondary_text = session_list[i].date_created
            gui_list[i].select_id = indices[i] if session_list_basis is not None else i# becomes open index when the corresponding list item is selected
     
    def word_search(self, instance, text): # unused but let instance param stay because of textfield callback arguments
        """run word search on background; then trigger refresh when done"""
        # run search on background to prevent potential lags when searching on large amounts of words or long text
        scheduler.run_background(lambda: self.word_search_thread(text),
                                 name='namescreen_thread',
                                 callback_func=lambda **kwargs: self.refresh_list_gui(**kwargs))
    
    def word_search_thread(self, text):
        if text in ['', ' ']: # if searched text is empty; just refresh to original order
            self.refresh_list_gui()
            return None
        
        word_keys = [] # array where to search
        obj_content = [] # paired value of word keys; can be anything; a list item widget in this case.
        i = 0

        for subwidget in fs.get_sessions(): # each session in fs; not really a subwidget
            # add data on word_keys and obj_content
            word_keys.append(subwidget.name)   
            x = len(fs.get_sessions()) - i - 1 
            obj_content.append([subwidget, x])
            i += 1

        search_system = SearchSystem(word_keys, obj_content) # initialize search engine containing pair of key and content
        result = search_system.search(text,True) # search function; returning result 
        scheduler.pass_parameter('namescreen_thread', 'session_list_basis',result[::-1]) # pass parameter on callback function;
        # reversed list because widgets are added top to bottom. this bottom to top; with top the closes word
        #self.refresh_list_gui(result[::-1]) # refresh list gui with different ordered list basis; upd: replaced with threading
        return None
    
    def add_new_sheet(self):
        """
        used when adding session
        """
        print("ADDING NEW SESSION")
        check_obj = fs.get_sheet(fs.open_index).check_sheets # get check sheets object of last opened sheet
        check_obj.add_session() # add session; see filesystem.py
        
        check_obj.get_session(-1).name = str(len(check_obj.check_sessions)) # gets last added sheet (index "-1")
      
        check_obj.get_session(-1).name = str(f'unnamed') # sets initial name
    
        self.add_item_to_list()
        msg("New Session Created!", (1,0,1,0.2), 1)

    def add_item_to_list(self):
        """similar process to widget initialization but only for a single widget;
        used after add new sheet method
        """
        check_list = self.ids.onecheck_list

        check_obj = fs.get_sheet(fs.open_index).check_sheets
        sessions = check_obj.check_sessions
        
        if len(sessions) > 0: 
            session_last = sessions[-1] # (-1) last appended item on sessions list
            session_instance = InstanceCheckScreen(text=session_last.name)
            session_instance.select_id = len(sessions)-1 # select id is new length; -1 cause index starts at 0
            session_instance.manager = self.manager #?
            session_instance.secondary_text = str(session_last.date_created) 
            session_instance.add_widget(IconLeftWidgetWithoutTouch(icon='account-outline'))
            session_instance.add_widget(IconRightWidgetWithoutTouch(icon='chevron-right'))
            check_list.add_widget(session_instance)
            #self.manager.current = 'check'
            self.instances.append(session_instance) # append to instances
            self.manager.change_screen('check') # proceed to checksreen screen

    def initialize_widgets(self):
        """initial processing of widgtes; one time process
        """
        print("INITIALIZING WIDGES FROM ONECHECK")
        check_list = self.ids.onecheck_list # reference to list widget
        check_sheets = fs.get_sheet(fs.open_index).check_sheets # gets sheet object based on opened index
        sessions = check_sheets.check_sessions # refernce to fs sessions for checking
        instances = [] # assure instances is iniitally empty
        for index in range(len(sessions)): # base loop on the number of sessions created
            session_last = sessions[index] # gets specific session based on for loop index
            session_instance = InstanceCheckScreen(text=session_last.name) # creates list item widget
            session_instance.add_widget(IconLeftWidgetWithoutTouch(icon='account-outline')) # sets icons
            session_instance.add_widget(IconRightWidgetWithoutTouch(icon='chevron-right'))
            session_instance.select_id = index # becomes open index when clicekd
            session_instance.manager = self.manager # ? non-functional
            session_instance.secondary_text =str(session_last.date_created)
            instances.append(session_instance) # add item widget to list
        self.instances = instances # sets widget as instances property
        

    def on_screen(self):
        """
        runs current screen is changed into this screen using change_screen()
        """

        print("OPENING CHECKSCREEN")
        check_list = self.ids.onecheck_list # reference list widget
        if len(fs.get_sessions()) != len(check_list.children):
        
            
            self.ids.onecheck_list.clear_widgets() # clears list widget
            for i,ins in zip(range(len(fs.get_sessions())),self.instances): # adds widget based on how many sessions
                check_list.add_widget(self.instances[i])
        self.word_search(None,self.ids.search.text) # continue to searched text
        # comments out refresh list in on_screen; word search auto refreshes.
        #self.refresh_list_gui() # setups list items: texts, select_ids etc.
        

class PreviewImage(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PreviewImage,self).__init__(**kwargs)
class ButtonImage(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ButtonImage,self).__init__(**kwargs)
        #self.text = 'hello world'
        #self.font_size = 32
        self.size_hint = (1,0.8)
        self.pos_hint = {'center_x':0.5,'center_y':0.5}
    
    def on_release(self, *args, **kwargs):
        self.parent.release_image()
        

class ButtonImagePopUp(FloatLayout):
    def __init__(self, btn_img_obj,**kwargs):
        super(ButtonImagePopUp,self).__init__(**kwargs)
        self.btn_img = btn_img_obj
        self.size_hint = (1,1)
        self.md_bg_color = (0.5,0.5,0.5,0.5)
        bg = Button(text='HELLO WORLD', size_hint=(1,1), background_color=(0,0,0,0.5))
        bg.on_release = self.btn_img.on_release
        self.add_widget(bg)
        self.add_widget(self.btn_img)

    def set_image(self,source):
        self.btn_img.source = source
        self.btn_img.reload()
        try:
            self.parent.remove_widget(self)
        except AttributeError as e:
            print(e)

    def release_image(self,*args,**kwargs):
        self.parent.remove_widget(self)

class TFAnalysis(Screen):
    def __init__(self, **kwargs):
        super(TFAnalysis, self).__init__(**kwargs)
        self.page = 1

class IDAnalysis(Screen):
    def __init__(self, **kwargs):
        super(IDAnalysis, self).__init__(**kwargs)
        self.page = 1
import random


class MCQAnalysisScreen(Screen):
    def __init__(self, **kwargs):
        super(MCQAnalysisScreen, self).__init__(**kwargs)
        self.page = 1
        self.test_type = 'mc'
        content = MDTextField(multiline=False,input_filter='int')
        self.allow_scroll_nav = True
        # Customize title label
        title_text = "Jump"
        
        self.dialog = MDDialog(
            title=title_text,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="TO PAGE", 
                    on_release=lambda *args: [self.next(page=int(content.text)) if content.text != '' else None, self.dialog.dismiss()]
                ),
                MDFlatButton(
                    text="TO ITEM",
                    on_release=lambda *args: [self.next(page=math.ceil(int(content.text)/4)) if content.text != '' else None, self.dialog.dismiss()]
                ),
            ],
        )
    def scroll_nav(self):
        def set_scroll():
                #time.sleep(1)
                if self.allow_scroll_nav == False:
                    self.allow_scroll_nav = True
                    self.scroll_nav()
                    print("SCROLLING")
        prevent_previous = True if self.page == 1 else False
        ans_= {'mc':0,'tf':1,'idtf':2}
        count = fs.get_item_count(fs.open_index)[ans_[self.test_type]]
        print(math.ceil(count/4))
        prevent_next = True if self.page == math.ceil(count/4) else False
        scroll_next_thresh = 0.30 if on_android else -0.2
        scroll_y = self.ids.scroll_view.scroll_y
        print(scroll_y)
        if scroll_y <= 1 - 0.2 and self.allow_scroll_nav and prevent_previous == False:
            self.allow_scroll_nav= False
            self.previous()
            vibrate(50)
            print("NEXT")
            anim_previous_display(self)
            #scheduler.bg_run_once(lambda *args: time.sleep(0.5),'set_scroll_key_screen',lambda *args: set_scroll())
            scroll_y = 1
        elif scroll_y >= 1.2 and self.allow_scroll_nav and prevent_next == False:
            self.next()
            vibrate(50)
            anim_next_display(self)
            print('previous')
            self.allow_scroll_nav= False
            #scheduler.bg_run_once(lambda *args: time.sleep(0.5),'set_scroll_key_screen',lambda *args: set_scroll())
            scroll_y = 1
        elif scroll_y > 1 - 0.08 and scroll_y <1.08:
            set_scroll()
            
    def on_screen(self,test_type,page=1):
        
        self.test_type = test_type
        
        for image in self.ids.mcqlist.children[::-1]:
            if type(image) == Image:
                image.source = ''
                    
                # Assign the new texture
                image.texture = CoreImage('assets/loading.jpg')
                
                
                image.source = 'assets/loading.jpg'
                image.reload()
            else:
                image.opacity = 0

        print("TYESTPE", self.test_type)
        self.ids.title.text = 'Multiple Choice Statistics' if self.test_type == 'mc' else 'True or False Statistics'
        self.page = page

        #self.generate_bar_graph(self.test_type)
        #self.load_images(self.test_type)
        self.generate_images()
        self.get_stats()
        self.ids.previous.disabled = True if self.page == 1 else False
        items = getattr(fs.sheets[fs.open_index].answer_key, self.test_type).get_items()

        
       
        self.ids.next.disabled = True if self.page == int(math.ceil(len(items)/4)) else False

    def get_stats(self):
        scores = []
        check_sheet = fs.get_sheet(fs.open_index).check_sheets
        sessions = check_sheet.check_sessions
        get_session = lambda x: check_sheet.get_session(x) # gets session (each person)
        items = getattr(fs.sheets[fs.open_index].answer_key,self.test_type).get_items()
        
        for session_i in range(len(sessions)):
            indi_score = getattr(get_session(session_i), f'_{self.test_type}_score')
            if indi_score is not None:
                scores.append(indi_score)
        scores = np.array(scores)
        if len(scores) == 0:
            mean, minimum, maximum, sdev = [None for x in range(4)]
        else:
            
            mean = int(round(scores.mean(),0))
            minimum = round(scores.min(),2)
            maximum = round(scores.max(),2)
            sdev = round(scores.std(),2)
        
        
        self.ids.mean_label.text = f'Average Score: {mean}/{len(items)}'
        self.ids.min_label.text = f'Lowest Score: {minimum}/{len(items)}'
        self.ids.max_label.text = f'Highest Score: {maximum}/{len(items)}'
        self.ids.std_label.text = f'Standard Deviation: {sdev}'
        return mean, minimum, maximum,sdev
        
        




    def get_values(self, check_sheet, test_type):
        sessions=check_sheet.check_sessions
        get_session = lambda x: check_sheet.get_session(x) # gets session (each person)
        if test_type =='mc':
            items = fs.sheets[fs.open_index].answer_key.mc.get_items()
            item_count = len(items)
            index_dict = {key:value for key,value in zip(['A','B','C','D','None'], range(5))} # index of num to add in value array
            data_vals = [[0,0,0,0,0] for times in range(item_count)]
        elif test_type == 'tf':
            items = fs.sheets[fs.open_index].answer_key.tf.get_items()
            item_count = len(items)
            index_dict = {key:value for key,value in zip(['T','F','None'], range(3))} # index of num to add in value array
            data_vals = [[0,0,0] for times in range(item_count)]
        else:
            items = fs.sheets[fs.open_index].answer_key.idtf.get_items()
            item_count = len(items)
            index_dict = {key:value for key,value in zip(['CORRECT','WRONG','None'], range(3))} # index of num to add in value array
            data_vals = [[0,0,0] for times in range(item_count)]

        for session_i in range(len(sessions)):
            for item_i in range(item_count):
                try:
                    if test_type == 'mc':
                        answer_item = get_session(session_i).mc_answer[item_i] # each item
                    elif test_type =='tf':
                        answer_item = get_session(session_i).tf_answer[item_i] # each item
                    else:
                        answer_item = get_session(session_i).idtf_eval_array[item_i]
                        answer_item = 'CORRECT' if answer_item == 1 else 'WRONG' if answer_item == 0 else 'NONE' 

                except IndexError as e:
                    #print('no answer; filled answer as None',e)
                    print(e)
                    answer_item = 'None'
                print(" ANSWER ITEM",answer_item)
                if answer_item not in list(index_dict.keys()):
                    answer_item = 'None'
                #answer_item = self.answer_item
                data_vals[item_i][index_dict[answer_item]] += 1
        number_of_students = len(   sessions)
        return list(index_dict.keys()), data_vals, number_of_students
    def open_file_manager(self,*args):
        Clock.schedule_once(lambda x: self.set_loading_opacity(0.5),0)
        
        #self.ids.loading.opacity = 0.8
        Clock.schedule_once(lambda x: self.export_analysis(),0.1)
        Clock.schedule_once(lambda x: self.set_loading_opacity(0),0.2)
    
    def change_loading_text(self, text):
        print("SETTING LOADING TEXT TEXT")
        self.ids.loading_text.text = text

    def set_loading_opacity(self, value):
        print("SETTING LOADING OPACITY")
        self.ids.loading.opacity = value

    def share(self):
        Clock.schedule_once(lambda x: self.set_loading_opacity(0.5),0)
        #self.ids.loading.opacity = 0.8
        Clock.schedule_once(lambda x: self.export_analysis(for_sharing=True),0.1)
        Clock.schedule_once(lambda x: self.set_loading_opacity(0),0.2)

    def export_analysis(self,for_sharing=False):
        original_page = self.page
        pdf_path = 'assets/output.pdf'
        max_items = len(getattr(fs.sheets[fs.open_index].answer_key,self.test_type).get_items())
        max_page = math.ceil(max_items/4)
        paths = []
        
        for num_page in range(max_page+1):
            self.page = num_page
            path = self.generate_bar_graph(self.test_type, for_export=True)
            
            paths += path
            #Clock.schedule_once(lambda x: self.change_loading_text(f'{num_page+1} / {max_page+1}'),0.1)
            
        texts = [[] for x in paths]
        
        test_type_title = ''
        test_type = self.test_type
        if test_type == 'mc':
            test_type_title = 'Multiple Choice'
        elif test_type =='tf':
            test_type_title = 'True or False'
        else:
            test_type_title = 'Identification'
        texts[0] = [f'Sheet: {fs.sheets[fs.open_index].name}',
                    test_type_title,
                    self.ids.mean_label.text,
                    self.ids.min_label.text,
                    self.ids.max_label.text,
                    self.ids.std_label.text]
        generate_pdf(paths, pdf_path,texts)
        self.page = original_page
        sheet_name = fs.sheets[fs.open_index].name
        name=f'{sheet_name}-{test_type_title}'
        unique_name = str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        name = f'{name} [{unique_name}].pdf'
        if for_sharing:
            Function.share(name)
        else:
            fm = FileManager(lambda x: Function.copy_file(pdf_path, x+'/'+name), fs.filemanager_last_dir).file_manager_open()
        

    def generate_bar_graph(self,test_type, for_export = False):
        self.test_type = test_type
        check_sheet = fs.get_sheet(fs.open_index).check_sheets
        item_choices, data_vals, students_num = self.get_values(check_sheet, test_type)
        print("STUDENTS NUM", students_num)
        print(test_type)
        print(data_vals)
        if students_num == 0:
            students_num = 1
        data_fill = lambda choices, data: {'categories': choices, 'values':data}
        data = [data_fill(item_choices, val_num) for val_num in data_vals]
        mc_key = [x.answer_key for x in fs.sheets[fs.open_index].answer_key.mc.get_items()]
        tf_key = [x.answer_key for x in fs.sheets[fs.open_index].answer_key.tf.get_items()]
        idtf_key = [x.answer_key for x in fs.sheets[fs.open_index].answer_key.idtf.get_items()]
        key = mc_key if self.test_type == 'mc' else tf_key
        if test_type == 'mc':
            key = mc_key
        elif test_type == 'tf':
            key = tf_key
        else:
            key = ['CORRECT' for x in idtf_key]
        print("DATA",data)
        """data = [
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [10, 20, 15, 25, 0]}, # no.1, array refers to answers of each choic letter
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [5, 15, 10, 20, 5]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [15, 10, 5, 30, 0]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [45, 10, 50, 30, 40]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [0, 0, 0, 0, 0]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [5, 15, 10, 20, 5]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [15, 10, 5, 30, 0]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [45, 10, 50, 30, 40]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [10, 20, 15, 25, 0]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [5, 15, 10, 20, 5]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [10, 20, 15, 25, 0]},
            {'categories': ['A', 'B', 'C', 'D', 'None'], 'values': [5, 15, 10, 20, 5]},
        ]"""

        start_ind = (self.page-1) * 4
        end_ind = (self.page * 4)
        graph = start_ind
        graphs_dir = "assets/graphs/mcq"
        os.makedirs(graphs_dir, exist_ok=True)
        print("KEY",key)
        if for_export:
            paths = []
        for i, d in enumerate(data[start_ind: end_ind]):
            plt.ioff()
            plt.figure(i, figsize=(3.3, 1))
            padding = 0.1
            plt.subplots_adjust(left=padding, right=(1 - padding), top=(1 - padding), bottom=padding)
        
            correct = key[graph]
            print("CATEFORI")
            print(correct)
            color = []
            for cat in (d['categories']):
                if len(correct) > 0:
                    print('category',cat)
                    if cat not in correct:
                        color.append('black')
                    else:
                        color.append('green')
                else:
                    color.append('black')
    
            color[-1] = 'black'
            print("COLOR",color)
            print(correct)
            bars = plt.bar(d['categories'], d['values'],color='#b6ccf0')

            for category, value,color in zip(d['categories'], d['values'],color):
                name = category
                
                if name=='T':
                    name='True'
                elif name == 'F':
                    name='False'
                else:
                    name = name
                
                plt.text(category, 0.1, f"{name.upper()}\n{value}\n{int(round((value/students_num)*100,0))}%", ha='center', va='bottom', fontsize=8,c = color)
                #plt.text(category, -1.1, f"{int(round((value/students_num)*100,0))}%", ha='center', va='bottom', fontsize=8)

            plt.tick_params(axis='y', left=False, labelleft=False)
            plt.tick_params(axis='x', bottom=False, labelbottom=False)
            plt.gca().spines['top'].set_visible(False)
            plt.ylim(0,students_num +0.5)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['left'].set_visible(True)
            plt.gca().spines['top'].set_visible(False)
            filename = f'{graph+1}'
            plt.text(-1.3 if self.test_type == 'mc' else -0.9, students_num/2, filename, ha='left', va='top', fontsize=14, color='black')
            #plt.title(filename, fontsize=14, color='black', loc='left',pad=20)  # Add title
            chart_path = os.path.join(graphs_dir, f'{graph+1}.png')
            plt.savefig(chart_path,dpi=150)
            graph = graph + 1
            if for_export:
                name_ = f'assets/analysis_export_temp/{graph}.png'
                plt.savefig(name_, dpi=150)
                paths.append(name_)

            #print(filename)
            plt.close()
        
        print('data values',data_vals)
        if for_export:
            return paths

    def load_images(self,*args,**kwargs):
        test_type=self.test_type
        items = getattr(fs.sheets[fs.open_index].answer_key, test_type).get_items()
        #items = fs.sheets[fs.open_index].answer_key.mc.get_items() if test_type=='mc' else  fs.sheets[fs.open_index].answer_key.mc.get_items()
        items_num = len(items)
        images_dir = "assets/graphs/mcq"
        image_files = [filename for filename in os.listdir(images_dir)[:items_num] if filename.endswith(".png")]
        page = self.page
        hide_count = 4
        #diff = len(image_files)- len(self.ids.mcqlist.children)
        #for x in range(diff):
          #  img = Image(height='100dp')
            #self.ids.mcqlist.add_widget(img)

        for i, image in zip(range(1,len(image_files)+1), self.ids.mcqlist.children[::-1]):
            if type(image) != Image:
                print("IS A BOXLAYOJUT")
                image.opacity = 0
                continue
            print( ((page-1)*4+i),items_num)
            try:
                image.source = os.path.join(images_dir, f"{(page-1)*4+i}.png")
                image.reload()
            except Exception as e:
                print(e)
            if ((page-1)*4+i) > items_num:
                image.source = ''
                
                # Assign the new texture
                #image.texture = CoreImage('assets/up.png')
                
                #image.source = 'assets/up.png'
                image.reload()
                image.opacity = 1
                #self.ids.mcqlist.remove_widget(image)

            else:
                image.opacity = 1
            if ((page-1)*4+i) >= ((page)*4):
                break
        self.ids.scroll_view.scroll_y = 1

    def jump(self):
        self.dialog.open()

    def next(self, page = None):
        
        for image in self.ids.mcqlist.children[::-1]:
        
            print("OPACITY OFF!")
            image.source = ''
            
            # Assign the new texture
            
            if type(image) == Image:
                image.texture = CoreImage('assets/loading.jpg')
                image.source = 'assets/loading.jpg'
                image.reload()
            else:
                image.opacity = 0
        if page is None:
            self.page += 1
        else:
            #self.page = int(re.sub('[^0-9]','',str(self.page)))
            self.page = abs(page)
        self.generate_images()
        #self.generate_bar_graph(self.test_type)
        #self.load_images(self.test_type)
        #self.ids.previous.disabled = True if self.page == 1 else False
        items = getattr(fs.sheets[fs.open_index].answer_key, self.test_type).get_items()

       
        #self.ids.next.disabled = True if self.page == int(math.ceil(len(items)/4)) else False
    def previous(self):
        for image in self.ids.mcqlist.children[::-1]:
            print("OPACITY OFF!")
            image.source = ''
            
            # Assign the new texture
            
            if type(image) == Image:
                image.texture = CoreImage('assets/loading.jpg')
            
                image.source = 'assets/loading.jpg'
                image.reload()
            else:
                image.opacity = 0
        self.page -= 1
        self.generate_images()
        #self.generate_bar_graph(self.test_type)
        #self.load_images(self.test_type)
        #self.ids.previous.disabled = True if self.page == 1 else False
        items = getattr(fs.sheets[fs.open_index].answer_key, self.test_type).get_items()

        #self.ids.next.disabled = True if self.page == int(math.ceil(len(items)/4)) else False
    
    def generate_images(self):
        test_type = self.test_type
        page = self.page
        self.page = self.page if page is None else page
        if test_type=='mc':
            answer_key = fs.sheets[fs.open_index].answer_key.mc # set variable for reference on file system attribute for ease
            self.test_type_open = 'mc'
            #self.ids.pos_nav_label.text = 'Home > Sheets > Answer Keys (Multiple Choice)'
        elif test_type=='tf':
            answer_key = fs.sheets[fs.open_index].answer_key.tf # set variable for reference on file system attribute for ease
            self.test_type_open = 'tf'
            #self.ids.pos_nav_label.text = 'Home > Sheets > Answer Keys (True or False)'
        elif test_type=='idtf':
            answer_key = fs.sheets[fs.open_index].answer_key.idtf # set variable for reference on file system attribute for ease
            self.test_type_open = 'idtf'
        if page is not None:
            if page > math.ceil(len(answer_key.get_items())/4):
                self.page = math.ceil(len(answer_key.get_items())/4)
                
        #saved_list = self.ids.saved_list
        #iterations = 0
        self.ids.page_num_label.text = f'Page Number: {page} of {math.ceil(len(answer_key.get_items())/4)}'
       
        self.ids.total_items_label.text = f'Total Items: {(len(answer_key.get_items()))}'
        #self.test_type = test_type
        
        scheduler.run_background(lambda: self.generate_bar_graph(self.test_type),
                                 'analysis_thread',
                                 callback_func=lambda **kwargs: self.load_images(**kwargs))

    """def __init__(self, **kwargs):
        super(OneCheckScreen, self).__init__(**kwargs)"""

class InstanceCheckScreen(TwoLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super(InstanceCheckScreen, self).__init__(**kwargs)
        self.select_id = None
        self.manager = None
    
    def on_release(self, *args, **kwargs):
        print("GETTING THERE___________________________ ")
        print(self.select_id)
        #fs.get_sheet(self.select_id).name = str(fs.get_sheet(self.select_id).name)
        fs.get_sheet(fs.open_index).check_sheets.session_open_index = self.select_id
        self.manager.get_screen('check')
        self.manager.change_screen('check')
        #self.manager.current = 'check'
        
class Instance(ThreeLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super(Instance, self).__init__(**kwargs)
        self.select_id = None
        self.manager = None
        self.secondary_font_style = 'Caption'
        self.tertiary_font_style = 'Caption'
    
    
    def on_release(self, *args, **kwargs):
        
        #fs.get_sheet(self.select_id).name = str(fs.get_sheet(self.select_id).name)
        #name_screen = self.manager.get_screen('name')
        #name_screen.ids.text_field.text = fs.get_sheet(self.select_id).name
        fs.open_index = self.select_id
        self.manager.change_screen('name')
        #self.manager.current = 'name'

class MCInstanceBox(BoxLayout):
    def __init__(self, number, **kwargs):
        super(MCInstanceBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(2)
        self.size_hint_x = None
        self.size_hint_y = None
        self.buttons = []
        self.padding = (10,10)
        self.minimum_width = dp(1)
        self.number = number
        self.width = dp(50)
        self.true_answer = fs.sheets[fs.open_index].answer_key.mc.items[self.number].answer_key
        print(self.true_answer)
        # Add label
        

        # Add buttons
        for letter in ['A','B','C','D','None']:
            button = MDFlatButton(text=letter, id=letter)
             # Bind size changes to update_button_size method
            self.add_widget(button)
            
            
            self.buttons.append(button)
            self.toggle_button_state(button,self.true_answer)
            button.bind(on_release=lambda btn=button: self.toggle_button_state(btn))

    def toggle_button_state(self,button, initialize=None):
        # Deselect all buttons
        buttons = self.buttons
        #print(button.text)
        for btn in buttons:
            btn.size_hint = (0.8,1)  # Ensure size_hint is set before width and height
            if btn.text != button.text if initialize is None else btn.text != initialize:
                btn.md_bg_color = [1, 1, 1, 1]  # Revert background color to white
            else:
                btn.md_bg_color = [0.5,0.5,0.5,1]
                fs.sheets[fs.open_index].answer_key.mc.items[self.number].answer_key = [btn.text]
        # Highlight the pressed button
                        
class TFInstanceBox(BoxLayout):
    def __init__(self, number, **kwargs):
        super(TFInstanceBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(2)
        self.size_hint_x = None
        self.size_hint_y = None
        self.buttons = []
        self.number = number
        self.true_answer = fs.sheets[fs.open_index].answer_key.tf.items[self.number].answer_key
        print(self.true_answer)
        # Add label
        label = MDLabel(text=f'  {number+1}.', adaptive_width=True)
        self.add_widget(label)

        # Add buttons
        for letter in ['T','F','None']:
            button = MDFlatButton(text=letter, id=letter)
            #button.bind(size=self.update_button_size)  # Bind size changes to update_button_size method
            self.add_widget(button)
            
            
            self.buttons.append(button)
            self.toggle_button_state(button,self.true_answer)
            button.bind(on_release=lambda btn=button: self.toggle_button_state(btn))
            



    def toggle_button_state(self,button, initialize=None):
        # Deselect all buttons
        buttons = self.buttons
        #print(button.text)
        for btn in buttons:
            if btn.text != button.text if initialize is None else btn.text != initialize:
                btn.md_bg_color = [1, 1, 1, 1]  # Revert background color to white
            else:
                btn.md_bg_color = [0.5,0.5,0.5,1]
                fs.sheets[fs.open_index].answer_key.tf.items[self.number].answer_key = [btn.text]
        
        
        # Highlight the pressed button

class CustomListItem(MDStackLayout):
    def __init__(self, **kwargs):
        super(CustomListItem, self).__init__(**kwargs)
        self.icon_names = 'alpha-a alpha-b alpha-c alpha-d alpha-t alpha-f alpha-a-circle alpha-b-circle alpha-c-circle alpha-d-circle alpha-t-circle alpha-f-circle'.split(' ') 
        self.key_equiv = {key: equivalent for key, equivalent in zip(list('ABCDTFABCDTF'), self.icon_names)}
        self.ans_equiv = {key: equivalent for key, equivalent in zip(self.icon_names, list('ABCDTFABCDTF'))}
        
        
    def choice_click(self, button,app, *args, **kwargs):
        print("SELECTING")
        btn=button
        keyscreen = app.manager.get_screen('keyscreen')
        saved_list = app.manager.get_screen('keyscreen').ids.saved_list
        iterations = 0
        for x in saved_list.children[::-1]:
            index = ((keyscreen.page-1)*10)+iterations
            iterations += 1
            
            
            for choices in x.children:
                
                if btn == choices:
                    print('yes')
                    
                    
                    if self.ans_equiv[btn.icon] in ['T','F']:
                        answer_keys = fs.sheets[fs.open_index].answer_key.tf
                    else:
                        answer_keys = fs.sheets[fs.open_index].answer_key.mc
                    #print("INDEX",index,answer_key.items[index].answer_key)
                    print(btn.icon.split('-'))
                    if 'circle' not in btn.icon.split('-'):
                    #if btn.icon == 'alpha-a':
                        try:
                            
                            answer_keys.items[index].answer_key = answer_keys.items[index].answer_key + [self.ans_equiv[btn.icon]]
                            print(len(answer_keys.items))
                            print([x.answer_key for x in answer_keys.items])
                            print(index)
                            print(answer_keys.items[index].answer_key)
                        except IndexError as e:
                            print('error',e)
                            break
                        btn.icon = btn.icon+'-circle'
                    else:
                        btn.icon = '-'.join(btn.icon.split('-')[:-1])
                        print(btn.icon)
                        print(index)
                        print([x.answer_key for x in answer_keys.items])
                        answer_keys.items[index].answer_key.remove(self.ans_equiv[btn.icon])
                    


class KeyScreen(Screen):
    def __init__(self, **kwargs):
        super(KeyScreen, self).__init__(**kwargs)
        self.icon_names = 'alpha-a alpha-b alpha-c alpha-d alpha-t alpha-f alpha-a-circle alpha-b-circle alpha-c-circle alpha-d-circle alpha-t-circle alpha-f-circle'.split(' ') 
        self.key_equiv = {key: equivalent for key, equivalent in zip(list('ABCDTFABCDTF'), self.icon_names)}
        self.ans_equiv = {key: equivalent for key, equivalent in zip(self.icon_names, list('ABCDTFABCDTF'))}
        self.page = 1
        self.test_type_open = None
        self.allow_scroll_nav = True
        content = MDTextField(multiline=False,input_filter='int')
        self.expanded = False
        self.items_per_page = 10
        self.next_threshold = 1.2
        self.previous_threshold = 1 - 0.2
        self.dialog = MDDialog(
            title="Jump",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="TO PAGE", 
                    on_release=lambda *args: [self.on_screen(self.test_type_open, page=abs(int(content.text))) if content.text != '' else None, self.dialog.dismiss()]
                ),
                MDFlatButton(
                    text="TO ITEM",
                    on_release=lambda *args: [self.on_screen(self.test_type_open, page=math.ceil(abs(int(content.text)/10))) if content.text != '' else None, self.dialog.dismiss()]
                ),
            ],
        )
    
   
    def scroll_nav(self):
        def set_scroll():
            #time.sleep(1)
            if self.allow_scroll_nav == False:
                self.allow_scroll_nav = True
                self.scroll_nav()
                print("SCROLLING")
        
        prevent_previous = True if self.page == 1 else False
        ans_= {'mc':0,'tf':1,'idtf':2}
        count = fs.get_item_count(fs.open_index)[ans_[self.test_type_open]]
        prevent_next = True if self.page == math.ceil(count/self.items_per_page) else False
        scroll_y = self.ids.scroll_view.scroll_y
        print(scroll_y)
        if scroll_y >= 1.2 and self.allow_scroll_nav == True and prevent_next ==False :
            print("GOING NEXT")
            self.allow_scroll_nav= False
            self.next()
            vibrate(50)
            scroll_y = 1
            anim_next_display(self)
            #scheduler.bg_run_once(lambda *args: time.sleep(1),'set_scroll_key_screen',lambda *args: set_scroll())
            #scroll_y = 1
        elif scroll_y <= 1 - 0.2 and self.allow_scroll_nav == True and prevent_previous == False:
            self.previous()
            vibrate(50)
            self.allow_scroll_nav= False
            vibrate(0.1)
            anim_previous_display(self)
            scroll_y = 1
            #scheduler.bg_run_once(lambda *args: time.sleep(1),'set_scroll_key_screen',lambda *args: set_scroll())
            #scroll_y = 1
        elif scroll_y > 1 - 0.08 and scroll_y <1.08:
            set_scroll()
    
    def next(self):

        self.page+=1
        self.on_screen(self.test_type_open, page=self.page)

    def previous(self):
        self.page-=1
        self.on_screen(self.test_type_open, page=self.page)

    def jump(self):
        self.dialog.open()

    def on_screen(self, test_type='mc',page=None):
        
        self.page = self.page if page is None else page
        if test_type=='mc':
            answer_key = fs.sheets[fs.open_index].answer_key.mc # set variable for reference on file system attribute for ease
            self.test_type_open = 'mc'
            self.ids.pos_nav_label.text = 'Home > Sheets > Answer Keys (Multiple Choice)'
        elif test_type=='tf':
            answer_key = fs.sheets[fs.open_index].answer_key.tf # set variable for reference on file system attribute for ease
            self.test_type_open = 'tf'
            self.ids.pos_nav_label.text = 'Home > Sheets > Answer Keys (True or False)'
        if page is not None:
            if page > math.ceil(len(answer_key.get_items())/10):
                self.page = math.ceil(len(answer_key.get_items())/10)
                
        saved_list = self.ids.saved_list
        iterations = 0
        self.ids.page_num_label.text = f'Page Number: {self.page} of {math.ceil(len(answer_key.get_items())/10)}'
       
        self.ids.total_items_label.text = f'Total Items: {(len(answer_key.get_items()))}'
        if len(answer_key.get_items()) == 0:
            self.manager.change_screen('name')
            #self.manager.current = 'name'
            msg("Answer Key is empty.\nGo to `Sheet Settings` to set items.")
            
        if test_type == 'mc':
            for x in saved_list.children[::-1]:
                iterations+= 1
                index = ((self.page-1)*10)+iterations - 1
                
                print('num',index,len(answer_key.get_items())-1)
                
                if index >= len(answer_key.get_items()):
                    print('above index')
                    x.opacity=0
                    for choice in x.children:
                        choice.disabled = True
                    continue
                else:
                    x.opacity=1
                    for choice in x.children:
                        choice.disabled = False
                truth = answer_key.items[index].answer_key
                for choices in x.children:
                    if type(choices) != MDLabel:
                        print("FUCLING")
                        set_icon = lambda choice_str: choice_str+'-circle' if self.ans_equiv[choice_str] in truth else choice_str
                        print('EQUIV',self.ans_equiv[choices.icon])
                        if self.ans_equiv[choices.icon] in ['A','T']:
                            print('is A')
                            choices.icon = set_icon('alpha-a')
                        elif self.ans_equiv[choices.icon] in ['B','F']:
                            choices.icon = set_icon('alpha-b')
                        elif self.ans_equiv[choices.icon] in ['C']:
                            print("Setting opacity")
                            choices.opacity = 1
                            choices.icon = set_icon('alpha-c')
                        elif self.ans_equiv[choices.icon] in ['D']:
                            print("Setting opacity")
                            choices.opacity = 1
                            choices.icon = set_icon('alpha-d')
                    else:
                        # this one is the label
                        print(type(choices))
                        print(choices.text)
                        choices.text = ''+str(index+1)+')'
                        print(choices.text)
                
        elif test_type == 'tf':
            print("OPENED TRUE FALSE")
            for x in saved_list.children[::-1]:
                iterations+= 1
                index = ((self.page-1)*10)+iterations - 1
                
                print('num',index,len(answer_key.get_items())-1)
                if index >= len(answer_key.get_items()):
                    print('above index')
                    x.opacity=0
                    for choice in x.children:
                        choice.disabled = True
                    continue
                else:
                    x.opacity=1
                    for choice in x.children:
                        choice.disabled = False
                truth = answer_key.items[index].answer_key
                for choices in x.children:
                    print(choices)
                    print(type(choices))
                    print(type(choices) != MDLabel)
                    if type(choices) != MDLabel:
                        print("FUCLING")
                        set_icon = lambda choice_str: choice_str+'-circle' if self.ans_equiv[choice_str] in truth else choice_str
                        print('EQUIV',self.ans_equiv[choices.icon])
                        if self.ans_equiv[choices.icon] in ['A','T']:
                            print('is A')
                            choices.icon = set_icon('alpha-t')
                        elif self.ans_equiv[choices.icon] in ['B','F']:
                            choices.icon = set_icon('alpha-f')
                        else:
                            print("Setting opacity")
                            choices.opacity = 0
                    else:
                        # this one is the label
                        print(type(choices))
                        print(choices.text)
                        choices.text = ''+str(index+1)+')'
                        print(choices.text)

        #print(self.ids.previous)
        #self.ids.previous.disabled = True if self.page == 1 else False
        #self.ids.next.disabled = True if self.page == math.ceil(len(answer_key.get_items())/10) else False
import re
class KeyScreenIDTF(KeyScreen):
    def __init__(self, **kwargs):
       super(KeyScreenIDTF, self).__init__(**kwargs)
       self.items_per_page = 5
       self.page = 1

    def autovalidate_item(self, gui_item_number):
        answer_key = fs.sheets[fs.open_index].answer_key.idtf
        # get fs index
        label_obj = getattr(self.ids,f'_{gui_item_number}')
        content = getattr(self.ids,f'_{gui_item_number}_field')
        content.text = re.sub(r'[^A-Za-z ]','', content.text).upper() #remove non words; to uppercase
        fs_index = int(label_obj.text[:-1]) # remove dot in string 
        print(f'index = {fs_index}')
        answer_item = answer_key.items[fs_index - 1]
        answer_item.answer_key = str(content.text)

    def on_screen(self, test_type=None, page=None):
        
        items_per_page = self.items_per_page
        self.page = self.page if page is None else page
        self.ids.pos_nav_label.text = 'Home > Sheets > Answer Keys (Identification)'
        answer_key = fs.sheets[fs.open_index].answer_key.idtf # set variable for reference on file system attribute for ease
        self.test_type_open = 'idtf'
        if self.page > math.ceil(len(answer_key.get_items())/items_per_page):
            self.page = math.ceil(len(answer_key.get_items())/items_per_page)
        if self.page < 0:
            self.page = 1
        saved_list = self.ids.idtf_items
        iterations = 0
        self.ids.page_num_label.text = f'Page Number: {self.page} of {math.ceil(len(answer_key.get_items())/items_per_page)}'
        self.ids.total_items_label.text = f'Total Items: {(len(answer_key.get_items()))}'
        print("KEEYSS", answer_key.get_items())
        if len(answer_key.get_items()) == 0:
            self.manager.change_screen('name')
            #self.manager.current = 'name'
            msg("Answer Key is empty.\nGo to `Sheet Settings` to set items.")
            return
        max_index_per_page = ((self.page-1)*items_per_page)+items_per_page - 1
        for x in saved_list.children[::-1]:
            iterations += 1
            index = ((self.page-1)*items_per_page)+iterations - 1
            print('num',index,len(answer_key.get_items())-1)
            if index >= len(answer_key.get_items()):
                print('above index')
                x.opacity=0
                for choice in x.children:
                    choice.disabled = True
                continue
            else:
                x.opacity=1
                for choice in x.children:
                    choice.disabled = False
            
            truth = answer_key.items[index].answer_key
            print('IDTF kYE',truth)
            print(iterations)
            getattr(self.ids,f'_{iterations}').text = f'{index+1}.'
            getattr(self.ids,f'_{iterations}_field').text = str(truth) if len(truth) > 0 else ''

    
class HomeScreen(Screen):
    def save_func(self, destination_path):
        fs.import_sheet(destination_path)
        #self.on_screen()
        self.add_item_to_list(proceed=False)
        self.on_screen()
        #fs.export_sheet(fs.open_index, destination_path)
        return True, '', destination_path
    def import_sheet(self):
        fm = FileManager(lambda x: self.save_func(x), fs.filemanager_last_dir,dir_only=False,ext=['.sheet']).file_manager_open()

    def add_new_sheet(self):
        """
        
        used when adding session
        """
        print("ADDING NEW SESSION")
        check_obj = fs # get check sheets object of last opened sheet
        check_obj.add_sheet() # add session; see filesystem.py
        
        #check_obj.get_sheet(-1).name = str(len(check_obj.check_sessions)) # gets last added sheet (index "-1")
      
        check_obj.get_sheet(-1).name = str(f'untitled') # sets initial name
    
        self.add_item_to_list()
        msg("New Session Created!", (1,0,1,0.2), 1)

    def initialize_widgets(self):
        """initial processing of widgtes; one time process
        """
        print("INITIALIZING WIDGES FROMHOMESCREEN")
        # copy pasted and modiefied from checksreen
        check_list = self.ids.saved_list # reference to list widget
        #check_sheets = fs.get_sheet(fs.open_index).check_sheets # gets sheet object based on opened index
        sessions = fs.sheets # refernce to fs sessions for checking
        instances = [] # assure instances is iniitally empty
        for index in range(len(sessions)): # base loop on the number of sessions created
            session_last = sessions[index] # gets specific session based on for loop index
            session_instance = Instance(text=session_last.name) # creates list item widget
            session_instance.add_widget(IconLeftWidgetWithoutTouch(icon='file-document-outline')) # sets icons
            session_instance.add_widget(IconRightWidgetWithoutTouch(icon='chevron-right'))
            session_instance.select_id = index # becomes open index when clicekd
            session_instance.manager = self.manager # ? non-functional
            #session_instance.secondary_text =str(session_last.date_created)
            instances.append(session_instance) # add item widget to list
        self.instances = instances # sets widget as instances 
        print("RESULT")
        print(self.instances)
        
    def refresh_list_gui(self, session_list_basis=None):
        print("DEBUG")
        if session_list_basis is None:
            session_list =fs.sheets # returns lists of sessinspr
            print(list(range(len(session_list))))
        else:
            #session_list,indices = session_list_basis
            session_list = [x[0] for x in session_list_basis]
            indices = [x[1] for x in session_list_basis]
            print(indices)
        print(session_list)
        gui_list = self.ids.saved_list.children # refernce to list widget childrens
        i=0 # initialize;readability purposes
       
        
        
        for session,i in zip(session_list,range(len(session_list))): # gets each session object paired with its index
            # binds widget info to session details
            self.set_list_labels(gui_list[i], indices[i] if session_list_basis is not None else i)
            #print(session_list[i].name, session_list[i].date_created)
            #gui_list[i].text = session_list[i].name
            #gui_list[i].secondary_text = session_list[i].date_created
            #gui_list[i].select_id = indices[i] if session_list_basis is not None else i# becomes open index when the corresponding list item is selected
            

    def show_key_button(self):
        pass
    
    def on_screen(self):
        """
        runs current screen is changed into this screen using change_screen()
        """
        #print(anim_next_display(self))
        if self.first_launch:
            self.first_launch= False
            analysis_init = self.manager.get_screen('mcqanalysis')
            onecheck_init = self.manager.get_screen('onecheck')
            try:
                onecheck_init.initialize_widgets()
                self.initialize_widgets()
            except Exception as e:
                print("ror1",e)
            try:
                analysis_init.generate_bar_graph('tf')
                pass
            except Exception as e:
                print('ror',e)
        if len(fs.sheets) != len(self.ids.saved_list.children):
            check_list = self.ids.saved_list # reference list widget
            check_list.clear_widgets() # clears list widget
            print("INSTACNCE",len(self.instances), len(fs.sheets))
            for i,ins in zip(range(len(fs.sheets)),self.instances): # adds widget based on how many sessions
                check_list.add_widget(self.instances[i])
                
        self.word_search(None,self.ids.search.text) # continue to searched text
        # comments out refresh list in on_screen; word search auto refreshes.
        #self.refresh_list_gui() # setups list items: texts, select_ids etc.
        print("ADDING TO LIST")
        saved_list = self.ids.saved_list
        #saved_list.clear_widgets()
        if len(fs.sheets) == 0:
            print("SHEETS NONE")
            self.ids.empty_label.text = 'You have no sheets.\nCreate one by tapping the + button'
            self.ids.box_label.height = 100
        else:
            self.ids.empty_label.text = ''
            self.ids.box_label.height = 5
        

    def word_search(self, instance, text): # unused but let instance param stay because of textfield callback arguments
        print('ENGGAING WORD SEARCH')
        """run word search on background; then trigger refresh when done"""
        # run search on background to prevent potential lags when searching on large amounts of words or long text
        scheduler.run_background(lambda: self.word_search_thread(text),
                                 name='homescreen_thread',
                                 callback_func=lambda **kwargs: self.refresh_list_gui(**kwargs))
    
    def word_search_thread(self, text):
        print("staritng wod search")
        if text in ['', ' ']: # if searched text is empty; just refresh to original order
            self.refresh_list_gui()
            return None
        
        word_keys = [] # array where to search
        obj_content = [] # paired value of word keys; can be anything; a list item widget in this case.
        i = 0
        for subwidget in fs.sheets: # each session in fs; not really a subwidget
            # add data on word_keys and obj_content
            word_keys.append(subwidget.name)    
            obj_content.append([subwidget, i])
            i += 1

        search_system = SearchSystem(word_keys, obj_content) # initialize search engine containing pair of key and content
        result = search_system.search(text,True) # search function; returning result 
        print("RESULT",[(c[0].name,c[1]) for c in result])
        scheduler.pass_parameter('homescreen_thread', 'session_list_basis',result[::-1]) # pass parameter on callback function;
        # reversed list because widgets are added top to bottom. this bottom to top; with top the closes word
        #self.refresh_list_gui(result[::-1]) # refresh list gui with different ordered list basis; upd: replaced with threading
        return None
        
    def add_item_to_list(self,proceed=True):
        """similar process to widget initialization but only for a single widget;
        used after add new sheet method
        """
        check_list = self.ids.saved_list

        #check_obj = fs.get_sheet(fs.open_index).check_sheets
        sessions = fs.sheets
        
        if len(sessions) > 0: 
            session_last = sessions[-1] # (-1) last appended item on sessions list
            session_instance = Instance(text=session_last.name)
            session_instance.select_id = len(sessions)-1 # select id is new length; -1 cause index starts at 0
            session_instance.manager = self.manager #?
            session_instance.secondary_text = str(session_last.date_created) 
            session_instance.add_widget(IconLeftWidgetWithoutTouch(icon='file-document-outline'))
            session_instance.add_widget(IconRightWidgetWithoutTouch(icon='chevron-right'))
            check_list.add_widget(session_instance)
            #self.manager.current = 'check'
            self.instances.append(session_instance) # append to instances
            self.manager.change_screen('name') if proceed else None # proceed to checksreen screen
            

    def set_list_labels(self, instance, index):
        name = fs.get_sheet(index).name
        counts = fs.get_item_count(index)
        instance.text = name
        instance.secondary_text =  f"{counts[0]} MC, {counts[1]} T/F, {counts[2]} IDTF"
        session_counts = len(fs.get_sessions(index))
        instance.tertiary_text = f'{session_counts} sessions [{sum(counts)} items]'
        instance.select_id = index

    def show_init_list(self, defined_sheets=[]):
        """Uodate list

        Args:
            defined_sheets (list, optional): _description_. Defaults to [].
        """
        

        #saved_list.add_widget(MDLabel(
         #           text="\n\n",
          #          halign="center",  # Center the text horizontally
           #         theme_text_color="Secondary",  # Set the color to gray
            #        size_hint_y=None,
             #       height=20,  # Adjust the height of the label
              #      padding=(20, 10) , # Add padding around the label
               #     pos_hint={"center_y": 0.5} 
                #))
        #saved_list.add_widget(label)

        
        self.ids.scroll_view.height = Window.height-(240)
    
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.thread = None
        self.first_launch = True
        self.thread_lock = threading.Lock()
        self.instances = []

class AnalysisScreen(Screen):
    def on_release(self, Screen):
        self.manager.change_screen(Screen)
    
    def on_screen(self):
        check_sheet = fs.get_sheet(fs.open_index).check_sheets # get sheet based on opened sheet
        sessions = check_sheet.check_sessions # get sessions inside sheet
        get_session = lambda x: check_sheet.get_session(x) # gets session (each person)
        scores = [] # storage for scores
        total = 0 # total number
        types = ['mc','tf','idtf']

        # get max items
        for test_type in types:
            items = getattr(fs.sheets[fs.open_index].answer_key,test_type).get_items()
            total += len(items)
        
        # get scores for each person by combining all test types
        for session_i in range(len(sessions)):
            score_per_person = None
            for test_type in types:
                indi_score = getattr(get_session(session_i), f'_{test_type}_score')
                if indi_score is not None:
                    if score_per_person is None:
                        score_per_person = 0
                    score_per_person += indi_score # add score of each person
                    #scores.append(indi_score) 
            scores.append(score_per_person) if score_per_person is not None else None

            
        scores = np.array(scores)
        if len(scores) == 0:
            mean, minimum, maximum, sdev = [None for x in range(4)]
        else:
            mean = int(round(scores.mean(),0))
            minimum = round(scores.min(),2)
            maximum = round(scores.max(),2)
            sdev = round(scores.std(),2)
        
        
        #scores = np.array(scores)
        self.ids.mean_label.text = f'Average Score: {mean}/{total}'
        self.ids.min_label.text = f'Lowest Score: {minimum}/{total}'
        self.ids.max_label.text = f'Highest Score: {maximum}/{total}'
        self.ids.std_label.text = f'Standard Deviation: {sdev}'
        

class NameScreen(Screen):
    #INIT_________________________________________________________
    def __init__(self, **kwargs):
        super(NameScreen, self).__init__(**kwargs)
        self.expanded = False
        self.allow_expand = True

    def share_sheet(self):
        sheet = fs.get_sheet(fs.open_index)
        unique_name = str(datetime.now().strftime('%Y-%m-%d][%H-%M-%S'))
        name = root_folder+'/'+f'(Export) {sheet.name} [{unique_name}].sheet'
        fs.export_sheet(fs.open_index, name)
        
        Function.share(name)
        
    def save_func(self, destination_path):
        fs.export_sheet(fs.open_index, destination_path)
        return True, '', destination_path
    
    def export_sheet(self):
        
        sheet = fs.get_sheet(fs.open_index)
        #save_func = lambda x: fs.export_sheet(fs.open_index, x+'/'+f'{sheet.name}.sheet')
        unique_name = str(datetime.now().strftime('%Y-%m-%d][%H-%M-%S'))
        fm = FileManager(lambda x: self.save_func(x+'/'+f'{sheet.name} [{unique_name}].sheet'), fs.filemanager_last_dir).file_manager_open()
      
    def expand_keys(self):
        #if self.allow_expand == False:
         #   print("TOO EARLY")
          #  return
        #self.allow_expand = False
        #def allow_expand():
         #   self.allow_expand = True
        mc = self.ids.mc
        tf = self.ids.tf
        idtf = self.ids.idtf
        mc.disabled = self.expanded # if self.expanded is false; mc disability is also False (becomes enabled) or vice versa
        tf.disabled = self.expanded
        idtf.disabled = self.expanded
        #anim = Animation(opacity=0, duration=1) 
        self.expanded = not self.expanded
        print(mc.opacity, tf.opacity, idtf.opacity)
        def switch_opacity(obj):
            return 1 if self.expanded else 0
        self.ids.btn_answer_key_icon.icon = 'chevron-down' if self.expanded else 'chevron-right'
        Clock.schedule_once(lambda x: Animation(opacity=switch_opacity(mc),duration=0.5).start(mc),0 if self.expanded else 0.3)
        Clock.schedule_once(lambda x: Animation(opacity=switch_opacity(tf),duration=0.5).start(tf),0.15)
        Clock.schedule_once(lambda x: Animation(opacity=switch_opacity(idtf),duration=0.5).start(idtf),0.3 if self.expanded else 0)
        #Clock.schedule_once(lambda x: allow_expand(),0.5)
        
    def delete_sheet(self):
        print("DELETING")
        confirmation_dialog('Are you sure you want to delete? \nThis process is irreversible.',
                            yes_func = lambda *args: (fs.delete_opened_sheet(),self.manager.change_screen('home')),
                            no_func = lambda instance: instance.parent.dismiss())
         # deletes last opened session


    def show_btn_keys(self, *args,**kwarg):
        print("HSOWING BTN KEYS")
        saved_list = self.ids.saved_list
        if len(saved_list.children) <= 4:
            saved_list.add_widget(OneLineAvatarIconListItem(IconRightWidgetWithoutTouch(icon='chevron-right'), text='Multiple Choice',on_release= lambda x: print(self.prepare_mc_keys(),self.manager.change_screen('MC'))))
            saved_list.add_widget(OneLineAvatarIconListItem(IconRightWidgetWithoutTouch(icon='chevron-right'), text='True or False',on_release= lambda x: print(self.prepare_tf_keys(),self.manager.change_screen('TF'))))
            saved_list.add_widget(OneLineAvatarIconListItem(IconRightWidgetWithoutTouch(icon='chevron-right'), text='Identification',on_release= lambda x: print(self.prepare_tf_keys(),self.manager.change_screen('ID'))))
            self.ids.btn_key_right.icon = 'chevron-down'
        else:
            saved_list.remove_widget(saved_list.children[0])
            saved_list.remove_widget(saved_list.children[0])
            saved_list.remove_widget(saved_list.children[0])
            self.ids.btn_key_right.icon = 'chevron-right'


    def on_screen(self,*args,**kwargs):
        print("NAMESCREEN ON SCREEN")
        if on_android:
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
            
        self.ids.text_field.text = fs.get_sheet(fs.open_index).name
        self.ids.date_label.text = "Date Created: "+ str(fs.get_sheet(fs.open_index).date_created)

   

    #METHOD_________________________________________________________
    def prepare_mc_keys(self):
        
        mc_screen = self.manager.get_screen('MC') # set variables to reference to screen attributes
        answer_key = fs.sheets[fs.open_index].answer_key.mc # set variable for reference on file system attribute for ease
        mc_screen.instances = [] # init instances for screen
        #mc_screen.ids.mc_box_all.clear_widgets() # out
        widgets_to_remove = [] # init
    
        # Iterate through the children of tf_box_all; which widgets to remove
        for child in mc_screen.ids.mc_box_all.children:
            # Check if the child is an instance of TopAppBar
            if not isinstance(child, MDTopAppBar): # exclude MDTOPAPP BAR; upd: condition not necessary
                # If it's not a TopAppBar, add it to the list of widgets to be removed
                widgets_to_remove.append(child)
        
        # Remove the widgets from tf_box_all
        for widget in widgets_to_remove:
            mc_screen.ids.mc_box_all.remove_widget(widget)


        bg_color = [(1,1,1,1),(0.5,0.5,0.5,1)] # bg color constant
        increment = 0 # init increment

        # base iteration on the amount of items on answer key
        # dynamic generation of list
        for answer_item in answer_key.get_items():
            label = MDLabel(text=f'{increment+1} ') # number count display
            label.color=(0.5,0.5,0.5,1) # label color

            # add on gui
            mc_screen.ids.mc_box_all.add_widget(label) # add number count display
            instance = MCInstanceBox(increment) # initialize box
            instance.md_bg_color=bg_color[int((increment+1)%2)] # upd: doesnt work; make bg color different per row by odd or even row count
            mc_screen.ids.mc_box_all.add_widget(instance)
            mc_screen.instances.append(instance) # add box to screen

            increment += 1

        # prevent from cutting off items from scroll view
        mc_screen.ids.mc_scroll_view.height = Window.height - (150)
        # debugging
        print(mc_screen.instances)

    def prepare_tf_keys(self):
        
        tf_screen = self.manager.get_screen('TF')
        answer_key = fs.sheets[fs.open_index].answer_key.tf
        tf_screen.instances = []
        #tf_screen.ids.tf_box_all.clear_widgets()
        widgets_to_remove = []
    
        # Iterate through the children of tf_box_all
        for child in tf_screen.ids.tf_box_all.children:
            # Check if the child is an instance of TopAppBar
            if not isinstance(child, MDTopAppBar):
                # If it's not a TopAppBar, add it to the list of widgets to be removed
                widgets_to_remove.append(child)
        
        # Remove the widgets from tf_box_all
        for widget in widgets_to_remove:
            tf_screen.ids.tf_box_all.remove_widget(widget)
        increment = 0
        for answer_item in answer_key.get_items():
            instance = TFInstanceBox(increment)
            tf_screen.ids.tf_box_all.add_widget(instance)
            
            tf_screen.instances.append(instance)
            increment += 1
            instance.size_hint = (1,None)
            instance.adaptive_width = True
        tf_screen.ids.tf_scroll_view.height = Window.height - (130)
        print(tf_screen.instances)
    
    def prepare_answer_sheet(self):
        """FUNCTION for click event before entering answer sheet. 
        SHow gui on sheet_screen based on registered data from filesystem
        """
        sheet_screen = self.manager.get_screen('answer_sheet')
        answer_key = fs.sheets[fs.open_index].answer_key

        sheet_screen.ids.mcq_textfield.text = str(len(answer_key.mc.get_items()))
        sheet_screen.ids.tf_textfield.text = str(len(answer_key.tf.get_items()))
        sheet_screen.ids.ident_textfield.text = str(len(answer_key.idtf.get_items()))
        sheet_screen.ids.mcq_checkbox.active = True if len(answer_key.mc.get_items()) > 0 else False
        sheet_screen.ids.tf_checkbox.active = True if len(answer_key.tf.get_items()) > 0 else False
        sheet_screen.ids.ident_checkbox.active = True if len(answer_key.idtf.get_items()) > 0 else False
        sheet_screen.set_hidden_field()
        name = fs.sheets[fs.open_index].name
        

   
    def rename(self):
        """Renaming Function
        """
        # debugging
        print("RENAMING")

        index = fs.open_index # index for currently opened sheet
        current_name = self.ids.text_field.text # use current name on text field gui
        fs.sheets[index].name = current_name
        #fs.get_sheet(fs.open_index).check_sheets.check_sessions[fs.get_sheet(fs.open_index).check_sheets.session_open_index].name = current_name # update filesystem 
        #self.manager.get_screen('onecheck')
        #fs.save() #out; now autosaves
        #home_screen = self.manager.get_screen('onecheck')
        #home_screen.respond_to_rename()
        
        #home_screen.add_item_to_list()

        # quick confirmation dialog
        msg("Renamed successfully.", (1,0,1,0.2), 1)


    def capitalize(self, instance, text):
        self.ids.text_field.text = text

class NameScreenExpanded(NameScreen):
    def __init__(self, **kwargs):
        super(NameScreenExpanded, self).__init__(**kwargs)
    
class MCScreen(Screen):
    def toggle_button_state(self, button):
        # Deselect all buttons
        buttons = self.ids.mc_buttons.children
        for btn in buttons:
            if btn != button:
                btn.md_bg_color = [1, 1, 1, 1]  # Revert background color to white
        
        # Highlight the pressed button
        if button.md_bg_color == [1, 1, 1, 1]:  # If the background color is white
            button.md_bg_color = [.5, .5, .5, 1]  # Change it to the desired color
        else:
            button.md_bg_color = [1, 1, 1, 1]  # Revert to white

    def on_pre_enter(self, *args):
        # Reset button background color when screen is entered
        #buttons = self.ids.mc_buttons.children
        #for button in buttons:
        #   button.md_bg_color = [1, 1, 1, 1]  # Set all buttons to white initially
        pass

    def on_leave(self, *args):
        # Reset button background color when leaving the screen
        self.on_pre_enter()

class TFScreen(Screen):
    def toggle_button_state(self, button):
        # Deselect all buttons
        buttons = self.ids.tf_buttons.children
        for btn in buttons:
            if btn != button:
                btn.md_bg_color = [1, 1, 1, 1]  # Revert background color to white
        
        # Highlight the pressed button
        if button.md_bg_color == [1, 1, 1, 1]:  # If the background color is white
            button.md_bg_color = [.5, .5, .5, 1]  # Change it to the desired color
        else:
            button.md_bg_color = [1, 1, 1, 1]  # Revert to white

    def on_pre_enter(self, *args):
        # Reset button background color when screen is entered
        pass

    def on_leave(self, *args):
        # Reset button background color when leaving the screen
        self.on_pre_enter()

    def show_text_input_dialog(self):
        content = MDTextField()
        
        # Customize title label
        title_text = "[size=16][b]Change point value for all questions[/b][/size]"
        
        dialog = MDDialog(
            title=title_text,
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL", 
                    on_release=lambda *args: dialog.dismiss()
                ),
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: self.process_text_input(content.text, dialog),
                ),
            ],
        )
        dialog.open()

    def process_text_input(self, text, dialog):
        print("Entered text:", text)
        # Here you can do something with the entered text, like updating the UI, etc.
        dialog.dismiss()

#CLASS____________________________________________________________

class FileManager(MDFileManager):
    def __init__(self,path_function,starting_path, dir_only=True,ext=None,**kwargs):
        super(FileManager, self).__init__(**kwargs)
        self.previous_path = starting_path
        self.show_hidden_files=False
        self.dir_only = dir_only
        if ext is None:
            self.ext = ['.????????????????'] if dir_only else []
        else:
            self.ext = ext
        
        self.path_function = path_function
        #self.save_path = None # stores save path after using path_function
        pass

    def file_manager_open(self):
        # Show file manager starting from the previous selected path or root directory
        
        self.show(self.previous_path)

    def select_path(self, path):
        if self.dir_only == False:
            if os.path.isfile(path):  # Check if the selected path is a file
                self.previous_path = path  # Store the selected path
                
                self.run_script(path)
                self.close()
            else:
                # Notify user that only files can be selected
                msg("Please select a file.")
        else:
            # Method to handle file selection event
            self.previous_path = path  # Store the selected path
            fs.filemanager_last_dir = path
            self.run_script(path)
            
            self.close()

    def run_script(self, file_path):
        # Method to run a script using the selected file path
        if os.path.isfile(file_path):
            # Example: Run a Python script
            print(f"python {file_path}")
        output, error,destination = self.path_function(file_path)
        #self.save_path = destination
        if output==True:
            msg(f"Success! Image saved as: \n{destination}.")
        else:
            msg(f"Export failed. {error}")
            

    def exit_manager(self, *args):
        # Method to handle exit event
        self.close()
        
        
# CLASS_________________________________________________________
        
class IDScreen(Screen):
    pass


class FeedBack(BoxLayout):
    def __init__(self,**kwargs):
        super(FeedBack, self).__init__(**kwargs)
        self.frame_image = Image(size_hint=(1,1), pos_hint={'center_x': 0.5, 'center_y': 0.5},allow_stretch=True, keep_ratio=False)

#CLASS________________________________________________________

class CheckScreen(Screen):
    def max_image(self, *args, **kwargs):
        self.preview_image.set_image('assets/feedback_stitched-flipped.png')
        self.add_widget(self.preview_image)
    #METHOD________________________________________________
    def delete_session(self):
        print("DELETING")
        confirmation_dialog('Are you sure you want to delete?\nThis process is irreversible.',
                            yes_func = lambda *args: (fs.delete_opened_session(),self.manager.change_screen('onecheck')),
                            no_func = lambda instance: None)
         # deletes last opened  session

    def share(self):
        name=f'{fs.get_last_opened_session().name}-{fs.sheets[fs.open_index].name}.png'
        print('share filename',name)
        Function.copy_file('assets/feedback_stitched.png', fs.filemanager_last_dir+'/'+f'{name}')
        Function.share( fs.filemanager_last_dir+'/'+f'{name}')

    #METHOD_____________________________________________________
    def open_file_manager(self, *args):
        name=f'{fs.get_last_opened_session().name}-{fs.sheets[fs.open_index].name}'
        unique_name = str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        name = f'{name}[{unique_name}].png'
        fm = FileManager(lambda x: Function.copy_file('assets/feedback_stitched.png', x+'/'+name), fs.filemanager_last_dir).file_manager_open()
    
    def cam_off(self):
        """Function for turning camera off
        """
        self.remove_widget(self.camera_widget)
        self.camera_widget.opacity = 0
        self.camera_widget.remove_camera = True # attribute from camera widget class; stop looping process on bg when True
        self.camera_widget.camera.remove_from_cache()
        self.camera_widget.camera.play = False # stop camera from playing
        del self.camera_widget.camera._camera
        del self.camera_widget
        self.cam_is_on = False  # status indicator
        check_sheet = fs.get_sheet(fs.open_index).check_sheets
        print(check_sheet.session_open_index)
        check_session=check_sheet.get_session(check_sheet.session_open_index)
        cam_btn = self.ids.cam_button
        cam_btn.icon = 'camera'
        for x in ['MULTIPLE CHOICE', 'TRUE OR FALSE', 'IDENTIFICATION']:
            self.update(x)
        self.img_display.keep_ratio=True
        print('children',self.children)
        self.img_display.opacity = 1
    
    def rename(self):
        """Renaming Function
        """
        # debugging
        print("RENAMING")

        index = fs.open_index # index for currently opened sheet
        current_name = self.ids.check_text_field.text # use current name on text field gui
        fs.get_last_opened_session().name = current_name
        #fs.get_sheet(fs.open_index).check_sheets.check_sessions[fs.get_sheet(fs.open_index).check_sheets.session_open_index].name = current_name # update filesystem 
        #self.manager.get_screen('onecheck')
        #fs.save() #out; now autosaves
        #home_screen = self.manager.get_screen('onecheck')
        #home_screen.respond_to_rename()
        
        #home_screen.add_item_to_list()

        # quick confirmation dialog
        msg("Renamed successfully.", (1,0,1,0.2), 1)

    def feedback_finish_load(self):
         #image_texture = CoreImage('assets/feedback_stitched.png').texture
        #self.add_widget(Image(source='assets/feedback_stitched.png',size_hint = (1,0.3),pos_hint = {'top': 0.8, 'center_x': 0.5}))
        #image = self.feedback_widget.frame_image
        print("FINISHED LOADED")
        self.img_display.source = 'assets/feedback_stitched.png'
        self.img_display.reload()
        
        print("DONE!")
    def swap_elements(self, array, from_index, target_index):
        my_list = array
        my_list[from_index], my_list[target_index] = my_list[target_index], my_list[from_index]
        return my_list

    def update_feedback(self,check_session):
        print('preparing feedback')
        img_stack = []
        img_stack = [None,None,None]
        mc_answers = check_session.mc_answer
        tf_answers = check_session.tf_answer
        idtf_answers = check_session.idtf_answer
        mc_key = [x.answer_key for x in fs.sheets[fs.open_index].answer_key.mc.get_items()]
        tf_key = [x.answer_key for x in fs.sheets[fs.open_index].answer_key.tf.get_items()]
        idtf_key = [x.answer_key for x in fs.sheets[fs.open_index].answer_key.idtf.get_items()]
        length = len(mc_answers)
        mcdiff = len(mc_key)-len(mc_answers)
        tfdiff = len(tf_key)-len(tf_answers)
        mc_answers = mc_answers + [''] * mcdiff  # Add empty elements based on mcdiff; for unanswered items.
        tf_answers = tf_answers + [''] * tfdiff  # Initialize with empty elements based on tfdiff
        idtf_answers = idtf_key
        print("MC ANSWERS",mc_answers)
        print("TF ANSWERS",tf_answers)
        print("MCCORRECT",mc_key)
        print("TFCORRECT",tf_key)
        #print(f'mc answers {mc_answers}x',)
        if len(mc_key) > 0 and len(mc_answers) > 0:
            result1 = feedback.feedback_quick(
                mc_answers,
                mc_key,
                'MULTIPLE CHOICE', len(mc_key),'assets/mc_feedback.png',fbc=fbc.fbc)
            result1 = True 
        else:
            result1 = False
        print('getting true or false feedback')

        #if result1:
         #   img_stack.append('assets/mc_feedback.png')
        img_stack[0] = 'assets/mc_feedback.png'
        if len(tf_key) > 0 and len(tf_answers) > 0:
            result2 = feedback.feedback_quick(
                tf_answers,
                tf_key,
                'TRUE OR FALSE', len(tf_key),'assets/tf_feedback.png',fbc=fbc.fbc)
            result2 = True
        else:
            result2 = False
        img_stack[1] = 'assets/tf_feedback.png'
        if result2 == False: # temp fix where multiple choice image goes to center when tf is not used
            img_stack = self.swap_elements(img_stack, 1, 0)
        print('KEY',idtf_key)
        print(len(idtf_key))
        if len(idtf_key) > 0:
            result3 = feedback.feedback_quick(
                ['KEVIN JOSEPH', "EUGENE DAVE", 'ROAN SCHUYLER'] if not on_android else idtf_answers,
                idtf_key,
                'IDENTIFICATION', 
                len(idtf_key),
                'assets/idtf_feedback.png',
                fbc=fbc.fbc,
                idtf_eval_array = [1,0,1] if not on_android else check_session.idtf_eval_array
            )
            result3 = True
            img_stack[2] = 'assets/idtf_feedback.png'
        else:
            result3 = False
        

        #if result2:
         #   img_stack.append('assets/tf_feedback.png')
        
        print('stitching')
        #saved_path = stitch_sheet(len(mc_answers), len(tf_answers), 0, title=check_session.name, save_path='assets/feedback_stitched.png',
         #            filepaths=['assets/mc_feedback.png','assets/tf_feedback.png'])
        mc_score = fs.get_last_opened_session()._mc_score
        mc_count =  len(mc_key)
        tf_score = fs.get_last_opened_session()._tf_score
        tf_count =  len(tf_key)
        idtf_score = fs.get_last_opened_session()._idtf_score
        idtf_count =  len(tf_key)
        recipient =  fs.get_last_opened_session().name
        sheetname = fs.sheets[fs.open_index].name
        string = f'Sheet [{sheetname}] Recipient [{recipient}] Multiple Choice Score [{mc_score}/{mc_count}] True or False Score [{tf_score}/{tf_count}] Identification [{idtf_score}/{idtf_count}]'

        stitch_sheet(1,1,1,string,'assets/feedback_stitched.png',img_stack, True,empty_header=True,font_scale=0.75)
        
    #METHOD____________________________________________
    def update(self, test_type,ignore_img=False):
        print("UPDATING SHET")
        value=None
        check_sheet = fs.get_sheet(fs.open_index).check_sheets
        print(check_sheet.session_open_index)
        check_session=check_sheet.get_session(check_sheet.session_open_index)
        print(check_session.name)
        self.ids.check_text_field.text = check_session.name
        self.ids.check_text_field.secondary_text = str(check_session.date_created)
        #
        # self.feedback_widget = FeedBack()
        #self.add_widget(self.feedback_widget)
        if test_type == 'MULTIPLE CHOICE':
            value = check_session._mc_score
            count = len(fs.sheets[fs.open_index].answer_key.mc.get_items())
            self.ids.mc_indicator.text = f'Multiple Choice: {value}/{count}'
            if value is not None:
                self.ids.mc_indicator.color = (0,0.5,0,1)
            else:
                self.ids.mc_indicator.color = (0.4,0.4,0,4)

        elif test_type == 'TRUE OR FALSE':
            value = check_session._tf_score
            count = len(fs.sheets[fs.open_index].answer_key.tf.get_items())
            self.ids.tf_indicator.text = f'True or False: {value}/{count}'
            if value is not None:
                self.ids.tf_indicator.color = (0,0.5,0,1)
            else:
                self.ids.tf_indicator.color = (0.4,0.4,0,4)
        else:
            value = check_session._idtf_score
            count = len(fs.sheets[fs.open_index].answer_key.idtf.get_items())
            self.ids.idtf_indicator.text = f'Identification: {value}/{count}'
        
            if value is not None:
                self.ids.idtf_indicator.color = (0,0.5,0,1)
            else:
                self.ids.idtf_indicator.color = (0.4,0.4,0,4)
        self.img_display.source = 'assets/loading.jpg'
        if ignore_img == False:
            print("GETTING FEEDBACK")
            scheduler.bg_run_once(func=lambda: self.update_feedback(check_session),
                                callback_func=lambda: self.feedback_finish_load(),
                                name='feedback_thread')

        # Temporarily clear the source to force a texture reload
        #image.source = ''
        
        # Assign the new texture
        #image.texture =image_texture
        
        # Assign the source again to ensure the update is triggered
        #image.source = 'assets/mc_feedback.png'
        
        # Trigger a layout update to force the image to redraw
        #image.reload()
        


    def cam_on(self):
        """Func for turning camera on
        """

        # reference file system variables for shortening
        if on_android:
            request_permissions([Permission.CAMERA])
        mc = fs.sheets[fs.open_index].answer_key.mc
        tf = fs.sheets[fs.open_index].answer_key.tf
        idtf = fs.sheets[fs.open_index].answer_key.idtf

        # renames 'None' string to literal None object
        mc_answers = [x.answer_key if x.answer_key != 'None' else None for x in mc.get_items()]
        tf_answers = [x.answer_key if x.answer_key != 'None' else None for x in tf.get_items()]
        idtf_answers = [x.answer_key for x in idtf.get_items()]
        cam_btn = self.ids.cam_button
        cam_btn.icon = 'close'
        # debugging
        print(mc,tf,idtf)
        self.img_display.opacity = 0
        #self.img_display.reload()
        #self.camera_widget = CameraWidget() # out
        # pass answer keys to camera widget as ground truth later.
        check_sheet = fs.get_sheet(fs.open_index).check_sheets
        self.camera_widget = CameraWidget(mcq_correct=mc_answers, 
                                          tf_correct=tf_answers,
                                          idtf_correct=idtf_answers,
                                          primary_storage=root_folder,
                                          check_session=check_sheet.get_session(check_sheet.session_open_index),
                                          checkscreen=self)
        #self.add_widget(self.camera_widget, len(self.children) - len(self.children)-2) # add widget, with max-(max-4) pos
        self.img_display.opacity = 1
        self.camera_widget.frame_image = self.img_display
        self.img_display.keep_ratio= False
        #self.img_display.source = self.camera_widget.frame_image.source
        #self.img_display.reload()
        # status indicatoron
        self.cam_is_on = True

    def on_screen(self,*args,**kwargs):
        Function.copy_file('assets/empty_template.png','assets/feedback_stitched.png')
        Function.copy_file('assets/empty_template.png','assets/mc_feedback.png')
        Function.copy_file('assets/empty_template.png','assets/tf_feedback.png')
        Function.copy_file('assets/empty_template.png','assets/feedback_stitched-flipped.png')
        Function.copy_file('assets/empty_template.png','assets/mc_feedback-flipped.png')
        Function.copy_file('assets/empty_template.png','assets/tf_feedback-flipped.png')
        self.img_display = self.ids.feedback_img
        self.img_display.opacity = 1
        cam_btn = self.ids.cam_button
        cam_btn.icon = 'camera'
        self.ids.date_label.text = 'Date Created: '+str(fs.get_last_opened_session().date_created)
        #cam_btn.md_bg_color = App.get_running_app().theme_cls.primary_color
        for x in ['MULTIPLE CHOICE', 'TRUE OR FALSE', 'IDENTIFICATION']:
            self.update(x)
        
        

    


    #METHOD________________________________________________

    def switch_cam(self,*args,**kwargs):
        """Switching cams based on status indicator
        """
        if self.cam_is_on == False:
            self.cam_on()
        else:
            self.cam_off()
    

    #INIT______________________________________________________
            
    def __init__(self,**kwargs):
        super(CheckScreen, self).__init__(**kwargs)
        self.cam_is_on = False # initialize status indicator
        #self.feedback_widget = None
        self.preview_image = btn_img
        #self.img_display = Image(source='assets/loading.jpg',size_hint = (1,0.3),pos_hint = {'top': 0.8, 'center_x': 0.5})

        #self.add_widget(self.img_display)

#CLASS_________________________________________________________

class AnswerSheetScreen(Screen):
    """Screen class for managing answer sheet functionalities.

    Attributes:
        None

    Methods:
        apply_count_for_type(key_type): Applies the count for a specific key type (e.g., mc, tf, idtf).
        apply_count(): Applies the count for all key types (mc, tf, idtf).
        show_text_field(active, checkbox_type): Enables or disables text fields based on checkbox state.
    """
    def __init__(self, **kwargs):
        super(AnswerSheetScreen, self).__init__(**kwargs)
        self.preview_img = btn_img

    def max_image(self, *args,**kwargs):
        self.preview_img.set_image('assets/whole_template-flipped.png')
        self.add_widget(self.preview_img)
    #METHOD___________________________________________________
    def share(self):
        name=f'{fs.sheets[fs.open_index].name}.png'
        Function.copy_file('assets/whole_template.png', fs.filemanager_last_dir+'/'+name)
        Function.share(fs.filemanager_last_dir+'/'+name)

    #METHOD_____________________________________________________
    def open_file_manager(self, *args):
        sheet_name = fs.sheets[fs.open_index].name
        unique_name = str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        name=f'{fs.sheets[fs.open_index].name}'
        unique_name = str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        name = f'{name}[{unique_name}].png'
        fm = FileManager(lambda x: Function.copy_file('assets/whole_template.png', x+'/'+name), fs.filemanager_last_dir).file_manager_open()
    
    #METHOD_________________________________________________________
    def get_fit(self):
         #file system obj; get sheet based on opened index (openeded sheet on gui). then get answer keys
    
        # set variables based on key type
        try:
            mc_count = int(self.ids.mcq_textfield.text)
            if self.ids.mcq_textfield.opacity ==0:
                raise ValueError('')
        except ValueError as e:
            print(e)
            mc_count = 0
        try:
            tf_count = int(self.ids.tf_textfield.text)
            if self.ids.tf_textfield.opacity ==0:
                raise ValueError('')
        except ValueError as e:
            print(e)
            tf_count = 0
        try:
            idtf_count = int(self.ids.ident_textfield.text)
            if self.ids.ident_textfield.opacity ==0:
                raise ValueError('')
        except ValueError as e:
            print(e)
            idtf_count = 0
        score = fit_score(mc_count,tf_count,idtf_count)*100
        score = round(score, 2)
        text = f'Fit: {score}%'
        self.ids.fit_label.text = text
        self.ids.mcq_textfield.text = '' if self.ids.mcq_textfield.text == 0 else self.ids.mcq_textfield.text
        self.ids.tf_textfield.text = '' if self.ids.tf_textfield.text == 0 else self.ids.tf_textfield.text
        self.ids.ident_textfield.text = '' if self.ids.ident_textfield.text == 0 else self.ids.ident_textfield.text
        if score > 100:
            self.ids.fit_label.text_color =(1,0,0,0.7)
            self.ids.apply.disabled = True
            self.ids.share.disabled = True
            self.ids.export.disabled = True
        else:
            self.ids.fit_label.text_color = (0,0,1,0.7)
            self.ids.apply.disabled = False
            self.ids.share.disabled = False
            self.ids.export.disabled = False
        for textfield, limit in zip([
            self.ids.mcq_textfield,
            self.ids.tf_textfield,
            self.ids.ident_textfield
        ], [100,175,10]):
            try:
                text_int =int(textfield.text.strip()) 
                if text_int > limit:
                    textfield.text = textfield.text[:-1]
                    msg('Cannot exceed item limit.')
                """if textfield.text[-1] not in ['1234567890']:
                    print('ERASING LAST CHAR; NOT A NUM')
                    textfield.text = textfield.text[:-1]"""
            except ValueError as e:
                print(e)
                continue
        self.apply_count(set_items=False)
        
    #METHOD_____________________________________________________-

    def apply_count_for_type(self, key_type,set_items=True):
        """Applies the count for a specific key type.

        Args:
            key_type (str): The type of key (mc, tf, idtf).

        Returns:
            None
        """
         #file system obj; get sheet based on opened index (openeded sheet on gui). then get answer keys
        answer_key = fs.sheets[fs.open_index].answer_key
        textfield = None # init
        count = 0 # init

        # set variables based on key type
        if key_type == 'mc':
            answer_key = answer_key.mc
            textfield = self.ids.mcq_textfield
        elif key_type == 'tf':
            answer_key = answer_key.tf
            textfield = self.ids.tf_textfield
        elif key_type == 'idtf':
            answer_key = answer_key.idtf
            textfield = self.ids.ident_textfield

        # if textfield is disabled. Assume 0 count
        if textfield.disabled == True or textfield.text == '':
            count = 0
            #textfield.opacity = 0
        else:
            count = int(textfield.text)
            #textfield.opacity = 1

        # Debugging
        print(textfield.disabled)
        print(f'{key_type} item count: {count}')
        print('showing', answer_key.show_items)
        if set_items:
            answer_key.set_items(count) # setting items using method from FileSystem
            msg("Sheet Updated.")
        self.set_hidden_field()
        return count
    
    #METHOD__________________________________________________
    def generate_template(self,mc,tf,idtf,name):
        generate_func = lambda: self.generate(mc,tf,idtf,name)
        
        scheduler.run_background(generate_func, 'generate_template_thread',lambda **kwargs: self.update_image_texture(**kwargs))

    def generate(self, mc, tf, idtf, name):
        print("GENERATING SHEET")
        template_path = stitch_sheet(mc_num=mc,
                     idtf_num=idtf,
                     tf_num=tf,
                     title=name)
        
        image_texture = CoreImage(template_path).texture
        self.ids.apply.disabled = False
        self.ids.export.disabled = False
        self.ids.share.disabled = False
        # Update the texture of the Image widget
        print("GENERATING DONE, PASSING PARaMETERS")
        scheduler.pass_parameter('generate_template_thread','texture',image_texture)
        scheduler.pass_parameter('generate_template_thread', 'path',template_path)
        #self.update_image_texture(image_texture,template_path)
        
    def update_image_texture(self, texture,path):
        # Get a reference to the Image widget
        image = self.ids.generated_image
        
        # Temporarily clear the source to force a texture reload
        image.source = ''
        
        # Assign the new texture
        image.texture = texture
        
        # Assign the source again to ensure the update is triggered
        image.source = path
        
        # Trigger a layout update to force the image to redraw
        image.reload()



    #METHOD__________________________________________________
        

    def apply_count(self,set_items=True):
        """Applies the count for all key types (mc, tf, idtf).

        Args:
            None

        Returns:
            None
        """
        mc_count = self.apply_count_for_type('mc',set_items)
        tf_count = self.apply_count_for_type('tf',set_items)
        idtf_count = self.apply_count_for_type('idtf',set_items)
        name = fs.sheets[fs.open_index].name
        self.generate_template(mc_count, tf_count, idtf_count, name)
        
        

    def set_hidden_field(self):
        print('setting hidden')
        ansheet_ids = self.manager.get_screen('answer_sheet').ids
        mcq_field_disabled = ansheet_ids.mcq_textfield.disabled == False
        tf_field_disabled = ansheet_ids.tf_textfield.disabled == False
        idtf_field_disabled = ansheet_ids.ident_textfield.disabled == False
        ansheet_ids.mcq_textfield.opacity = 1 if mcq_field_disabled else 0
        ansheet_ids.tf_textfield.opacity = 1 if tf_field_disabled else 0
        ansheet_ids.ident_textfield.opacity = 1 if idtf_field_disabled else 0
        self.ids.mcq_textfield.text = '' if self.ids.mcq_textfield.text == '0' else self.ids.mcq_textfield.text
        self.ids.tf_textfield.text = '' if self.ids.tf_textfield.text == '0' else self.ids.tf_textfield.text
        self.ids.ident_textfield.text = '' if self.ids.ident_textfield.text == '0' else self.ids.ident_textfield.text

    def show_text_field(self, active, checkbox_type):
        """Enables or disables text fields based on checkbox state.

        Args:
            active (bool): Flag indicating whether the checkbox is active or not.
            checkbox_type (str): The type of checkbox ('mcq', 'tf_textfield', 'ident').

        Returns:
            None
        """
        if checkbox_type == 'mcq':
            self.manager.get_screen('answer_sheet').ids.mcq_textfield.disabled = not active
        elif checkbox_type == 'tf_textfield':
            self.manager.get_screen('answer_sheet').ids.tf_textfield.disabled = not active
        elif checkbox_type == 'ident':
            self.manager.get_screen('answer_sheet').ids.ident_textfield.disabled = not active
        self.set_hidden_field()

    def on_screen(self, *args,**kwargs):
        self.apply_count(set_items=False)


#CLASS_____________________

#_________________________________________________

manager = None
if on_android:
    root_folder = android_storage
else:
    root_folder = os.getcwd()


def autosave():
    """Autosaves changes on filesystem into permanent local storage.

    TODO: Prevent data corruption while saving

    """
    #print('saving')
    try:
        #safe_exit=False
        fs.save() # saves filesystem
        fs.save(root_folder+'/'+f'qm_localdb_DO_NOT_DELETE_backup.pkl')
        #print('saving')
        #print('f')
    except Exception as e:
        print(e)


#_______________________________________________
def autosave_callback():
    global manager
    """Function for scheduler on thread.
    Used to retrigger saving only after previous saving is done.
    """
    #scheduler.safe_exit=True
    if scheduler.safe_exit:
        manager.stop()
        
        
    autosave_sched() # restart when don

def autosave_sched():
   
    scheduler.run_background(lambda: autosave(),'autosave_thread',lambda **kwargs: autosave_callback(),make_queue=True)
    #Clock.schedule_once(lambda x:threading.Thread(target=lambda: autosave()).start(),0.01) # using kivy scheduler; do thread.

import sys
#_________________________________________________
class Scheduler:
    def __init__(self):
        self.run_background = self.bg_run_once
        self.next_queue = None
        self.working = False
        self.thread_names = [t.name for t in threading.enumerate()]
        self.parameters = {}
        self.safe_exit = False
        self.thread_queues = {}
        #self.thread_queues_paramaters = {}
        self.periodic_functions =[]
    
    def start_periodic_functions(self):
        #Clock.schedule_interval(self.run_periodic_functions, 0.5)
        pass

    def run_periodic_functions(self):
        for func in self.periodic_functions:
            func()

    def add_periodic_function(self, func):
        self.periodic_functions.append(func)
        

    def pass_parameter(self, name, param_name, value,can_queue=False):
        self.parameters[name][param_name] = value
        #print(self.thread_queues)
        if can_queue:
            self.thread_queues[name][-1][2][param_name] = value


    def not_working(self):
        self.working = False

    def bg_run_once(self,func,name, callback_func = None, make_queue= False):
        """_summary_

        Args:
            func (function): ex. lambda: yourFunction(), function to run on the background/thread.
            callback_func (function, optional): ex. lambda: yourFunction2(), function to run when process is done. 
                callback_func is processed on the main thread.
        """
        #____________________________________________
        def trigger_function(func, callback,name,make_queue):
            func()
            #print(self.thread_queues)
            self._do_callback(callback,name,make_queue) if callback is not None else None
            #self._execute_queued_functions(name) if make_queue else None

            
        #_________________________________________
            
        # 
        self.parameters[name] = {} if name not in self.parameters.keys() else self.parameters[name]
        func0, cb_func0 = func, callback_func

        #print("THREADS",self.thread_names)
        #print('current threads',[t.name for t in threading.enumerate()])
        if name not in [t.name for t in threading.enumerate()]:
            thread = threading.Thread(target = lambda: trigger_function(func0, cb_func0,name, make_queue), name=name)
            Clock.schedule_once(lambda x: thread.start(),0.01)
        else:
            if make_queue:
                #print("MAKING QUEUES!")
                self.thread_queues[name] = []
                self.thread_queues[name].append([func, callback_func,{}])
        
   
    def _do_callback(self, func,name,make_queue):
        kwargs = self.parameters[name]
        queue = []
        self.parameters[name] = {}
        if make_queue and name in self.thread_queues:
            queue = self.thread_queues[name]
            
            #print("QUEUE",queue)
            if len(queue) > 0:
                func, callback_func,param = queue.pop(0)
                self.parameters[name] = param
            
        Clock.schedule_once(lambda x: (self.not_working(),func(**kwargs),self.bg_run_once(func,name,callback_func,make_queue) if len(queue) > 1 else None),0.01) # using kivy scheduler; do thread.
        
        #self.bg_run_once(func, callback, first_startup=False)
        #queue = self.thread_queues.get(name, [])
        
            #Clock.schedule_once(lambda x: ,0.01)
        return 
    
    
    
class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.transition =FadeTransition()
        self.transition.duration = 0.10
        

    def change_screen(self, screen_name,**kwargs):
        screen = self.get_screen(screen_name)
        
        self.current = screen_name
        try:
            screen.on_screen(**kwargs)
        except AttributeError as e:
            print('screen.change_screen():',e)

class App(MDApp):
    def build(self):
       
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.screen = Builder.load_string(KV)
        self.manager = None
        
        return self.screen

   
    #________________________________________________
   

    def on_start(self):
        """on startup initiializations
        """
        home_screen = self.root.get_screen('home')
        #home_screen.add_item_to_list()
        self.root.change_screen('home')
        home_screen.show_init_list()
        
        self.manager = self.root
        autosave_sched()
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        global manager
        manager = self

    #_____________________________________________________
    
    def screen_manager_func(self):
        """
        Screen manager function for managing Back button event or esc keyboard event.
        """
        dummy = self.root.get_screen('home') # just for obvious accessing of manager attribute
        
        if dummy.manager.current == 'home': # on first screen
            confirmation_dialog('Are you sure you want to exit?',
                            yes_func = lambda *args: setattr(scheduler, 'safe_exit',True),
                            no_func = lambda *args: None)
            #scheduler.safe_exit = True
            
        elif dummy.manager.current in ['name','name_expanded']:
            dummy.manager.change_screen('home') # go back to home
        elif dummy.manager.current =='check': # CHecking/Scanning of sheet
            try:
                if self.root.get_screen('check').cam_is_on == True:  # turn off camera when onn
                    self.root.get_screen('check').cam_off()
                else: # if camera is already off; go back screen
                    dummy.manager.change_screen( 'onecheck')
            except Exception as e:
                print(e)
                pass
        elif dummy.manager.current == 'mcqanalysis':
            dummy.manager.change_screen('analysis')
            
        else: # othere else screens unlisted: go back to name
            dummy.manager.change_screen('name')
    
    #_________________________________________________________

    def hook_keyboard(self, window, key, *largs):
        """Add keyboard event for back or esc
        """
        if key == 27:
            self.screen_manager_func()
            return True 
        
    #__________________________________________________________

    def update_label(self, instance):
        """?..."""
        text_input = instance.text
        display_label = self.root.get_screen('name').ids.display_label
        current_date = datetime.now().strftime('%Y-%m-%d')
        display_label.text = f"{text_input}\n{current_date}"
        text_field = self.root.get_screen('name').ids.text_field
        self.root.get_screen('name').remove_widget(text_field)
        save_button = self.root.get_screen('name').ids.save_button
        self.root.get_screen('name').remove_widget(save_button.parent)

    #____________________________________________________________

    def save_and_display_text(self):
        """?...
        """
        text_input = self.root.get_screen('name').ids.text_field.text
        self.update_label(self.root.get_screen('name').ids.text_field)

        # Add item to the list
        home_screen = self.root.get_screen('home')
        home_screen.add_item_to_list(text_input)

        # Remove save button
        save_button = self.root.get_screen('name').ids.save_button
        self.root.get_screen('name').remove_widget(save_button.parent)


class Function:
    def copy_file(source_path, destination_path):
        """
        Copy a file from the source path to the destination path.

        Args:
        - source_path (str): The path of the source file.
        - destination_path (str): The path where the file will be copied.

        Returns:
        - bool: True if the file was successfully copied, False otherwise.
        """
        try:
            # Copy the file
            shutil.copy(source_path, destination_path)
            return True, '', destination_path
        except Exception as e:
            print(f"An error occurred: {e}")
            return False, str(e), destination_path
        
    def share(path):
        try:
            from android.storage import primary_external_storage_path
            from jnius import autoclass
            from jnius import cast
            import os
            
            StrictMode = autoclass('android.os.StrictMode')
            StrictMode.disableDeathOnFileUriExposure()
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')

            shareIntent = Intent(Intent.ACTION_SEND)
            shareIntent.setType('image/png')
            #path = fs.filemanager_last_dir+'/'+'temp--QM.png'
            imageFile = File(path)
            uri = Uri.fromFile(imageFile)
            parcelable = cast('android.os.Parcelable', uri)
            shareIntent.putExtra(Intent.EXTRA_STREAM, parcelable)
            #shareIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            #shareIntent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            currentActivity.startActivity(shareIntent)

            #________________________________________
            
        except Exception as e:
            msg(str(e))

def anim_next_display(self):
    print(self.ids.next_display.source)
    self.ids.next_display.opacity = 0.8
    anim = Animation(opacity=0, duration=1)  # Animate opacity to 1 over 1 second
    #anim2 = Animation(opacity=0, duration=1)  # Animate opacity to 1 over 1 second

    anim.start(self.ids.next_display)
    #anim2.start(self.ids.next_display)

def anim_previous_display(self):
    print(self.ids.previous_display.source)
    self.ids.previous_display.opacity = 0.8
    anim = Animation(opacity=0, duration=1)  # Animate opacity to 1 over 1 second
    #anim2 = Animation(opacity=0, duration=1)  # Animate opacity to 1 over 1 second

    anim.start(self.ids.previous_display)
    #anim2.start(self.ids.next_display)
def set_fbc_callback(object):
    fbc.fbc = object

def get_fbc():
    print('GETTING FBC')
    fbc_object = feedback.read_presaved_feedback()
    scheduler.pass_parameter('get_presaved_thread','object',fbc_object)
    print("DONE GETTING FBC, PASSING PARAMETER")

class SchedClassDummy:
    def __init__(self):
        self.fbc = None

def confirmation_dialog(text, yes_func, no_func):
    
    dialog = MDDialog(
        text=text
    )
    dialog = MDDialog(
        text=text,
        buttons = [
            MDFlatButton(
                text="Yes", on_release=lambda x: (yes_func(), dialog.dismiss(force=True))
            ),
            MDFlatButton(
                text="No", on_release=lambda x: dialog.dismiss(force=True)
            ),
        ]
    )
    dialog.open()
scheduler = Scheduler()
fbc = SchedClassDummy()
btn_img_obj = ButtonImage()
btn_img = ButtonImagePopUp(btn_img_obj)
scheduler.start_periodic_functions()

#START OF SCRIPT___________________________________________________
scheduler.run_background(lambda: get_fbc(), 'get_presaved_thread',lambda **kwargs: set_fbc_callback(**kwargs))
# feedback.read_presaved_feedback()
def update_filesystem():
    fs = FileSystem()
    try:
        fs_previous = fs.load(root_folder+'/'+f'qm_localdb_DO_NOT_DELETE_backup.pkl')
    except Exception as e:
        fs_previous = fs.load()

    def update_class1_to_class2(obj):
        if isinstance(obj, fs_previous.__class__):
            for attr_name in dir(fs_previous):
                if not attr_name.startswith('__') and not hasattr(obj, attr_name):
                    setattr(obj, attr_name, getattr(fs_previous, attr_name))
        for attr_name in dir(obj):
            if not attr_name.startswith('__'): 
                attr = getattr(obj, attr_name)
                if hasattr(attr, '__dict__'):
                    update_class1_to_class2(attr)

    update_class1_to_class2(fs_previous)
    return fs_previous


# load filesystem previous data from permanent local storage;
# comment out to not use previous data (warning; overwrites with empty new data because of autosave on app run)

fs = FileSystem()
try:
    fs = fs.load(root_folder+'/'+f'qm_localdb_DO_NOT_DELETE_backup.pkl') # use local by default.
except Exception as e:
    try:
        fs = fs.load()
    except Exception as e:
        fs = FileSystem()
print(dir(fs))

fs.filemanager_last_dir = root_folder

App().run() # RUN APP; init
