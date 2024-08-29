# C4mBruH4ck

# RTSP Scanner

This script allows you to scan domains and their subdomains to check the availability of RTSP streams using provided usernames and passwords. It uses Sublist3r to find subdomains and `ffmpeg` to check RTSP streams.

## Requirements

Before running the script, make sure you have the following tools installed:

- **Sublist3r**: A tool for subdomain enumeration.
- **ffmpeg**: A tool for handling video and audio streams.
- **dig**: A utility for DNS queries.

### Installing Sublist3r

1. Clone the Sublist3r repository:

```bash
git clone https://github.com/aboul3la/Sublist3r.git

Navigate to the Sublist3r directory:

bash

cd Sublist3r

Install the required dependencies:

bash

pip install -r requirements.txt

Verify that the tool is working by running:

bash

python sublist3r.py -h

Installing ffmpeg

Install ffmpeg using your package manager. For example, on Debian-based systems:

bash

sudo apt-get install ffmpeg

Installing dig

dig is usually included in the dnsutils package. Install it with:

bash

sudo apt-get install dnsutils

Configuration
Ensure that the path to the Sublist3r utility is correctly specified in the script. By default, it is set 
/home/s3r4ph1/Desktop/MeProScripts/Scripts/C4mBruH4ck/Sublist3r/sublist3r.
Prepare the login and password lists:
users.txt: A file containing a list of usernames (one per line).
passwords.txt: A file containing a list of passwords (one per line).

Running the Script

To run the script, use the following command:
python C4mBruH4ck.py <domain> <user_file> <pass_file> [--sublist3r_path <path_to_Sublist3r>] [--max_workers <number_of_threads>] [--timeout <timeout_seconds>]

Examples

    Scanning the domain example.com with usernames and passwords listed in users.txt and passwords.txt, respectively:
python C4mBruH4ck.py target.com users.txt passwords.txt


Specifying a custom path to Sublist3r and setting the number of threads and timeout:
python C4mBruH4ck.py target.com users.txt passwords.txt --sublist3r_path /path/to/Sublist3r/sublist3r --max_workers 20 --timeout 60



Command-Line Options

    --sublist3r_path <path_to_Sublist3r>: Path to the Sublist3r executable. Default is /home/s3r4ph1/Desktop/MeProScripts/Scripts/C4mBruH4ck/Sublist3r/sublist3r.
    --max_workers <number_of_threads>: Maximum number of threads for brute-forcing. Default is 10.
    --timeout <timeout_seconds>: Timeout for connecting to the RTSP stream in seconds. Default is 30.



# RTSP Scanner

Этот скрипт позволяет сканировать домены и их поддомены для проверки доступности RTSP потоков с использованием логинов и паролей. Он использует утилиту Sublist3r для поиска поддоменов и `ffmpeg` для проверки RTSP потоков.

## Требования

Перед запуском скрипта убедитесь, что у вас установлены следующие утилиты:

- **Sublist3r**: Инструмент для поиска поддоменов.
- **ffmpeg**: Утилита для работы с видео и аудио потоками.
- **dig**: Утилита для DNS-запросов.

### Установка Sublist3r

1. Клонируйте репозиторий Sublist3r:

   ```bash

git clone https://github.com/aboul3la/Sublist3r.git

Перейдите в директорию Sublist3r:

bash

cd Sublist3r

Установите необходимые зависимости:

bash

pip install -r requirements.txt

Проверьте, что утилита работает, запустив:

bash

python sublist3r.py -h

Установка ffmpeg

Установите ffmpeg с помощью вашего менеджера пакетов. Например, на Debian-based системах используйте:

bash

sudo apt-get install ffmpeg

Установка dig

dig обычно входит в пакет dnsutils. Установите его с помощью:

bash

sudo apt-get install dnsutils

Настройка

    Убедитесь, что путь к утилите Sublist3r указан верно в скрипте. По умолчанию он установлен на /home/s3r4ph1/Desktop/MeProScripts/Scripts/C4mBruH4ck/Sublist3r/sublist3r.

    Подготовьте файлы со списками логинов и паролей:
        users.txt: Файл, содержащий список логинов (по одному на строку).
        passwords.txt: Файл, содержащий список паролей (по одному на строку).

Запуск скрипта

Для запуска скрипта используйте следующую команду:

bash

python C4mBruH4ck.py <домен> <файл_с_логинами> <файл_с_паролями> [--sublist3r_path <путь_к_Sublist3r>] [--max_workers <количество_потоков>] [--timeout <время_ожидания>]

Примеры

    Сканирование домена example.com с логинами и паролями, расположенными в users.txt и passwords.txt соответственно:

    bash

python C4mBruH4ck.py target.com users.txt passwords.txt

Указание нестандартного пути к Sublist3r, а также настройка количества потоков и времени ожидания:

bash

python C4mBruH4ck.py target.com users.txt passwords.txt --sublist3r_path /path/to/Sublist3r/sublist3r --max_workers 20 --timeout 60


