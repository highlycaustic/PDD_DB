import os
import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox

# Предварительные данные
title_basename = 'База нарушителей ПДД'
caption_name = ['act_code', 'initials', 'passport', 'violation', 'date', 'fine']
caption_data = ['Код акта', 'ФИО нарушителя', 'Паспортные данные', 'Вид нарушения', 'Дата', 'Размер штрафа']
database = []
save_flag = False
open_flag = False
filepath_curr = ''
filename_curr = ''


# Обновление таблицы
def table_reload(xxarg):
    xxwindow, xxtree = xxarg
    for row in xxtree.get_children():
        xxtree.delete(row)
    xxwindow.update()
    for datarec in database:
        xxtree.insert(parent='', index=tkinter.END, values=datarec)


# Диалог открытия файла
def open_file(xarg):
    xwindow, xtree = xarg
    global open_flag, save_flag, database, filepath_curr, filename_curr
    if (not save_flag) and open_flag:  # Предлагает сохранить файл, если были внесены изменения
        open_not_saved_dialog = tkinter.messagebox.askyesnocancel(title=title_basename,
                                                                  message='Сохранить изменения в базе данных'
                                                                          + filename_curr + '?')
        if open_not_saved_dialog is True:
            save_file('save')
        elif open_not_saved_dialog is None:
            return None

    filepath = tkinter.filedialog.askopenfilename(defaultextension='csv', filetypes=[('CSV-файл', '*.csv')])
    if filepath != '':
        try:
            database.clear()
            datafile = open(file=filepath, mode='r', encoding='utf-8')
            for record in datafile:
                database.append(record.strip(';\n').split(';'))
            datafile.close()
            table_reload(xarg)
            open_flag = True
            save_flag = True
            filepath_curr = filepath
            filename_curr = os.path.split(filepath_curr)[1]
            xwindow.title(filename_curr + ' - ' + title_basename)
            tkinter.messagebox.showinfo(title='Открытие файла', message='Файл открыт.')
        except Exception:
            tkinter.messagebox.showerror(title='Открытие файла', message='Ошибка открытия файла.')


# Сохранение файла
def save_file(mode):
    global save_flag
    if mode == 'save':  # Режим "Сохранить". Использует текущий путь файла
        filepath = filepath_curr
    elif mode == 'save_as':  # Режим "Сохранить как". Вызывает системный диалог сохранения
        filepath = tkinter.filedialog.asksaveasfilename(defaultextension='csv', filetypes=[('CSV-файл', '*.csv')])
    else:
        raise Exception('Save mod was not set')
    if filepath != '':
        try:
            datafile = open(file=filepath, mode='w', encoding='utf-8')
            for record in database:
                datafile.write(';'.join(record) + ';\n')
            datafile.close()
            save_flag = True
            tkinter.messagebox.showinfo(title='Сохранение файла', message='Файл сохранен.')
        except Exception:
            tkinter.messagebox.showerror(title='Сохранение файла', message='Ошибка сохранения файла.')


# Закрыть файл. Если нет несохраненных изменений, возвращает программу в исходное состояние
def close_file(xarg):
    xwindow, xtree = xarg
    global open_flag, save_flag, database, filepath_curr, filename_curr
    if (not save_flag) and open_flag:
        close_not_saved_dialog = tkinter.messagebox.askyesnocancel(title=title_basename,
                                                                   message='Сохранить изменения в базе данных '
                                                                           + filename_curr + '?')
        if close_not_saved_dialog is True:
            save_file('save')
        elif close_not_saved_dialog is None:
            return None
    database.clear()
    table_reload(xarg)
    save_flag = False
    open_flag = False
    filepath_curr = ''
    filename_curr = ''
    xwindow.title(title_basename)


# Выход из программы.
def close_app(xarg):
    global open_flag, save_flag
    if (not open_flag) or (open_flag and save_flag):
        xarg.destroy()
    else:
        exit_dialog = tkinter.messagebox.askyesnocancel(title=title_basename,
                                                        message='Сохранить изменения в базе данных '
                                                                + filename_curr + '?')
        if exit_dialog is True:
            save_file('save')
            xarg.destroy()
        elif exit_dialog is False:
            xarg.destroy()


def get_number(numbr):
    nx = 0
    found = -1
    for elem in database:
        if elem[0] == numbr:
            found = nx
            break
        else:
            nx += 1
    return found


