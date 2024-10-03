import pygame
import random
import sys
import time
import pickle
from collections import Counter

# Initialize Pygame
pygame.init()

# Constants
FPS = 50
MONEY_PER_CLICK = 1000
BOX_PRICE = 20000
upgrade_cost = 50000
upgrade_increment = 50000
INVENTORY_SIZE_PER_PAGE = 10
ACHIEVEMENTS_PER_PAGE = 6
TRADE_TICK_INTERVAL = 5  # Time interval for generating new trade offers (in seconds)
BOT_TRADE_INTERVAL = 10  # Time interval for bot trades (in seconds)

# Setup the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
clock = pygame.time.Clock()

# Game variables
total_time_played = 0
money = 0
safe_money = 0
inventory = []
safe_inventory = []
current_screen = 'main_menu'
inventory_page = 0
safe_inventory_page = 0
selected_car = None
race_in_progress = False
race_start_time = 0
player_car_pos = 0
opponent_car_pos = 0
opponent_car = None
car_index_page = 0
race_page = 0
races_won = 0
boxes_opened = 0
total_cars_owned = 0
achievement_page = 0
sort_by_speed = False
sort_by_rarity = False
sort_by_price = False
trade_offers = []
next_trade_tick = time.time() + TRADE_TICK_INTERVAL
next_bot_trade_tick = time.time() + BOT_TRADE_INTERVAL
market_page = 0
jackpot_amount = 100000
current_screen = 'loading'
game_start_time = time.time()





# Achievements and Quests
achievements = [
    {"name": "First Box", "description": "Open your first box", "completed": False},
    {"name": "Millionaire", "description": "Earn $1,000,000", "completed": False},
    {"name": "Collector", "description": "Collect 10 cars", "completed": False},
    {"name": "Racer", "description": "Win 5 drag races", "completed": False},
    {"name": "High Roller", "description": "Have $10,000,000", "completed": False},
    {"name": "Speed Demon", "description": "Own a car with speed over 250 mph", "completed": False},
    {"name": "Box Master", "description": "Open 50 boxes", "completed": False},
    {"name": "Billionaire", "description": "Have $1,000,000,000", "completed": False},
    {"name": "Nitro Boost", "description": "Own 5 cars with nitro", "completed": False},
    {"name": "Neon Collector", "description": "Own 5 cars with neon", "completed": False},
    {"name": "Legendary Collector", "description": "Collect 5 Legendary cars", "completed": False},
    {"name": "Mythical Hunter", "description": "Collect 3 Mythical cars", "completed": False},
    {"name": "Epic Win", "description": "Win 10 drag races", "completed": False},
    {"name": "Safe Keeper", "description": "Deposit $1,000,000 in the safe", "completed": False},
    {"name": "Banker", "description": "Earn $100,000 in interest", "completed": False},
    {"name": "Drag Racer", "description": "Participate in 20 drag races", "completed": False},
    {"name": "Rare Collector", "description": "Collect 10 Rare cars", "completed": False},
    {"name": "Ultimate Collector", "description": "Own 2 Ultimate cars", "completed": False},
    {"name": "Car Enthusiast", "description": "Own 20 cars", "completed": False},
    {"name": "Speed Addict", "description": "Own a car with speed over 300 mph", "completed": False},
    {"name": "Transcendent Seeker", "description": "Collect a Transcendent car", "completed": False},
    {"name": "Supreme Driver", "description": "Win a race with a Supreme car", "completed": False},
    {"name": "Exotic Owner", "description": "Own 3 Exotic cars", "completed": False},
    {"name": "Luxury Taste", "description": "Own a car worth over $1,000,000", "completed": False},
    {"name": "Box Addict", "description": "Open 100 boxes", "completed": False},
    {"name": "Savings Account", "description": "Deposit $10,000,000 in the safe", "completed": False},
    {"name": "Turbocharger", "description": "Own a car with turbo", "completed": False},
    {"name": "Legendary Win", "description": "Win a race with a Legendary car", "completed": False},
    {"name": "Garage Master", "description": "Own 50 cars", "completed": False},
    {"name": "Celestial Collector", "description": "Collect 2 Celestial cars", "completed": False},
]

quests = [
    {"name": "Collect 5 Cars", "description": "Have 5 cars in your inventory", "completed": False},
    {"name": "Win 3 Races", "description": "Win 3 drag races", "completed": False},
    # Add more quests as needed
]

# Save and Load Functions
def save_game():
    with open('savegame.pkl', 'wb') as f:
        pickle.dump({
            'money': money,
            'safe_money': safe_money,
            'inventory': inventory,
            'safe_inventory': safe_inventory,
            'races_won': races_won,
            'boxes_opened': boxes_opened,
            'total_cars_owned': total_cars_owned,
            'achievements': achievements,
            'quests': quests,
            'trade_offers': trade_offers,
            'jackpot_amount': jackpot_amount,
            'MONEY_PER_CLICK': MONEY_PER_CLICK,  # Add this line
            'upgrade_cost': upgrade_cost, 
        }, f)
    print("Game saved!")

def load_game():
    global money, safe_money, inventory, safe_inventory, races_won, boxes_opened, total_cars_owned, achievements, quests, trade_offers, jackpot_amount, MONEY_PER_CLICK, upgrade_cost
    try:
        with open('savegame.pkl', 'rb') as f:
            data = pickle.load(f)
            money = data['money']
            safe_money = data['safe_money']
            inventory = data['inventory']
            safe_inventory = data['safe_inventory']
            races_won = data['races_won']
            boxes_opened = data['boxes_opened']
            total_cars_owned = data['total_cars_owned']
            achievements = data['achievements']
            quests = data['quests']
            trade_offers = data['trade_offers']
            jackpot_amount = data.get('jackpot_amount', 100000)
            MONEY_PER_CLICK = data.get('MONEY_PER_CLICK', 1000)  # Add this line            
            upgrade_cost = data.get('upgrade_cost', 100000)
        print("Game loaded!")
    except FileNotFoundError:
        print("No saved game found.")

# Car rarities and their probabilities
CAR_RARITIES = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary', 'Mythical', 'Exotic', 'Special', 'Celestial', 'Ultimate', 'Transcendent', 'Supreme', 'Legendary Classics', 'Unreal']


REVERSE_CAR_RARITIES = CAR_RARITIES[::-1]
RARITY_COLORS = {
    'Common': (169, 169, 169),
    'Uncommon': (34, 139, 34),
    'Rare': (65, 105, 225),
    'Epic': (138, 43, 226),
    'Legendary': (255, 215, 0),
    'Mythical': (255, 69, 0),
    'Exotic': (255, 20, 147),
    'Special': (173, 216, 230),
    'Celestial': (72, 61, 139),
    'Ultimate': (255, 0, 0),
    'Transcendent': (75, 0, 130),
    'Supreme': (64, 224, 208),
    'Legendary Classics': (255, 223, 0),
    'Unreal': (123, 45, 67)
}

RARITY_PROBABILITIES = {
    'Common': 50,
    'Uncommon': 30,
    'Rare': 15,
    'Epic': 3,
    'Legendary': 1,
    'Mythical': 0.5,
    'Exotic': 0.3,
    'Special': 0.25,
    'Celestial': 0.1,
    'Ultimate': 0.05,
    'Transcendent': 0.02,
    'Supreme': 0.01,
    'Legendary Classics': 0.005,
    'Unreal': 0.000001
}



