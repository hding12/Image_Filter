###################################################
#           Author: Huangwei Ding                 #
#           Date: 2/5/2019                        #
###################################################


import tkinter as tk
import os
import cv2
import pytesseract
import csv


Empty_Path_Error = 'Error: Empty path! Please enter the path of folder with images'
File_Error = 'Error: One or more files are not images! Please check the folder. \nEvery file in this folder should be in image format.'
Faces_Entry_Type_Error = 'Error: Please enter an integer.'
No_InfoCSV_Error = 'Error: Extract information from images first !'
Search_Disabled_Error = 'Error: Empty textfield. Enable textfield and Enter number or text'


class ImageFilter(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('HomePage')
        self.master.geometry('500x300')
        self.master.configure(background='black')

        self.homepage_frame = tk.Frame(self.master, height='300', width='500', bg='white')
        self.extract_frame = tk.Frame(self.master, height='300', width='500', bg='white')
        self.search_frame = tk.Frame(self.master, height='300', width='500', bg='white')

        self.path_frame = tk.Frame(self.extract_frame, height='155', width='438', bg='white', relief='solid', borderwidth=2)
        self.error_label_extract = tk.Label(self.extract_frame)

        self.face_entry = tk.Entry(self.search_frame)
        self.text_entry = tk.Entry(self.search_frame)
        self.error_label_search = tk.Label(self.search_frame)
        self.result_label = tk.Label(self.search_frame)

        self.check_state_face = tk.IntVar()
        self.check_state_text = tk.IntVar()

        self.create_homepage()

    def create_homepage(self):
        self.homepage_frame.place(x=0, y=0, anchor='nw')

        main_title = tk.Label(self.homepage_frame)
        main_title['text'] = 'Image Filter'
        main_title['bg'] = 'white'
        main_title['font'] = ('times', 30)
        main_title.place(x='150', anchor='nw')

        button_extract = tk.Button(self.homepage_frame)
        button_extract['text'] = 'Extract'
        button_extract['command'] = self.create_extract_window
        button_extract.place(x=10, y=100, anchor='nw')

        button_search = tk.Button(self.homepage_frame)
        button_search['text'] = 'Search'
        button_search['command'] = self.create_search_window
        button_search.place(x=10, y=140, anchor='nw')

        instruction_label = tk.Label(self.homepage_frame)
        instruction_text1 = 'Instruction:\n    '
        instruction_text2 = 'Click Extract to extract information from images in a folder\n    '
        instruction_text3 = 'Click Search to find images\n    '
        instruction_text4 = '(Enter the amount of faces or/and part of texts to search)'
        instruction_label['text'] = instruction_text1 + instruction_text2 + instruction_text3 + instruction_text4
        instruction_label['bg'] = 'white'
        instruction_label['font'] = ('times', 12)
        instruction_label['relief'] = 'solid'
        instruction_label['justify'] = 'left'
        instruction_label.place(x='100', y='100', anchor='nw')

    def create_extract_window(self):
        self.extract_frame.place(x=0, y=0, anchor='nw')
        self.master.title('Extract Images Information')

        path_label = tk.Label(self.extract_frame)
        path_label['text'] = 'Path:'
        path_label['bg'] = 'white'
        path_label['font'] = ('times', 14)
        path_label.place(x='20', y='33', anchor='nw')

        var_path_entry = tk.StringVar()
        var_path_entry.set('/home/hd35cm/Desktop/ocr/')
        path_entry = tk.Entry(self.extract_frame)
        path_entry['textvariable'] = var_path_entry
        path_entry['font'] = ('times', 13)
        path_entry['width'] = '35'
        path_entry.place(x='70', y='30', anchor='nw')

        button_start = tk.Button(self.extract_frame)
        button_start['text'] = 'Start'
        button_start['command'] = lambda: self.extract_information(var_path_entry)
        button_start.place(x='400', y='30', anchor='nw')

        self.path_frame.place(x='20', y='70', anchor='nw')

        frameName = 'extract'
        button_return_home_extract = tk.Button(self.extract_frame)
        button_return_home_extract['text'] = 'Homepage'
        button_return_home_extract['command'] = lambda: self.return_homepage(frameName)
        button_return_home_extract.place(x='20', y='230', anchor='nw')

    def create_search_window(self):
        self.check_state_face = 0
        self.check_state_text = 0
        self.search_frame.place(x=0, y=0, anchor='nw')
        self.master.title('Search Images')

        path_label = tk.Label(self.search_frame)
        path_label['text'] = 'Path:'
        path_label['bg'] = 'white'
        path_label['font'] = ('times', 14)
        path_label.place(x='30', y='33', anchor='nw')

        face_label = tk.Label(self.search_frame)
        face_label['text'] = 'Faces:'
        face_label['bg'] = 'white'
        face_label['font'] = ('times', 14)
        face_label.place(x='30', y='63', anchor='nw')

        text_label = tk.Label(self.search_frame)
        text_label['text'] = 'Texts:'
        text_label['bg'] = 'white'
        text_label['font'] = ('times', 14)
        text_label.place(x='30', y='93', anchor='nw')

        var_path_entry = tk.StringVar()
        var_path_entry.set('/home/hd35cm/Desktop/ocr/')
        path_entry = tk.Entry(self.search_frame)
        path_entry['textvariable'] = var_path_entry
        path_entry['font'] = ('times', 13)
        path_entry['width'] = '35'
        path_entry.place(x='80', y='30', anchor='nw')

        var_face_entry = tk.StringVar()
        self.face_entry['textvariable'] = var_face_entry
        self.face_entry['font'] = ('times', 13)
        self.face_entry['width'] = '15'
        self.face_entry['state'] = 'disabled'
        self.face_entry.place(x='80', y='60', anchor='nw')

        var_text_entry = tk.StringVar()
        self.text_entry['textvariable'] = var_text_entry
        self.text_entry['font'] = ('times', 13)
        self.text_entry['width'] = '35'
        self.text_entry['state'] = 'disabled'
        self.text_entry.place(x='80', y='90', anchor='nw')

        checkbutton_face = tk.Checkbutton(self.search_frame)
        checkbutton_face['bg'] = 'white'
        checkbutton_face['variable'] = self.check_state_face
        checkbutton_face['onvalue'] = 1
        checkbutton_face['offvalue'] = 0
        checkbutton_face['command'] = self.filter_selection_face
        checkbutton_face.place(x='0', y='65', anchor='nw')

        checkbutton_text = tk.Checkbutton(self.search_frame)
        checkbutton_text['bg'] = 'white'
        checkbutton_text['variable'] = self.check_state_text
        checkbutton_text['onvalue'] = 1
        checkbutton_text['offvalue'] = 0
        checkbutton_text['command'] = lambda: self.filter_selection_text
        checkbutton_text.place(x='0', y='95', anchor='nw')

        self.result_label['bg'] = 'white'
        self.result_label['font'] = ('times', 10)
        self.result_label['wraplength'] = '450'
        self.result_label['relief'] = 'solid'
        self.result_label['height'] = '4'
        self.result_label['width'] = '68'
        self.result_label.place(x='10', y='153', anchor='nw')

        button_search = tk.Button(self.search_frame)
        button_search['text'] = 'Search'
        button_search['command'] = lambda: self.search_images(var_path_entry, var_face_entry, var_text_entry)
        button_search.place(x='200', y='120', anchor='nw')

        frameName = 'search'
        button_return_home_search = tk.Button(self.search_frame)
        button_return_home_search['text'] = 'Homepage'
        button_return_home_search['command'] = lambda: self.return_homepage(frameName)
        button_return_home_search.place(x='200', y='230', anchor='nw')

    def extract_information(self, var_path):
        path = var_path.get()
        if path == '':
            self.extract_error(Empty_Path_Error)
            return
        csv_path = path + 'imgInfo.csv'
        files = os.listdir(path)
        if 'imgInfo.csv' in files:
            os.remove(csv_path)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        out = open(csv_path, 'a', newline='')
        csv_writer = csv.writer(out, dialect='excel')
        for name in files:
            if name != 'imgInfo.csv':
                try:
                    img = cv2.imread(path + name)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    img_text = pytesseract.image_to_string(img)
                    info = [name, img_text, len(faces)]
                    csv_writer.writerow(info)
                except:
                    self.extract_error(File_Error)

    def search_images(self, path, faces, texts):
        path = path.get()
        if faces.get() == '':
            faces = 0
        else:
            try:
                faces = int(faces.get())
            except:
                self.search_error(Faces_Entry_Type_Error)
                return
        texts = texts.get()

        mode = 0                                    ### both faces and text
        if self.check_state_face.get() == 0 and self.check_state_text.get() == 0:
            self.search_error(Search_Disabled_Error)
            return
        elif self.check_state_face.get() == 0 and self.check_state_text.get() == 1:
            mode = 1                                ### texts only
        elif self.check_state_face.get() == 1 and self.check_state_text.get() == 0:
            mode = 2                                ### faces only

        csv_path = path + 'imgInfo.csv'
        if path == '':
            self.extract_error(Empty_Path_Error)
            return
        files = os.listdir(path)
        if 'imgInfo.csv' not in files:
            self.search_error(No_InfoCSV_Error)
            return

        images_matched = []
        if mode == 0:
            with open(csv_path) as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for row in reader:
                    if texts in row[1] and faces in row[2]:
                        images_matched.append(row[0])
                csv_file.close()
        elif mode == 1:
            with open(csv_path) as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for row in reader:
                    if texts in row[1]:
                        images_matched.append(row[0])
                csv_file.close()
        elif mode == 2:
            with open(csv_path) as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for row in reader:
                    if str(faces) in row[2]:
                        images_matched.append(row[0])
                csv_file.close()
        if not images_matched:
            self.result_label['text'] = 'no image found'
        else:
            self.result_label['text'] = ',   '.join(images_matched)

    def filter_selection_face(self):
        if self.check_state_face.get() == 1:
            self.face_entry['state'] = 'normal'
        else:
            self.face_entry['state'] = 'disabled'

    def filter_selection_text(self):
        if self.check_state_text.get() == 1:
            self.text_entry['state'] = 'normal'
        else:
            self.text_entry['state'] = 'disabled'

    def return_homepage(self, frame):
        if frame == 'extract':
            self.extract_frame.place_forget()
            self.error_label_extract.place_forget()
        elif frame == 'search':
            self.search_frame.place_forget()
            self.error_label_search.place_forget()
            self.result_label['text'] = ''

    def extract_error(self, error):
        self.error_label_extract['text'] = error
        self.error_label_extract['bg'] = 'white'
        self.error_label_extract['font'] = ('times', 12)
        self.error_label_extract['fg'] = 'red'
        self.error_label_extract.place(x='20', y='260', anchor='nw')
        return

    def search_error(self, error):
        self.error_label_search['text'] = error
        self.error_label_search['bg'] = 'white'
        self.error_label_search['font'] = ('times', 12)
        self.error_label_search['fg'] = 'red'
        self.error_label_search.place(x='20', y='260', anchor='nw')
        return



window = tk.Tk()
app = ImageFilter(master=window)
app.mainloop()