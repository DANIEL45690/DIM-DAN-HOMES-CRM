import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from time import sleep
import platform
import random
import hashlib
import re

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
PRODUCTS_FILE = 'products.json'
CATEGORIES_FILE = 'categories.json'
ORDERS_FILE = 'orders.json'
FEEDBACK_FILE = 'feedback.json'
NEWSLETTER_FILE = 'newsletter.json'
TASKS_FILE = 'tasks.json'
SUPPORT_TICKETS_FILE = 'support_tickets.json'
STOCK_FILE = 'stock.json'

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

def load_products():
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        default = {"products": [], "last_id": 0}
        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

def save_products(data):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_categories():
    try:
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        default = {"categories": []}
        with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

def save_categories(data):
    with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_orders():
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        default = {"orders": [], "last_id": 0}
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

def save_orders(data):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_feedback():
    try:
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        default = {"feedbacks": [], "last_id": 0}
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

def save_feedback(data):
    with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_newsletter():
    try:
        with open(NEWSLETTER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        default = {"subscribers": [], "sent_history": []}
        with open(NEWSLETTER_FILE, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

def save_newsletter(data):
    with open(NEWSLETTER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_tasks():
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        default = {"tasks": [], "last_id": 0}
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

def save_tasks(data):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_tickets():
    try:
        with open(SUPPORT_TICKETS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        default = {"tickets": [], "last_id": 0}
        with open(SUPPORT_TICKETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

def save_tickets(data):
    with open(SUPPORT_TICKETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_stock():
    try:
        with open(STOCK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        default = {"stock_movements": [], "last_id": 0}
        with open(STOCK_FILE, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

def save_stock(data):
    with open(STOCK_FILE, 'w', encoding='utf-8') as f:
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
        'orders_count': 0,
        'wishlist': [],
        'cart': [],
        'favorites': [],
        'preferences': {'notifications': True, 'promo_emails': True}
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
    
    newsletter = load_newsletter()
    if email not in newsletter['subscribers']:
        newsletter['subscribers'].append(email)
        save_newsletter(newsletter)
    
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

def add_product():
    print(smooth_gradient("✦ ДОБАВЛЕНИЕ ТОВАРА ✦", "#00ff88", "#00d4ff"))
    print()
    
    products = load_products()
    categories = load_categories()
    
    name = input(smooth_gradient("  название > ", "#6c5ce7", "#a8e6cf"))
    price = input(smooth_gradient("  цена > ", "#6c5ce7", "#a8e6cf"))
    stock = input(smooth_gradient("  количество > ", "#6c5ce7", "#a8e6cf"))
    category = input(smooth_gradient("  категория > ", "#6c5ce7", "#a8e6cf"))
    description = input(smooth_gradient("  описание > ", "#6c5ce7", "#a8e6cf"))
    
    if category not in categories['categories']:
        categories['categories'].append(category)
        save_categories(categories)
    
    product = {
        'id': products['last_id'] + 1,
        'name': name,
        'price': int(price),
        'stock': int(stock),
        'category': category,
        'description': description,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'rating': 0,
        'reviews': [],
        'sales_count': 0
    }
    
    products['products'].append(product)
    products['last_id'] = product['id']
    save_products(products)
    
    print()
    print(smooth_gradient(f"  ✓ товар {name} добавлен", "#00ff88", "#00ff88"))
    sleep(1.5)

def list_products():
    products = load_products()
    if not products['products']:
        print(smooth_gradient("  нет товаров", "#ff6b6b", "#ff6b6b"))
        input()
        return
    
    print(smooth_gradient("✦ КАТАЛОГ ТОВАРОВ ✦", "#00ff88", "#00d4ff"))
    print()
    
    for product in products['products']:
        stock_color = "#00ff88" if product['stock'] > 10 else "#ffd93d" if product['stock'] > 0 else "#ff6b6b"
        print(smooth_gradient(f"  #{product['id']} {product['name']}", "#00d4ff", "#6c5ce7"))
        print(f"    цена: {product['price']:,} ₽")
        print(smooth_gradient(f"    в наличии: {product['stock']}", stock_color, stock_color))
        print(f"    категория: {product['category']}")
        print(f"    продано: {product['sales_count']}")
        print()
    
    input(smooth_gradient("  нажмите enter", "#6c5ce7", "#a8e6cf"))

def add_to_cart():
    client_id = input(smooth_gradient("  id клиента > ", "#ffd93d", "#ff6b6b"))
    if not client_id.isdigit():
        return
    
    data = load_data()
    idx = None
    for i, c in enumerate(data['clients']):
        if c['id'] == int(client_id):
            idx = i
            break
    
    if idx is None:
        print(smooth_gradient("  клиент не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    products = load_products()
    if not products['products']:
        print(smooth_gradient("  нет товаров", "#ff6b6b", "#ff6b6b"))
        return
    
    list_products()
    
    product_id = input(smooth_gradient("  id товара > ", "#ffd93d", "#ff6b6b"))
    if not product_id.isdigit():
        return
    
    product = None
    for p in products['products']:
        if p['id'] == int(product_id):
            product = p
            break
    
    if not product:
        print(smooth_gradient("  товар не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    quantity = input(smooth_gradient("  количество > ", "#ffd93d", "#ff6b6b"))
    if not quantity.isdigit() or int(quantity) <= 0:
        return
    
    if int(quantity) > product['stock']:
        print(smooth_gradient(f"  недостаточно на складе (есть {product['stock']})", "#ff6b6b", "#ff6b6b"))
        return
    
    cart_item = {
        'product_id': product['id'],
        'name': product['name'],
        'price': product['price'],
        'quantity': int(quantity),
        'total': product['price'] * int(quantity)
    }
    
    data['clients'][idx].setdefault('cart', []).append(cart_item)
    save_data(data)
    
    print(smooth_gradient(f"  ✓ {product['name']} x{quantity} добавлен в корзину", "#00ff88", "#00ff88"))
    sleep(1.5)

def view_cart():
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
        print(smooth_gradient("  клиент не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    cart = client.get('cart', [])
    if not cart:
        print(smooth_gradient("  корзина пуста", "#ffd93d", "#ffd93d"))
        input()
        return
    
    print(smooth_gradient(f"✦ КОРЗИНА — {client['name']} ✦", "#00ff88", "#00d4ff"))
    print()
    
    total = 0
    for item in cart:
        print(smooth_gradient(f"  {item['name']}", "#00d4ff", "#6c5ce7"))
        print(f"    {item['quantity']} x {item['price']:,} ₽ = {item['total']:,} ₽")
        total += item['total']
    
    print()
    print(smooth_gradient(f"  итого: {total:,} ₽", "#ffd93d", "#ffd93d"))
    
    clear = input(smooth_gradient("  очистить корзину? (y/n) > ", "#ff6b6b", "#ff6b6b"))
    if clear == 'y':
        data['clients'][client['id']-1]['cart'] = []
        save_data(data)
        print(smooth_gradient("  корзина очищена", "#00ff88", "#00ff88"))
    
    input()

def checkout():
    client_id = input(smooth_gradient("  id клиента > ", "#ffd93d", "#ff6b6b"))
    if not client_id.isdigit():
        return
    
    data = load_data()
    products = load_products()
    orders = load_orders()
    
    idx = None
    for i, c in enumerate(data['clients']):
        if c['id'] == int(client_id):
            idx = i
            break
    
    if idx is None:
        print(smooth_gradient("  клиент не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    client = data['clients'][idx]
    cart = client.get('cart', [])
    
    if not cart:
        print(smooth_gradient("  корзина пуста", "#ffd93d", "#ffd93d"))
        return
    
    total = sum(item['total'] for item in cart)
    
    discount = 0
    if client.get('vip_status'):
        discount = 15
    elif client.get('silver_status'):
        discount = 7
    
    if discount > 0:
        discount_amount = total * discount / 100
        total -= discount_amount
        print(smooth_gradient(f"  скидка {discount}%: -{discount_amount:,} ₽", "#00ff88", "#00ff88"))
    
    use_bonus = input(smooth_gradient("  списать бонусы? (y/n) > ", "#6c5ce7", "#a8e6cf")).lower()
    
    bonus_discount = 0
    if use_bonus == 'y' and client['loyalty_points'] > 0:
        points_to_use = min(client['loyalty_points'], total)
        bonus_discount = points_to_use
        total -= bonus_discount
        client['loyalty_points'] -= points_to_use
        print(smooth_gradient(f"  → списано {points_to_use} бонусов", "#00ff88", "#00ff88"))
    
    for item in cart:
        for p in products['products']:
            if p['id'] == item['product_id']:
                p['stock'] -= item['quantity']
                p['sales_count'] += item['quantity']
                break
    
    order = {
        'id': orders['last_id'] + 1,
        'client_id': client['id'],
        'client_name': client['name'],
        'items': cart,
        'subtotal': sum(item['total'] for item in cart),
        'discount': discount,
        'discount_amount': discount_amount if discount > 0 else 0,
        'bonus_used': bonus_discount,
        'total': total,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'completed'
    }
    
    orders['orders'].append(order)
    orders['last_id'] = order['id']
    save_orders(orders)
    
    client['total_purchases'] += total
    client['orders_count'] += 1
    client['cart'] = []
    
    base_points = int(total // 100)
    
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
    
    if total >= 5000:
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
        'reason': f'Покупка на {total}₽'
    })
    
    if client.get('referred_by'):
        for i, c in enumerate(data['clients']):
            if c['id'] == client['referred_by']:
                referral_bonus = int(total // 20)
                data['clients'][i]['loyalty_points'] += referral_bonus
                data['clients'][i]['bonus_history'].append({
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'amount': referral_bonus,
                    'reason': f'5% от покупки реферала {client["name"]}'
                })
                print(smooth_gradient(f"  → пригласивший получил +{referral_bonus} бонусов", "#00ff88", "#00ff88"))
                break
    
    save_products(products)
    save_data(data)
    
    print()
    print(smooth_gradient("  ─────────────────────────────", "#00d4ff", "#00d4ff"))
    print(smooth_gradient(f"  заказ #{order['id']} оформлен", "#00ff88", "#00ff88"))
    print(smooth_gradient(f"  к оплате: {total:,} ₽", "#00ff88", "#00ff88"))
    print(smooth_gradient(f"  начислено бонусов: +{bonus_points}", "#ffd93d", "#ffd93d"))
    print(smooth_gradient(f"  итого бонусов: {client['loyalty_points']}", "#6c5ce7", "#a8e6cf"))
    print(smooth_gradient("  ─────────────────────────────", "#00d4ff", "#00d4ff"))
    sleep(2.5)

def order_history():
    client_id = input(smooth_gradient("  id клиента > ", "#ffd93d", "#ff6b6b"))
    if not client_id.isdigit():
        return
    
    orders = load_orders()
    client_orders = [o for o in orders['orders'] if o['client_id'] == int(client_id)]
    
    if not client_orders:
        print(smooth_gradient("  история заказов пуста", "#ffd93d", "#ffd93d"))
        input()
        return
    
    print(smooth_gradient(f"✦ ИСТОРИЯ ЗАКАЗОВ ✦", "#00ff88", "#00d4ff"))
    print()
    
    for order in reversed(client_orders):
        print(smooth_gradient(f"  заказ #{order['id']}", "#00d4ff", "#6c5ce7"))
        print(f"    дата: {order['date']}")
        print(f"    сумма: {order['total']:,} ₽")
        print(f"    статус: {order['status']}")
        print()
    
    input()

def add_feedback():
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
        print(smooth_gradient("  клиент не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    print(smooth_gradient(f"✦ ОТЗЫВ — {client['name']} ✦", "#00ff88", "#00d4ff"))
    print()
    
    rating = input(smooth_gradient("  оценка (1-5) > ", "#ffd93d", "#ff6b6b"))
    if not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        return
    
    comment = input(smooth_gradient("  комментарий > ", "#6c5ce7", "#a8e6cf"))
    
    feedbacks = load_feedback()
    feedback = {
        'id': feedbacks['last_id'] + 1,
        'client_id': client['id'],
        'client_name': client['name'],
        'rating': int(rating),
        'comment': comment,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'pending'
    }
    
    feedbacks['feedbacks'].append(feedback)
    feedbacks['last_id'] = feedback['id']
    save_feedback(feedbacks)
    
    bonus = 50
    client['loyalty_points'] += bonus
    client['bonus_history'].append({
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'amount': bonus,
        'reason': 'Бонус за отзыв'
    })
    save_data(data)
    
    print(smooth_gradient(f"  ✓ отзыв добавлен, +{bonus} бонусов", "#00ff88", "#00ff88"))
    sleep(1.5)

def view_feedback():
    feedbacks = load_feedback()
    if not feedbacks['feedbacks']:
        print(smooth_gradient("  нет отзывов", "#ffd93d", "#ffd93d"))
        input()
        return
    
    print(smooth_gradient("✦ ВСЕ ОТЗЫВЫ ✦", "#00ff88", "#00d4ff"))
    print()
    
    for fb in reversed(feedbacks['feedbacks'][-20:]):
        stars = "★" * fb['rating'] + "☆" * (5 - fb['rating'])
        print(smooth_gradient(f"  {fb['client_name']} — {stars}", "#ffd93d", "#ff6b6b"))
        print(f"    {fb['comment']}")
        print(smooth_gradient(f"    {fb['date'][:10]}", "#6c5ce7", "#a8e6cf"))
        print()
    
    input()

def send_newsletter():
    newsletter = load_newsletter()
    if not newsletter['subscribers']:
        print(smooth_gradient("  нет подписчиков", "#ffd93d", "#ffd93d"))
        return
    
    print(smooth_gradient("✦ РАССЫЛКА ✦", "#00ff88", "#00d4ff"))
    print()
    print(smooth_gradient(f"  подписчиков: {len(newsletter['subscribers'])}", "#00d4ff", "#00d4ff"))
    
    subject = input(smooth_gradient("  тема > ", "#6c5ce7", "#a8e6cf"))
    message = input(smooth_gradient("  сообщение > ", "#6c5ce7", "#a8e6cf"))
    
    confirm = input(smooth_gradient(f"  отправить {len(newsletter['subscribers'])} получателям? (y/n) > ", "#ff6b6b", "#ff6b6b"))
    
    if confirm == 'y':
        newsletter['sent_history'].append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'subject': subject,
            'message': message,
            'recipients': len(newsletter['subscribers'])
        })
        save_newsletter(newsletter)
        print(smooth_gradient(f"  ✓ рассылка отправлена", "#00ff88", "#00ff88"))
    sleep(1.5)

def subscribe_email():
    email = input(smooth_gradient("  email для подписки > ", "#6c5ce7", "#a8e6cf"))
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        print(smooth_gradient("  неверный email", "#ff6b6b", "#ff6b6b"))
        return
    
    newsletter = load_newsletter()
    if email in newsletter['subscribers']:
        print(smooth_gradient("  уже подписан", "#ffd93d", "#ffd93d"))
    else:
        newsletter['subscribers'].append(email)
        save_newsletter(newsletter)
        print(smooth_gradient("  ✓ подписка оформлена", "#00ff88", "#00ff88"))
    sleep(1.5)

def add_task():
    print(smooth_gradient("✦ ДОБАВИТЬ ЗАДАЧУ ✦", "#00ff88", "#00d4ff"))
    print()
    
    tasks = load_tasks()
    
    title = input(smooth_gradient("  заголовок > ", "#6c5ce7", "#a8e6cf"))
    description = input(smooth_gradient("  описание > ", "#6c5ce7", "#a8e6cf"))
    due_date = input(smooth_gradient("  срок (ДД-ММ-ГГГГ) > ", "#6c5ce7", "#a8e6cf"))
    priority = input(smooth_gradient("  приоритет (low/medium/high) > ", "#ffd93d", "#ff6b6b"))
    
    task = {
        'id': tasks['last_id'] + 1,
        'title': title,
        'description': description,
        'due_date': due_date,
        'priority': priority,
        'status': 'pending',
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    tasks['tasks'].append(task)
    tasks['last_id'] = task['id']
    save_tasks(tasks)
    
    print(smooth_gradient(f"  ✓ задача добавлена", "#00ff88", "#00ff88"))
    sleep(1.5)

def list_tasks():
    tasks = load_tasks()
    if not tasks['tasks']:
        print(smooth_gradient("  нет задач", "#ffd93d", "#ffd93d"))
        input()
        return
    
    print(smooth_gradient("✦ СПИСОК ЗАДАЧ ✦", "#00ff88", "#00d4ff"))
    print()
    
    for task in tasks['tasks']:
        status_color = "#00ff88" if task['status'] == 'completed' else "#ffd93d" if task['status'] == 'pending' else "#ff6b6b"
        priority_color = "#ff6b6b" if task['priority'] == 'high' else "#ffd93d" if task['priority'] == 'medium' else "#00ff88"
        
        print(smooth_gradient(f"  #{task['id']} {task['title']}", "#00d4ff", "#6c5ce7"))
        print(f"    описание: {task['description']}")
        print(f"    срок: {task['due_date']}")
        print(smooth_gradient(f"    приоритет: {task['priority']}", priority_color, priority_color))
        print(smooth_gradient(f"    статус: {task['status']}", status_color, status_color))
        print()
    
    task_id = input(smooth_gradient("  отметить задачу как выполненную (id) или enter > ", "#6c5ce7", "#a8e6cf"))
    if task_id.isdigit():
        for task in tasks['tasks']:
            if task['id'] == int(task_id):
                task['status'] = 'completed'
                save_tasks(tasks)
                print(smooth_gradient(f"  ✓ задача #{task_id} выполнена", "#00ff88", "#00ff88"))
                sleep(1)
                return

def support_ticket():
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
        print(smooth_gradient("  клиент не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    print(smooth_gradient(f"✦ ОБРАЩЕНИЕ В ПОДДЕРЖКУ — {client['name']} ✦", "#00ff88", "#00d4ff"))
    print()
    
    subject = input(smooth_gradient("  тема > ", "#6c5ce7", "#a8e6cf"))
    message = input(smooth_gradient("  сообщение > ", "#6c5ce7", "#a8e6cf"))
    
    tickets = load_tickets()
    ticket = {
        'id': tickets['last_id'] + 1,
        'client_id': client['id'],
        'client_name': client['name'],
        'subject': subject,
        'message': message,
        'status': 'open',
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'response': None
    }
    
    tickets['tickets'].append(ticket)
    tickets['last_id'] = ticket['id']
    save_tickets(tickets)
    
    print(smooth_gradient(f"  ✓ обращение #{ticket['id']} создано", "#00ff88", "#00ff88"))
    sleep(1.5)

def view_tickets():
    tickets = load_tickets()
    if not tickets['tickets']:
        print(smooth_gradient("  нет обращений", "#ffd93d", "#ffd93d"))
        input()
        return
    
    print(smooth_gradient("✦ ОБРАЩЕНИЯ В ПОДДЕРЖКУ ✦", "#00ff88", "#00d4ff"))
    print()
    
    for ticket in tickets['tickets']:
        status_color = "#ff6b6b" if ticket['status'] == 'open' else "#00ff88"
        print(smooth_gradient(f"  #{ticket['id']} — {ticket['client_name']}", "#00d4ff", "#6c5ce7"))
        print(f"    тема: {ticket['subject']}")
        print(f"    сообщение: {ticket['message']}")
        print(smooth_gradient(f"    статус: {ticket['status']}", status_color, status_color))
        print(f"    создано: {ticket['created_at'][:10]}")
        
        if ticket['status'] == 'open':
            response = input(smooth_gradient("    ответить? (y/n) > ", "#6c5ce7", "#a8e6cf"))
            if response == 'y':
                answer = input(smooth_gradient("    ответ > ", "#ffd93d", "#ff6b6b"))
                ticket['response'] = answer
                ticket['status'] = 'closed'
                ticket['closed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_tickets(tickets)
                print(smooth_gradient("    ✓ ответ отправлен", "#00ff88", "#00ff88"))
        print()
    
    input()

def add_to_wishlist():
    client_id = input(smooth_gradient("  id клиента > ", "#ffd93d", "#ff6b6b"))
    if not client_id.isdigit():
        return
    
    data = load_data()
    idx = None
    for i, c in enumerate(data['clients']):
        if c['id'] == int(client_id):
            idx = i
            break
    
    if idx is None:
        print(smooth_gradient("  клиент не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    products = load_products()
    list_products()
    
    product_id = input(smooth_gradient("  id товара > ", "#ffd93d", "#ff6b6b"))
    if not product_id.isdigit():
        return
    
    product = None
    for p in products['products']:
        if p['id'] == int(product_id):
            product = p
            break
    
    if not product:
        print(smooth_gradient("  товар не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    if product['id'] not in data['clients'][idx].get('wishlist', []):
        data['clients'][idx].setdefault('wishlist', []).append(product['id'])
        save_data(data)
        print(smooth_gradient(f"  ✓ {product['name']} добавлен в вишлист", "#00ff88", "#00ff88"))
    else:
        print(smooth_gradient("  уже в вишлисте", "#ffd93d", "#ffd93d"))
    sleep(1.5)

def view_wishlist():
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
        print(smooth_gradient("  клиент не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    wishlist = client.get('wishlist', [])
    if not wishlist:
        print(smooth_gradient("  вишлист пуст", "#ffd93d", "#ffd93d"))
        input()
        return
    
    products = load_products()
    print(smooth_gradient(f"✦ ВИШЛИСТ — {client['name']} ✦", "#00ff88", "#00d4ff"))
    print()
    
    for pid in wishlist:
        product = next((p for p in products['products'] if p['id'] == pid), None)
        if product:
            print(smooth_gradient(f"  #{product['id']} {product['name']}", "#00d4ff", "#6c5ce7"))
            print(f"    цена: {product['price']:,} ₽")
            print()
    
    input()

def stock_movement():
    print(smooth_gradient("✦ ДВИЖЕНИЕ СКЛАДА ✦", "#00ff88", "#00d4ff"))
    print()
    
    products = load_products()
    stock = load_stock()
    
    list_products()
    
    product_id = input(smooth_gradient("  id товара > ", "#ffd93d", "#ff6b6b"))
    if not product_id.isdigit():
        return
    
    product = None
    idx = None
    for i, p in enumerate(products['products']):
        if p['id'] == int(product_id):
            product = p
            idx = i
            break
    
    if not product:
        print(smooth_gradient("  товар не найден", "#ff6b6b", "#ff6b6b"))
        return
    
    movement_type = input(smooth_gradient("  тип (in/out) > ", "#6c5ce7", "#a8e6cf"))
    quantity = input(smooth_gradient("  количество > ", "#6c5ce7", "#a8e6cf"))
    
    if not quantity.isdigit() or int(quantity) <= 0:
        return
    
    if movement_type == 'in':
        products['products'][idx]['stock'] += int(quantity)
    elif movement_type == 'out':
        if int(quantity) > products['products'][idx]['stock']:
            print(smooth_gradient("  недостаточно на складе", "#ff6b6b", "#ff6b6b"))
            return
        products['products'][idx]['stock'] -= int(quantity)
    else:
        print(smooth_gradient("  неверный тип", "#ff6b6b", "#ff6b6b"))
        return
    
    stock['stock_movements'].append({
        'id': stock['last_id'] + 1,
        'product_id': product['id'],
        'product_name': product['name'],
        'type': movement_type,
        'quantity': int(quantity),
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    stock['last_id'] = stock['last_id'] + 1
    
    save_products(products)
    save_stock(stock)
    
    print(smooth_gradient(f"  ✓ склад обновлен", "#00ff88", "#00ff88"))
    sleep(1.5)

def low_stock_report():
    products = load_products()
    low_stock = [p for p in products['products'] if p['stock'] <= 5]
    
    print(smooth_gradient("✦ НИЗКИЙ ОСТАТОК ✦", "#00ff88", "#00d4ff"))
    print()
    
    if not low_stock:
        print(smooth_gradient("  нет товаров с низким остатком", "#00ff88", "#00ff88"))
    else:
        for product in low_stock:
            print(smooth_gradient(f"  #{product['id']} {product['name']}", "#ff6b6b", "#ff6b6b"))
            print(f"    остаток: {product['stock']}")
            print()
    
    input()

def bestsellers():
    products = load_products()
    sorted_products = sorted(products['products'], key=lambda x: x['sales_count'], reverse=True)[:10]
    
    print(smooth_gradient("✦ ТОП-10 ХИТОВ ПРОДАЖ ✦", "#00ff88", "#00d4ff"))
    print()
    
    for i, product in enumerate(sorted_products, 1):
        if i == 1:
            icon = "🏆"
        elif i == 2:
            icon = "🥈"
        elif i == 3:
            icon = "🥉"
        else:
            icon = f" {i}."
        
        print(smooth_gradient(f"  {icon} {product['name']}", "#ffd93d", "#ffd93d"))
        print(f"      продано: {product['sales_count']} шт.")
        print(f"      выручка: {product['price'] * product['sales_count']:,} ₽")
        print()
    
    input()

def revenue_report():
    data = load_data()
    orders = load_orders()
    
    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    today_orders = [o for o in orders['orders'] if o['date'][:10] == today]
    week_orders = [o for o in orders['orders'] if o['date'][:10] >= week_ago]
    month_orders = [o for o in orders['orders'] if o['date'][:10] >= month_ago]
    all_orders = orders['orders']
    
    print(smooth_gradient("✦ ОТЧЕТ ПО ВЫРУЧКЕ ✦", "#00ff88", "#00d4ff"))
    print()
    
    print(smooth_gradient("  сегодня:", "#00d4ff", "#00d4ff"))
    print(f"    заказов: {len(today_orders)}")
    print(f"    выручка: {sum(o['total'] for o in today_orders):,} ₽")
    print()
    
    print(smooth_gradient("  за неделю:", "#00d4ff", "#00d4ff"))
    print(f"    заказов: {len(week_orders)}")
    print(f"    выручка: {sum(o['total'] for o in week_orders):,} ₽")
    print()
    
    print(smooth_gradient("  за месяц:", "#00d4ff", "#00d4ff"))
    print(f"    заказов: {len(month_orders)}")
    print(f"    выручка: {sum(o['total'] for o in month_orders):,} ₽")
    print()
    
    print(smooth_gradient("  всего:", "#00d4ff", "#00d4ff"))
    print(f"    заказов: {len(all_orders)}")
    print(f"    выручка: {sum(o['total'] for o in all_orders):,} ₽")
    
    input()

def client_analytics():
    data = load_data()
    
    total_clients = len(data['clients'])
    active = sum(1 for c in data['clients'] if c['status'] == 'active')
    vip = sum(1 for c in data['clients'] if c.get('vip_status'))
    silver = sum(1 for c in data['clients'] if c.get('silver_status'))
    
    avg_purchase = sum(c['total_purchases'] for c in data['clients']) / total_clients if total_clients > 0 else 0
    
    print(smooth_gradient("✦ АНАЛИТИКА КЛИЕНТОВ ✦", "#00ff88", "#00d4ff"))
    print()
    print(smooth_gradient(f"  всего клиентов: {total_clients}", "#00d4ff", "#00d4ff"))
    print(smooth_gradient(f"  активных: {active}", "#00ff88", "#00ff88"))
    print(smooth_gradient(f"  VIP клиентов: {vip}", "#ffd93d", "#ffd93d"))
    print(smooth_gradient(f"  SILVER клиентов: {silver}", "#c0c0c0", "#c0c0c0"))
    print()
    print(smooth_gradient(f"  средняя выручка на клиента: {avg_purchase:,.0f} ₽", "#6c5ce7", "#a8e6cf"))
    
    print()
    print(smooth_gradient("  топ по покупкам:", "#00d4ff", "#00d4ff"))
    sorted_clients = sorted(data['clients'], key=lambda x: x['total_purchases'], reverse=True)[:5]
    for i, c in enumerate(sorted_clients, 1):
        print(f"    {i}. {c['name']} — {c['total_purchases']:,} ₽")
    
    input()

def export_clients_csv():
    data = load_data()
    if not data['clients']:
        print(smooth_gradient("  нет данных", "#ff6b6b", "#ff6b6b"))
        return
    
    import csv
    filename = f"clients_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'phone', 'email', 'total_purchases', 'loyalty_points', 'status', 'registration_date'])
        writer.writeheader()
        for c in data['clients']:
            writer.writerow({
                'id': c['id'],
                'name': c['name'],
                'phone': c['phone'],
                'email': c['email'],
                'total_purchases': c['total_purchases'],
                'loyalty_points': c['loyalty_points'],
                'status': c['status'],
                'registration_date': c['registration_date']
            })
    
    print(smooth_gradient(f"  экспортировано в {filename}", "#00ff88", "#00ff88"))
    sleep(1.5)

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
    print(smooth_gradient(f"  средний чек: {revenue//total if total > 0 else 0:,} ₽", "#6c5ce7", "#a8e6cf"))
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
{ smooth_gradient("  ─────────── НОВЫЕ ФУНКЦИИ ───────────", "#00d4ff", "#00ff88")}
{ smooth_gradient("  [14] управление товарами", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [15] корзина + оформление заказа", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [16] история заказов", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [17] отзывы клиентов", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [18] рассылка новостей", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [19] задачи и напоминания", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [20] поддержка (тикеты)", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [21] вишлист (список желаний)", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [22] управление складом", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [23] отчеты и аналитика", "#6c5ce7", "#a8e6cf")}
{ smooth_gradient("  [24] экспорт клиентов (CSV)", "#6c5ce7", "#a8e6cf")}
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
        elif choice == '14':
            sub_menu_products()
        elif choice == '15':
            sub_menu_cart()
        elif choice == '16':
            order_history()
        elif choice == '17':
            sub_menu_feedback()
        elif choice == '18':
            sub_menu_newsletter()
        elif choice == '19':
            sub_menu_tasks()
        elif choice == '20':
            sub_menu_support()
        elif choice == '21':
            sub_menu_wishlist()
        elif choice == '22':
            sub_menu_stock()
        elif choice == '23':
            sub_menu_reports()
        elif choice == '24':
            export_clients_csv()
        elif choice == '0':
            print(smooth_gradient(f"\n  спасибо, что выбрали {COMPANY_NAME}!", "#ffd93d", "#ff6b6b"))
            sleep(1.5)
            sys.exit(0)

def sub_menu_products():
    while True:
        clear_screen()
        print(smooth_gradient("✦ УПРАВЛЕНИЕ ТОВАРАМИ ✦", "#00ff88", "#00d4ff"))
        print()
        print(smooth_gradient("  [1] добавить товар", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [2] список товаров", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [3] назад", "#ff6b6b", "#ff6b6b"))
        
        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            add_product()
        elif choice == '2':
            list_products()
        elif choice == '3':
            break

def sub_menu_cart():
    while True:
        clear_screen()
        print(smooth_gradient("✦ КОРЗИНА И ЗАКАЗЫ ✦", "#00ff88", "#00d4ff"))
        print()
        print(smooth_gradient("  [1] добавить в корзину", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [2] посмотреть корзину", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [3] оформить заказ", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [4] назад", "#ff6b6b", "#ff6b6b"))
        
        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            add_to_cart()
        elif choice == '2':
            view_cart()
        elif choice == '3':
            checkout()
        elif choice == '4':
            break

def sub_menu_feedback():
    while True:
        clear_screen()
        print(smooth_gradient("✦ ОТЗЫВЫ ✦", "#00ff88", "#00d4ff"))
        print()
        print(smooth_gradient("  [1] оставить отзыв", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [2] все отзывы", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [3] назад", "#ff6b6b", "#ff6b6b"))
        
        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            add_feedback()
        elif choice == '2':
            view_feedback()
        elif choice == '3':
            break

def sub_menu_newsletter():
    while True:
        clear_screen()
        print(smooth_gradient("✦ РАССЫЛКА ✦", "#00ff88", "#00d4ff"))
        print()
        print(smooth_gradient("  [1] отправить рассылку", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [2] подписаться", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [3] назад", "#ff6b6b", "#ff6b6b"))
        
        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            send_newsletter()
        elif choice == '2':
            subscribe_email()
        elif choice == '3':
            break

def sub_menu_tasks():
    while True:
        clear_screen()
        print(smooth_gradient("✦ ЗАДАЧИ ✦", "#00ff88", "#00d4ff"))
        print()
        print(smooth_gradient("  [1] добавить задачу", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [2] список задач", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [3] назад", "#ff6b6b", "#ff6b6b"))
        
        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            add_task()
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            break

def sub_menu_support():
    while True:
        clear_screen()
        print(smooth_gradient("✦ ПОДДЕРЖКА ✦", "#00ff88", "#00d4ff"))
        print()
        print(smooth_gradient("  [1] новое обращение", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [2] все обращения", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [3] назад", "#ff6b6b", "#ff6b6b"))
        
        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            support_ticket()
        elif choice == '2':
            view_tickets()
        elif choice == '3':
            break

def sub_menu_wishlist():
    while True:
        clear_screen()
        print(smooth_gradient("✦ ВИШЛИСТ ✦", "#00ff88", "#00d4ff"))
        print()
        print(smooth_gradient("  [1] добавить в вишлист", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [2] посмотреть вишлист", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [3] назад", "#ff6b6b", "#ff6b6b"))
        
        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            add_to_wishlist()
        elif choice == '2':
            view_wishlist()
        elif choice == '3':
            break

def sub_menu_stock():
    while True:
        clear_screen()
        print(smooth_gradient("✦ УПРАВЛЕНИЕ СКЛАДОМ ✦", "#00ff88", "#00d4ff"))
        print()
        print(smooth_gradient("  [1] движение товаров", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [2] товары с низким остатком", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [3] хиты продаж", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [4] назад", "#ff6b6b", "#ff6b6b"))
        
        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            stock_movement()
        elif choice == '2':
            low_stock_report()
        elif choice == '3':
            bestsellers()
        elif choice == '4':
            break

def sub_menu_reports():
    while True:
        clear_screen()
        print(smooth_gradient("✦ ОТЧЕТЫ И АНАЛИТИКА ✦", "#00ff88", "#00d4ff"))
        print()
        print(smooth_gradient("  [1] отчет по выручке", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [2] аналитика клиентов", "#6c5ce7", "#a8e6cf"))
        print(smooth_gradient("  [3] назад", "#ff6b6b", "#ff6b6b"))
        
        choice = input(smooth_gradient("\n  → ", "#ffd93d", "#ff6b6b"))
        
        if choice == '1':
            revenue_report()
        elif choice == '2':
            client_analytics()
        elif choice == '3':
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(smooth_gradient("\n\n  до свидания!", "#ffd93d", "#ff6b6b"))
        sys.exit(0)