CAR_DATA = {
    'Common': [
        ('Toyota Camry', 24000, 130, 'Common'),
        ('Honda Civic', 20000, 125, 'Common'),
        ('Ford Focus', 19000, 120, 'Common'),
        ('Chevrolet Cruze', 18000, 118, 'Common'),
        ('Hyundai Elantra', 19000, 123, 'Common'),
        ('Kia Soul', 17000, 115, 'Common'),
        ('Mazda3', 20000, 128, 'Common'),
        ('Toyota Corolla', 20000, 120, 'Common'),
        ('Ford Fiesta', 15000, 115, 'Common'),
        ('Chevrolet Malibu', 22000, 130, 'Common'),
        ('Hyundai Sonata', 23000, 129, 'Common'),
        ('Kia Optima', 21000, 126, 'Common'),
        ('Nissan Altima', 24000, 130, 'Common'),
        ('Mazda6', 22000, 129, 'Common'),
        ('Mitsubishi Galant GTO', 7000, 103, 'Common'),
        ('Mitsubishi Lancer Evolution', 21000, 160, 'Common'),
        ('Mitsubishi Eclipse', 16000, 134, 'Common'),
        ('Mitsubishi Sigma Diamante', 5000, 103, 'Common'),
        ('Volkswagen Passat', 23000, 128, 'Common'),
        ('Subaru Legacy', 22000, 127, 'Common'),
        ('Toyota RAV4', 26000, 120, 'Common'),
        ('Honda CR-V', 25000, 118, 'Common'),
        ('Ford Escape', 25000, 120, 'Common'),
        ('Mitsubishi Jeep', 15000, 102, 'Common'),
        ('Chevrolet Equinox', 23000, 118, 'Common'),
        ('Hyundai Tucson', 23000, 120, 'Common'),
        ('Kia Sportage', 24000, 118, 'Common'),
        ('Nissan Rogue', 25000, 118, 'Common'),
        ('Mazda CX-5', 25000, 120, 'Common'),
        ('Volkswagen Tiguan', 24000, 120, 'Common'),
        ('Subaru Forester', 24000, 118, 'Common'),
        ('Nissan Sentra', 14000, 115, 'Common'),
        ('Volkswagen Jetta', 12000, 120, 'Common'),
        ('Subaru Impreza', 11000, 115, 'Common'),
        ('Toyota Prius', 23000, 120, 'Common'),
        ('Honda Fit', 16000, 115, 'Common'),
        ('Chevrolet Spark', 13000, 98, 'Common'),
        ('Mitsubishi Mirage', 15000, 100, 'Common'),
        ('Ford Fusion', 22000, 124, 'Common'),
        ('Nissan Versa', 15000, 110, 'Common'),
        ('Kia Rio', 16000, 110, 'Common'),
        ('Mazda CX-3', 20000, 120, 'Common'),
        ('Hyundai Kona', 21000, 125, 'Common'),
        ('Honda HR-V', 23000, 121, 'Common'),
        ('Jeep Renegade', 25000, 118, 'Common'),
        ('Chevrolet Trax', 22000, 115, 'Common'),
        ('Ford EcoSport', 21000, 120, 'Common'),
        ('Toyota C-HR', 25000, 120, 'Common'),
        ('Hyundai Venue', 18000, 121, 'Common'),
        ('Buick Encore', 24000, 118, 'Common'),
        ('Chevrolet Sonic', 18000, 110, 'Common'),
        ('Nissan Kicks', 20000, 115, 'Common'),
        ('Honda Insight', 23000, 125, 'Common'),
        ('Mazda MX-5 Miata', 26000, 135, 'Common'),
        ('Hyundai Veloster', 21000, 130, 'Common'),
        ('Kia Forte', 18000, 120, 'Common'),
        ('Volkswagen Golf', 23000, 125, 'Common'),
        ('Ford C-Max', 25000, 120, 'Common'),
        ('Chevrolet Bolt', 36000, 110, 'Common'),
        ('Fiat 500', 17000, 105, 'Common'),
        ('Mini Cooper', 25000, 130, 'Common'),
        ('Dodge Dart', 20000, 120, 'Common'),
        ('Jeep Compass', 26000, 130, 'Common'),
        ('Subaru Crosstrek', 24000, 130, 'Common'),
        ('Hyundai Ioniq', 23000, 125, 'Common'),
        ('Kia Niro', 24000, 120, 'Common'),
        ('Honda Clarity', 36000, 110, 'Common'),
        ('Toyota Yaris', 15000, 105, 'Common'),
        ('Nissan Leaf', 30000, 110, 'Common'),
        ('Ford Ranger', 27000, 135, 'Common'),
        ('Chevrolet Colorado', 28000, 140, 'Common'),
        ('Toyota Tacoma', 29000, 135, 'Common'),
        ('Corvette C4', 18000, 179, 'Common'),
        ('Corvette C5', 26000, 174, 'Common'),
        ('Honda Ridgeline', 36000, 140, 'Common'),
        ('Nissan Frontier', 27000, 130, 'Common')
    ],
    'Uncommon': [
        ('BMW 3 Series', 40000, 155, 'Uncommon'),
        ('BMW X1 xDrive28i', 40950, 155, 'Uncommon'),
        ('Mitsubishi FTO', 27000, 140, 'Uncommon'),
        ('Mitsubishi 500', 40950, 99, 'Uncommon'),
        ('Mitsubishi 360', 40950, 99, 'Uncommon'),
        ('BMW X1 M35i', 50350, 155, 'Uncommon'),
        ('BMW X2 M35i', 51850, 155, 'Uncommon'),
        ('BMW X3 M50', 64100, 155, 'Uncommon'),
        ('BMW X3 xDrive30', 49500, 155, 'Uncommon'),
        ('BMW X2 xDrive28i', 42450, 155, 'Uncommon'),
        ('BMW iX xDrive50', 87250, 124, 'Uncommon'),
        ('BMW iX M60', 111500, 155, 'Uncommon'),
        ('Alfa Romeo Giulia', 40000, 160, 'Uncommon'),
        ('Corvette C3', 35000, 124, 'Uncommon'),
        ('Audi A3', 33000, 145, 'Uncommon'),
        ('BMW 2 Series', 35000, 150, 'Uncommon'),
        ('Cadillac ATS', 36000, 149, 'Uncommon'),
        ('Dodge Challenger', 28000, 160, 'Uncommon'),
        ('Fiat 124 Spider', 25000, 140, 'Uncommon'),
        ('Genesis G70', 35000, 155, 'Uncommon'),
        ('Infiniti Q50', 36000, 150, 'Uncommon'),
        ('Jaguar XE', 39000, 155, 'Uncommon'),
        ('Kia Stinger', 33000, 160, 'Uncommon'),
        ('Land Rover Discovery Sport', 37000, 130, 'Uncommon'),
        ('Lexus IS', 38000, 145, 'Uncommon'),
        ('Mini Cooper Clubman', 29000, 140, 'Uncommon'),
        ('Nissan 370Z', 30000, 155, 'Uncommon'),
        ('Peugeot 508', 35000, 150, 'Uncommon'),
        ('Renault Megane RS', 32000, 160, 'Uncommon'),
        ('Saab 9-3', 28000, 140, 'Uncommon'),
        ('Seat Leon Cupra', 34000, 150, 'Uncommon'),
        ('Skoda Octavia RS', 30000, 150, 'Uncommon'),
        ('Tesla Model 3', 48000, 162, 'Uncommon'),
        ('Vauxhall Insignia VXR', 38000, 150, 'Uncommon'),
        ('Volvo S60', 36000, 150, 'Uncommon'),
        ('Acura TLX', 37000, 145, 'Uncommon'),
        ('Buick Regal GS', 39000, 150, 'Uncommon'),
        ('Chevrolet SS', 47000, 160, 'Uncommon'),
        ('Chrysler 300 SRT', 51000, 155, 'Uncommon'),
        ('Ford Mustang GT', 36000, 155, 'Uncommon'),
        ('Honda S2000', 34000, 145, 'Uncommon'),
        ('Jeep Wrangler', 32000, 110, 'Uncommon'),
        ('Alfa Romeo 4C', 57000, 160, 'Uncommon'),
        ('Audi TT', 47000, 155, 'Uncommon'),
        ('BMW 4 Series', 45000, 155, 'Uncommon'),
        ('Cadillac CT5', 42000, 150, 'Uncommon'),
        ('Chevrolet Camaro', 37000, 155, 'Uncommon'),
        ('Dodge Charger', 36000, 150, 'Uncommon'),
        ('Genesis G80', 46000, 155, 'Uncommon'),
        ('Infiniti Q60', 48000, 150, 'Uncommon'),
        ('Jaguar XF', 52000, 155, 'Uncommon'),
        ('Kia Cadenza', 39000, 145, 'Uncommon'),
        ('Lexus ES', 41000, 140, 'Uncommon'),
        ('Lincoln MKZ', 42000, 140, 'Uncommon'),
        ('Mercedes-Benz CLA', 40000, 145, 'Uncommon'),
        ('Nissan Maxima', 39000, 145, 'Uncommon'),
        ('Subaru WRX', 32000, 150, 'Uncommon'),
        ('Toyota Avalon', 38000, 145, 'Uncommon'),
        ('Volkswagen Arteon', 43000, 150, 'Uncommon'),
        ('Volvo S90', 51000, 150, 'Uncommon'),
        ('BMW X1', 39000, 140, 'Uncommon'),
        ('Mercedes-Benz GLA', 40000, 140, 'Uncommon'),
        ('Audi Q3', 38000, 140, 'Uncommon'),
        ('Infiniti QX30', 39000, 140, 'Uncommon'),
        ('Lexus NX', 41000, 140, 'Uncommon'),
        ('Land Rover Range Rover Velar', 58000, 140, 'Uncommon'),
        ('Porsche Cayenne', 67000, 160, 'Uncommon'),
        ('Chevrolet Blazer', 43000, 140, 'Uncommon'),
        ('Ford Explorer', 49000, 135, 'Uncommon'),
        ('Honda Passport', 43000, 135, 'Uncommon'),
        ('Hyundai Santa Fe', 42000, 135, 'Uncommon'),
        ('Jeep Grand Cherokee', 50000, 130, 'Uncommon'),
        ('Kia Sorento', 41000, 130, 'Uncommon'),
        ('Mazda CX-9', 46000, 130, 'Uncommon'),
        ('Toyota Highlander', 47000, 130, 'Uncommon'),
        ('Volkswagen Atlas', 48000, 130, 'Uncommon'),
        ('Volvo XC90', 60000, 130, 'Uncommon')
    ],
    'Rare': [
        ('Porsche Macan', 50000, 155, 'Rare'),
        ('1964 Ford Mustang', 35000, 120, 'Rare'),
        ('1967 Pontiac GTO', 60000, 130, 'Rare'),
        ('1970 Dodge Super Bee', 60000, 130, 'Rare'),
        ('Alfa Romeo Stelvio', 45000, 160, 'Rare'),
        ('Jaguar F-Pace', 42000, 155, 'Rare'),
        ('Cadillac XT5', 41000, 150, 'Rare'),
        ('BMW X3', 47000, 155, 'Rare'),
        ('BMW M4 Competition xDrive', 88300, 155, 'Rare'),
        ('BMW M4 Competition', 83200, 155, 'Rare'),
        ('BMW M4', 79100, 155, 'Rare'),
        ('Audi Q5', 43000, 155, 'Rare'),
        ('Mercedes-Benz GLC', 40000, 155, 'Rare'),
        ('Lexus RX', 44000, 145, 'Rare'),
        ('1966 Alfa Romeo Spider', 60000, 110, 'Rare'),
        ('Volvo XC60', 39000, 150, 'Rare'),
        ('Corvette C6', 53000, 192, 'Rare'),
        ('Corvette C7', 46000, 190, 'Rare'),
        ('Infiniti QX50', 37000, 150, 'Rare'),
        ('Land Rover Range Rover Evoque', 43000, 143, 'Rare'),
        ('Tesla Model Y', 51000, 155, 'Rare'),
        ('Chevrolet Camaro SS', 42000, 165, 'Rare'),
        ('Ford Bronco', 50000, 130, 'Rare'),
        ('Toyota Supra', 55000, 155, 'Rare'),
        ('BMW Z4', 50000, 155, 'Rare'),
        ('Jeep Grand Cherokee SRT', 69000, 160, 'Rare'),
        ('Audi S4', 55000, 155, 'Rare'),
        ('Mercedes-Benz C-Class AMG', 60000, 160, 'Rare'),
        ('Cadillac Escalade', 76000, 130, 'Rare'),
        ('Lincoln Navigator', 80000, 130, 'Rare'),
        ('Porsche Boxster', 62000, 160, 'Rare'),
        ('Chevrolet Corvette', 65000, 185, 'Rare'),
        ('Maserati Levante', 78000, 155, 'Rare'),
        ('Jaguar I-Pace', 70000, 150, 'Rare'),
        ('Lexus GX', 55000, 130, 'Rare'),
        ('Infiniti QX80', 75000, 130, 'Rare'),
        ('Dodge Viper', 90000, 177, 'Rare')
    ],
    'Epic': [
        ('Tesla Model S', 80000, 200, 'Epic'),
        ('BMW i8', 147000, 155, 'Epic'),
        ('Porsche 911', 99000, 190, 'Epic'),
        ('1969 Dodge Challenger R/T', 80000, 140, 'Epic'),
        ('Audi RS 5', 74000, 174, 'Epic'),
        ('Mercedes-Benz S-Class', 94000, 155, 'Epic'),
        ('Range Rover Sport', 68000, 140, 'Epic'),
        ('Maserati Ghibli', 75000, 178, 'Epic'),
        ('Lexus LC', 92000, 168, 'Epic'),
        ('Corvette Z06', 115000, 195, 'Epic'),
        ('Corvette C1', 111000, 125, 'Epic'),
        ('Corvette C2', 119000, 148, 'Epic'),
        ('Corvette C8', 68000, 194, 'Epic'),
        ('Chevrolet Corvette E-Ray', 104000, 183, 'Epic'),
        ('Bentley Continental GT', 202000, 207, 'Epic'),
        ('Ferrari California T', 202000, 196, 'Epic'),
        ('Lamborghini Urus', 218000, 190, 'Epic'),
        ('Porsche Panamera Turbo', 178000, 190, 'Epic'),
        ('Rolls-Royce Ghost', 311000, 155, 'Epic'),
        ('Bentley Bentayga', 245000, 187, 'Epic'),
        ('Mercedes-AMG GT', 115000, 189, 'Epic'),
        ('Ferrari Portofino', 210000, 199, 'Epic'),
        ('Porsche Taycan', 150000, 161, 'Epic'),
        ('Ferrari 488 GTB', 262000, 205, 'Epic'),
        ('McLaren 600LT', 240000, 204, 'Epic'),
        ('McLaren 12C Spider', 99000, 204, 'Epic'),
        ('McLaren 12C', 95000, 204, 'Epic'),
        ('Aston Martin Vantage AMR', 180000, 195, 'Epic'),
        ('Bentley Mulsanne', 310000, 190, 'Epic'),
        ('Mercedes-Maybach S650', 200000, 155, 'Epic'),
        ('Jeep Grand Cherokee Trackhawk', 86000, 180, 'Epic'),
        ('Dodge Charger SRT Hellcat', 75000, 204, 'Epic'),
        ('Cadillac CTS-V', 86000, 200, 'Epic'),
        ('Ferrari Roma', 222000, 199, 'Epic'),
        ('Aston Martin DBX', 189000, 181, 'Epic'),
        ('Porsche Cayenne Turbo', 127000, 177, 'Epic'),
        ('Bentley Flying Spur', 214000, 207, 'Epic'),
        ('Mercedes-Maybach GLS 600', 161550, 155, 'Epic'),
        ('Lexus LC 500', 92000, 168, 'Epic'),
        ('Maserati Levante Trofeo', 127000, 187, 'Epic'),
        ('Rolls-Royce Cullinan', 325000, 155, 'Epic'),
        ('Porsche 911 Turbo', 197200, 199, 'Epic'),
        ('Ferrari GTC4Lusso', 300000, 208, 'Epic'),
        ('Lamborghini Huracan EVO', 261274, 202, 'Epic'),
        ('McLaren 600LT Spider', 256500, 204, 'Epic'),
        ('Aston Martin DBS Superleggera', 304995, 211, 'Epic'),
        ('Bentley Continental GT Speed', 240000, 207, 'Epic'),
        ('Mercedes-AMG GT R', 163000, 198, 'Epic'),
        ('Ferrari F12 Berlinetta', 319995, 211, 'Epic'),
        ('Hennessey Venom GT', 1200000, 270, 'Epic'),
        ('Mercedes-Benz G-Class', 150000, 130, 'Epic'),
        ('Audi R8', 170000, 205, 'Epic'),
        ('Nissan GT-R', 110000, 195, 'Epic'),
        ('Maserati Quattroporte', 110000, 180, 'Epic'),
        ('Aston Martin Vantage', 140000, 195, 'Epic'),
        ('Porsche Taycan Turbo S', 185000, 161, 'Epic'),
        ('Mercedes-Benz AMG One', 2700000, 217, 'Epic')
    ],
    'Legendary': [
        ('Ferrari 488', 280000, 211, 'Legendary'),
        ('Lamborghini Huracan', 240000, 202, 'Legendary'),
        ('McLaren 720S', 300000, 212, 'Legendary'),
        ('Ferrari F8 Tributo', 276000, 211, 'Legendary'),
        ('Rolls-Royce Wraith', 330000, 155, 'Legendary'),
        ('Rolls-Royce Dawn', 350000, 155, 'Legendary'),
        ('McLaren GT', 210000, 203, 'Legendary'),
        ('McLaren GTS', 219400, 203, 'Legendary'),
        ('Bugatti Veyron', 1500000, 254, 'Legendary'),
        ('McLaren P1', 1200000, 217, 'Legendary'),
        ('Ferrari Enzo', 2900000, 221, 'Legendary'),
        ('Lamborghini Centenario', 1900000, 217, 'Legendary'),
        ('Aston Martin One-77', 1500000, 220, 'Legendary'),
        ('Pagani Huayra', 2700000, 238, 'Legendary'),
        ('Koenigsegg Agera RS', 2500000, 278, 'Legendary'),
        ('Pagani Zonda Cinque', 2000000, 217, 'Legendary'),
        ('Porsche 718 Cayman', 72800, 171, 'Legendary'),
        ('Ferrari LaFerrari', 1500000, 217, 'Legendary'),
        ('Ferrari Monza SP2', 1800000, 186, 'Legendary'),
        ('McLaren Sabre', 3700000, 218, 'Legendary'),
        ('Porsche 911 Turbo Cabriolet', 210000, 199, 'Legendary'),
        ('Porsche 911 Turbo S Cabriolet', 243200, 205, 'Legendary'),
        ('Porsche 911 GT3', 293000, 211, 'Legendary'),
        ('2010 Tesla Roadster', 109000, 125, 'Legendary'),
        ('Mercedes-Benz Maybach Exelero', 8000000, 218, 'Legendary'),
        ('Lykan Hypersport', 3400000, 245, 'Legendary'),
        ('Pagani Huayra Roadster', 3700000, 238, 'Legendary'),
        ('Ferrari Pininfarina Sergio', 3000000, 199, 'Legendary'),
        ('Rolls-Royce Silver Seraph', 45000, 140, 'Legendary'),
        ('Bentley Mulliner Bacalar', 1900000, 200, 'Legendary')
    ],
    'Mythical': [
        ('Hennessey Venom F5', 1800000, 250, 'Mythical'),
        ('Lotus Evija', 2000000, 217, 'Mythical'),
        ('Rimac C_Two', 2100000, 258, 'Mythical'),
        ('Mercedes-AMG Project One', 2700000, 217, 'Mythical'),
        ('Pininfarina Battista', 2200000, 217, 'Mythical'),
        ('Gordon Murray T.50', 2800000, 217, 'Mythical'),
        ('Ferrari FXX K Evo', 4000000, 217, 'Mythical'),
        ('Lamborghini Sesto Elemento', 2800000, 211, 'Mythical'),
        ('McLaren 750S', 324000, 206, 'Mythical'),
        ('McLaren 750S Spider', 345000, 206, 'Mythical'),
        ('McLaren Elva', 1700000, 203, 'Mythical'),
        ('Aston Martin AM-RB 003', 1000000, 217, 'Mythical'),
        ('Koenigsegg One:1', 6000000, 273, 'Mythical'),
        ('Pagani Imola', 5000000, 233, 'Mythical')
    ],
    'Exotic': [
        ('Chevrolet Corvette ZR1', 120000, 212, 'Exotic'),
        ('1959 Jaguar XK150', 150000, 120, 'Exotic'),
        ('Dodge Viper ACR', 150000, 177, 'Exotic'),
        ('Nissan GT-R Nismo', 210000, 205, 'Exotic'),
        ('Jaguar F-Type SVR', 130000, 200, 'Exotic'),
        ('Acura NSX', 157000, 191, 'Exotic'),
        ('McLaren 720S GT3', 315000, 212, 'Exotic'),
        ('McLaren 620R', 299000, 200, 'Exotic'),
        ('McLaren 650S', 265000, 207, 'Exotic'),
        ('McLaren 650S Spider', 284000, 207, 'Exotic'),
        ('650S Can-Am Spider', 334500, 207, 'Exotic'),
        ('McLaren 720S GT3 Evo', 342000, 212, 'Exotic'),
        ('McLaren Artura', 237000, 205, 'Exotic'),
        ('McLaren 675LT', 250000, 203, 'Exotic'),
        ('McLaren 675LT Spider', 269000, 203, 'Exotic'),
        ('McLaren Artura', 237000, 205, 'Exotic'),
        ('McLaren Artura Spider', 273000, 205, 'Exotic'),
        ('McLaren Artura GT4', 215000, 205, 'Exotic'),
        ('Lamborghini Huracan Performante', 274000, 202, 'Exotic'),
        ('Porsche 911 GT2 RS', 293000, 211, 'Exotic'),
        ('Aston Martin Vanquish Zagato', 850000, 201, 'Exotic'),
        ('Tesla Model S Plaid', 130000, 200, 'Exotic'),
        ('BMW M8 Competition', 146000, 190, 'Exotic'),
        ('Porsche 718 Cayman GT4', 100000, 189, 'Exotic'),
        ('Alfa Romeo 4C Spider', 67000, 160, 'Exotic'),
        ('Maserati GranTurismo', 150000, 187, 'Exotic'),
        ('Chevrolet Corvette Stingray', 60000, 184, 'Exotic'),
        ('Audi R8', 170000, 204, 'Exotic'),
        ('Lotus Exige', 100000, 170, 'Exotic'),
        ('Mercedes-AMG GT R', 163000, 198, 'Exotic'),
        ('Audi RS5', 75000, 174, 'Exotic'),
        ('Jaguar XKR-S', 132000, 186, 'Exotic'),
        ('Porsche 718 Boxster', 95000, 170, 'Exotic'),
        ('Mercedes-Benz SL-Class', 110000, 155, 'Exotic'),
        ('Lexus LC 500', 95000, 168, 'Exotic'),
        ('Aston Martin DB9', 185000, 183, 'Exotic'),
        ('Ferrari 458 Italia', 245000, 202, 'Exotic'),
        ('Lamborghini Gallardo', 200000, 202, 'Exotic'),
        ('Maserati MC20', 210000, 202, 'Exotic'),
        ('Porsche 911 Carrera', 115000, 182, 'Exotic'),
        ('Ferrari F12berlinetta', 320000, 211, 'Exotic'),
        ('Lamborghini Aventador', 420000, 217, 'Exotic'),
        ('McLaren 570S', 200000, 204, 'Exotic'),
        ('McLaren 540C', 350000, 199, 'Exotic'),
        ('McLaren 570 GT', 197000, 204, 'Exotic'),
        ('McLaren 570S Spider', 210000, 204, 'Exotic'),
        ('Porsche Panamera', 150000, 190, 'Exotic'),
        ('Aston Martin V8 Vantage', 140000, 190, 'Exotic'),
        ('Audi R8 Spyder', 182000, 205, 'Exotic'),
        ('Ferrari 812 Superfast', 335000, 211, 'Exotic'),
        ('bentley zagato gtz', 610000, 187, 'Exotic'),
        ('Porsche Macan Turbo', 85000, 164, 'Exotic'),
        ('Audi Q8', 95000, 155, 'Exotic')
    ],
    'Special': [
        ('Oscar Mayer Wienermobile', 100000, 60, 'Special'),
        ('Batman Tumbler', 1000000, 160, 'Special'),
        ('DeLorean DMC-12 (Back to the Future)', 85000, 88, 'Special'),
        ('Ecto-1 (Ghostbusters)', 200000, 80, 'Special'),
        ('The Flintstones Car', 3000, 10, 'Special'),
        ('Mutt Cutts Van (Dumb and Dumber)', 50000, 75, 'Special'),
        ('Peel P50', 120000, 38, 'Special'),
        ('Reliant Regal (Mr. Bean)', 15000, 55, 'Special'),
        ('Jet Car (The Jetsons)', 300000, 300, 'Special'),
        ('AeroMobil 3.0 Flying Car', 1000000, 160, 'Special'),
        ('John Deere X9 Combine', 1079000, 25, 'Special'),
        ('M1 Abrams Tank', 6000000, 42, 'Special'),
        ('Revzani Hercules 6x6', 459000, 142, 'Special'),
        ('Cybertruck', 50000, 130, 'Special'),
        ('Lamborghini LM002', 120000, 118, 'Special'),
        ('Hummer H1', 140000, 85, 'Special'),
        ('Toyota Mega Cruiser', 100000, 85, 'Special'),
        ('Mercedes-Benz Unimog', 250000, 80, 'Special'),
        ('AM General Humvee', 150000, 85, 'Special'),
        ('Volkswagen Type 2 (Microbus)', 35000, 70, 'Special'),
        ('Fiat Multipla', 5000, 85, 'Special'),
        ('Subaru Baja', 20000, 110, 'Special'),
        ('Nissan Juke', 21000, 110, 'Special'),
        ('Daihatsu Copen', 15000, 100, 'Special'),
        ('Mini Moke', 30000, 70, 'Special'),
        ('Ariel Atom', 80000, 150, 'Special'),
        ('Polaris Slingshot', 30000, 130, 'Special'),
        ('Morgan 3-Wheeler', 50000, 115, 'Special'),
        ('Citroen 2CV', 2000, 60, 'Special'),
        ('Peugeot 404', 10000, 80, 'Special'),
        ('AMC Gremlin', 3000, 90, 'Special'),
        ('Yugo GV', 2000, 70, 'Special'),
        ('DeLorean DMC-12', 25000, 110, 'Special'),
        ('Trabant 601', 1000, 70, 'Special'),
        ('Reliant Robin', 5000, 70, 'Special'),
        ('AMC Pacer', 2000, 85, 'Special'),
        ('BMW Isetta', 10000, 50, 'Special'),
        ('Tata Nano', 2500, 65, 'Special'),
        ('Chevrolet Corvair', 10000, 100, 'Special'),
        ('Ford Pinto', 3000, 100, 'Special'),
        ('Cadillac Eldorado', 30000, 100, 'Special'),
        ('Plymouth Prowler', 30000, 120, 'Special'),
        ('Chevrolet SSR', 30000, 125, 'Special'),
        ('Mitsubishi i-MiEV', 20000, 80, 'Special'),
        ('Suzuki X-90', 15000, 90, 'Special'),
        ('Pontiac Aztek', 5000, 110, 'Special')
    ],
    'Celestial': [

        ('Mercedes-Maybach S 650 Cabriolet', 300000, 155, 'Celestial'),
        ('Rolls-Royce Arcadia Droptail', 38000000, 150, 'Celestial'),
        ('Mercedes-Maybach G 650 Landaulet', 850000, 112, 'Celestial'),
        ('Aston Martin Lagonda Taraf', 1000000, 195, 'Celestial'),
        ('Rolls-Royce Phantom Oribe', 450000, 155, 'Celestial'),
        ('Rolls-Royce 40/50 HP Silver Ghost Skiff', 1120000, 60, 'Celestial'),
        ('Rolls-Royce Phantom Oribe', 450000, 155, 'Celestial'),
        ('Maybach Zeppelin', 1800000, 150, 'Celestial'),
        ('Rolls-Royce Phantom VIII', 450000, 155, 'Celestial'),
        ('2009 Bentley Azure T', 650000, 179, 'Celestial'),
        ('Rolls-Royce Amethyst Droptail', 40000000, 155, 'Celestial'),
        ('Rolls-Royce Silver Ghost Piccadilly Roadster', 1330000, 78, 'Celestial'),
        ('Rolls-Royce Phantom II Continental Berline', 1760000, 90, 'Celestial'),
        ('Rolls-Royce 10 HP', 7040000, 39, 'Celestial'),
        ('Rolls-Royce Ghost Extended', 400000, 155, 'Celestial'),
        ('Rolls-Royce Black Badge Ghost', 350000, 155, 'Celestial'),
        ('Bentley Arnage', 200000, 180, 'Celestial'),
        ('Rolls-Royce Silver Cloud', 300000, 130, 'Celestial'),
        ('Maybach 57', 380000, 155, 'Celestial'),
        ('Rolls-Royce Silver Wraith', 250000, 130, 'Celestial'),
        ('Aston Martin DB5', 4500000, 145, 'Celestial'),
        ('Jaguar XJ', 100000, 150, 'Celestial'),
        ('Cadillac Escalade ESV', 100000, 130, 'Celestial'),
        ('Lincoln Continental', 90000, 130, 'Celestial'),
        ('Chrysler Imperial', 85000, 130, 'Celestial'),
        ('Mercedes-Maybach S600 Pullman', 1500000, 130, 'Celestial'),
        ('Range Rover SVAutobiography', 220000, 155, 'Celestial'),
        ('Rolls-Royce Phantom', 450000, 155, 'Celestial'),
        ('Lexus LS 500', 100000, 130, 'Celestial'),
        ('Audi A8', 90000, 130, 'Celestial'),
        ('BMW 7 Series', 85000, 130, 'Celestial'),
        ('Genesis G90', 70000, 130, 'Celestial'),
        ('Maserati Quattroporte', 120000, 180, 'Celestial'),
        ('1967 Porsche 907', 4200000, 184, 'Celestial'),
        ('mclaren M6GT', 430000, 180, 'Celestial'),
        ('Tesla Model X', 81000, 155, 'Celestial'),
        ('Lexus LS', 76000, 130, 'Celestial'),
        ('1965 Shelby GT350', 175000, 135, 'Celestial'),
        ('Mercedes-Benz S-Class', 94000, 155, 'Celestial'),
        ('Audi S8', 120000, 190, 'Celestial'),
        ('BMW Alpina B7', 140000, 205, 'Celestial')
    ],
    'Ultimate': [
        ('Pagani Zonda Revolucion', 3000000, 233, 'Ultimate'),
        ('Bugatti Chiron Pur Sport', 3600000, 261, 'Ultimate'),
        ('Lamborghini Aventador SVJ', 500000, 217, 'Ultimate'),
        ('Lamborghini Sesto Elemento', 2800000, 221, 'Ultimate'),
        ('Pagani Huayra Roadster BC', 3700000, 238, 'Ultimate'),
        ('Vector M12', 250000, 189, 'Ultimate'),
        ('Lancia Stratos HF', 600000, 144, 'Ultimate'),
        ('Ferrari 512 BB', 300000, 174, 'Ultimate'),
        ('Lamborghini Miura', 1700000, 170, 'Ultimate'),
        ('Porsche 959', 1500000, 198, 'Ultimate'),
        ('Jaguar XJ220', 600000, 212, 'Ultimate'),
        ('Bugatti EB110', 500000, 213, 'Ultimate'),
        ('Ferrari F40', 1200000, 201, 'Ultimate'),
        ('Porsche Carrera GT', 500000, 205, 'Ultimate'),
        ('Lamborghini Reventon', 1600000, 211, 'Ultimate'),
        ('Ferrari J50', 2500000, 211, 'Ultimate')
    ],
    'Transcendent': [
        ('Rolls-Royce Sweptail', 13000000, 150, 'Transcendent'),
        ('Mercedes-Benz Maybach Exelero', 8000000, 218, 'Transcendent'),
        ('Koenigsegg CCXR Trevita', 4800000, 254, 'Transcendent'),
        ('Lamborghini Veneno Roadster', 4500000, 221, 'Transcendent'),
        ('Lykan Hypersport', 3400000, 245, 'Transcendent'),
        ('Aston Martin Valkyrie', 3000000, 220, 'Transcendent'),
        ('Pagani Huayra BC', 2800000, 238, 'Transcendent'),
        ('Pagani Huayra Codalunga', 7000000, 217, 'Transcendent'),
        ('Ferrari Pininfarina Sergio', 3000000, 199, 'Transcendent'),
        ('Bugatti Centodieci', 9000000, 236, 'Transcendent'),
        ('Aston Martin Victor', 3000000, 220, 'Transcendent'),
        ('McLaren Speedtail', 2250000, 250, 'Transcendent'),
        ('McLaren Senna GTR', 1370000, 208, 'Transcendent'),
        ('McLaren Senna', 1430000, 208, 'Transcendent'),
        ('Ferrari LaFerrari Aperta', 2200000, 217, 'Transcendent'),
        ('Koenigsegg Jesko', 3000000, 330, 'Transcendent'),
        ('Rolls-Royce Phantom Gold', 8100000, 155, 'Transcendent'),
        ('1999 Bentley Hunaudières', 4000000, 220, 'Transcendent'),
        ('1996 Bentley Rapier', 4500000, 158, 'Transcendent'),
        ('1930 Bentley Speed Six Open Tourer', 5700000, 148, 'Transcendent'),
        ('1982 Porsche 956', 10120000, 225, 'Transcendent'),
        ('Lamborghini Aventador SVJ', 517000, 217, 'Transcendent'),
        ('Bugatti Chiron Super Sport 300+', 4000000, 304, 'Transcendent'),
        ('SSC Tuatara', 2000000, 283, 'Transcendent'),
        ('Aston Martin DB11', 200000, 200, 'Transcendent'),
        ('Porsche 911 Turbo S', 200000, 205, 'Transcendent'),
        ('McLaren 765LT', 400000, 205, 'Transcendent'),
        ('McLaren 765LT Spider', 415000, 205, 'Transcendent'),
        ('Lamborghini Huracan STO', 330000, 192, 'Transcendent'),
        ('Mercedes-AMG GT Black Series', 300000, 202, 'Transcendent'),
        ('Lamborghini Aventador S', 400000, 217, 'Transcendent'),
        ('Ferrari 488 Pista', 350000, 211, 'Transcendent'),
        ('Koenigsegg Regera', 2100000, 255, 'Transcendent')
    ],
    'Supreme': [
        ('Bugatti Centodieci', 9000000, 236, 'Supreme'),
        ('Lamborghini Sian FKP 37', 3600000, 220, 'Supreme'),
        ('Pagani Zonda HP Barchetta', 17500000, 221, 'Supreme'),
        ('Rolls-Royce Boat Tail', 28000000, 155, 'Supreme'),
        ('Bentley Mulliner Bacalar', 1900000, 200, 'Supreme'),
        ('1970 Porsche 917K', 14080000, 198, 'Supreme'),
        ('Bugatti Divo', 5800000, 236, 'Supreme'),
        ('Porsche 911 GT1', 5670000, 191, 'Supreme'),
        ('Rolls-Royce Droptail', 30000000, 155, 'Supreme'),
        ('Tesla Roadster', 250000, 250, 'Supreme'),
        ('Lamborghini Sian', 3600000, 220, 'Supreme'),
        ('Ferrari Monza SP2', 1800000, 186, 'Supreme'),
        ('Lamborghini Centenario LP 770-4', 2500000, 217, 'Supreme'),
        ('Bugatti La Voiture Noire', 18680000, 261, 'Supreme'),
        ('Koenigsegg CCXR Trevita', 4800000, 254, 'Supreme'),
        ('Lamborghini Veneno Roadster', 4500000, 221, 'Supreme'),
        ('McLaren P1 LM', 3600000, 217, 'Supreme'),
        ('McLaren P1 GTR', 3100000, 217, 'Supreme'),
        ('Lykan Hypersport', 3400000, 245, 'Supreme'),
        ('Ferrari Pininfarina Sergio', 3000000, 199, 'Supreme'),
        ('Koenigsegg Jesko Absolut', 3000000, 330, 'Supreme'),
        ('Bugatti Chiron', 3000000, 261, 'Supreme'),
        ('Lamborghini Sian', 3600000, 220, 'Supreme'),
        ('Bugatti Bolide', 5000000, 311, 'Supreme'),
        ('Porsche 918 Spyder', 3937500, 214, 'Supreme'),
        ('Ferrari SF90 Stradale', 500000, 211, 'Supreme'),
        ('Lamborghini Aventador S', 400000, 217, 'Supreme'),
        ('Lamborghini Aventador SVJ', 500000, 217, 'Supreme'),
        ('Lamborghini Sesto Elemento', 2800000, 221, 'Supreme'),
        ('Vector W8', 450000, 242, 'Supreme'),
        ('Lancia Stratos HF', 600000, 144, 'Supreme'),
        ('Ferrari 512 BB', 300000, 174, 'Supreme'),
        ('Porsche 959', 1500000, 198, 'Supreme'),
        ('Jaguar XJ220', 600000, 212, 'Supreme'),
        ('Porsche Carrera', 500000, 205, 'Supreme'),
        ('McLaren Solus GT', 4000000, 200, 'Supreme'),
        ('McLaren F1', 14000000, 240, 'Supreme')
    ],
    'Legendary Classics': [
        ('1963 Ferrari 250 GTO', 70000000, 174, 'Legendary Classics'),
        ('1957 Ferrari 335 S', 35000000, 190, 'Legendary Classics'),
        ('1954 Mercedes-Benz W196', 30000000, 186, 'Legendary Classics'),
        ('1956 Ferrari 290 MM', 28000000, 177, 'Legendary Classics'),
        ('1967 Ferrari 275 GTB/4*S NART Spider', 27500000, 166, 'Legendary Classics'),
        ('1964 Ferrari 275 GTB/C Speciale', 26000000, 167, 'Legendary Classics'),
        ('1955 Jaguar D-Type', 23000000, 172, 'Legendary Classics'),
        ('1961 Ferrari 250 GT SWB California Spider', 18500000, 150, 'Legendary Classics'),
        ('1956 Aston Martin DBR1', 22500000, 160, 'Legendary Classics'),
        ('1962 Aston Martin DB4GT Zagato', 14000000, 153, 'Legendary Classics'),
        ('Mercedes-Benz 300 SLR Gullwing Uhlenhaut', 142500000, 180, 'Legendary Classics'),
        ('1966 Ford GT40', 12000000, 210, 'Legendary Classics'),
        ('1967 Chevrolet Corvette Sting Ray', 300000, 150, 'Legendary Classics'),
        ('1970 Plymouth Hemi Cuda', 1000000, 155, 'Legendary Classics'),
        ('1969 Dodge Charger Daytona', 900000, 155, 'Legendary Classics'),
        ('1961 Jaguar E-Type', 150000, 150, 'Legendary Classics'),
        ('1955 Mercedes-Benz 300SL Gullwing', 4000000, 161, 'Legendary Classics'),
        ('1971 Lamborghini Miura SV', 3000000, 180, 'Legendary Classics'),
        ('1969 Chevrolet Camaro ZL1', 700000, 150, 'Legendary Classics'),
        ('1955 Porsche 356 Speedster', 300000, 110, 'Legendary Classics'),
        ('1966 Shelby Cobra 427', 2000000, 160, 'Legendary Classics'),
        ('1963 Corvette Sting Ray Split-Window', 200000, 140, 'Legendary Classics'),
        ('1953 Chevrolet Corvette', 500000, 120, 'Legendary Classics'),
        ('1969 Ford Mustang Boss 429', 500000, 140, 'Legendary Classics'),
        ('1965 Aston Martin DB5', 4500000, 145, 'Legendary Classics'),
        ('1957 BMW 507', 2000000, 130, 'Legendary Classics'),
        ('1974 Lancia Stratos', 500000, 140, 'Legendary Classics'),
        ('1956 Porsche 550 Spyder', 5000000, 130, 'Legendary Classics'),
        ('1968 Ferrari 365 GTB/4 Daytona', 3000000, 160, 'Legendary Classics'),
        ('1962 Maserati 3500 GT', 500000, 130, 'Legendary Classics'),
        ('1964 AC Cobra', 1000000, 160, 'Legendary Classics'),
        ('1963 Aston Martin DB4GT', 3500000, 145, 'Legendary Classics'),
        ('1932 Bentley', 7060000, 140, 'Legendary Classics'),
        ('1957 Ferrari 250 GT California Spyder', 18000000, 150, 'Legendary Classics'),
        ('1955 Mercedes-Benz 300 SLR', 100000000, 180, 'Legendary Classics'),
        ('1964 Ferrari 250 LM', 17000000, 160, 'Legendary Classics'),
        ('1966 Ferrari 330 P3', 40000000, 180, 'Legendary Classics'),
        ('1967 Ferrari 330 P4', 45000000, 180, 'Legendary Classics'),
        ('1965 Ferrari 275 GTB', 3000000, 160, 'Legendary Classics'),
        ('1972 Ferrari Dino 246 GT', 400000, 150, 'Legendary Classics'),
        ('1970 Plymouth Superbird', 200000, 150, 'Legendary Classics'),
        ('1965 Ford GT40', 5000000, 210, 'Legendary Classics'),
        ('La Marquise', 4600000, 38, 'Legendary Classics'),
        ('1963 Jaguar E-Type', 150000, 150, 'Legendary Classics'),
        ('1969 Dodge Charger', 100000, 150, 'Legendary Classics'),
        ('1966 Ferrari 365 GTB/4 Daytona', 3000000, 160, 'Legendary Classics'),
        ('1962 Shelby Cobra', 5000000, 160, 'Legendary Classics')
    ],
    'Unreal': [
        ('Devel Sixteen', 1800000, 350, 'Unreal'),
        ('Ferrari P4/5 by Pininfarina', 4000000, 233, 'Unreal'),
        ('McLaren F1 LM', 30000000, 225, 'Unreal'),
        ('Duesenberg SSJ', 22000000, 140, 'Unreal'),
        ('Bugatti Type 57SC Atlantic', 160000000, 130, 'Unreal'),
        ('Rolls-Royce 15 HP', 35000000, 60, 'Unreal'),
        ('McLaren F1 Chassis 39', 25000000, 243, 'Unreal')
    ]
    }




