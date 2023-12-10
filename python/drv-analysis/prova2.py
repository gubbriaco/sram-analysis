import matplotlib.pyplot as plt
import pandas as pd

# Dati di esempio
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'San Francisco', 'London', 'Tokyo']
}

# Creazione di un DataFrame da un dizionario
df = pd.DataFrame(data)

# Creazione della tabella grafica utilizzando matplotlib
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('off')  # Nascondi gli assi

# Creazione della tabella con la prima riga evidenziata e in grassetto
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='upper center',
                 cellColours=[['#e0e0e0'] * len(df.columns)] + [['#f0f0f0']*len(df.columns)] * (len(df) - 1))

# Imposta lo stile della tabella
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

# Imposta il testo in grassetto per la prima riga
for (i, j), cell in table.get_celld().items():
    if i == 0:
        cell.set_text_props(fontweight='bold')

# Mostra il grafico con la tabella
plt.show()
