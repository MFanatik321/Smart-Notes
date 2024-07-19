from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QMessageBox, QTextEdit, QListWidget, QLineEdit, QInputDialog
import json

#Windows
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle('Умный заметки (страшные заметки)')
window_text = QTextEdit()
window_list1 = QListWidget()
window_list2 = QListWidget()
window_line = QLineEdit()
list_zametki = QLabel('Список заметок')
list_TAGS = QLabel('Список тегов')



#layouts
note_h_layout = QHBoxLayout()
tag_h_layout = QHBoxLayout()
main_v_layout = QVBoxLayout()
main_layout = QHBoxLayout()


SEARCH_TXT = 'Искать заметки по тегу'
IN_PROCESS_TXT = 'Сбросить поиск'


#buttons
create = QPushButton('Создать заметку')
delete = QPushButton('Удалить заметку')
save = QPushButton('Сохранить заметку')
add = QPushButton('Добавить к заметке')
otkrepit = QPushButton('Открепить от заметки')
find = QPushButton(SEARCH_TXT)

#work with layouts
main_v_layout.addWidget(list_zametki)
main_v_layout.addWidget(window_list1)
note_h_layout.addWidget(create)
note_h_layout.addWidget(delete)
tag_h_layout.addWidget(add)
tag_h_layout.addWidget(otkrepit)
main_v_layout.addLayout(note_h_layout)
main_v_layout.addWidget(save)
main_v_layout.addWidget(list_TAGS)
main_v_layout.addWidget(window_list2)
main_v_layout.addWidget(window_line)
main_v_layout.addLayout(tag_h_layout)
main_v_layout.addWidget(find)
main_layout.addWidget(window_text)
main_layout.addLayout(main_v_layout)

#lol
TEXT = 'текст'
TAGS = "тэги"


note_title = 'О жизни и бесконечно вечном'

NOTES = {
	note_title: {
		TEXT: "Я не философ чтоб об этом рассуждать",
		TAGS: ['Жизнь', "Философия"]
	},
	'Nigga.py': {
		TEXT: "ЧЁРНЫЙ юмор это плохо",
		TAGS: ['чёрный', "юмор"]
	},
}

#functions
def write_notes(notes):
	with open('notes.json', 'w') as file:
		json.dump(notes, file)
		
def read_notes():
	with open('notes.json', 'r', encoding='utf-8') as file:
		notes = json.load(file)
		return notes


def errorWindow(txt, title='Ошибка'):
	msg_window = QMessageBox()
	msg_window.setWindowTitle(title)
	msg_window.setText(txt)
	msg_window.exec()


def filter_dict(my_dict, value):
	filtred_dict = {}
	for item in my_dict:
		if value in my_dict[item][TAGS]:
			filtred_dict[item] = my_dict[item]
	return filtred_dict


NOTES = read_notes()

#functions x2
def show_note():
    name = window_list1.selectedItems()[0].text()
    window_text.setText(NOTES[name][TEXT])
    window_list2.clear()
    window_list2.addItems(NOTES[name][TAGS])


def add_note():
	note_text, ok = QInputDialog.getText(main_window, 'Добавить заметку', 'Название заметки:')
	if ok:
		NOTES[note_text] = {TEXT: '', TAGS: []}
		window_list1.clear()
		window_list2.clear()
		window_list1.addItems(NOTES)
		window_list2.addItems(NOTES[note_text][TAGS])
		write_notes(NOTES)
create.clicked.connect(add_note)


def del_note():
	if window_list1.selectedItems():
		name = window_list1.selectedItems()[0].text()
		del NOTES[name]
		window_list1.clear()
		window_list2.clear()
		window_list1.addItems(NOTES)
		write_notes(NOTES)
	else:
		errorWindow('Заметка не выбрана!')
delete.clicked.connect(del_note)


def save_note():
	if window_list1.selectedItems():
		name = window_list1.selectedItems()[0].text()
		note_text = window_text.toPlainText()
		NOTES[name][TEXT] = note_text
		write_notes(NOTES)
	else:
		errorWindow('Заметка не выбрана!')
save.clicked.connect(save_note)



def add_tag():
	if window_list1.selectedItems():
		name = window_list1.selectedItems()[0].text()
		tag_text, ok = QInputDialog.getText(main_window, 'Добавить тег', 'Ввести теги через пробел:')
		if ok:
			NOTES[name][TAGS] +=  tag_text.split(' ')
			window_list2.clear()
			window_list2.addItems(NOTES[name][TAGS])
			write_notes(NOTES)
	else:
		errorWindow('Заметка не выбрана!')
add.clicked.connect(add_tag)


def delete_tag():
	if window_list1.selectedItems():
		if window_list2.selectedItems():
			name = window_list1.selectedItems()[0].text()
			tag_name = window_list2.selectedItems()[0].text()
			NOTES[name][TAGS].remove(tag_name)
			window_list2.clear()
			window_list2.addItems(NOTES[name][TAGS])
			write_notes(NOTES)
		else:
			errorWindow('Тег не выбран!')
	else:
		errorWindow('Тег не выбран!')
otkrepit.clicked.connect(delete_tag)


def search_by_tag():
	tag_list = window_line.text()
	if find.text() == SEARCH_TXT and tag_list != ' ':
		find.setText(IN_PROCESS_TXT)
		filtred_notes = filter_dict(NOTES, tag_list)
		window_list1.clear()
		window_list2.clear()
		window_text.clear()
		window_list1.addItems(filtred_notes)
	elif find.text() == IN_PROCESS_TXT:
		find.setText(SEARCH_TXT)
		window_list1.clear()
		window_list2.clear()
		window_text.clear()
		window_list1.addItems(NOTES)
find.clicked.connect(search_by_tag)


#lol x2
main_window.resize(400, 200)
main_window.setLayout(main_layout)
main_window.show()
window_list1.addItems(NOTES)
window_list1.itemClicked.connect(show_note)
create.clicked.connect(add_note)
app.exec_()