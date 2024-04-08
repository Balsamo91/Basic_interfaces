import random

# Simultae a creating a largo log file

def create_large_log_file(filename, num_rows=1000000):
    with open(filename, 'w') as file:
        for row in range(num_rows):
            user_id = random.randint(1, 100) # Simulate user IDs between 1 to 100
            amount = round(random.uniform(1, 1000), 2)# Random transaction amount
            file.write(f"{user_id}, {amount}\n")


create_large_log_file("large_log_file.txt")