# Utility functions
def format_money(value):
    if value < 1e3:
        return str(value)
    elif value < 1e6:
        return f"{value/1e3:.1f}K"
    elif value < 1e9:
        return f"{value/1e6:.1f}M"
    elif value < 1e12:
        return f"{value/1e9:.1f}B"
    elif value < 1e15:
        return f"{value/1e12:.1f}T"
    else:
        return f"{value/1e15:.1f}Q"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
NEON_GREEN = (57, 255, 20)
DARK_RED = (139, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (50, 50, 200)
BUTTON_TEXT_COLOR = WHITE



class Button:
    def __init__(self, color, x, y, width, height, text='', text_color=WHITE, hover_color=BUTTON_HOVER_COLOR):
        self.color = color
        self.hover_color = hover_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.hover = False

    def draw(self, win, outline=None):
        if self.hover:
            pygame.draw.rect(win, self.hover_color, (self.x, self.y, self.width, self.height), border_radius=10)
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), border_radius=10)
        if self.text != '':
            font = pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.04))
            text = font.render(self.text, True, self.text_color)
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def update(self, pos):
        self.hover = self.is_over(pos)




# Create buttons
open_box_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.3), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Open Box')
inventory_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.365), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Inventory')
probability_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.27), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Probability')
race_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.43), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Drag Race')
safe_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.495), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Safe')
car_index_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.2), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Car Index')
achievements_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.34), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Achievements')
boxes_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.56), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Boxes')
back_button = Button(BUTTON_COLOR, 20, SCREEN_HEIGHT - 100, int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Back to Menu')
sort_button = Button(BUTTON_COLOR, SCREEN_WIDTH - 220, 80, 200, 40, 'Sort by Speed')
next_page_button = Button(BUTTON_COLOR, SCREEN_WIDTH - 220, SCREEN_HEIGHT - 60, 200, 40, 'Next Page')
prev_page_button = Button(BUTTON_COLOR, 20, SCREEN_HEIGHT - 60, 200, 40, 'Previous Page')
deposit_money_button = Button(BUTTON_COLOR, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 200, 200, 40, 'Deposit Money')
withdraw_money_button = Button(BUTTON_COLOR, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 150, 200, 40, 'Withdraw Money')
deposit_car_button = Button(BUTTON_COLOR, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 250, 200, 40, 'Deposit Car')
withdraw_car_button = Button(BUTTON_COLOR, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 40, 'Withdraw Car')
sell_duplicates_button = Button(BUTTON_COLOR, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50, 200, 40, 'Sell Duplicates')
sort_by_speed_button = Button(BUTTON_COLOR, SCREEN_WIDTH - 420, 80, 200, 40, 'Sort by Speed')
sort_by_rarity_button = Button(BUTTON_COLOR, SCREEN_WIDTH - 620, 80, 200, 40, 'Sort by Rarity')
sort_by_price_button = Button(BUTTON_COLOR, SCREEN_WIDTH - 220, 80, 200, 40, 'Sort by Price')
save_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.41), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Save Game')
load_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.48), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Load Game')
list_car_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.69), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'List Car for Trade')
global_market_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.755), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Global Market')
coinflip_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.625), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Coinflip')
stats_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.55), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Statistics')
upgrade_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * 0.82), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Upgrade Click')
settings_button = Button(BUTTON_COLOR, 20, int(SCREEN_HEIGHT * .885), int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.07), 'Settings')