# Поиск
def search(xarg):
    selection_ids = []
    search_counter = 0
    query_last = ''
    category_last = 0

    def search_operate(mode):
        category = esearch_category.current()
        query = esearch_query.get()
        nonlocal search_counter, query_last, category_last

        def value_not_found():
            tkinter.messagebox.showerror(title='Поиск', message='Значение не найдено.')

        if len(xtree.get_children()) > 0:
            if mode == 'once':  # Режим "Найти". Ищет один раз, после закрывает окно поиска
                selection_ids.clear()
                for rec_id, record in enumerate(xtree.get_children()):
                    if query == database[rec_id][category]:
                        xtree.selection_set(record)
                        search_window.destroy()
                        return None
                value_not_found()
                return None
            elif mode == 'next':  # Режим "Найти далее". Выделяет подходящие значения по кругу
                if not selection_ids or query_last != query or category_last != category:
                    query_last = query
                    category_last = category
                    selection_ids.clear()
                    for rec_id, record in enumerate(xtree.get_children()):
                        if query == database[rec_id][category]:
                            selection_ids.append(record)
                    if len(selection_ids) == 0:
                        value_not_found()
                        return None
                    search_item = selection_ids[search_counter]
                    xtree.selection_set(search_item)
                else:
                    if search_counter < (len(selection_ids) - 1):
                        search_counter += 1
                    else:
                        search_counter = 0
                    search_item = selection_ids[search_counter]
                xtree.selection_set(search_item)
        else:
            tkinter.messagebox.showerror(title='Поиск', message='База пуста.')
            return None

    xwindow, main_font, xtree = xarg
    category_var = tkinter.StringVar(value=caption_data[0])  # Переменная, содержащая категории поиска

    search_window = tkinter.Toplevel(xwindow)
    search_window.title('Поиск')
    search_window.geometry('+450+250')
    search_window.resizable(False, False)

    search_frame = tkinter.Frame(master=search_window, borderwidth=4, relief='raised')
    search_frame.grid(row=0, column=0, padx=4, pady=4, ipadx=4, ipady=4)

    search_category = tkinter.Label(master=search_frame, text='Искать по столбцу:', width=22, font=main_font,
                                    anchor='w')
    search_category.grid(row=0, column=0, padx=4, pady=4)

    search_query = tkinter.Label(master=search_frame, text='Искать:', width=22, font=main_font, anchor='w')
    search_query.grid(row=1, column=0, padx=4, pady=4)

    esearch_category = tkinter.ttk.Combobox(master=search_frame, width=22, state='readonly', font=main_font,
                                            textvariable=category_var, values=caption_data)
    esearch_category.grid(row=0, column=1, padx=4, pady=4)

    esearch_query = tkinter.Entry(master=search_frame, width=30, font=main_font, justify='left')
    esearch_query.grid(row=1, column=1, padx=4, pady=4)

    button_group_frame = tkinter.Frame(master=search_window)
    button_group_frame.grid(row=2, columnspan=2, padx=4, pady=4)

    search_button = tkinter.Button(master=button_group_frame, text='Найти', width=12,
                                   command=lambda: search_operate('once'),
                                   relief='raised', borderwidth=4, font=main_font)
    search_button.pack(side='left', padx=4)

    search_next_button = tkinter.Button(master=button_group_frame, text='Найти далее', width=12,
                                        command=lambda: search_operate('next'),
                                        relief='raised', borderwidth=4, font=main_font)
    search_next_button.pack(side='left', padx=4)

    search_cancel_button = tkinter.Button(master=button_group_frame, text='Отмена', width=12,
                                          command=search_window.destroy,
                                          relief='raised', borderwidth=4, font=main_font)
    search_cancel_button.pack(side='left', padx=4)

    search_window.focus_set()


