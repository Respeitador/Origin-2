from tksheet import Sheet
import tkinter as tk
import matplotlib.pyplot as plt

class Demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
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

        self.sheet.set_options(table_bg="#34353d")

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
        # y_values = []
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
                    separate_values[f'{col}'].append(float(y_valor.replace(',', '.'))) 

        row_size = len(separate_values['1']) + 1
        # print(row_size,separate_values['1'])
        for row in range(row_size):
            if row == 0:  # First row as legend
                legendas.append(self.sheet.get_cell_data(row, 0))
            else:
                x_valor = self.sheet.get_cell_data(row, 0)
                x_values.append(float(x_valor.replace(',', '.')))
            # print(separate_values)


        # Plot values using matplotlib
        for legenda, data in zip(legendas,separate_values.values()):
                # print(data)
            if len(data) > 0:
                print(x_values,data.sort())
                plt.scatter(x_values, data, label=legenda)  # Plot x_values with y_values
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