# Helper functions
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def apply_modifiers(car):
    name, price, speed, rarity = car
    neon = random.random() < 0.01
    nitro = random.random() < 0.01
    if neon and nitro:
        name = f"N{name}"
        price *= 1.3
        speed += 15
    elif neon:
        name = f"N{name}"
        price *= 1.1
        speed += 5
    elif nitro:
        name = f"N{name}"
        price *= 1.1
        speed += 10
    return name, price, speed, rarity, neon, nitro

def boxes_screen():
    global current_screen, money
    screen.fill(WHITE)
    draw_text('Boxes', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, 20, 20)

    # Define box types with adjusted probabilities
    boxes = [
        {"name": "Normal Box", "price": 20000, "probabilities": {'Common': 40, 'Uncommon': 30, 'Rare': 15, 'Epic': 7, 'Legendary': 5, 'Mythical': 2, 'Exotic': 0.5, 'Special': 0.25, 'Celestial': 0.1, 'Ultimate': 0.05, 'Transcendent': 0.02, 'Supreme': 0.01, 'Legendary Classics': 0.005, 'Unreal': 0.000001}},
        {"name": "Drag Race Box", "price": 30000, "probabilities": {'Common': 30, 'Uncommon': 30, 'Rare': 20, 'Epic': 10, 'Legendary': 7, 'Mythical': 2.5, 'Exotic': 0.75, 'Special': 0.5, 'Celestial': 0.25, 'Ultimate': 0.1, 'Transcendent': 0.05, 'Supreme': 0.03, 'Legendary Classics': 0.01, 'Unreal': 0.000005}},
        {"name": "Luxury Box", "price": 50000, "probabilities": {'Common': 20, 'Uncommon': 25, 'Rare': 25, 'Epic': 15, 'Legendary': 10, 'Mythical': 3, 'Exotic': 1, 'Special': 0.75, 'Celestial': 0.5, 'Ultimate': 0.2, 'Transcendent': 0.1, 'Supreme': 0.05, 'Legendary Classics': 0.02, 'Unreal': 0.00002}},
        {"name": "Speed Box", "price": 80000, "probabilities": {'Common': 15, 'Uncommon': 20, 'Rare': 25, 'Epic': 20, 'Legendary': 12, 'Mythical': 5, 'Exotic': 1.5, 'Special': 1, 'Celestial': 0.75, 'Ultimate': 0.3, 'Transcendent': 0.15, 'Supreme': 0.1, 'Legendary Classics': 0.05, 'Unreal': 0.00005}},
        {"name": "Mythical Box", "price": 500000, "probabilities": {'Common': 2, 'Uncommon': 5, 'Rare': 10, 'Epic': 15, 'Legendary': 20, 'Mythical': 25, 'Exotic': 10, 'Special': 5, 'Celestial': 3, 'Ultimate': 1.5, 'Transcendent': 1, 'Supreme': 0.5, 'Legendary Classics': 0.3, 'Unreal': 0.0002}},
        {"name": "Ultimate Box", "price": 1000000, "probabilities": {'Common': 0.5, 'Uncommon': 1.5, 'Rare': 3, 'Epic': 7, 'Legendary': 10, 'Mythical': 15, 'Exotic': 20, 'Special': 15, 'Celestial': 10, 'Ultimate': 7, 'Transcendent': 5, 'Supreme': 3, 'Legendary Classics': 2, 'Unreal': 0.001}},
        {"name": "Jackpot Box", "price": 2000000, "probabilities": {'Common': 0.05, 'Uncommon': 0.2, 'Rare': 0.5, 'Epic': 2, 'Legendary': 3, 'Mythical': 5, 'Exotic': 7, 'Special': 10, 'Celestial': 15, 'Ultimate': 20, 'Transcendent': 15, 'Supreme': 10, 'Legendary Classics': 7, 'Unreal': 0.005}},
        {"name": "God Box", "price": 5000000, "probabilities": {'Common': 0.005, 'Uncommon': 0.02, 'Rare': 0.05, 'Epic': 0.2, 'Legendary': 0.5, 'Mythical': 1, 'Exotic': 2, 'Special': 3, 'Celestial': 5, 'Ultimate': 7, 'Transcendent': 10, 'Supreme': 15, 'Legendary Classics': 20, 'Unreal': 0.01}},
        {"name": "Unreal Box", "price": 10000000, "probabilities": {'Common': 0.005, 'Uncommon': 0.02, 'Rare': 0.05, 'Epic': 0.1, 'Legendary': 0.5, 'Mythical': 1, 'Exotic': 0.2, 'Special': 0.5, 'Celestial': 1, 'Ultimate': 2, 'Transcendent': 3, 'Supreme': 5, 'Legendary Classics': 30, 'Unreal': 0.05}},
    ]


    start_y = 60
    box_buttons = []

    for box in boxes:
          box_button = Button(BUTTON_COLOR, 40, start_y, SCREEN_WIDTH - 80, 40, f"{box['name']} - ${format_money(box['price'])}", WHITE)
          box_buttons.append((box_button, box))
          start_y += 40

    for box_button, box in box_buttons:
          box_button.draw(screen, BLACK)

    back_button.draw(screen, BLACK)

    for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN:
              pos = pygame.mouse.get_pos()
              if event.button == 1:  # Left click
                  if back_button.is_over(pos):
                      current_screen = 'main_menu'
                  for box_button, box in box_buttons:
                      if box_button.is_over(pos):
                          print(open_box(box))
                          break
          if event.type == pygame.MOUSEMOTION:
              pos = pygame.mouse.get_pos()
              back_button.update(pos)
              for box_button, _ in box_buttons:
                  box_button.update(pos)


