
class Color():
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    WHITE = '\033[37m'
    
def print_menu():
    print("\n", 30 * f"{Color.BLUE}-", f"{Color.BLUE}MENU", 30 * f"{Color.BLUE}-")
    print(f"""{Color.WHITE}
        1. First-Come, First-Served Scheduling 
        2. Nonpreemptive Shortest-Job-First Scheduling
        3. Preemptive Shortest-Job-First Scheduling
        4. Round-Robin Scheduling
        5. Nonpreemptive Priority Scheduling
        6. Preemptive Priority Scheduling 
        7. Exit
    """)
    print(67 * f"{Color.BLUE}-")

def main():
    loop = True
    while loop:
        print_menu()
        choice = input(f"{Color.WHITE} \n Enter your choice [1-7]: ")
        try:
            choice = int(choice)

            if(choice == 1):
                print("FCFS") 
            elif(choice == 7):
                loop = False

        except ValueError:
            print(f"{Color.RED} \n Invalid input")

main()