import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from time import sleep
import platform
import random
import hashlib

def auto_install_libs():
    libs = ['rich', 'colorama']
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            print(f"[*] Установка {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

auto_install_libs()

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import box
from rich.live import Live
from rich.layout import Layout
from rich.progress import Progress, BarColumn, TextColumn
from colorama import init, Fore, Back, Style
import math

init(autoreset=True)
console = Console()

DATA_FILE = 'clients_data.json'
PROMO_FILE = 'promotions.json'

COMPANY_NAME = "DIM & DAN HOMES"
COMPANY_TAGLINE = "уют в каждом доме"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_ansi(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def smooth_gradient(text, start_color, end_color):
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    result = ""
    length = len(text)

    for i, char in enumerate(text):
        if char == ' ':
            result += ' '
            continue
        t = i / length if length > 0 else 0
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b_val = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        result += f'\033[38;2;{r};{g};{b_val}m{char}'

    result += '\033[0m'
    return result

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_header():
    clear_screen()

    logo_lines = [
        "██████╗ ██╗███╗   ███╗     ██████╗  █████╗ ███╗   ██╗    ██╗  ██╗ ██████╗ ███╗   ███╗███████╗███████╗",
        "██╔══██╗██║████╗ ████║    ██╔════╝ ██╔══██╗████╗  ██║    ██║  ██║██╔═══██╗████╗ ████║██╔════╝██╔════╝",
        "██║  ██║██║██╔████╔██║    ██║  ███╗███████║██╔██╗ ██║    ███████║██║   ██║██╔████╔██║█████╗  ███████╗",
        "██║  ██║██║██║╚██╔╝██║    ██║   ██║██╔══██║██║╚██╗██║    ██╔══██║██║   ██║██║╚██╔╝██║██╔══╝  ╚════██║",
        "██████╔╝██║██║ ╚═╝ ██║    ╚██████╔╝██║  ██║██║ ╚████║    ██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗███████║",
        "╚═════╝ ╚═╝╚═╝     ╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝"
    ]

    for line in logo_lines:
        print(smooth_gradient(line, "#00ff88", "#00d4ff"))

    print()
    title = f"✦ {COMPANY_NAME} ✦"
    print(" " * (50 - len(title)//2) + smooth_gradient(title, "#ff6b6b", "#ffd93d"))
    print(" " * (55 - len(COMPANY_TAGLINE)//2) + smooth_gradient(COMPANY_TAGLINE, "#6c5ce7", "#a8e6cf"))
    print()
    print(smooth_gradient("═" * 70, "#00d4ff", "#00ff88"))
    print()

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"clients": [], "last_id": 0, "referral_stats": {"total_referrals": 0, "total_bonus_given": 0}}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_promotions():
    default_promotions = {
        "active_promotions": [
            {"id": 1, "name": "Новогодняя сказка", "bonus": 500, "code": "NEWYEAR2025", "desc": "+500 бонусов"},
            {"id": 2, "name": "Приведи друга", "bonus": 300, "code": "FRIEND300", "desc": "+300 за реферала"},
            {"id": 3, "name": "Именинник", "multiplier": 2, "type": "birthday", "desc": "x2 бонусы"},
            {"id": 4, "name": "Первый заказ", "bonus": 200, "type": "first", "desc": "+200 бонусов"},
            {"id": 5, "name": "Черная пятница", "multiplier": 3, "code": "BLACK2025", "desc": "x3 бонусы"},
            {"id": 6, "name": "VIP статус", "bonus": 1000, "min_total": 50000, "discount": 15, "desc": "+1000 бонусов + скидка 15%"},
            {"id": 7, "name": "Добро пожаловать", "bonus": 100, "discount": 10, "code": "WELCOME100", "desc": "+100 бонусов + скидка 10%"},
            {"id": 8, "name": "Крупная покупка", "bonus": 500, "min_purchase": 5000, "desc": "+500 бонусов"},
            {"id": 9, "name": "Счастливый час", "bonus": 50, "daily": True, "desc": "+50 бонусов ежедневно"},
            {"id": 10, "name": "Серебряный статус", "bonus": 500, "min_total": 25000, "discount": 7, "desc": "+500 бонусов + скидка 7%"},
        ],
        "used_codes": []
    }
    try:
        with open(PROMO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        with open(PROMO_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_promotions, f, ensure_ascii=False, indent=4)
        return default_promotions

def generate_referral_code(client_id, name):
    return hashlib.md5(f"{name}{client_id}{random.randint(100,999)}".encode()).hexdigest()[:8].upper()

def add_client():
    print(smooth_gradient("✦ РЕГИСТРАЦИЯ НОВОГО КЛИЕНТА ✦", "#00ff88", "#00d4ff"))
    print()

    data = load_data()

    name = input(smooth_gradient("  имя > ", "#6c5ce7", "#a8e6cf"))
    phone = input(smooth_gradient("  телефон > ", "#6c5ce7", "#a8e6cf"))
    email = input(smooth_gradient("  email > ", "#6c5ce7", "#a8e6cf"))
    address = input(smooth_gradient("  адрес > ", "#6c5ce7", "#a8e6cf"))
    birthday = input(smooth_gradient("  день рождения (ДД-ММ-ГГГГ) > ", "#6c5ce7", "#a8e6cf"))
    referrer_code = input(smooth_gradient("  реферальный код (если есть) > ", "#ffd93d", "#ff6b6b"))

    client = {
        'id': data['last_id'] + 1,
        'name': name,
        'phone': phone,
        'email': email,
        'address': address,
        'birth_date': birthday,
        'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'notes': input(smooth_gradient("  заметки > ", "#6c5ce7", "#a8e6cf")),
        'status': 'active',
        'total_purchases': 0,
        'loyalty_points': 100,
        'referral_code': "",
        'referred_by': None,
        'referrals': [],
        'bonus_history': [{'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'amount': 100, 'reason': 'Приветственный бонус'}],
        'used_codes': [],
        'first_purchase': False,
        'last_daily': None,
        'vip_status': False,
        'silver_status': False,
        'orders_count': 0
    }

    client['referral_code'] = generate_referral_code(client['id'], name)

    if referrer_code:
        for existing in data['clients']:
            if existing.get('referral_code') == referrer_code:
                client['referred_by'] = existing['id']
                existing['loyalty_points'] += 300
                existing['referrals'].append(client['id'])
                existing['bonus_history'].append({
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'amount': 300,
                    'reason': f'Реферал: {name}'
                })
                data['referral_stats']['total_referrals'] += 1
                data['referral_stats']['total_bonus_given'] += 300
                print()
                print(smooth_gradient(f"  → пригласивший получил +300 бонусов!", "#00ff88", "#00ff88"))
                break

    data['clients'].append(client)
    data['last_id'] = client['id']
    save_data(data)

    print()
    print(smooth_gradient(f"  ✓ клиент {name} зарегистрирован", "#00ff88", "#00ff88"))
    print(smooth_gradient(f"  ✓ ваш реферальный код: {client['referral_code']}", "#00d4ff", "#00d4ff"))
    print(smooth_gradient(f"  ✓ получено 100 приветственных бонусов", "#ffd93d", "#ffd93d"))
    sleep(2.5)

def list_clients():
    data = load_data()
    if not data['clients']:
        print(smooth_gradient("  нет клиентов", "#ff6b6b", "#ff6b6b"))
        input()
        return

    print(smooth_gradient("✦ СПИСОК КЛИЕНТОВ ✦", "#00ff88", "#00d4ff"))
    print()

    for client in data['clients']:
        status_color = "#00ff88" if client['status'] == 'active' else "#ff6b6b"
        print(smooth_gradient(f"  #{client['id']} {client['name']}", "#00d4ff", "#6c5ce7"))
        print(f"    тел: {client['phone']}")
        print(f"    почта: {client['email']}")
        print(f"    бонусов: {client['loyalty_points']}")
        print(f"    покупок: {client['total_purchases']:,} ₽")
        print(f"    рефералов: {len(client.get('referrals', []))}")
        print(smooth_gradient(f"    статус: {client['status']}", status_color, status_color))
        print()

    input(smooth_gradient("  нажмите enter", "#6c5ce7", "#a8e6cf"))

def add_purchase():
    print(smooth_gradient("✦ ОФОРМЛЕНИЕ ПОКУПКИ ✦", "#00ff88", "#00d4ff"))
    print()

    client_id = input(smooth_gradient("  id клиента > ", "#ffd93d", "#ff6b6b"))
    if not client_id.isdigit():
        print(smooth_gradient("  ошибка", "#ff6b6b", "#ff6b6b"))
        sleep(1.5)
        return

    data = load_data()
    promos = load_promotions()
    idx = None

    for i, c in enumerate(data['clients']):
        if c['id'] == int(client_id):
            idx = i
            break

    if idx is None:
        print(smooth_gradient("  клиент не найден", "#ff6b6b", "#ff6b6b"))
        sleep(1.5)
        return

    client = data['clients'][idx]

    print()
    print(smooth_gradient(f"  клиент: {client['name']}", "#00d4ff", "#00d4ff"))
    print(smooth_gradient(f"  баланс бонусов: {client['loyalty_points']}", "#ffd93d", "#ffd93d"))

    amount = input(smooth_gradient("  сумма покупки > ", "#6c5ce7", "#a8e6cf"))
    if not amount.isdigit():
        print(smooth_gradient("  ошибка", "#ff6b6b", "#ff6b6b"))
        sleep(1.5)
        return

    amount = int(amount)

    use_bonus = input(smooth_gradient("  списать бонусы? (y/n) > ", "#6c5ce7", "#a8e6cf")).lower()

    bonus_discount = 0
    if use_bonus == 'y' and client['loyalty_points'] > 0:
        points_to_use = min(client['loyalty_points'], amount)
        bonus_discount = points_to_use
        amount -= bonus_discount
        client['loyalty_points'] -= points_to_use
        print(smooth_gradient(f"  → списано {points_to_use} бонусов", "#00ff88", "#00ff88"))

    client['total_purchases'] += amount
    client['orders_count'] += 1

    base_points = amount // 100

    birthday_multiplier = 1
    if client.get('birth_date'):
        today = datetime.now().strftime("%d-%m")
        birth = client['birth_date'][:5] if client['birth_date'] else ""
        if today == birth:
            birthday_multiplier = 2
            print(smooth_gradient("  🎂 С ДНЕМ РОЖДЕНИЯ! БОНУСЫ x2 🎂", "#ffd93d", "#ff6b6b"))

    bonus_points = base_points * birthday_multiplier

    if not client.get('first_purchase'):
        client['first_purchase'] = True
        bonus_points += 200
        print(smooth_gradient("  → +200 бонусов за первую покупку", "#00ff88", "#00ff88"))

    if amount >= 5000:
        bonus_points += 500
        print(smooth_gradient("  → +500 бонусов за крупную покупку", "#00ff88", "#00ff88"))

    if client['total_purchases'] >= 50000 and not client.get('vip_status'):
        client['vip_status'] = True
        client['discount'] = 15
        bonus_points += 1000
        print(smooth_gradient("  👑 VIP СТАТУС ПОЛУЧЕН! +1000 бонусов, скидка 15%", "#ffd93d", "#ff6b6b"))
    elif client['total_purchases'] >= 25000 and not client.get('silver_status'):
        client['silver_status'] = True
        client['discount'] = 7
        bonus_points += 500
        print(smooth_gradient("  🥈 SILVER СТАТУС! +500 бонусов, скидка 7%", "#c0c0c0", "#ffd93d"))

    client['loyalty_points'] += bonus_points
    client['bonus_history'].append({
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'amount': bonus_points,
        'reason': f'Покупка на {amount}₽'
    })

    if client.get('referred_by'):
        for i, c in enumerate(data['clients']):
            if c['id'] == client['referred_by']:
                referral_bonus = amount // 20
                data['clients'][i]['loyalty_points'] += referral_bonus
                data['clients'][i]['bonus_history'].append({
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'amount': referral_bonus,
                    'reason': f'5% от покупки реферала {client["name"]}'
                })
                print(smooth_gradient(f"  → пригласивший получил +{referral_bonus} бонусов", "#00ff88", "#00ff88"))
                break

    save_data(data)

    print()
    print(smooth_gradient("  ─────────────────────────────", "#00d4ff", "#00d4ff"))
    print(smooth_gradient(f"  к оплате: {amount:,} ₽", "#00ff88", "#00ff88"))
    print(smooth_gradient(f"  начислено бонусов: +{bonus_points}", "#ffd93d", "#ffd93d"))
    print(smooth_gradient(f"  итого бонусов: {client['loyalty_points']}", "#6c5ce7", "#a8e6cf"))
    print(smooth_gradient("  ─────────────────────────────", "#00d4ff", "#00d4ff"))
    sleep(2.5)

def show_referral_info():
    client_id = input(smooth_gradient("  id клиента > ", "#ffd93d", "#ff6b6b"))
    if not client_id.isdigit():
        return

    data = load_data()
    client = None
    for c in data['clients']:
        if c['id'] == int(client_id):
            client = c
            break

    if not client:
        print(smooth_gradient("  не найден", "#ff6b6b", "#ff6b6b"))
        sleep(1)
        return

    print()
    print(smooth_gradient(f"✦ РЕФЕРАЛЬНАЯ ПРОГРАММА {COMPANY_NAME} ✦", "#00ff88", "#00d4ff"))
    print()
    print(smooth_gradient(f"  код: {client['referral_code']}", "#00d4ff", "#00d4ff"))
    print(smooth_gradient(f"  приглашено: {len(client.get('referrals', []))} друзей", "#6c5ce7", "#a8e6cf"))

    total_bonus = sum(b['amount'] for b in client.get('bonus_history', []) if 'реферал' in b.get('reason', '').lower())
    print(smooth_gradient(f"  получено бонусов: {total_bonus}", "#ffd93d", "#ffd93d"))

    if client.get('referred_by'):
        referrer = next((c for c in data['clients'] if c['id'] == client['referred_by']), None)
        if referrer:
            print(smooth_gradient(f"  пригласил: {referrer['name']}", "#a8e6cf", "#a8e6cf"))

    print()
    print(smooth_gradient("  как это работает:", "#6c5ce7", "#6c5ce7"))
    print(smooth_gradient("  1. поделись кодом с другом", "#ffffff", "#ffffff"))
    print(smooth_gradient("  2. друг регистрируется по коду", "#ffffff", "#ffffff"))
    print(smooth_gradient("  3. ты получаешь +300 бонусов", "#00ff88", "#00ff88"))
    print(smooth_gradient("  4. за его покупки — еще 5%", "#ffd93d", "#ffd93d"))

    input()

def show_promotions():
    promos = load_promotions()

    print(smooth_gradient("✦ АКТИВНЫЕ АКЦИИ ✦", "#00ff88", "#00d4ff"))
    print()

    for promo in promos['active_promotions']:
        print(smooth_gradient(f"  {promo['name']}", "#ffd93d", "#ff6b6b"))
        print(smooth_gradient(f"    {promo['desc']}", "#6c5ce7", "#a8e6cf"))
        if promo.get('code'):
            print(smooth_gradient(f"    код: {promo['code']}", "#00d4ff", "#00d4ff"))
        print()

def apply_promo():
    client_id = input(smooth_gradient("  id клиента > ", "#ffd93d", "#ff6b6b"))
    if not client_id.isdigit():
        return

    data = load_data()
    promos = load_promotions()

    idx = None
    for i, c in enumerate(data['clients']):
        if c['id'] == int(client_id):
            idx = i
            break

    if idx is None:
        print(smooth_gradient("  не найден", "#ff6b6b", "#ff6b6b"))
        return

    code = input(smooth_gradient("  промокод > ", "#ffd93d", "#ff6b6b")).upper()

    if code in data['clients'][idx].get('used_codes', []):
        print(smooth_gradient("  уже использован", "#ff6b6b", "#ff6b6b"))
        return

    promo = None
    for p in promos['active_promotions']:
        if p.get('code') == code:
            promo = p
            break

    if not promo:
        print(smooth_gradient("  недействительный код", "#ff6b6b", "#ff6b6b"))
        return

    bonus = promo.get('bonus', 0)
    discount = promo.get('discount', 0)

    if bonus:
        data['clients'][idx]['loyalty_points'] += bonus
        data['clients'][idx]['bonus_history'].append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': bonus,
            'reason': f'Промокод {code}'
        })
        print(smooth_gradient(f"  → +{bonus} бонусов", "#00ff88", "#00ff88"))

    if discount:
        print(smooth_gradient(f"  → скидка {discount}% на следующий заказ", "#ffd93d", "#ffd93d"))

    if 'used_codes' not in data['clients'][idx]:
        data['clients'][idx]['used_codes'] = []
    data['clients'][idx]['used_codes'].append(code)
    save_data(data)

    input()

def show_stats():
    data = load_data()
    clients = data['clients']

    if not clients:
        print(smooth_gradient("  нет данных", "#ff6b6b", "#ff6b6b"))
        input()
        return

    total = len(clients)
    active = sum(1 for c in clients if c['status'] == 'active')
    revenue = sum(c['total_purchases'] for c in clients)
    points = sum(c['loyalty_points'] for c in clients)
    referrals = sum(len(c.get('referrals', [])) for c in clients)
    vip = sum(1 for c in clients if c.get('vip_status'))

    print(smooth_gradient("✦ СТАТИСТИКА ✦", "#00ff88", "#00d4ff"))
    print()
    print(smooth_gradient(f"  клиентов: {total}", "#00d4ff", "#00d4ff"))
    print(smooth_gradient(f"  активных: {active}", "#00ff88", "#00ff88"))
    print(smooth_gradient(f"  выручка: {revenue:,} ₽", "#ffd93d", "#ffd93d"))
    print(smooth_gradient(f"  средний чек: {revenue//total:,} ₽", "#6c5ce7", "#a8e6cf"))
    print(smooth_gradient(f"  бонусов в системе: {points:,}", "#ff6b6b", "#ff6b6b"))
    print(smooth_gradient(f"  рефералов: {referrals}", "#00d4ff", "#00d4ff"))
    print(smooth_gradient(f"  vip клиентов: {vip}", "#ffd93d", "#ffd93d"))
    input()

def referral_top():
    data = load_data()
    sorted_clients = sorted(data['clients'], key=lambda x: len(x.get('referrals', [])), reverse=True)[:10]

    print(smooth_gradient("✦ ТОП-10 РЕФЕРАЛОВ ✦", "#00ff88", "#00d4ff"))
    print()

    for i, client in enumerate(sorted_clients, 1):
        if i == 1:
            icon = "🥇"
        elif i == 2:
            icon = "🥈"
        elif i == 3:
            icon = "🥉"
        else:
            icon = f" {i}."

        ref_count = len(client.get('referrals', []))
        print(smooth_gradient(f"  {icon} {client['name']}", "#00d4ff", "#00d4ff"))
        print(f"      пригласил: {ref_count} друзей")
        print()

    input()

def bonus_history():
    client_id = input(smooth_gradient("  id клиента > ", "#ffd93d", "#ff6b6b"))
    if not client_id.isdigit():
        return

    data = load_data()
    client = None
    for c in data['clients']:
        if c['id'] == int(client_id):
            client = c
            break

    if not client:
        print(smooth_gradient("  не найден", "#ff6b6b", "#ff6b6b"))
        return

    print(smooth_gradient(f"✦ ИСТОРИЯ БОНУСОВ — {client['name']} ✦", "#00ff88", "#00d4ff"))
    print()

    for bonus in reversed(client.get('bonus_history', [])[-15:]):
        sign = "+" if bonus['amount'] > 0 else ""
        color = "#00ff88" if bonus['amount'] > 0 else "#ff6b6b"
        print(smooth_gradient(f"  {bonus['date'][:10]} {sign}{bonus['amount']} — {bonus['reason']}", color, color))

    print()
    print(smooth_gradient(f"  итого: {client['loyalty_points']} бонусов", "#ffd93d", "#ffd93d"))
    input()

def daily_bonus():
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0

    for client in data['clients']:
        last = client.get('last_daily')
        if not last or last != today:
            client['loyalty_points'] += 50
            client['last_daily'] = today
            client['bonus_history'].append({
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'amount': 50,
                'reason': 'Ежедневный бонус'
            })
            count += 1

    save_data(data)
    print(smooth_gradient(f"  ежедневный бонус (+50) получен {count} клиентами", "#00ff88", "#00ff88"))
    sleep(1.5)

def backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{timestamp}.json"
    data = load_data()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(smooth_gradient(f"  бэкап создан: {filename}", "#00ff88", "#00ff88"))
    sleep(1.5)

def restore():
    backups = [f for f in os.listdir() if f.startswith('backup_') and f.endswith('.json')]
    if not backups:
        print(smooth_gradient("  нет бэкапов", "#ff6b6b", "#ff6b6b"))
        sleep(1.5)
        return

    print(smooth_gradient("✦ ДОСТУПНЫЕ БЭКАПЫ ✦", "#00ff88", "#00d4ff"))
    for i, f in enumerate(backups, 1):
        print(f"  {i}. {f}")

    choice = input(smooth_gradient("  выбрать номер > ", "#ffd93d", "#ff6b6b"))
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(backups):
        return

    selected = backups[int(choice)-1]
    confirm = input(smooth_gradient("  восстановить? (y/n) > ", "#ff6b6b", "#ff6b6b")).lower()

    if confirm == 'y':
        with open(selected, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        save_data(backup_data)
        print(smooth_gradient("  данные восстановлены", "#00ff88", "#00ff88"))
    sleep(1.5)

def export_csv():
    data = load_data()
    if not data['clients']:
        print(smooth_gradient("  нет данных", "#ff6b6b", "#ff6b6b"))
        return

    import csv
    filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=data['clients'][0].keys())
        writer.writeheader()
        writer.writerows(data['clients'])

    print(smooth_gradient(f"  экспортировано в {filename}", "#00ff88", "#00ff88"))
    sleep(1.5)

def main_menu():
    while True:
        print_header()

        menu = f"""
{ smooth_gradient("  [1]  добавить клиента", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [2]  список клиентов", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [3]  оформить покупку", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [4]  история бонусов", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [5]  акции и промокоды", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [6]  активировать промокод", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [7]  реферальная программа", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [8]  топ рефералов", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [9]  статистика", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [10] ежедневный бонус", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [11] создать бэкап", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [12] восстановить из бэкапа", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [13] экспорт в csv", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [0] выход", "#ff6b6b", "#ff6b6b")}
"""
        print(menu)

        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            add_client()
        elif choice == '2':
            list_clients()
        elif choice == '3':
            add_purchase()
        elif choice == '4':
            bonus_history()
        elif choice == '5':
            show_promotions()
            input(smooth_gradient("  нажмите enter", "#6c5ce7", "#a8e6cf"))
        elif choice == '6':
            apply_promo()
        elif choice == '7':
            show_referral_info()
        elif choice == '8':
            referral_top()
        elif choice == '9':
            show_stats()
        elif choice == '10':
            daily_bonus()
        elif choice == '11':
            backup()
        elif choice == '12':
            restore()
        elif choice == '13':
            export_csv()
        elif choice == '0':
            print(smooth_gradient(f"\n  спасибо, что выбрали {COMPANY_NAME}!", "#ffd93d", "#ff6b6b"))
            sleep(1.5)
            sys.exit(0)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(smooth_gradient("\n\n  до свидания!", "#ffd93d", "#ff6b6b"))
        sys.exit(0)