def upgrade_click_power():
    global money, MONEY_PER_CLICK, upgrade_cost, upgrade_increment
    if money >= upgrade_cost:
        money -= upgrade_cost
        MONEY_PER_CLICK += 100  # Adjust this value as needed
        upgrade_cost += upgrade_increment
        upgrade_button.text = f'Upgrade Click Power: ${format_money(upgrade_cost)}'

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if event.button == 1:  # Left click
            if upgrade_button.is_over(pos):
                upgrade_click_power()
            # Handle other buttons similarly...

    if event.type == pygame.MOUSEMOTION:
        pos = pygame.mouse.get_pos()
        upgrade_button.update(pos)

pygame.display.flip()



def open_box(box):
      global money, inventory, boxes_opened, total_cars_owned
      if money >= box['price']:
          money -= box['price']
          boxes_opened += 1
          rarity = random.choices(CAR_RARITIES, weights=[box['probabilities'].get(rarity, 0) for rarity in CAR_RARITIES], k=1)[0]
          car = random.choice(CAR_DATA[rarity])
          car = apply_modifiers(car)
          inventory.append(car)
          total_cars_owned += 1
          check_achievements()
          return f"You got a {rarity} car: {car[0]}!"
      else:
          return "Not enough money to open a box."




def find_fastest_car(cars_owned):
    if not cars_owned:  # Check if the list is empty
        return None
    return max(cars_owned, key=lambda car: car['speed'])  # Find the car with the highest speed




def sell_car(index):
    global money, inventory
    if 0 <= index < len(inventory):
        car = inventory.pop(index)
        money += car[1]
        check_achievements()
        return f"You sold {car[0]} for ${format_money(car[1])}."
    else:
        return "Invalid selection."

def sell_duplicates():
    global money, inventory
    car_counter = Counter((car[0], car[4], car[5]) for car in inventory)
    for car_key, count in car_counter.items():
        if count > 1:
            for _ in range(count - 1):
                for car in inventory:
                    if (car[0], car[4], car[5]) == car_key:
                        inventory.remove(car)
                        money += car[1]
                        break
    check_achievements()

def check_achievements():
    global races_won, boxes_opened, total_cars_owned, safe_money
    # Check achievements and quests
    if not achievements[0]["completed"] and boxes_opened >= 1:
        achievements[0]["completed"] = True
    if not achievements[1]["completed"] and money >= 1000000:
        achievements[1]["completed"] = True
    if not achievements[2]["completed"] and total_cars_owned >= 10:
        achievements[2]["completed"] = True
    if not achievements[3]["completed"] and races_won >= 5:
        achievements[3]["completed"] = True
    if not achievements[4]["completed"] and money >= 10000000:
        achievements[4]["completed"] = True
    if not achievements[5]["completed"] and any(car[2] > 250 for car in inventory):
        achievements[5]["completed"] = True
    if not achievements[6]["completed"] and boxes_opened >= 50:
        achievements[6]["completed"] = True
    if not achievements[7]["completed"] and money >= 1000000000:
        achievements[7]["completed"] = True
    if not achievements[8]["completed"] and sum(1 for car in inventory if car[5]) >= 5:
        achievements[8]["completed"] = True
    if not achievements[9]["completed"] and sum(1 for car in inventory if car[4]) >= 5:
        achievements[9]["completed"] = True
    if not achievements[10]["completed"] and sum(1 for car in inventory if car[3] == 'Legendary') >= 5:
        achievements[10]["completed"] = True
    if not achievements[11]["completed"] and sum(1 for car in inventory if car[3] == 'Mythical') >= 3:
        achievements[11]["completed"] = True
    if not achievements[12]["completed"] and races_won >= 10:
        achievements[12]["completed"] = True
    if not achievements[13]["completed"] and safe_money >= 1000000:
        achievements[13]["completed"] = True
    if not achievements[14]["completed"] and safe_money * 0.05 >= 100000:
        achievements[14]["completed"] = True
    if not achievements[15]["completed"] and sum(1 for car in inventory if car) >= 20:
        achievements[15]["completed"] = True
    if not achievements[16]["completed"] and sum(1 for car in inventory if car[3] == 'Rare') >= 10:
        achievements[16]["completed"] = True
    if not achievements[17]["completed"] and sum(1 for car in inventory if car[3] == 'Ultimate') >= 2:
        achievements[17]["completed"] = True
    if not achievements[18]["completed"] and total_cars_owned >= 20:
        achievements[18]["completed"] = True
    if not achievements[19]["completed"] and any(car[2] > 300 for car in inventory):
        achievements[19]["completed"] = True
    if not achievements[20]["completed"] and any(car[3] == 'Transcendent' for car in inventory):
        achievements[20]["completed"] = True
    if not achievements[21]["completed"] and any(car[3] == 'Supreme' and races_won > 0 for car in inventory):
        achievements[21]["completed"] = True
    if not achievements[22]["completed"] and sum(1 for car in inventory if car[3] == 'Exotic') >= 3:
        achievements[22]["completed"] = True
    if not achievements[23]["completed"] and any(car[1] > 1000000 for car in inventory):
        achievements[23]["completed"] = True
    if not achievements[24]["completed"] and boxes_opened >= 100:
        achievements[24]["completed"] = True
    if not achievements[25]["completed"] and safe_money >= 10000000:
        achievements[25]["completed"] = True
    if not achievements[26]["completed"] and any(car[3] == 'Ultimate' for car in inventory):
        achievements[26]["completed"] = True
    if not achievements[27]["completed"] and any(car[3] == 'Legendary' and races_won > 0 for car in inventory):
        achievements[27]["completed"] = True
    if not achievements[28]["completed"] and total_cars_owned >= 50:
        achievements[28]["completed"] = True
    if not achievements[29]["completed"] and sum(1 for car in inventory if car[3] == 'Celestial') >= 2:
        achievements[29]["completed"] = True

    # Check quests
    if not quests[0]["completed"] and len(inventory) >= 5:
        quests[0]["completed"] = True
    if not quests[1]["completed"] and races_won >= 3:
        quests[1]["completed"] = True

def calculate_interest_rate(safe_balance):
    if safe_balance < 100000:
        return 0.05
    elif safe_balance < 1000000:
        return 0.03
    elif safe_balance < 10000000:
        return 0.02
    elif safe_balance < 100000000:
        return 0.01
    else:
        return 0.005

def generate_trade_offer():
    rarity = random.choices(CAR_RARITIES, weights=list(RARITY_PROBABILITIES.values()), k=1)[0]
    car = random.choice(CAR_DATA[rarity])
    car = apply_modifiers(car)

    offer_type = random.choice(['sell', 'trade', 'trade_plus_money', 'buy'])
    if offer_type == 'sell':
        price_multiplier = 1 + random.uniform(0.5, 1.5)
        offer = {'type': 'sell', 'car': car, 'price': car[1] * price_multiplier}
    elif offer_type == 'trade':
        trade_rarity = random.choices(CAR_RARITIES, weights=list(RARITY_PROBABILITIES.values()), k=1)[0]
        trade_car = random.choice(CAR_DATA[trade_rarity])
        trade_car = apply_modifiers(trade_car)
        offer = {'type': 'trade', 'car': car, 'trade_for': trade_car}
    elif offer_type == 'trade_plus_money':
        trade_rarity = random.choices(CAR_RARITIES, weights=list(RARITY_PROBABILITIES.values()), k=1)[0]
        trade_car = random.choice(CAR_DATA[trade_rarity])
        trade_car = apply_modifiers(trade_car)
        price_difference = car[1] - trade_car[1]
        if price_difference > 0:
            offer = {'type': 'trade_plus_money', 'car': car, 'trade_for': trade_car, 'money': price_difference}
        else:
            offer = {'type': 'trade_plus_money', 'car': trade_car, 'trade_for': car, 'money': -price_difference}
    else:  # buy
        price_multiplier = 1 + random.uniform(0.5, 1.5)
        offer = {'type': 'buy', 'car': car, 'price': car[1] * price_multiplier}

    trade_offers.append(offer)