# Окно редактирования записи
def command_data(xarg):
    def int_validate(xinput):  # Проверка ввода на целочисленность
        if xinput.isdigit() or xinput == '':
            return True
        else:
            return False

    def float_validate(xinput):  # Проверка ввода на вещественность
        try:
            float(xinput)
            return True
        except ValueError:
            return False

    def entry_range_validate(event):  # Проверка полей на корректность ввода

        def clear_entry(xevent):
            xevent.widget.delete(0, tkinter.END)

        if event.widget.get():
            if event.widget is dd:
                if int(event.widget.get()) not in range(1, 32):
                    clear_entry(event)
            elif event.widget is mm:
                if int(event.widget.get()) not in range(1, 13):
                    clear_entry(event)
            elif event.widget is hours:
                if int(event.widget.get()) not in range(24):
                    clear_entry(event)
            elif event.widget is minutes:
                if int(event.widget.get()) not in range(60):
                    clear_entry(event)
            elif event.widget is efine:
                if float_validate(event.widget.get()):
                    if float(event.widget.get()) < 0:
                        clear_entry(event)
                else:
                    clear_entry(event)

    def check_and_operate():  # Проверка полей на заполненность
        if cmnd != 'delete':
            if not all([einitials.get(), epassport.get(), eviolation.get(),
                        dd.get(), mm.get(), yy.get(), hours.get(), minutes.get(), efine.get()]):
                tkinter.messagebox.showerror(title='Ошибка', message='Заполните пустые поля.')
            else:
                operate()
        else:
            operate()

    def operate():
        global database, save_flag
        if cmnd == 'delete':
            foundx = get_number(eact_code.get())
            if foundx == -1:
                tkinter.messagebox.showerror(message='Запись с указанным ID не найдена.')
            else:
                try:
                    database = database[:foundx] + database[foundx + 1:]
                    com_window.destroy()
                    table_reload((xwindow, xtree))
                    save_flag = False
                    tkinter.messagebox.showinfo(message='Запись удалена.')
                except Exception:
                    tkinter.messagebox.showerror(message='Ошибка удаления записи.')
        elif cmnd == 'append':
            try:
                next_act = '000001'
                if len(database) > 0:
                    next_act = str(max([int(record[0]) for record in database]) + 1).zfill(6)
                database.append([next_act, einitials.get(), epassport.get(), eviolation.get(),
                                 dd.get().zfill(2) + '.' + mm.get().zfill(2) + '.' + yy.get()
                                 + ' ' + hours.get().zfill(2) + ':' + minutes.get().zfill(2),
                                 efine.get()])
                com_window.destroy()
                table_reload((xwindow, xtree))
                save_flag = False
                tkinter.messagebox.showinfo(message='Запись добавлена.')
            except Exception:
                tkinter.messagebox.showerror(message='Ошибка добавления записи.')
        elif cmnd == 'edit':
            foundx = get_number(eact_code.get())
            if foundx == -1:
                tkinter.messagebox.showerror(message='Запись с указанным ID не найдена.')
            else:
                try:
                    database[foundx] = [eact_code.get(), einitials.get(), epassport.get(), eviolation.get(),
                                        dd.get().zfill(2) + '.' + mm.get().zfill(2) + '.' + yy.get()
                                        + ' ' + hours.get().zfill(2) + ':' + minutes.get().zfill(2),
                                        efine.get()]
                    com_window.destroy()
                    table_reload((xwindow, xtree))
                    save_flag = False
                    tkinter.messagebox.showinfo(message='Запись изменена.')
                except Exception:
                    tkinter.messagebox.showerror(message='Ошибка изменения записи.')

    selector = ['append', 'edit', 'delete']
    btn_lines = ['Добавить запись', 'Изменить запись', 'Удалить запись']
    xwindow, cmnd, main_font, xtree = xarg
    btn_text = btn_lines[selector.index(cmnd)]
    com_window = tkinter.Toplevel(xwindow)
    com_window.geometry('+450+250')
    com_window.resizable(False, False)

    reg_int_val = com_window.register(int_validate)

    com_frame = tkinter.Frame(master=com_window, borderwidth=4, relief='raised')
    com_frame.grid(row=0, column=0, padx=4, pady=4, ipadx=4, ipady=4)

    act_code = tkinter.Label(master=com_frame, text='Код акта', width=22, font=main_font, anchor='w')
    act_code.grid(row=0, column=0, padx=4, pady=4)

    initials = tkinter.Label(master=com_frame, text='ФИО нарушителя', width=22, font=main_font, anchor='w')
    initials.grid(row=1, column=0, padx=4, pady=4)

    passport = tkinter.Label(master=com_frame, text='Паспортные данные', width=22, font=main_font, anchor='w')
    passport.grid(row=2, column=0, padx=4, pady=4)

    violation = tkinter.Label(master=com_frame, text='Вид нарушения', width=22, font=main_font, anchor='w')
    violation.grid(row=3, column=0, padx=4, pady=4)

    date = tkinter.Label(master=com_frame, text='Дата [ДД.ММ.ГГГГ чч:мм]', width=22, font=main_font, anchor='w')
    date.grid(row=4, column=0, padx=4, pady=4)

    fine = tkinter.Label(master=com_frame, text='Размер штрафа', width=22, font=main_font, anchor='w')
    fine.grid(row=5, column=0, padx=4, pady=4)

    eact_code = tkinter.Entry(master=com_frame, width=27, font=main_font, justify='left')
    eact_code.grid(row=0, column=1, padx=4, pady=4)

    einitials = tkinter.Entry(master=com_frame, width=27, font=main_font, justify='left')
    einitials.grid(row=1, column=1, padx=4, pady=4)

    epassport = tkinter.Entry(master=com_frame, width=27, font=main_font, justify='left')
    epassport.grid(row=2, column=1, padx=4, pady=4)

    eviolation = tkinter.Entry(master=com_frame, width=27, font=main_font, justify='left')
    eviolation.grid(row=3, column=1, padx=4, pady=4)

    edate = tkinter.Frame(master=com_frame, borderwidth=0, relief='flat')
    edate.grid(row=4, column=1, padx=4, pady=0)
    edate_left = tkinter.Frame(master=edate, borderwidth=0, relief='flat')
    edate.grid_columnconfigure(0, weight=1)
    edate_left.grid(row=0, column=0, sticky='w')
    edate_center_placeholder = tkinter.Frame(master=edate, borderwidth=0, relief='flat')
    edate_center_placeholder.grid(row=0, column=1, padx=4, pady=0)
    edate_right = tkinter.Frame(master=edate, borderwidth=0, relief='flat')
    edate.grid_columnconfigure(1, weight=1)
    edate_right.grid(row=0, column=2, sticky='e')

    dd = tkinter.Entry(master=edate_left, width=3, font=main_font)
    dd.grid(row=0, column=0, padx=0, pady=4)
    d_dot1 = tkinter.Label(master=edate_left, text='.', width=1, font=main_font, anchor='center')
    d_dot1.grid(row=0, column=1, padx=0, pady=0)
    mm = tkinter.Entry(master=edate_left, width=3, font=main_font)
    mm.grid(row=0, column=2, padx=0, pady=4)
    d_dot2 = tkinter.Label(master=edate_left, text='.', width=1, font=main_font, anchor='center')
    d_dot2.grid(row=0, column=3, padx=0, pady=0)
    yy = tkinter.Entry(master=edate_left, width=4, font=main_font)
    yy.grid(row=0, column=4, padx=0, pady=4)
    hours = tkinter.Entry(master=edate_right, width=3, font=main_font)
    hours.grid(row=0, column=0, padx=0, pady=4)
    hm_colon = tkinter.Label(master=edate_right, text=':', width=1, font=main_font, anchor='center')
    hm_colon.grid(row=0, column=1, padx=0, pady=0)
    minutes = tkinter.Entry(master=edate_right, width=3, font=main_font)
    minutes.grid(row=0, column=2, padx=0, pady=4)

    efine = tkinter.Entry(master=com_frame, width=27, font=main_font, justify='left')
    efine.grid(row=5, column=1, padx=4, pady=4)

    ed_button = tkinter.Button(master=com_window, text=btn_text, width=49, command=check_and_operate,
                               relief='raised', borderwidth=4, font=main_font)
    ed_button.grid(row=1, column=0, padx=4, pady=4)

    date_widgets = [dd, mm, yy, hours, minutes]  # Задает валидацию полям даты
    for widget in date_widgets:
        widget.config(validate='key', validatecommand=(reg_int_val, '%P'))
        widget.bind('<FocusOut>', entry_range_validate)
    efine.bind('<FocusOut>', entry_range_validate)  # Валидация поля штрафа

    if cmnd == 'append':
        widgets_to_config = [eact_code]
        com_window.title('Добавить запись')
    elif cmnd == 'delete':
        widgets_to_config = [einitials, epassport, eviolation, dd, mm, yy, hours, minutes, efine]
        com_window.title('Удалить запись')
    else:
        widgets_to_config = []
        com_window.title('Редактировать запись')
    for widget in widgets_to_config:
        widget.configure(state=tkinter.DISABLED)

    com_window.grab_set()
    com_window.focus_set()
    com_window.wait_window()
