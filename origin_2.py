# Python3

# This program opens a sheet in which is possible to select values to plot a scatter graph where the
# column 1 is always the X axis and line 1 is the names of the columns. Along with that, it does statistical
# analysis in linear fit and gives the slope values for those fits and with that value, calculate the
# HexUÁc for the heparin used.

# Este programa abre uma planilha em que é possível selecionar valores para plotar um gráfico de scatter
# em que a coluna 1 é sempre o eixo X e a linha 1 é a legenda das colunas. Juntamente, faz uma análise
# estatística de linear fit, da o valor de slope das linhas e com esse valor, calcula o valor de
# Ácido Hexurônico nas amostras utilizadas para plotar o gráfico.

from tksheet import Sheet
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry(f"{1100}x{350}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.sheet = Sheet(self.frame,
                           data=[[f"" for c in range(10)] for r in range(10)])
        self.sheet.enable_bindings()
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.sheet.grid(row=0, column=0, sticky="nswe")

        self.sheet.set_options(table_bg="#82C294") # trocar hexadecimal
        for row in range(2):
            for column in range(10):
                if column == 10:
                    row =+ 1
                    column = 0
                self.sheet.highlight_cells(row, column, bg="#e9a6ff")
                column =+ 1

        # Create a figure and canvas for the plot
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=2, sticky="nswe")

        # Add a button to trigger plotting
        self.plot_button = tk.Button(self, text="Plotar Selecionados", command=self.plot_selected)
        self.plot_button.grid(row=1, column=0, sticky="ew")

    def plot_selected(self):
        # Get selected cells
        selected_cells = self.sheet.get_selected_cells(sort_by_column=True)
        if not selected_cells:
            return  # No selection, do nothing

        # Get data from selected cells
        legendas = []
        dataSets = {}

        for row, col in selected_cells:
            if str(col) not in dataSets.keys():
                dataSets[f'{col}'] = [[],[]]
            if row == 0:  # First row as legend
                legendas.append(self.sheet.get_cell_data(row, col))
            elif self.sheet.get_cell_data(row, col) != '':
                    y_valor = self.sheet.get_cell_data(row, col)
                    x_valor = self.sheet.get_cell_data(row, 0)
                    if str(col) in dataSets.keys():
                        try:
                            dataSets[f'{col}'][1].append(float(y_valor.replace(',', '.')))
                            dataSets[f'{col}'][0].append(float(x_valor.replace(',', '.')))
                        except:
                            None

        # Plot values using matplotlib
        self.ax.clear()  # Clear the previous plot
        for legenda, dataSet in zip(legendas, dataSets.values()):
            xData = dataSet[0]
            x_vectorized = np.array(dataSet[0])[:,np.newaxis]
            yData = dataSet[1]
            slope, _, _, _ = np.linalg.lstsq(x_vectorized, yData)
            self.ax.plot(x_vectorized, slope*x_vectorized)
            self.ax.scatter(xData, yData, label=f'{legenda} / slope = {slope[0]:.5f}')
        self.ax.set_xlabel("Volume uL")
        self.ax.set_ylabel("Eixo Y")
        self.ax.set_title("Valores Selecionados")
        self.ax.legend()  # Add legend with Y axis names
        self.canvas.draw()  # Update the canvas

app = Demo()
app.mainloop()