def evaluate_trade_quality(offer):
    if offer['type'] == 'sell' or offer['type'] == 'buy':
        quality = offer['price'] / offer['car'][1]
        if quality < 0.8:
            return NEON_GREEN  # Very good
        elif quality < 1:
            return GREEN  # Good
        elif quality < 1.2:
            return YELLOW  # Okay
        elif quality < 1.5:
            return ORANGE  # Bad
        else:
            return RED  # Very bad
    elif offer['type'] == 'trade':
        quality = offer['car'][1] / offer['trade_for'][1]
        if quality < 0.8:
            return NEON_GREEN  # Very good
        elif quality < 1:
            return GREEN  # Good
        elif quality < 1.2:
            return YELLOW  # Okay
        elif quality < 1.5:
            return ORANGE  # Bad
        else:
            return RED  # Very bad
    elif offer['type'] == 'trade_plus_money':
        quality = (offer['car'][1] + offer['money']) / offer['trade_for'][1]
        if quality < 0.8:
            return NEON_GREEN  # Very good
        elif quality < 1:
            return GREEN  # Good
        elif quality < 1.2:
            return YELLOW  # Okay
        elif quality < 1.5:
            return ORANGE  # Bad
        else:
            return RED  # Very bad

def bot_buy_car():
    global trade_offers, inventory, money
    if trade_offers:
        player_offers = [offer for offer in trade_offers if offer.get('is_player_listed')]
        if player_offers:
            offer = random.choice(player_offers)
            if offer['type'] == 'sell':
                # Ensure the car being bought by the bot is not in the player's inventory
                if offer['car'] in inventory:
                    inventory.remove(offer['car'])
                money += offer['price']
                trade_offers.remove(offer)
                print(f"Bot bought {offer['car'][0]} for ${format_money(offer['price'])}")

def main_menu():
    global money, current_screen, next_trade_tick, next_bot_trade_tick
    screen.fill(DARK_GRAY)
    draw_text('Car Collection Game', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), WHITE, screen, 20, 20)
    draw_text(f"Money: ${format_money(money)}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), WHITE, screen, 20, 80)
    draw_text('Click to earn money', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), WHITE, screen, 20, 120)
    draw_text('Boxes cost $20k', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), WHITE, screen, 20, 160)

    # Draw buttons
    open_box_button.draw(screen)
    inventory_button.draw(screen)
    race_button.draw(screen)
    safe_button.draw(screen)
    list_car_button.draw(screen)
    global_market_button.draw(screen)
    coinflip_button.draw(screen)
    boxes_button.draw(screen)
    settings_button.draw(screen)  # Ensure settings_button is drawn
    upgrade_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                if open_box_button.is_over(pos):
                    print(open_box({"name": "Normal Box", "price": 20000, "probabilities": {'Common': 50, 'Uncommon': 30, 'Rare': 15, 'Epic': 3, 'Legendary': 1}}))  # Default to Normal Box
                elif inventory_button.is_over(pos):
                    current_screen = 'inventory'
                elif race_button.is_over(pos):
                    current_screen = 'drag_race'
                elif safe_button.is_over(pos):
                    current_screen = 'safe'
                elif list_car_button.is_over(pos):
                    current_screen = 'list_car'
                elif global_market_button.is_over(pos):
                    current_screen = 'global_market'
                elif coinflip_button.is_over(pos):
                    current_screen = 'coinflip'
                elif boxes_button.is_over(pos):
                    current_screen = 'boxes'
                elif settings_button.is_over(pos):
                    current_screen = 'settings'
                elif upgrade_button.is_over(pos):
                    upgrade_click_power()
                else:
                    money += MONEY_PER_CLICK
                    check_achievements()
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            open_box_button.update(pos)
            inventory_button.update(pos)
            race_button.update(pos)
            safe_button.update(pos)
            list_car_button.update(pos)
            global_market_button.update(pos)
            coinflip_button.update(pos)
            boxes_button.update(pos)
            settings_button.update(pos)  # Ensure settings_button is updated on mouse hover
            upgrade_button.update(pos)




# Generate new trade offers periodically
if time.time() >= next_trade_tick:
    generate_trade_offer()
    next_trade_tick = time.time() + TRADE_TICK_INTERVAL

# Bot buys car from the market
if time.time() >= next_bot_trade_tick:
    bot_buy_car()
    next_bot_trade_tick = time.time() + BOT_TRADE_INTERVAL


def drag_race_screen():
    global current_screen, selected_car, money, race_in_progress, player_car_pos, opponent_car_pos, opponent_car, race_start_time, race_page, races_won, sort_by_speed, sort_by_price
    screen.fill(WHITE)
    draw_text('Drag Race', pygame.font.SysFont(None, 50), BLACK, screen, 20, 20)

    if race_in_progress:
        # Draw the road
        road_color = (50, 50, 50)
        lane_color = (255, 255, 255)
        road_height = 150
        pygame.draw.rect(screen, road_color, (0, SCREEN_HEIGHT // 2 - road_height // 2, SCREEN_WIDTH, road_height))

        # Draw lane dividers
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(screen, lane_color, (i, SCREEN_HEIGHT // 2), (i + 20, SCREEN_HEIGHT // 2), 2)

        elapsed_time = time.time() - race_start_time
        if elapsed_time > 7:
            race_in_progress = False
            result_text = ""
            if selected_car and opponent_car:
                if player_car_pos >= opponent_car_pos:
                    result_text = f"You won! Your {selected_car[0]} beat the {opponent_car[0]}!"
                    money_reward = selected_car[1] * 0.1
                    races_won += 1
                else:
                    result_text = f"You lost! Your {selected_car[0]} was beaten by the {opponent_car[0]}."
                    money_reward = -selected_car[1] * 0.1

                money += money_reward
                draw_text(result_text, pygame.font.SysFont(None, 36), BLACK, screen, 20, 120)
                draw_text(f"Money: ${format_money(money)}", pygame.font.SysFont(None, 36), BLACK, screen, 20, 160)
                check_achievements()
            selected_car = None
            opponent_car = None
        else:
            if selected_car and opponent_car:
                player_car_speed = selected_car[2] / 200
                opponent_car_speed = opponent_car[2] / 200

                player_car_pos += player_car_speed
                opponent_car_pos += opponent_car_speed

                pygame.draw.rect(screen, RARITY_COLORS[selected_car[3]], (player_car_pos, SCREEN_HEIGHT // 2 - 50, 50, 20))
                pygame.draw.rect(screen, RARITY_COLORS[opponent_car[3]], (opponent_car_pos, SCREEN_HEIGHT // 2 + 30, 50, 20))
    else:
        if selected_car:
            opponent_car = random.choice(random.choice(list(CAR_DATA.values())))
            opponent_car = apply_modifiers(opponent_car)
            player_car_pos = 0
            opponent_car_pos = 0
            race_start_time = time.time()
            race_in_progress = True
        else:
            draw_text('Select a car from your inventory', pygame.font.SysFont(None, 36), BLACK, screen, 20, 80)

            # Sort inventory based on criteria
            if sort_by_speed:
                sorted_inventory = sorted(inventory, key=lambda x: x[2], reverse=True)
            elif sort_by_price:
                sorted_inventory = sorted(inventory, key=lambda x: x[1], reverse=True)
            else:
                sorted_inventory = inventory

            start_y = 160
            cars_per_page = 10
            start_index = race_page * cars_per_page
            end_index = start_index + cars_per_page
            displayed_cars = sorted_inventory[start_index:end_index]

            car_rects = []
            for index, (car_name, car_price, car_speed, car_rarity, neon, nitro) in enumerate(displayed_cars):
                rarity_color = RARITY_COLORS[car_rarity]
                prefix_color = None
                prefix = ""

                if neon and nitro:
                    prefix_color = (NEON_GREEN, DARK_RED)
                    prefix = "N"
                elif neon:
                    prefix_color = (NEON_GREEN,)
                    prefix = "N"
                elif nitro:
                    prefix_color = (DARK_RED,)
                    prefix = "N"

                car_rect = pygame.Rect(40, start_y, SCREEN_WIDTH // 2, 21)  # Hitbox for the car name
                car_rects.append((car_rect, (car_name, car_price, car_speed, car_rarity, neon, nitro)))
                draw_text(f"{index + 1}. {car_name} - ${format_money(car_price)}, Speed: {car_speed} mph", pygame.font.SysFont(None, 21), rarity_color, screen, 60, start_y)

                # Draw prefixes
                if prefix:
                    for i, color in enumerate(prefix_color):
                        draw_text(prefix, pygame.font.SysFont(None, 21), color, screen, 40 + i * 15, start_y)

                start_y += 21  # Visual spacing

            sort_by_speed_button.draw(screen, BLACK)
            sort_by_price_button.draw(screen, BLACK)
            next_page_button.draw(screen, BLACK)
            prev_page_button.draw(screen, BLACK)

    back_button.draw(screen, BLACK)
    for event in pygame.event.get():  # Make sure this is placed correctly inside the loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
                    selected_car = None
                    opponent_car = None
                elif sort_by_speed_button.is_over(pos):
                    sort_by_speed = True
                    sort_by_price = False
                elif sort_by_price_button.is_over(pos):
                    sort_by_price = True
                    sort_by_speed = False
                elif next_page_button.is_over(pos) and end_index < len(inventory):
                    race_page += 1
                elif prev_page_button.is_over(pos) and race_page > 0:
                    race_page -= 1
                else:
                    for car_rect, car in car_rects:
                        if car_rect.collidepoint(pos):
                            selected_car = car
                            break
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            sort_by_speed_button.update(pos)
            sort_by_price_button.update(pos)
            next_page_button.update(pos)
            prev_page_button.update(pos)
            back_button.update(pos)

    if opponent_car:
        draw_text(f"Opponent Car: {opponent_car[0]}, Speed: {opponent_car[2]} mph", pygame.font.SysFont(None, 24), BLACK, screen, 20, 100)
        draw_text(f"Prize for Winning: ${format_money(selected_car[1] * 0.1)}", pygame.font.SysFont(None, 24), GREEN, screen, 20, 120)
        draw_text(f"Penalty for Losing: ${format_money(selected_car[1] * 0.1)}", pygame.font.SysFont(None, 24), RED, screen, 20, 140)






back_button.draw(screen, BLACK)
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if event.button == 1:
            if back_button.is_over(pos):
                current_screen = 'main_menu'
                selected_car = None
                opponent_car = None
    if event.type == pygame.MOUSEMOTION:
        pos = pygame.mouse.get_pos()
        back_button.update(pos)

def calculate_time_played(game_start_time, total_time_played):
    # Calculate elapsed time in the current session
    current_time = time.time()
    session_time = current_time - game_start_time

    # Total time played is the sum of previous sessions and the current one
    total_elapsed_time = total_time_played + session_time
    return total_elapsed_time

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"

# List to store owned cars
cars_owned = []

# Function to add a car to the list of cars owned
def add_car(name, speed):
    car = {'name': name, 'speed': speed}
    cars_owned.append(car)
    print(f"Car added: {car}")

# Function to return the current list of owned cars
def get_cars_owned():
    return cars_owned



def probability_screen():
    global current_screen
    screen.fill(WHITE)
    draw_text('Rarity Probabilities', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, 20, 20)
    start_y = 80

    for rarity in CAR_RARITIES:
        color = RARITY_COLORS[rarity]
        probability = RARITY_PROBABILITIES[rarity]
        draw_text(f"{rarity}: {probability}%", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.04)), color, screen, 20, start_y)
        start_y += 19

    # Add Nitro and Neon probabilities with colors
    draw_text("Nitro Chance: 1%", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.04)), DARK_RED, screen, 20, start_y)
    start_y += 23
    draw_text("Neon Chance: 1%", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.04)), NEON_GREEN, screen, 20, start_y)
    start_y += 23

    back_button.draw(screen, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                back_button.update(pos)



def safe_screen():
    global current_screen, safe_money, safe_inventory, inventory, money, safe_inventory_page, inventory_page, selected_car, sort_by_speed, sort_by_price
    screen.fill(WHITE)
    draw_text('Safe', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, 20, 20)
    draw_text(f"Money in Safe: ${format_money(safe_money)}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 60)
    draw_text(f"Total Money: ${format_money(money)}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 100)
    draw_text(f"Interest Rate: {calculate_interest_rate(safe_money) * 100:.2f}% per minute", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.04)), BLACK, screen, 20, 140)

    total_safe_value = sum(car[1] for car in safe_inventory)
    draw_text(f"Safe Car Value: ${format_money(total_safe_value)}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, SCREEN_WIDTH - 300, 20)

    # Draw buttons
    deposit_money_button.draw(screen, BLACK)
    withdraw_money_button.draw(screen, BLACK)
    deposit_car_button.draw(screen, BLACK)
    withdraw_car_button.draw(screen, BLACK)
    sort_by_speed_button.draw(screen, BLACK)
    sort_by_price_button.draw(screen, BLACK)
    next_page_button.draw(screen, BLACK)
    prev_page_button.draw(screen, BLACK)
    back_button.draw(screen, BLACK)

    # Sort safe inventory based on criteria
    if sort_by_speed:
        sorted_safe_inventory = sorted(safe_inventory, key=lambda x: x[2], reverse=True)
    elif sort_by_price:
        sorted_safe_inventory = sorted(safe_inventory, key=lambda x: x[1], reverse=True)
    else:
        sorted_safe_inventory = safe_inventory

    # Display cars in safe
    start_y = 200
    page_safe_inventory = sorted_safe_inventory[safe_inventory_page * INVENTORY_SIZE_PER_PAGE:(safe_inventory_page + 1) * INVENTORY_SIZE_PER_PAGE]
    for index, (car_name, car_price, car_speed, car_rarity, neon, nitro) in enumerate(page_safe_inventory):
        rarity_color = RARITY_COLORS[car_rarity]
        prefix_color = None
        prefix = ""

        if neon and nitro:
            prefix_color = (NEON_GREEN, DARK_RED)
            prefix = "N"
        elif neon:
            prefix_color = (NEON_GREEN,)
            prefix = "N"
        elif nitro:
            prefix_color = (DARK_RED,)
            prefix = "N"

        draw_text(f"{index + 1}. {car_name} - ${format_money(car_price)}, Speed: {car_speed} mph", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.03)), rarity_color, screen, 520, start_y)

        # Draw prefixes
        if prefix:
            for i, color in enumerate(prefix_color):
                draw_text(prefix, pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.03)), color, screen, 500 + i * 15, start_y)

        start_y += 18

    # Sort inventory for depositing
    if sort_by_speed:
        sorted_inventory = sorted(inventory, key=lambda x: x[2], reverse=True)
    elif sort_by_price:
        sorted_inventory = sorted(inventory, key=lambda x: x[1], reverse=True)
    else:
        sorted_inventory = inventory

    # Display cars in inventory for depositing
    start_y = 200
    page_inventory = sorted_inventory[inventory_page * INVENTORY_SIZE_PER_PAGE:(inventory_page + 1) * INVENTORY_SIZE_PER_PAGE]
    for index, (car_name, car_price, car_speed, car_rarity, neon, nitro) in enumerate(page_inventory):
        rarity_color = RARITY_COLORS[car_rarity]
        prefix_color = None
        prefix = ""

        if neon and nitro:
            prefix_color = (NEON_GREEN, DARK_RED)
            prefix = "N"
        elif neon:
            prefix_color = (NEON_GREEN,)
            prefix = "N"
        elif nitro:
            prefix_color = (DARK_RED,)
            prefix = "N"

        draw_text(f"{index + 1}. {car_name} - ${format_money(car_price)}, Speed: {car_speed} mph", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.03)), rarity_color, screen, 30, start_y)

        # Draw prefixes
        if prefix:
            for i, color in enumerate(prefix_color):
                draw_text(prefix, pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.03)), color, screen, 10 + i * 15, start_y)

        start_y += 18

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                if deposit_money_button.is_over(pos):
                    if money > 0:
                        safe_money += money
                        money = 0
                elif withdraw_money_button.is_over(pos):
                    money += safe_money
                    safe_money = 0
                elif deposit_car_button.is_over(pos):
                    if selected_car and selected_car in inventory:
                        safe_inventory.append(selected_car)
                        inventory.remove(selected_car)
                        selected_car = None
                elif withdraw_car_button.is_over(pos):
                    if selected_car and selected_car in safe_inventory:
                        inventory.append(selected_car)
                        safe_inventory.remove(selected_car)
                        selected_car = None
                elif sort_by_speed_button.is_over(pos):
                    sort_by_speed = True
                    sort_by_price = False
                elif sort_by_price_button.is_over(pos):
                    sort_by_price = True
                    sort_by_speed = False
                elif next_page_button.is_over(pos):
                    if (safe_inventory_page + 1) * INVENTORY_SIZE_PER_PAGE < len(safe_inventory):
                        safe_inventory_page += 1
                    elif (inventory_page + 1) * INVENTORY_SIZE_PER_PAGE < len(inventory):
                        inventory_page += 1
                elif prev_page_button.is_over(pos):
                    if safe_inventory_page > 0:
                        safe_inventory_page -= 1
                    elif inventory_page > 0:
                        inventory_page -= 1
                elif back_button.is_over(pos):
                    current_screen = 'main_menu'
                    selected_car = None
                else:
                    for index, car in enumerate(page_inventory):
                        car_pos_y = 200 + index * 18
                        if 30 < pos[0] < 220 and car_pos_y < pos[1] < car_pos_y + 18:
                            selected_car = car
                            break
                    for index, car in enumerate(page_safe_inventory):
                        car_pos_y = 200 + index * 18
                        if SCREEN_WIDTH // 2 + 110 < pos[0] < SCREEN_WIDTH // 2 + 400 and car_pos_y < pos[1] < car_pos_y + 18:
                            selected_car = car
                            break
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                deposit_money_button.update(pos)
                withdraw_money_button.update(pos)
                deposit_car_button.update(pos)
                withdraw_car_button.update(pos)
                sort_by_speed_button.update(pos)
                sort_by_price_button.update(pos)
                next_page_button.update(pos)
                prev_page_button.update(pos)
                back_button.update(pos)

    # Draw box around selected car
    if selected_car:
        if selected_car in safe_inventory:
            car_index = safe_inventory.index(selected_car)
            x_pos = SCREEN_WIDTH // 2 + 110
        elif selected_car in inventory:
            car_index = inventory.index(selected_car)
            x_pos = 30
        else:
            car_index = -1

        if car_index != -1:
            y_pos = 200 + (car_index % INVENTORY_SIZE_PER_PAGE) * 18
            pygame.draw.rect(screen, BLACK, (x_pos, y_pos, 275, 18), 2)

    # Interest calculation
    interest_rate = calculate_interest_rate(safe_money)
    safe_money += safe_money * interest_rate / 60 / FPS

