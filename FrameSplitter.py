import cv2
import os
from tqdm import tqdm


def get_video_path():
    video_path = input("Digite o caminho do vídeo: ")
    while not os.path.isfile(video_path):
        print("Caminho do vídeo inválido. Por favor, tente novamente.")
        video_path = input("Digite o caminho do vídeo: ")
    return video_path


def get_save_path():
    save_path = input("Digite a pasta onde deseja salvar os frames: ")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path


def get_frame_interval():
    while True:
        interval_str = input("Digite o intervalo de frames: ")
        try:
            interval = int(interval_str)
            if interval > 0:
                return interval
            else:
                print("Por favor, insira um número positivo.")
        except ValueError:
            print("Por favor, insira um número válido.")


def extract_frames(video_path, save_path, interval):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    pbar = tqdm(total=total_frames, desc="Extraindo frames")

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval == 0:
            frame_filename = os.path.join(save_path, f"{video_name}_{saved_count:05d}.png")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
        frame_count += 1
        pbar.update(1)

    cap.release()
    pbar.close()
    print("Process finished")


def main():
    video_path = get_video_path()
    save_path = get_save_path()
    interval = get_frame_interval()
    extract_frames(video_path, save_path, interval)


if __name__ == "__main__":
    main()
