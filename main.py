from tkinter import *
from tkinter import ttk

from tkinter.filedialog import askopenfile

import csv
from fpdf import FPDF
import os

def readCSVFile(csvFile):
  identifiers = []
  lineCount = 0
  csvReader = csv.reader(csvFile, delimiter=',')
  data = []
  for row in csvReader:
    if lineCount == 0:
      identifiers = row
    else:
      entry = {}
      for field, value in enumerate(row):
        entry[identifiers[field]] = value
      data.append(entry)
    lineCount += 1
  return data

def generatePDFFromCSV(csvFile):
  if csvFile is None:
    return
  data = readCSVFile(csvFile)
  pdf = FPDF('P', 'mm', [152,102])
  for line in data[1::]:
    pdf.add_page()
    pdf.set_font('arial', 'B', 12)
    pdf.cell(0, 5, txt="Afzender", ln=1, align='L')
    pdf.set_font('arial', '', 12)
    pdf.cell(0, 5, txt=data[0]['company'], ln=2, align='L')
    pdf.cell(0, 5, txt=data[0]['street'], ln=3, align='L')
    pdf.cell(0, 5, txt="{} {}".format(data[0]["postal"], data[0]["city"]), ln=4, align='L')

    pdf.rect(30, 40.2, 112, 50)
    startY = 45 if line["company"] == "" else 50
    increment = 5
    pdf.text(35, startY, line["company"])
    pdf.text(35, startY + increment, line["name"])
    pdf.text(35, startY + 2 * increment, line["street"])
    pdf.text(35, startY + 3 * increment, "{} {}".format(line["postal"], line["city"]))
  pdf.output("labels.pdf")
  os.startfile("labels.pdf")


def addLabels():
  ttk.Label(frm, text="Select address CSV: ", anchor='w').grid(column=0, row=1)
  ttk.Label(frm, text="First entry in CSV file will be entered as the sender", anchor='w').grid(column=0, row=0)
  ttk.Label(frm, text="Expected CSV fields: \n-company\n-name\n-street\n-postal\n-city", anchor='w').grid(column=0, row=3)

def addButtons():
  ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=5)
  ttk.Button(frm, text="select file", command=lambda:open_file()).grid(column=1, row=1)

def open_file():
  global file
  tmpFile = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
  if tmpFile is None:
    ttk.Label(frm, text="Error, no file found").grid(column=0, row=2)
  else:
    file = tmpFile
    ttk.Button(frm, text="Create PDF", command=lambda:generatePDFFromCSV(file)).grid(column=1, row=5)

def main():
  global root
  global frm

  root = Tk("Shipping label generator")
  frm = ttk.Frame(root, padding=10)
  frm.grid()

  addLabels()
  addButtons()

  root.mainloop()

if __name__ == "__main__":
  main()