def car_index_screen():
    global current_screen, car_index_page
    screen.fill(WHITE)
    draw_text('Car Index', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, 20, 20)

    all_cars = [
        (car[0], car[3]) for rarity in CAR_RARITIES for car in CAR_DATA[rarity]
    ]

    cars_per_page = INVENTORY_SIZE_PER_PAGE * 2
    start_index = car_index_page * cars_per_page
    end_index = start_index + cars_per_page
    displayed_cars = all_cars[start_index:end_index]

    start_y = 80
    left_x = 20
    right_x = SCREEN_WIDTH // 2 + 20

    for index, (car_name, car_rarity) in enumerate(displayed_cars):
        x_pos = left_x if index % 2 == 0 else right_x
        y_pos = start_y + (index // 2) * 30
        # Check if car is owned
        car_color = GREEN if any(car_name == car[0] for car in inventory + safe_inventory) else RED
        draw_text(car_name, pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.03)), car_color, screen, x_pos, y_pos)

    next_page_button.draw(screen, BLACK)
    prev_page_button.draw(screen, BLACK)
    back_button.draw(screen, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
                elif next_page_button.is_over(pos) and end_index < len(all_cars):
                    car_index_page += 1
                elif prev_page_button.is_over(pos) and car_index_page > 0:
                    car_index_page -= 1
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            next_page_button.update(pos)
            prev_page_button.update(pos)
            back_button.update(pos)



def settings_screen():
    global current_screen
    screen.fill(WHITE)
    draw_text('Settings', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, 20, 20)

    # Draw the buttons for save, load, achievements, etc.
    save_button.draw(screen)
    load_button.draw(screen)
    achievements_button.draw(screen)
    car_index_button.draw(screen)
    stats_button.draw(screen)
    back_button.draw(screen)
    probability_button.draw(screen)

    # Handle button clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
                elif save_button.is_over(pos):
                    save_game()
                elif load_button.is_over(pos):
                    load_game()
                elif achievements_button.is_over(pos):
                    current_screen = 'achievements'
                elif car_index_button.is_over(pos):
                    current_screen = 'car_index'
                elif stats_button.is_over(pos):
                    current_screen = 'stats'
                elif probability_button.is_over(pos):
                    current_screen = 'probability'
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            back_button.update(pos)
            save_button.update(pos)
            load_button.update(pos)
            achievements_button.update(pos)
            car_index_button.update(pos)
            stats_button.update(pos)
            probability_button.update(pos)


def inventory_screen():
    global current_screen, inventory_page, sort_by_speed, sort_by_rarity, sort_by_price
    screen.fill(WHITE)
    draw_text('Inventory', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, 20, 20)

    # Calculate total value
    total_value = sum(car[1] for car in inventory)
    formatted_total_value = format_money(total_value)
    draw_text(f'Total Value: {formatted_total_value}', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, SCREEN_WIDTH - 500, 20)

    # Draw buttons
    back_button.draw(screen, BLACK)
    next_page_button.draw(screen, BLACK)
    prev_page_button.draw(screen, BLACK)
    sell_duplicates_button.draw(screen, BLACK)
    sort_by_speed_button.draw(screen, BLACK)
    sort_by_rarity_button.draw(screen, BLACK)
    sort_by_price_button.draw(screen, BLACK)

    # Sort and display inventory based on the chosen criteria
    if sort_by_speed:
        sorted_inventory = sorted(Counter(inventory).items(), key=lambda x: x[0][2], reverse=True)
    elif sort_by_rarity:
        rarity_order = {rarity: i for i, rarity in enumerate(REVERSE_CAR_RARITIES)}
        sorted_inventory = sorted(Counter(inventory).items(), key=lambda x: rarity_order[x[0][3]])
    elif sort_by_price:
        sorted_inventory = sorted(Counter(inventory).items(), key=lambda x: x[0][1], reverse=True)
    else:
        sorted_inventory = sorted(Counter(inventory).items(), key=lambda x: x[0][1], reverse=True)

    page_inventory = sorted_inventory[inventory_page * INVENTORY_SIZE_PER_PAGE:(inventory_page + 1) * INVENTORY_SIZE_PER_PAGE]

    start_y = 120
    for index, ((car_name, car_price, car_speed, car_rarity, neon, nitro), count) in enumerate(page_inventory):
        rarity_color = RARITY_COLORS[car_rarity]
        prefix_color = None
        prefix = ""

        if neon and nitro:
            prefix_color = (NEON_GREEN, DARK_RED)
            prefix = "N"
        elif neon:
            prefix_color = (NEON_GREEN,)
            prefix = "N"
        elif nitro:
            prefix_color = (DARK_RED,)
            prefix = "N"

        draw_text(f"{car_name} x{count} - ${format_money(car_price)}, Speed: {car_speed} mph", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.04)), rarity_color, screen, 60, start_y)

        # Draw prefixes
        if prefix:
            for i, color in enumerate(prefix_color):
                draw_text(prefix, pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.04)), color, screen, 40 + i * 15, start_y)

        start_y += 28

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
                elif next_page_button.is_over(pos) and (inventory_page + 1) * INVENTORY_SIZE_PER_PAGE < len(sorted_inventory):
                    inventory_page += 1
                elif prev_page_button.is_over(pos) and inventory_page > 0:
                    inventory_page -= 1
                elif sell_duplicates_button.is_over(pos):
                    sell_duplicates()
                elif sort_by_speed_button.is_over(pos):
                    sort_by_speed = True
                    sort_by_rarity = False
                    sort_by_price = False
                elif sort_by_rarity_button.is_over(pos):
                    sort_by_rarity = True
                    sort_by_speed = False
                    sort_by_price = False
                elif sort_by_price_button.is_over(pos):
                    sort_by_price = True
                    sort_by_speed = False
                    sort_by_rarity = False
                else:
                    for index, ((car_name, car_price, car_speed, car_rarity, neon, nitro), count) in enumerate(page_inventory):
                        car_pos_y = 120 + index * 28  # Adjusted to match the text spacing
                        if 40 < pos[0] < SCREEN_WIDTH // 2 and car_pos_y < pos[1] < car_pos_y + 28:
                            car_to_sell = (car_name, car_price, car_speed, car_rarity, neon, nitro)
                            car_index = inventory.index(car_to_sell)
                            print(sell_car(car_index))
                            break
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                back_button.update(pos)
                next_page_button.update(pos)
                prev_page_button.update(pos)
                sell_duplicates_button.update(pos)
                sort_by_speed_button.update(pos)
                sort_by_rarity_button.update(pos)
                sort_by_price_button.update(pos)

def display_fastest_car(screen):
    # Define the font size for displaying the fastest car
    font = pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05))

    # Find the fastest car in the owned cars list
    fastest_car = find_fastest_car(cars_owned)

    # Check if a fastest car exists, then display the appropriate text
    if fastest_car:
        draw_text(f"Fastest Car: {fastest_car['name']} ({fastest_car['speed']} km/h)", font, BLACK, screen, 20, 280)
    else:
        draw_text("Fastest Car: None", font, BLACK, screen, 20, 280)


def calculate_total_value(inventory):
    """
    Calculate the total value of cars in the inventory.

    Args:
    inventory (list of tuples): Each tuple contains information about a car, 
                                where the second element is the car's value.

    Returns:
    int: Total value of all cars in the inventory.
    """
    return sum(car[1] for car in inventory)


