#!/usr/bin/python3

from tkinter import Tk, Label, Entry, Button
from sqlite3 import connect

global table_label, tables, file_location_entry, sql_entry
table_label, tables, file_location_entry, sql_entry = {}, [], None, None

def root_setup():
    root.title('db viewer')
    try:
        root.iconbitmap('icon.icns')
    except Exception as e:
        print(e)
    root.geometry('854x480+0+0')
    root.maxsize(width = 1280, height = 720)
    root.minsize(width = 256, height = 144)
    root.config(bg = '#E2A8FD')
    root.attributes('-alpha', 0.75)
    root.attributes('-topmost', 0)

def labels_setup():
    file_location_label = Label(text = 'File Location:', bg = '#E2A8FD', fg = '#1975D1')
    file_location_label.grid(row = 0, column = 0)
    sql_label = Label(text = 'SQL:', bg = '#E2A8FD', fg = '#1975D1')
    sql_label.grid(row = 1, column = 0)

def entries_setup():
    global file_location_entry, sql_entry
    file_location_entry = Entry(text = 'C:⧵Users⧵user⧵Documents⧵file.db', bg = '#F3D8FF', fg = '#99004D')
    file_location_entry.grid(row = 0, column = 1)
    sql_entry = Entry(text = 'SELECT * FROM TABLE', bg = '#F3D8FF', fg = '#99004D')
    sql_entry.grid(row = 1, column = 1)


def run():
    def running_sql(sql):
        global table_label, tables
        try:
            conn = connect(file_location)
            c = conn.cursor()
            rows = c.execute(sql)
            table_label = {}
            tables = []
            names = list(map(lambda x: x[0], rows.description))
            y = 0
            for name in names:
                table_label[name] = [Label(text = name, bg = '#E2A8FD')]
                table_label[name][0].grid(row = 2, column = y)
                y += 1
            x = 3
            print(table_label)
            for row in rows:
                y = 0
                i = 0
                for column in table_label:
                    table_label[column].append(Label(text = row[i], bg = '#E2A8FD'))
                    table_label[column][len(table_label[column]) - 1].grid(row = x, column = y)
                    y += 1
                    i += 1
                x += 1
            conn.close()
        except Exception as e:
            print(e)
    def show_all_tables():
        global table_label, tables
        try:
            conn = connect(file_location)
            c = conn.cursor()
            tables = c.execute('SELECT name from sqlite_master where type = "table"').fetchall()
            table_label = {}
            for i in range(len(tables)):
                tables[i] = Label(text = tables[i][0], bg = '#E2A8FD')
                tables[i].grid(row = i + 2, column = 0)
            conn.close()
        except Exception as e:
            print(e)
    global table_label, tables
    file_location = file_location_entry.get()
    sql = sql_entry.get()
    print(file_location, sql)
    if sql[:6].upper() == 'SELECT' or sql == '.tables' or sql == '.tab':
        for column_name in table_label:
            for label in table_label[column_name]:
                label.destroy()
        for table in tables:
            table.destroy()
        if sql[:6].upper() == 'SELECT':
            running_sql(sql)
        elif sql == '.tables' or sql == '.tab':
            show_all_tables()

root = Tk()

root_setup()

labels_setup()

entries_setup()

run_button = Button(text = 'Run', bg = "#FF00FF", width = 2, height = 1, command = run)
run_button.grid(row = 0, column = 2, rowspan = 2)

root.mainloop()