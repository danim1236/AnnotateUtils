import os
from tqdm import tqdm


def get_directory_path():
    path = input("Digite o caminho do diretório de arquivos para renomear: ")
    while not os.path.isdir(path):
        print("Caminho inválido. Por favor, tente novamente.")
        path = input("Digite o caminho do diretório de arquivos para renomear: ")
    return path


def get_prefix():
    return input("Digite o prefixo para renomear: ")


def rename_files(directory_path, prefix):
    files = [f for f in sorted(os.listdir(directory_path)) if os.path.isfile(os.path.join(directory_path, f))]
    total_files = len(files)

    print("Renomeando arquivos...")
    with tqdm(total=total_files, desc="Arquivos renomeados") as pbar:
        for i, filename in enumerate(files):
            file_extension = os.path.splitext(filename)[1]
            new_name = f"{prefix}_{i + 1:05d}{file_extension}"
            src_file_path = os.path.join(directory_path, filename)
            dest_file_path = os.path.join(directory_path, new_name)
            os.rename(src_file_path, dest_file_path)
            pbar.update(1)

    print("Process finished")


def main():
    directory_path = get_directory_path()
    prefix = get_prefix()
    rename_files(directory_path, prefix)


if __name__ == "__main__":
    main()
