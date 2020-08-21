"""
Welcome to Scraper.

This application is a very simple program with a command-line interface and its purpose was
initially to automate a very simple scraping algorithm that was often by the author.

The application features numerous commands that work to give control over the interface itself, the
csv file that is specified and the scraping options.

While web scraping remains a task that has numerous tools and demands, this application attempts to
keep it simple by allowing the user to simply specify 2 things:
-HTML Element
-Element Class

While one might want to scrape on the basis of id or options other than class, the author has deemed
for the sake of simplicity class to be the best and only option to feature in this application.

As this application has been born from a necessity to automate some simple scraping, it is regularly
updated to meet first and foremost the needs of its author.

Commands have been made very simple and short, but perhaps at the cost of total off-the-bat clarity
of what they do. However, proper documentation has been provided for the commands and can be viewed
using help/? <cmd>.

The application requires some peculiar things as well:
1)Parser
-lxml
-html.parser
-html5lib

2)Webpages
-An initial webpage
-A template for the rest of the pages replacing page number in the url with $

Follow command documentation carefully.
"""
import cmd
import csv
import datetime as datetime
import os
try:
    from bs4 import BeautifulSoup
    from colorama import init, Fore, Style
    from selenium import webdriver
except ModuleNotFoundError as error:
    print(f"{error}")
    print("You cannot run this script without this module.")
    input()
    exit(1)
init(autoreset=False)

exitInputs = ['leave', 'break', 'quit', 'exit', 'end']
acceptedParsers = ['lxml', 'html5lib', 'html.parser']


