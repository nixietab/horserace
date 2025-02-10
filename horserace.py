import random
import time
import json
import hashlib
import argparse
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# List of racing horse names
racing_horse_names = [
    "Thunderbolt", "Lightning", "Blaze", "Storm", "Comet", "Rocket", "Shadow", "Flash",
    "Tornado", "Hurricane", "Blizzard", "Cyclone", "Inferno", "Avalanche", "Whirlwind", "Typhoon",
    "Phoenix", "Meteor", "Pegasus", "Vortex", "Eclipse", "Thunder", "Zephyr", "Tempest",
    "Starlight", "Nebula", "Galaxy", "Cosmos", "Nova", "Orbit", "Radiance", "Aurora", "Princesa", "Delibery", "Malambo"
]

# List of random race names
race_names = [
    "Champions", "Legends", "Speedsters", "Titans", "Warriors", "Gladiators", "Masters", "Riders",
    "Sprinters", "Racers", "Gallopers", "Dashers", "Runners", "Contenders", "Marauders"
]

# haracter for the horse
horse_char = Fore.WHITE + "♞" + Style.RESET_ALL

# Leaderboard file
leaderboard_file = "leaderboard.json"

# Function to get player names
def get_player_names(num_players, specified_names):
    names = specified_names[:num_players]
    available_names = racing_horse_names[:]
    while len(names) < num_players:
        if not available_names:
            raise ValueError("Not enough unique horse names to satisfy the number of players.")
        name = random.choice(available_names)
        available_names.remove(name)  # Remove the name from the list to avoid duplicates
        names.append(name)
    return names

# Function to load the leaderboard from a JSON file
def load_leaderboard():
    try:
        with open(leaderboard_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save the leaderboard to a JSON file
def save_leaderboard(leaderboard):
    with open(leaderboard_file, "w") as file:
        json.dump(leaderboard, file, indent=4)

# Function to update the leaderboard
def update_leaderboard(winner, horses):
    leaderboard = load_leaderboard()
    if winner not in leaderboard:
        leaderboard[winner] = {"total_points": 0, "races": []}
    winner_position = next(horse['position'] for horse in horses if horse['name'] == winner)
    points = 10  # Start with max points for the winner
    for horse in horses:
        horse_position = horse['position']
        difference = int(abs(winner_position - horse_position))
        race_points = max(1, points - difference)
        horse['race_points'] = race_points  # Add race points to horse data
        if horse['name'] in leaderboard:
            leaderboard[horse['name']]["total_points"] += race_points
            leaderboard[horse['name']]["races"].append(race_points)
        else:
            leaderboard[horse['name']] = {"total_points": race_points, "races": [race_points]}
    save_leaderboard(leaderboard)
    return leaderboard

# Function to generate a color based on horse name
def generate_color(horse_name):
    hash_code = int(hashlib.md5(horse_name.encode()).hexdigest(), 16)
    color_code = hash_code % 12
    if color_code == 0:
        return Fore.RED
    elif color_code == 1:
        return Fore.GREEN
    elif color_code == 2:
        return Fore.YELLOW
    elif color_code == 3:
        return Fore.BLUE
    elif color_code == 4:
        return Fore.MAGENTA
    elif color_code == 5:
        return Fore.CYAN
    elif color_code == 6:
        return Fore.LIGHTRED_EX
    elif color_code == 7:
        return Fore.LIGHTGREEN_EX
    elif color_code == 8:
        return Fore.LIGHTYELLOW_EX
    elif color_code == 9:
        return Fore.LIGHTBLUE_EX
    elif color_code == 10:
        return Fore.LIGHTMAGENTA_EX
    elif color_code == 11:
        return Fore.LIGHTCYAN_EX

# Function to display the leaderboard
def display_leaderboard(leaderboard, raced_horses, display_limit, winner=None):
    if leaderboard:
        max_name_length = max(len(horse) for horse in leaderboard.keys())
    else:
        max_name_length = 0
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1]["total_points"], reverse=True)
    leaderboard_str = f"{Fore.CYAN}{'Leaderboard:':^50}\n" + f"{'='*50}\n"
    for rank, (horse, data) in enumerate(sorted_leaderboard[:display_limit], start=1):
        color = generate_color(horse)
        points_color = Fore.YELLOW if horse == winner else Fore.WHITE
        new_indicator = "*" if horse in raced_horses else ""
        points_text = f"{points_color}{data['total_points']}{new_indicator}{Style.RESET_ALL}"
        leaderboard_str += f"{rank:>2} | {color}{horse:<{max_name_length}}{Style.RESET_ALL} | {points_text:>5} points\n"
    leaderboard_str += f"{'='*50}"
    return leaderboard_str

