import tkinter.ttk
import tkinter.font
import db

# Основное окно
window = tkinter.Tk()
main_font = tkinter.font.Font(family='Tahoma', size=10)
window.title(db.title_basename)
window.geometry('814x244+400+200')
window.minsize(814, 244)
window.iconbitmap(default='icon.ico')

# Основная таблица
tree = tkinter.ttk.Treeview(columns=db.caption_name, show='headings')
for col_num in range(len(db.caption_name)):
    if col_num == 0:
        colwidth = 100
    else:
        colwidth = 135
    tree.column(column=db.caption_name[col_num], width=colwidth, anchor='w')
    tree.heading(column=db.caption_name[col_num], text=db.caption_data[col_num], anchor='c')
tree.pack(expand=1, fill=tkinter.BOTH, side='left', padx=4, pady=4, ipadx=4, ipady=4)

# Полоса прокрутки
scrollbar = tkinter.ttk.Scrollbar(orient=tkinter.VERTICAL, command=tree.yview())
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='left', fill=tkinter.Y)

# Главное меню
main_menu = tkinter.Menu(master=window, font=main_font)
window.config(menu=main_menu)

# Меню "Файл"
files = tkinter.Menu(master=main_menu, tearoff=0)
main_menu.add_cascade(label='Файл', menu=files)
files.add_command(label='Открыть',
                  command=lambda arg=(window, tree): db.open_file(arg),
                  font=main_font, compound='left')
files.add_command(label='Сохранить',
                  command=lambda: db.save_file('save'),
                  font=main_font, compound='left')
files.add_command(label='Сохранить как',
                  command=lambda: db.save_file('save_as'),
                  font=main_font, compound='left')
files.add_command(label='Закрыть',
                  command=lambda arg=(window, tree): db.close_file(arg),
                  font=main_font, compound='left')
files.add_separator()
files.add_command(label='Выход',
                  command=lambda arg=window: db.close_app(arg),
                  font=main_font, compound='left')

# Меню "Данные"
datas = tkinter.Menu(master=main_menu, tearoff=0)
main_menu.add_cascade(label='Данные', menu=datas)
datas.add_command(label='Добавить',
                  command=lambda arg=(window, 'append', main_font, tree): db.command_data(arg),
                  font=main_font, compound='left')
datas.add_command(label='Редактировать',
                  command=lambda arg=(window, 'edit', main_font, tree): db.command_data(arg),
                  font=main_font, compound='left')
datas.add_command(label='Удалить',
                  command=lambda arg=(window, 'delete', main_font, tree): db.command_data(arg),
                  font=main_font, compound='left')

# Меню "Поиск"
search_menu = tkinter.Menu(master=main_menu, tearoff=0)
main_menu.add_cascade(label='Поиск', menu=search_menu)
search_menu.add_command(label='Найти',
                        command=lambda arg=(window, main_font, tree): db.search(arg),
                        font=main_font, compound='left')

# Запуск программы
window.protocol(name='WM_DELETE_WINDOW', func=lambda arg=window: db.close_app(arg))
window.mainloop()