# noinspection PyUnusedLocal,PyUnboundLocalVariable
class Scraper(cmd.Cmd):
    intro = "Scraper"
    prompt = "|>"
    file = None

    def __init__(self):
        super(Scraper, self).__init__()

        self.csv_file = ""
        self.csv_mode = 'a'
        self.initial_row = []
        self.variable = 0
        self.initial_webpage = ''
        self.rpages = ''
        self.parser = 'html5lib'

    # Functions for Setting Values
    def do_file(self, arg):
        """Set the path or just a name for your CSV file."""
        self.csv_file = str(arg)

    def do_mode(self, arg):
        """Set the mode you want your CSV file to be opened in."""
        self.csv_mode = str(arg)

    def do_irow(self, arg):
        """Specify the initial row of your CSV file."""
        self.initial_row = arg.split(',')

    def do_setup(self, arg):
        """Setup CSV file essential settings."""
        try:
            self.csv_file = input(f"{Fore.BLUE}CSV File: {Fore.GREEN}")
            self.csv_mode = input(f"{Fore.BLUE}Open Mode: {Fore.GREEN}")
            self.initial_row = (input(f"{Fore.BLUE}Initial Row: {Fore.GREEN}")).split(',')
            print(Style.RESET_ALL)
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

    def do_var(self, arg):
        """Set the variable which is equal to the total number of webpages."""
        try:
            self.variable = int(arg)
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

    def do_ipage(self, arg):
        """Set the url for the initial webpage."""
        self.initial_webpage = str(arg)

    def do_rpages(self, arg):
        """Set the template for the remainder of webpages."""
        self.rpages = str(arg)

    def do_parser(self, arg):
        """Set parser."""
        if arg in acceptedParsers:
            self.parser = str(arg)
        else:
            print(f"{Fore.RED}The parser chosen does not exist. See list of accepted parsers.{Style.RESET_ALL}")

    def do_info(self, arg):  # print server, port, username, password....
        """View the information you have entered so far."""
        print(Fore.RED)
        print("CSV File: " + self.csv_file)
        print("CSV Mode: " + self.csv_mode)
        print("Initial Row: " + str(self.initial_row))
        print("Initial Webpage: " + self.initial_webpage)
        print("Rest of Pages: " + self.rpages)
        print("Variable: " + str(self.variable))
        print("Parser: " + str(self.parser))
        print(Style.RESET_ALL)

    @staticmethod
    def do_parsers(arg):
        """Show list of parsers you can use."""
        print(f"{Fore.RED}\nAvailable Parsers:\n1)html5lib\n2)lxml\n3)html.parser{Style.RESET_ALL}")

    @staticmethod
    def do_modes(arg):
        """Show the available file modes which can be used to open files."""
        print(Fore.RED)
        print(
            "1)r: Opens the file in read-only mode. Starts reading from the beginning of the file and is the default "
            "mode for the open() function.")
        print(
            "2)rb: Opens the file as read-only in binary format and starts reading from the beginning of the file. "
            "While binary format can be used\n\t for different purposes, it is usually used when dealing with things "
            "like images, videos, etc.")
        print("3)r+: Opens a file for reading and writing, placing the pointer at the beginning of the file.")
        print(
            "4)w: Opens in write-only mode. The pointer is placed at the beginning of the file and this will "
            "overwrite any existing file with the\n\t same name. It will create a new file if one with the same name "
            "doesn't exist.")
        print("5)wb: Opens a write-only file in binary mode.")
        print("6)w+: Opens a file for writing and reading.")
        print("7)wb+: Opens a file for writing and reading in binary mode.")
        print(
            "8)a: Opens a file for appending new information to it. The pointer is placed at the end of the file. A "
            "new file is created if one with\n\t the same name doesn't exist.")
        print("9)ab: Opens a file for appending in binary mode.")
        print("10)a+: Opens a file for both appending and reading.")
        print("11)ab+: Opens a file for both appending and reading in binary mode.")
        print(Style.RESET_ALL)

    def do_scrape(self, arg):
        """Scrape data from specified webpages."""
        print(f"\n{Fore.GREEN}Scraping Operation Initiated: ")
        try:
            csv_file = open(self.csv_file, self.csv_mode, newline='')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.initial_row)

            print(f"{Fore.BLUE}\nCSV File: {Fore.GREEN}" + self.csv_file)
            print(f"{Fore.BLUE}CSV Mode: {Fore.GREEN}" + self.csv_mode)
            print(f"{Fore.BLUE}Initial Row: {Fore.GREEN}" + str(self.initial_row))
            print(f"{Fore.BLUE}Initial Webpage: {Fore.GREEN}" + self.initial_webpage)
            print(f"{Fore.BLUE}Rest of Pages: {Fore.GREEN}" + self.rpages)
            print(f"{Fore.BLUE}Variable: {Fore.GREEN}" + str(self.variable))
            print(Style.RESET_ALL)
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

        x = 2
        webpages = [self.initial_webpage]
        # noinspection PyBroadException
        try:
            while x < self.variable:
                new_page = self.rpages.replace('$', str(x))
                webpages.append(new_page)
                x += 1
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            pass

        try:
            print(Fore.BLUE)
            print("\nWebpages: ")
            for webpage in webpages:
                print(Fore.GREEN)
                print(webpage)
            print(Style.RESET_ALL)
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

        elements_list = []
        class_list = []
        element_index = 1
        while True:
            element = input(f'{Fore.BLUE}Element {element_index}: {Fore.GREEN}')
            if element in exitInputs:
                break
            else:
                elements_list.append(element)
                class_of_element = input(f'{Fore.BLUE}Class of Element {element_index}: {Fore.GREEN}')
                class_list.append(class_of_element)
                element_index += 1
        print(Fore.BLUE)
        print("\nElements: ")
        for (element, _class) in zip(elements_list, class_list):
            print(f"{Fore.BLUE}{element} of class = {Fore.GREEN}{_class}{Style.RESET_ALL}")
        print("\n")

        for page in webpages:
            try:
                print(f"\n{Fore.BLUE}Current Page: {Fore.GREEN}{page}{Style.RESET_ALL}")
                driver = webdriver.Chrome()
                driver.get(page)
                page_soup = BeautifulSoup(driver.page_source, self.parser)
            except Exception as e:
                print(f"{Fore.RED}{e}{Style.RESET_ALL}")
                break

            print(Fore.RED)
            individual_element_data = []
            for (element, element_class) in zip(elements_list, class_list):
                if element_class == '#':
                    data = page_soup.find_all(element)
                else:
                    element = str(element.strip())
                    _class = str(element_class.strip())
                    print(element, _class)
                    data = page_soup.find_all(element, class_=_class)
                individual_element_data.append(data)

            print(f"\n{Fore.BLUE}Scraped Data From Elements: {Fore.GREEN}\n{individual_element_data}")

            length_of_element_data = len(individual_element_data[0])
            print(
                f"\n{Fore.BLUE}Number of Elements Scraped in this Page: {Fore.GREEN}{length_of_element_data}")

            print(f"\n{Fore.RED}Now Writing to CSV File: {Fore.GREEN}")
            x = 0
            while x < length_of_element_data:
                row = []
                for element_data in individual_element_data:
                    list_length = len(element_data)
                    row.append((element_data[x]).text.strip())
                    print(f"{x + 1}) {(element_data[x]).text.strip()}")
                x += 1
                csv_writer.writerow(row)

        print(f"\n{Fore.GREEN}Scraping Operation Terminated Successfully.\n{Style.RESET_ALL}")

    # CSV Functions
    def do_wrow(self, arg):
        """Write in a row in the chosen CSV file."""
        try:
            csv_file = open(self.csv_file, self.csv_mode, newline='')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(arg.split(','))
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

    def do_ocsv(self, arg):
        """Open the chosen CSV file to view."""
        try:
            os.startfile(self.csv_file)
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

    # CMD Functions
    def do_prompt(self, arg):
        """Change the prompt of the program."""
        try:
            self.prompt = arg
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

    @staticmethod
    def do_clear(arg):
        """Clear the console window."""
        os.system('cls')

    @staticmethod
    def do_date(arg):
        """Print Date and Time."""
        print(Fore.RED)
        print(datetime.datetime.now())
        print(Style.RESET_ALL)

    @staticmethod
    def do_ping(arg):
        """Send packets to specified website to test communication."""
        try:
            os.system('ping ' + str(arg))
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

    def do_scsv(self, arg):
        """Search for word or sentence in the chosen CSV file."""
        try:
            os.system(f"FIND \"{str(arg)}\" {self.csv_file}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

    @staticmethod
    def do_open(arg):
        """Open files and folders."""
        try:
            os.startfile(arg)
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

    @staticmethod
    def do_about(arg):
        """Scraping and CSV procedures."""
        print("""
            Welcome to Scraper.
            
            This application is a very simple program with a command-line interface and its purpose was
            initially to automate a very simple scraping algorithm that was often by the author.
            
            The application features numerous commands that work to give control over the interface itself, the
            csv file that is specified and the scraping options.
            
            While web scraping remains a task that has numerous tools and demands, this application attempts to 
            keep it simple by allowing the user to simply specify 2 things:
            -HTML Element
            -Element Class
            
            While one might want to scrape on the basis of id or options other than class, the author has deemed
            for the sake of simplicity class to be the best and only option to feature in this application.
            
            As this application has been born from a necessity to automate some simple scraping, it is regularly 
            updated to meet first and foremost the needs of its author.
            
            Commands have been made very simple and short, but perhaps at the cost of total off-the-bat clarity
            of what they do. However, proper documentation has been provided for the commands and can be viewed
            using help/? <cmd>.
            
            The application requires some peculiar things as well:
            1)Parser
            -lxml
            -html.parser
            -html5lib
            
            2)Webpages
            -An initial webpage
            -A template for the rest of the pages replacing page number in the url with $
            
            Follow command documentation carefully.""")
        print("\nCSV File:")
        print("1. You can specify a csv file in which the scraped contents can be written.")
        print("2. You can open that csv file or write a row in it from the console.\n")
        print("Scraping Procedure:")
        print("1. Specify the url of the initial webpage you wish to scrape.")
        print(
            "2. Specify the url template for the rest of the webpages replacing the number of the webpage with a '$'.")
        print("3. The variable is the number of webpages you will scrape.")
        print("4. Specify the HTML Elements you want to scrape.")
        print("5. Specify the class of that element.")
        print("6. If there is no specific class, type '#'.")
        print("7. If there are no more elements to scrape, type 'end'.")
        print("8. The scraping process will start instantly.")

    @staticmethod
    def do_exit(arg):
        """Exit the console."""
        quit()


if __name__ == '__main__':
    scraper = Scraper()
    scraper.cmdloop()
