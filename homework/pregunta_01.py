# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
from pathlib import Path
import shutil
import pandas as pd
from glob import glob
import fileinput
import zipfile

def _create_output_directory(output_directory):
    output_path = Path(output_directory)
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

def _save_output(output_directory, filename, df):
    output_path = Path("files") / output_directory
    output_path.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path / f"{filename}.csv", index=False)

def pregunta_01():
    zip_path = Path("files/input.zip")
    input_dir = Path("files/input")

    # Asegurarse de que el directorio de entrada esté vacío
    _create_output_directory(input_dir)

    # Extraer archivos directamente en `files/input` sin crear subcarpetas
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            zip_ref.extract(file, input_dir)
    
    # Cargar y procesar datos
    seq = []
    files = glob(f"{input_dir}/**/*.txt", recursive=True)
    with fileinput.input(files=files) as f:
        for line in f:
            seq.append((f.filename(), line.strip()))

    train_data, test_data = [], []
    for k, v in seq:
        target = (
            "neutral"
            if "neutral" in k
            else "negative" if "negative" in k else "positive"
        )
        data = {"phrase": v, "target": target}
        if "train" in k:
            train_data.append(data)
        else:
            test_data.append(data)

    train_dataset = pd.DataFrame(train_data)
    test_dataset = pd.DataFrame(test_data)

    # Crear directorio de salida y guardar los datasets
    _create_output_directory("files/output")
    _save_output("output", "train_dataset", train_dataset)
    _save_output("output", "test_dataset", test_dataset)

    return 1

pregunta_01()