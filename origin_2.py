# Python3

# Este programa abre uma planilha em que é possivel selecionar valores para plotar um gráfico de scatter
# em que a coluna 1 é sempre o eixo X e a linha 1 é a legenda das colunas. Juntamente, faz uma análise
# estatística de linnear fit, da o valor de slope das linhas e com esse valor, calcula o valor de
# Ácido Hexurônico nas amostras utilizadas para plotar o gráfico.

from tksheet import Sheet
import tkinter as tk
import matplotlib.pyplot as plt
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

        self.sheet.set_options(table_bg="#82C294")

        # Add a button to trigger plotting
        self.plot_button = tk.Button(self, text="Plotar Selecionados", command=self.plot_selected)
        self.plot_button.grid(row=1, column=0, sticky="ew")

    def plot_selected(self):
        # Get selected cells
        selected_cells = self.sheet.get_selected_cells(sort_by_column=True)
        if not selected_cells:
            return  # No selection, do nothing

        # Get data from selected cells
        x_values = []
        legendas = []
        separate_values = {}

        for row, col in selected_cells:
            if str(col) not in separate_values.keys():
                separate_values[f'{col}'] = []
            if row == 0:  # First row as legend
                legendas.append(self.sheet.get_cell_data(row, col))
            else:
                y_valor = self.sheet.get_cell_data(row, col)
                if str(col) in separate_values.keys():
                    try:
                        separate_values[f'{col}'].append(float(y_valor.replace(',', '.')))
                    except:
                        # separate_values[f'{col}'].append(y_valor)
                        None

        row_size = len(separate_values['1']) + 1
        for row in range(row_size):
            if row == 0:  # First row as legend
                legendas.append(self.sheet.get_cell_data(row, 0))
            else:
                x_valor = self.sheet.get_cell_data(row, 0)
                x_values.append(float(x_valor.replace(',', '.')))
            # print(separate_values)
        x_vectorized = np.array(x_values)[:,np.newaxis]

        # Plot values using matplotlib
        for legenda, data in zip(legendas,separate_values.values()):
                # print(data)
            if len(data) > 0:
                data = sorted(data)
                slope, _, _, _ = np.linalg.lstsq(x_vectorized, data)
                print(f'Slope for {legenda} is {slope}')
                plt.plot(x_vectorized, slope*x_vectorized)
                plt.scatter(x_values, data, label=legenda)
                  # Plot x_values with y_values
        # plt.xticks(x_values, rotation=45)  # Rotate X axis labels
        # plt.yticks(y_values)  # Add Y axis labels
        plt.xlabel("Eixo X")
        plt.ylabel("Eixo Y")
        plt.title("Valores Selecionados")
        plt.legend()  # Add legend with Y axis names
        plt.show()
        # else:
        #     print("Selecione células válidas para plotar")

app = Demo()
app.mainloop()
