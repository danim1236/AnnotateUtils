import os
import shutil
from tqdm import tqdm


def get_directory_path(prompt):
    path = input(prompt)
    while not os.path.isdir(path):
        print("Caminho inválido. Por favor, tente novamente.")
        path = input(prompt)
    return path


def get_save_path():
    save_path = input("Digite a pasta onde deseja salvar as imagens: ")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path


def get_interval():
    while True:
        interval_str = input("Digite o intervalo de imagens: ")
        try:
            interval = int(interval_str)
            if interval > 0:
                return interval
            else:
                print("Por favor, insira um número positivo.")
        except ValueError:
            print("Por favor, insira um número válido.")


def get_cycle_number():
    cycle_str = input("Digite o número do ciclo ou pressione Enter se for a primeira vez: ")
    if cycle_str == '':
        return 1
    try:
        cycle = int(cycle_str)
        if cycle > 0:
            return cycle
        else:
            print("Número do ciclo inválido. Usando 1.")
            return 1
    except ValueError:
        print("Entrada inválida. Usando 1.")
        return 1


def move_images(source_path, dest_path, interval, cycle_number):
    images = [f for f in sorted(os.listdir(source_path)) if os.path.isfile(os.path.join(source_path, f))]
    total_images = len(images)

    print("Movendo imagens...")
    with tqdm(total=(total_images // interval) + 1, desc="Imagens movidas") as pbar:
        for i in range(0, total_images, interval):
            src_image_path = os.path.join(source_path, images[i])
            if images[i].startswith(f"Ciclo_"):
                # Remove o prefixo de ciclo anterior se existir
                name_parts = images[i].split("_", 2)  # Dividir em 3 partes no máximo
                dest_image_name = f"Ciclo_{cycle_number:02d}_" + name_parts[-1]
            else:
                dest_image_name = f"Ciclo_{cycle_number:02d}_" + images[i]
            dest_image_path = os.path.join(dest_path, dest_image_name)
            shutil.move(src_image_path, dest_image_path)
            pbar.update(1)

    print("Process finished")


def main():
    source_path = get_directory_path("Digite o caminho do diretório de imagens: ")
    save_path = get_save_path()
    interval = get_interval()
    cycle_number = get_cycle_number()
    move_images(source_path, save_path, interval, cycle_number)


if __name__ == "__main__":
    main()
