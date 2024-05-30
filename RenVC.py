import os
import shutil
from tqdm import tqdm


def get_directory_path():
    path = input("Digite o caminho do diretório com as imagens e anotações: ")
    while not os.path.isdir(path):
        print("Caminho inválido. Por favor, tente novamente.")
        path = input("Digite o caminho do diretório com as imagens e anotações: ")
    return path


def check_annotations(directory_path):
    images = [f for f in sorted(os.listdir(directory_path)) if f.endswith(('.png', '.jpg', '.jpeg'))]
    for image in images:
        annotation = os.path.splitext(image)[0] + '.txt'
        if not os.path.isfile(os.path.join(directory_path, annotation)):
            print("ANOTE AS IMAGENS PRIMEIRO")
            return False
    return True


def check_divisibility(directory_path):
    images = [f for f in sorted(os.listdir(directory_path)) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if len(images) % 3 != 0:
        print("É NECESSÁRIO 1/3 DE IMAGENS DE VALIDAÇÃO")
        return False
    return True


def get_phase():
    return input("Qual a fase? ")


def get_name():
    return input("Qual o nome (6 caracteres)? ")


def get_size():
    while True:
        size = input("É um recorte (s/n)? ")
        if size in ['s', 'n']:
            return 'ROI' if size == 's' else 'FSC'
        print("Entrada inválida. Digite 's' ou 'n'.")


def get_camera():
    return input("Qual a câmera? ")


def get_version():
    return input("Qual a versão? ")


def organize_files(directory_path, phase, name, size, camera, version):
    images = [f for f in sorted(os.listdir(directory_path)) if f.endswith(('.png', '.jpg', '.jpeg'))]
    annotations = [os.path.splitext(f)[0] + '.txt' for f in images]

    train_path = os.path.join(directory_path, 'train')
    val_path = os.path.join(directory_path, 'val')
    os.makedirs(os.path.join(train_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(train_path, 'labels'), exist_ok=True)
    os.makedirs(os.path.join(val_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(val_path, 'labels'), exist_ok=True)

    train_images = []
    train_labels = []
    val_images = []
    val_labels = []

    for i, (image, annotation) in enumerate(zip(images, annotations)):
        if (i + 1) % 3 == 0:
            val_images.append(image)
            val_labels.append(annotation)
        else:
            train_images.append(image)
            train_labels.append(annotation)

    print("Movendo e renomeando arquivos de treino...")
    with tqdm(total=len(train_images), desc="Treinamento") as pbar:
        for i, (image, annotation) in enumerate(zip(train_images, train_labels)):
            new_name = f"T_F{phase}_{name}_{size}_CAM{camera}_V{version}_{i + 1:05d}"
            image_extension = os.path.splitext(image)[1]
            new_image_name = new_name + image_extension
            new_annotation_name = new_name + '.txt'

            shutil.move(os.path.join(directory_path, image), os.path.join(train_path, 'images', new_image_name))
            shutil.move(os.path.join(directory_path, annotation),
                        os.path.join(train_path, 'labels', new_annotation_name))
            pbar.update(1)

    print("Movendo e renomeando arquivos de validação...")
    with tqdm(total=len(val_images), desc="Validação") as pbar:
        for i, (image, annotation) in enumerate(zip(val_images, val_labels)):
            new_name = f"V_F{phase}_{name}_{size}_CAM{camera}_V{version}_{i + 1:05d}"
            image_extension = os.path.splitext(image)[1]
            new_image_name = new_name + image_extension
            new_annotation_name = new_name + '.txt'

            shutil.move(os.path.join(directory_path, image), os.path.join(val_path, 'images', new_image_name))
            shutil.move(os.path.join(directory_path, annotation), os.path.join(val_path, 'labels', new_annotation_name))
            pbar.update(1)

    print("Process finished")


def main():
    directory_path = get_directory_path()

    if not check_annotations(directory_path):
        return
    if not check_divisibility(directory_path):
        return

    phase = get_phase()
    name = get_name()
    size = get_size()
    camera = get_camera()
    version = get_version()

    organize_files(directory_path, phase, name, size, camera, version)


if __name__ == "__main__":
    main()