# Function to display the horse race
def display_race(horses, track_length, leaderboard, speed, display_limit, show_clock):
    max_name_length = max(len(horse['name']) for horse in horses)
    race_name = f"Race of the {random.choice(race_names)}"
    divisor = f"{'='* (track_length + max_name_length + 5)}"
    
    while True:
        # Get the current date and time
        if show_clock:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_date = now.strftime("%A %d of %B")
            
            # Display the date and time at the top, this is trash changing later
            date_time_display = f"{Fore.CYAN}{current_date:^25}{current_time:^25}\n" + f"{'='*50}\n"
        else:
            date_time_display = ""

        race_display = date_time_display + f"{Fore.GREEN}{race_name:^50}\n" + divisor + "\n"
        for i, horse in enumerate(horses):
            # Move the horse randomly
            horse['position'] += random.randint(1, 5) * 0.1
            horse['position'] = min(horse['position'], track_length)
            
            # Print the horse's trail and the horse character
            trail = '-' * int(horse['position'])
            name_with_padding = horse['name'].ljust(max_name_length)
            color = generate_color(horse['name'])
            race_display += f"{color}{name_with_padding} | {trail}{horse_char}\n" + Style.RESET_ALL
        
        # Check if any horse has won
        for horse in horses:
            if horse['position'] >= track_length:
                winner_line = f"{Fore.YELLOW}{horse['name']} wins the race!{Style.RESET_ALL}"
                leaderboard = update_leaderboard(horse['name'], horses)
                raced_horses = set(horse['name'] for horse in horses)
                race_display += f"\n{winner_line}\n" + display_leaderboard(leaderboard, raced_horses, display_limit, winner=horse['name'])
                print(f"\033[H\033[J", end="")  # Clear the screen
                print(race_display)
                return
        
        # Display the race and leaderboard
        race_display += f"\n{Fore.YELLOW}{'Race in Progress...':^50}{Style.RESET_ALL}\n" + display_leaderboard(leaderboard, set(horse['name'] for horse in horses), display_limit)
        print(f"\033[H\033[J", end="")  # Clear the screen
        print(race_display)
        
        # Add a shorter delay between frames
        time.sleep(0.1 / speed)

def main():
    parser = argparse.ArgumentParser(description='Horse Racing Game')
    parser.add_argument('--num_horses', type=int, default=4, help='Number of horses in the race')
    parser.add_argument('--names', nargs='*', default=[], help='Names of the horses')
    parser.add_argument('--speed', type=float, default=1.0, help='Speed of the race')
    parser.add_argument('--track_length', type=int, default=50, help='Length of the race track')
    parser.add_argument('--display_limit', type=int, default=10, help='Number of horses to display on the leaderboard')
    parser.add_argument('--screensaver', action='store_true', help='Shows the races in a loop and waits 3 seconds before starting another one')
    parser.add_argument('--clock', action='store_true', help='Shows the current time in a cool way')

    args = parser.parse_args()

    try:
        while True:
            # Get player names
            player_names = get_player_names(args.num_horses, args.names)
            
            # Initialize horses
            horses = [{'name': name, 'position': 0} for name in player_names]
            
            # Load the initial leaderboard
            leaderboard = load_leaderboard()
            
            # Display the horse race
            display_race(horses, args.track_length, leaderboard, args.speed, args.display_limit, args.clock)

            if not args.screensaver:
                break

            time.sleep(3)
    except KeyboardInterrupt:
        print("\nGoodbye")

if __name__ == "__main__":
    main()
