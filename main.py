###### IMPORTS ######
import datetime

####### GLOBAL########
book_names = []
membership_list = []


####### HANDLE BORROW BOOK ######

def count_books_borrowed(membership):
    count = 0
    with open('borrowed_books.txt', 'r') as document:
        for line in document:
            parts = line.strip().split(',')
            if str(membership) == parts[1].strip():
                count += 1
    return count

def handle_borrow(name:str, membership_number:int,book):
    # here we are open the file as reading, then split each part and appending it in the array
    with open('book_inventory.txt', 'r') as document:
        for line in document:
            parts = line.split(',', 1)
            book_name = parts[0].strip()
            book_names.append(book_name)

    # transform the int in string
    membership_str = str(membership_number)
    if len(membership_str) != 6:
        print('Membership number must be exactly 6 digits, try again!')
        return None
    
    print(f'Name: {name}, Membership Number: {membership_number}')

    more_than_4 = count_books_borrowed(membership_number)
    # Here, we are checking if the user has more than 4 or not, if he/she has more they cannot borrow anymore
    if book in book_names:
        print(f'{book} is in the inventory, you can borrow it!')
        while True:
            if more_than_4 > 4:
                print(f'Sorry, you cannot borrow anymore, you borrowed more than 4 books.')
                break
            else:
                print(f'You borrowed less than 4 books, so you are available to borrow!')
            borrow = input('Would you like to borrow it? (yes/no)')
            if borrow.lower() == 'yes':
                print('done')
                with open('borrowed_books.txt', 'a') as document:
                    while True:
                        today = datetime.date.today()
                        date_today = today.strftime("%Y-%m-%d")
                        document.write(f'{name}, {membership_number}, {book}, {date_today}\n')
                        print(f'Information was saved successfully!')
                        break
                break
            elif borrow.lower() == 'no':
                print('ok, thank you')
                break
            else:
                print('Please enter a valid command (yes or no)')
    else:
        print(f'Sorry, {book} is not in the inventory.')

    return name, membership_number, book        


################################

####### HANDLE RETURN THE BOOK #######

# Here, due_date will be equal 7
def calculate_fine(today, due_date):
    '''
    Function created to calculate the fine
    :param today:
    :param due_date:
    :return: fine that the person will pay
    '''
    fine = today - due_date
    if fine.days > 7:
        #Here is 2 because it is 2 euros per day
        return 2 * (fine.days - 7)

    return 0

def list_books_borrowed_by_user(name, membership):
    '''
    The idea behind this function is read the file borrowed_book.txt
    and bring the membership number and date separate
    :param name:
    :param membership:
    :return:
    '''
    books_borrowed = []
    with open('borrowed_books.txt', 'r') as document:
        for line in document:
            parts = line.strip().split(',')
            if parts[0].strip() == name and parts[1].strip() == membership:
                book_title = parts[2].strip()
                borrow_date = parts[3].strip()
                books_borrowed.append((book_title, borrow_date))
    return books_borrowed

def handle_return_book(membership):
    '''
    This function bring us the books that the user wants to return
    showing us via index the books selected
    :param membership:
    '''
    name = input('Enter your name >>> ')
    books_borrowed = list_books_borrowed_by_user(name, membership)
    if not books_borrowed:
        print('No books were found to return.')
        return

    print('Books you have borrowed:')
    for i, (title, due_date) in enumerate(books_borrowed, start=1):
        print(f'{i}. {title} (Due by: {due_date})')

    book_index = int(input('Select the number of the book you wish to return: ')) - 1
    book_to_return, due_date_str = books_borrowed[book_index]

    #Here, we are going to check if the book is overdue
    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
    today = datetime.date.today()
    fine = 0
    if(today - due_date).days > 7:
        fine = calculate_fine(today, due_date)
        print(f'The book is overdue. Your fine is {fine} euros')
    else:
        print('Thank you for returning the book on time.')
    # Here, remove the book from borrowed_books.txt
    with open('borrowed_books.txt', 'r') as document:
        lines = document.readlines()
    with open('borrowed_books.txt', 'w') as document:
        for line in lines:
            if line.strip() != f"{name}, {membership}, {book_to_return}, {due_date_str}":
                document.write(line)
    print(f'{book_to_return} has been returned successfully!')

#################################

####### REVIEW BORROWED BOOK #######

def display_borrowed_books():
    '''
    It is going to show the books borrowed
    :return:
    '''
    print('All borrowed books:')
    with open('borrowed_books.txt', 'r') as document:
        for line in document:
            parts = line.strip().split(',')
            if len(parts) < 4: continue
            print(f"Member: {parts[0]}, Book: {parts[2]}, Borrow Date: {parts[3]}")