def achievements_screen():
    global current_screen, achievement_page
    screen.fill(WHITE)
    draw_text('Achievements', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, 20, 20)

    start_y = 100
    achievements_per_page = ACHIEVEMENTS_PER_PAGE
    start_index = achievement_page * achievements_per_page
    end_index = start_index + achievements_per_page
    displayed_achievements = achievements[start_index:end_index]

    for achievement in displayed_achievements:
        name = achievement["name"]
        description = achievement["description"]
        completed = achievement["completed"]
        color = GREEN if completed else BLACK
        draw_text(f"{name} - {description}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.04)), color, screen, 20, start_y)
        start_y += 25

    next_page_button.draw(screen, BLACK)
    prev_page_button.draw(screen, BLACK)
    back_button.draw(screen, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
                elif next_page_button.is_over(pos) and end_index < len(achievements):
                    achievement_page += 1
                elif prev_page_button.is_over(pos) and achievement_page > 0:
                    achievement_page -= 1
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            next_page_button.update(pos)
            prev_page_button.update(pos)
            back_button.update(pos)

def list_car_screen():
    global current_screen, inventory_page, trade_offers
    screen.fill(WHITE)
    draw_text('List Car for Trade', pygame.font.SysFont(None, 50), BLACK, screen, 20, 20)

    back_button.draw(screen, BLACK)
    next_page_button.draw(screen, BLACK)
    prev_page_button.draw(screen, BLACK)

    start_y = 120
    cars_per_page = 10
    start_index = inventory_page * cars_per_page
    end_index = start_index + cars_per_page
    displayed_cars = inventory[start_index:end_index]

    for index, (car_name, car_price, car_speed, car_rarity, neon, nitro) in enumerate(displayed_cars):
        rarity_color = RARITY_COLORS[car_rarity]
        prefix_color = None
        prefix = ""

        if neon and nitro:
            prefix_color = (NEON_GREEN, DARK_RED)
            prefix = "N"
        elif neon:
            prefix_color = (NEON_GREEN,)
            prefix = "N"
        elif nitro:
            prefix_color = (DARK_RED,)
            prefix = "N"

        draw_text(f"{car_name} - ${format_money(car_price)}, Speed: {car_speed} mph", pygame.font.SysFont(None, 21), rarity_color, screen, 60, start_y)





        
        # Draw prefixes
        if prefix:
            for i, color in enumerate(prefix_color):
                draw_text(prefix, pygame.font.SysFont(None, 21), color, screen, 40 + i * 15, start_y)

        start_y += 21

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
                elif next_page_button.is_over(pos) and end_index < len(inventory):
                    inventory_page += 1
                elif prev_page_button.is_over(pos) and inventory_page > 0:
                    inventory_page -= 1
                else:
                    for car_index, car in enumerate(displayed_cars):
                        car_pos_y = 120 + car_index * 21
                        if 40 < pos[0] < SCREEN_WIDTH // 2 and car_pos_y < pos[1] < car_pos_y + 21:
                            trade_offer = {
                                'type': 'sell',
                                'car': car,
                                'price': car[1] * 1.5,  # List car for 1.5 times its price
                                'is_player_listed': True  # Indicate that this offer was listed by the player
                            }
                            trade_offers.append(trade_offer)
                            inventory.remove(car)
                            print(f"Listed {car[0]} for ${format_money(trade_offer['price'])}")
                            break
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                back_button.update(pos)
                next_page_button.update(pos)
                prev_page_button.update(pos)

def global_market_screen():
    global current_screen, market_page, money, inventory
    screen.fill(WHITE)
    draw_text('Global Market', pygame.font.SysFont(None, 50), BLACK, screen, 20, 20)

    back_button.draw(screen, BLACK)
    next_page_button.draw(screen, BLACK)
    prev_page_button.draw(screen, BLACK)

    start_y = 120
    offers_per_page = 10
    start_index = market_page * offers_per_page
    end_index = start_index + offers_per_page
    displayed_offers = trade_offers[start_index:end_index]

    for index, offer in enumerate(displayed_offers):
        offer_type = offer['type']
        car_name, car_price, car_speed, car_rarity, neon, nitro = offer['car']
        rarity_color = RARITY_COLORS[car_rarity]
        quality_color = evaluate_trade_quality(offer)

        offer_text = f"{car_name} - ${format_money(car_price)}, Speed: {car_speed} mph"
        if offer_type == 'sell':
            offer_text += f" - Selling for ${format_money(offer['price'])}"
        elif offer_type == 'trade':
            trade_for_name, trade_for_price, trade_for_speed, trade_for_rarity, trade_for_neon, trade_for_nitro = offer['trade_for']
            trade_for_text = f"{trade_for_name} - ${format_money(trade_for_price)}, Speed: {trade_for_speed} mph"
            offer_text += f" - Trading for {trade_for_text}"
        elif offer_type == 'trade_plus_money':
            trade_for_name, trade_for_price, trade_for_speed, trade_for_rarity, trade_for_neon, trade_for_nitro = offer['trade_for']
            trade_for_text = f"{trade_for_name} - ${format_money(trade_for_price)}, Speed: {trade_for_speed} mph"
            offer_text += f" - Trading for {trade_for_text} + ${format_money(offer['money'])}"
        elif offer_type == 'buy':
            offer_text += f" - Buying for ${format_money(offer['price'])}"

        draw_text(offer_text, pygame.font.SysFont(None, 21), quality_color, screen, 60, start_y)
        start_y += 21

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
                elif next_page_button.is_over(pos) and end_index < len(trade_offers):
                    market_page += 1
                elif prev_page_button.is_over(pos) and market_page > 0:
                    market_page -= 1
                else:
                    for offer_index, offer in enumerate(displayed_offers):
                        offer_pos_y = 120 + offer_index * 21
                        if 60 < pos[0] < SCREEN_WIDTH and offer_pos_y < pos[1] < offer_pos_y + 21:
                            if offer['type'] == 'sell':
                                if money >= offer['price']:
                                    money -= offer['price']
                                    inventory.append(offer['car'])
                                    trade_offers.remove(offer)
                                    print(f"Bought {offer['car'][0]} for ${format_money(offer['price'])}")
                            elif offer['type'] == 'buy':
                                car_to_sell = next((car for car in inventory if car[0] == offer['car'][0] and car[1] == offer['car'][1] and car[2] == offer['car'][2] and car[3] == offer['car'][3] and car[4] == offer['car'][4] and car[5] == offer['car'][5]), None)
                                if car_to_sell:
                                    money += offer['price']
                                    inventory.remove(car_to_sell)
                                    trade_offers.remove(offer)
                                    print(f"Sold {offer['car'][0]} for ${format_money(offer['price'])}")
                            elif offer['type'] == 'trade':
                                car_to_trade = next((car for car in inventory if car[0] == offer['trade_for'][0] and car[1] == offer['trade_for'][1] and car[2] == offer['trade_for'][2] and car[3] == offer['trade_for'][3] and car[4] == offer['trade_for'][4] and car[5] == offer['trade_for'][5]), None)
                                if car_to_trade:
                                    inventory.remove(car_to_trade)
                                    inventory.append(offer['car'])
                                    trade_offers.remove(offer)
                                    print(f"Traded {offer['trade_for'][0]} for {offer['car'][0]}")
                            elif offer['type'] == 'trade_plus_money':
                                if offer['money'] > 0:  # Trading car + money for another car
                                    car_to_trade = next((car for car in inventory if car[0] == offer['car'][0] and car[1] == offer['car'][1] and car[2] == offer['car'][2] and car[3] == offer['car'][3] and car[4] == offer['car'][4] and car[5] == offer['car'][5]), None)
                                    if car_to_trade and money >= offer['money']:
                                        money -= offer['money']
                                        inventory.remove(car_to_trade)
                                        inventory.append(offer['trade_for'])
                                        trade_offers.remove(offer)
                                        print(f"Traded {offer['car'][0]} + ${format_money(offer['money'])} for {offer['trade_for'][0]}")
                                else:  # Trading car for another car + money
                                    car_to_trade = next((car for car in inventory if car[0] == offer['trade_for'][0] and car[1] == offer['trade_for'][1] and car[2] == offer['trade_for'][2] and car[3] == offer['trade_for'][3] and car[4] == offer['trade_for'][4] and car[5] == offer['trade_for'][5]), None)
                                    if car_to_trade and money >= abs(offer['money']):
                                        money -= abs(offer['money'])
                                        inventory.remove(car_to_trade)
                                        inventory.append(offer['car'])
                                        trade_offers.remove(offer)
                                        print(f"Traded {offer['trade_for'][0]} for {offer['car'][0]} + ${format_money(offer['money'])}")
                            break
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                back_button.update(pos)
                next_page_button.update(pos)
                prev_page_button.update(pos)

def stats_screen():
    global current_screen
    screen.fill(WHITE)
    draw_text('Statistics', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, 20, 20)

    # Display game statistics
    draw_text(f"Races Won: {races_won}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 100)
    draw_text(f"Boxes Opened: {boxes_opened}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 120)
    draw_text(f"Total Money: ${format_money(money)}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 160)
    draw_text(f"Money in Safe: ${format_money(safe_money)}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 180)
    draw_text(f"Total Boxes Value: ${format_money(boxes_opened * 100)}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 200)
    draw_text(f"Total Cars Value: ${format_money(calculate_total_value(inventory))}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 220)
    draw_text(f"Net Worth: ${format_money(money + safe_money + calculate_total_value(inventory))}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 240)
    total_time_played_in_seconds = calculate_time_played(game_start_time, total_time_played)
    formatted_time_played = format_time(total_time_played_in_seconds)
    draw_text(f"Total Time Played: {formatted_time_played}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 260)
    draw_text(f"Total Cars Owned: {total_cars_owned}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 140)
    draw_text(f"Average Car Value: ${format_money(calculate_total_value(inventory) / total_cars_owned if total_cars_owned > 0 else 0)}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 280)







    
    # Add a back button
    back_button.draw(screen, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            back_button.update(pos)

# Add the stats button to the main menu
stats_button.draw(screen)

if event.type == pygame.MOUSEBUTTONDOWN:
    pos = pygame.mouse.get_pos()
    if event.button == 1:  # Left click
        if stats_button.is_over(pos):
            current_screen = 'stats'


# Draw the settings button
settings_button.draw(screen)

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if event.button == 1:
            if settings_button.is_over(pos):
                current_screen = 'settings'


if event.type == pygame.MOUSEMOTION:
    pos = pygame.mouse.get_pos()
    settings_button.update(pos)


def coinflip_screen():
    global current_screen, selected_car, money, inventory_page
    screen.fill(WHITE)
    draw_text('Coinflip', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, 20, 20)
    draw_text('Double or Nothing!', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 80)

    if selected_car:
        draw_text(f"Selected Car: {selected_car[0]}", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 140)
        flip_button = Button(GREEN, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100, 'Flip Coin')
        flip_button.draw(screen, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if flip_button.is_over(pos):
                    if random.random() < 0.5:
                        # Win
                        money += selected_car[1]
                        print(f"You won! You doubled your car value. Money: ${format_money(money)}")
                    else:
                        # Lose
                        inventory.remove(selected_car)
                        print(f"You lost! You lost your car. Money: ${format_money(money)}")
                    selected_car = None
                    current_screen = 'main_menu'
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                flip_button.update(pos)
    else:
        draw_text('Select a car from your inventory', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.05)), BLACK, screen, 20, 140)

        start_y = 200
        cars_per_page = 10
        start_index = inventory_page * cars_per_page
        end_index = start_index + cars_per_page
        displayed_cars = inventory[start_index:end_index]

        car_rects = []
        for index, (car_name, car_price, car_speed, car_rarity, neon, nitro) in enumerate(displayed_cars):
            rarity_color = RARITY_COLORS[car_rarity]
            prefix_color = None
            prefix = ""

            if neon and nitro:
                prefix_color = (NEON_GREEN, DARK_RED)
                prefix = "N"
            elif neon:
                prefix_color = (NEON_GREEN,)
                prefix = "N"
            elif nitro:
                prefix_color = (DARK_RED,)
                prefix = "N"

            car_rect = pygame.Rect(40, start_y, SCREEN_WIDTH // 2, 21)  # Hitbox for the car name
            car_rects.append((car_rect, (car_name, car_price, car_speed, car_rarity, neon, nitro)))
            draw_text(f"{car_name} - ${format_money(car_price)}, Speed: {car_speed} mph", pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.03)), rarity_color, screen, 60, start_y)

            # Draw prefixes
            if prefix:
                for i, color in enumerate(prefix_color):
                    draw_text(prefix, pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.03)), color, screen, 40 + i * 15, start_y)

            start_y += 28

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if back_button.is_over(pos):
                    current_screen = 'main_menu'
                elif next_page_button.is_over(pos) and end_index < len(inventory):
                    inventory_page += 1
                elif prev_page_button.is_over(pos) and inventory_page > 0:
                    inventory_page -= 1
                else:
                    for car_rect, car in car_rects:
                        if car_rect.collidepoint(pos):
                            selected_car = car
                            break
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                back_button.update(pos)
                next_page_button.update(pos)
                prev_page_button.update(pos)

    back_button.draw(screen, BLACK)
    next_page_button.draw(screen, BLACK)
    prev_page_button.draw(screen, BLACK)


def loading_screen():
    global current_screen
    screen.fill(WHITE)
    draw_text('Loading...', pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1)), BLACK, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
    pygame.display.update()
    time.sleep(2)  # Simulate loading time
    current_screen = 'main_menu'

# Main game loop
running = True
while running:
    if current_screen == 'loading':
        loading_screen()
    elif current_screen == 'main_menu':
        main_menu()
    elif current_screen == 'inventory':
        inventory_screen()
    elif current_screen == 'settings':
        settings_screen()
    elif current_screen == 'probability':
        probability_screen()
    elif current_screen == 'drag_race':
        drag_race_screen()
    elif current_screen == 'safe':
        safe_screen()
    elif current_screen == 'car_index':
        car_index_screen()
    elif current_screen == 'achievements':
        achievements_screen()
    elif current_screen == 'list_car':
        list_car_screen()
    elif current_screen == 'global_market':
        global_market_screen()
    elif current_screen == 'coinflip':
        coinflip_screen()
    elif current_screen == 'boxes':
        boxes_screen()
    elif current_screen == 'stats':
        stats_screen()


    pygame.display.update()
    clock.tick(FPS)


