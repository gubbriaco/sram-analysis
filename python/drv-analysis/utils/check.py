import os


def check_file(file_path: str) -> None:
    """
    Verifica l'esistenza di un file e stampa un messaggio appropriato.

    :param file_path: Percorso del file da verificare.
    :return: None
    :raises FileNotFoundError: Se il file specificato non esiste.
    :raises Exception: Se si verifica un errore durante l'apertura del file.
    """
    try:
        with open(file_path, "r"):
            print(f"File opened successfully: {file_path}", end="\n", flush=True)
    except FileNotFoundError:
        print(f"File not found: {file_path}", end="\n")
        raise
    except Exception as e:
        print(f"Error detected: {str(e)}", end="\n")
        raise


def check_image(image_path: str) -> None:
    """
    Verifica l'esistenza di un'immagine, stampa un messaggio appropriato e aggiorna o crea il file se necessario.

    :param image_path: Percorso dell'immagine da verificare o creare.
    :return: None
    :raises Exception: Se si verifica un errore durante l'aggiornamento o la creazione del file.
    """
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
            print(f"File updated successfully: {image_path}", end="\n", flush=True)
        except Exception as e:
            print(f"Error deleting file: {str(e)}", end="\n")
            raise
    else:
        print(f"File not found: {image_path}", end="\n")
        try:
            open(image_path, 'w').close()
            print(f"File created successfully: {image_path}", end="\n", flush=True)
        except Exception as e:
            print(f"Error creating file: {str(e)}", end="\n")
            raise