def display_books_by_user():
    '''
    Show us specific user's book
    :return:
    '''
    member_name = input('Enter the user name to view their borrowed books:')
    print(f'Borrowed books by {member_name}: ')
    found = False
    with open('borrowed_books.txt', 'r') as document:
        for line in document:
            parts = line.strip().split(',')
            if parts[0].strip() == member_name:
                found = True
            print(f"Member: {parts[0]}, Book: {parts[2]}, Borrow Date: {parts[3]}")
    if not found:
        print('No books found for this member!')

def review_borrowed_books():
    while True:
        print("Review Borrowed Books:\n"
              "1. Display all borrowed books\n"
              "2. Display books borrowed by a specific member\n"
              "3. Back to main menu:\n")
        choice = input('Choose an option: ')

        if choice == '1':
            display_borrowed_books()
        elif choice == '2':
            display_books_by_user()
        elif choice == '3':
            break
        else:
            print("Invalid option, please try again.")

#################################

########## MANAGE INVENTORY #############

def display_inventory():
    '''
    display the file book_inventory
    :return:
    '''
    with open('book_inventory.txt') as document:
        books = document.readlines()
        print('Current Inventory:')
        for book in books:
            print(book.strip())

def add_new_book():
    '''
    function to add new book in the list(file book_inventory.txt)
    :return:
    '''

    title = input('Enter the book title > ')
    author = input("Enter the author's name > ")
    total_copies = input('Enter the total copies available > ')
    copies_borrowed = input('Enter the copies borrowed > ')
    with open('book_inventory.txt', 'a') as document:
        document.write(f"{title}, {author}, {total_copies}, {copies_borrowed}\n")
    print('Book added!')

def remove_book():
    '''
    function to remove book in the list(file book_inventory.txt)
    :return:
    '''

    title_removed = input('Enter the title of the book to remove > ')
    with open('book_inventory.txt', 'r') as document:
        books = document.readlines()
    with open('book_inventory.txt', 'w') as document:
        for book in books:
            if title_removed not in book.split(',')[0]:
                document.write(book)
    print('Book remeved!')



def update_book():
    '''
    function to update book in the list(file book_inventory.txt)
    :return:
    '''

    title_to_update = input('Enter the title of the book to update: ')
    print("Do you want to update:\n"
          "1. Total copies available\n"
          "2. Copies borrowed")
    choice = input('Choose an option > ')
    new_value = input('Enter the new value > ')

    update_book = []

    with open('book_inventory.txt', 'r') as document:
        for book in document:
            parts = book.strip().split(', ')
            if parts[0] == title_to_update:
                if choice == '1':
                    parts[2] = new_value
                elif choice == '2':
                    parts[3] = new_value
                update_book.append(', '.join(parts) + '\n')
            else:
                update_book.append(book)

    with open('book_inventory.txt', 'w') as document:
        document.writelines(update_book)
    print('Book updated!')


def manage_inventory():
    '''
    This function will manage the inventory, so the admin choices
    :return:
    '''

    while True:
        print("Choose an option:\n"
              "1. Add a new book\n"
              "2. Remove a book\n"
              "3. Update book details:\n"
              "4. Return to main menu")
        choice = input('Choose an option: ')

        if choice == '1':
            add_new_book()
        elif choice == '2':
            remove_book()
        elif choice == '3':
            update_book()
        elif choice == '4':
            break
        else:
            print("Invalid option, please try again.")



####### FUNCTION MAIN ##########
def main():
    while True:
        print('-' * 40)
        user_choice = int(input('Choose an option:\n'
                                '1. Borrow Book.\n'
                                '2. Return Book.\n'
                                '3. Review Borrowed Books.\n'
                                '4. Manage Inventory.\n'
                                '5. Quit the program.'))
        print('-' * 40)
        if user_choice == 1:
            while True:
                name = input('Insert your name >>> ')
                if 1 <= len(name) <= 20 and name.isalpha():
                    print(name)
                    break
                else:
                    print('Please ensure the name is correct: not exceed 20 characters!')
            while True:
                try:
                    membership_number = int(input('Insert membership numbre >>> '))
                    break
                except ValueError:
                    print(
                        'Membership number should be numeric'
                    )
            while True:
                book = input('Insert a book name >>> ')
                handle_borrow(name, membership_number, book)
                break

        elif user_choice == 2:
            membership_number = input('Insert membership number >>> ')
            handle_return_book(membership_number)

        elif user_choice == 3:
            review_borrowed_books()
        elif user_choice == 4:
            manage_inventory()
################################

if __name__ == '__main__':
    main()
