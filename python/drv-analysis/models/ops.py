from utils.check import check_file, check_image
from PyLTSpice import RawRead, SpiceEditor
from IPython.display import Image, display
from matplotlib import pyplot


def load_asc(asc_file_path: str, schematic_image_path: str) -> SpiceEditor:
    """
    Carica un file .asc (netlist SPICE) e mostra l'immagine dello schema corrispondente.

    :param asc_file_path: Percorso del file .asc contenente il netlist SPICE.
    :param schematic_image_path: Percorso dell'immagine dello schema da visualizzare.
    :return: Un oggetto SpiceEditor rappresentante il netlist caricato.
    """

    # Verifica che il file .asc esista
    check_file(asc_file_path)

    # Carica il netlist SPICE dal file .asc
    netlist = SpiceEditor(asc_file_path)

    # Visualizza l'immagine dello schema
    display(Image(schematic_image_path))

    # Restituisci l'oggetto SpiceEditor contenente la netlist
    return netlist


def load_ltr(raw_file_path: str) -> RawRead:
    """
    Carica un file .raw contenente dati di simulazione LTspice.

    :param raw_file_path: Percorso del file .raw contenente i dati di simulazione LTspice.
    :return: Un oggetto RawRead rappresentante i dati caricati dalla simulazione LTspice.
    """

    # Verifica che il file .raw esista
    check_file(raw_file_path)

    # Carica i dati dalla simulazione LTspice dal file .raw
    ltr = RawRead(raw_file_path)

    # Restituisci l'oggetto RawRead contenente i dati di simulazione
    return ltr


def save_image(image_path: str, plt: pyplot) -> None:
    """
    Salva un'immagine utilizzando il percorso specificato e un oggetto pyplot di matplotlib.

    :param image_path: Percorso in cui salvare l'immagine.
    :param plt: Oggetto pyplot di matplotlib contenente l'immagine da salvare.
    :return: None
    """

    # Verifica che il percorso e l'immagine siano validi
    check_image(image_path)

    # Salva l'immagine utilizzando l'oggetto pyplot
    plt.savefig(image_path)
