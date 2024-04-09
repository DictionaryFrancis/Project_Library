###### IMPORTS ######
import datetime

####### GLOBAL########
book_names = []
membership_list = []


####### HANDLE BORROW BOOK ######
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

    more_than_4 = membership_list.count(membership_str)
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

        # elif user_choice == 3:
            
        # elif user_choice == 4:
        #     break
################################

if __name__ == '__main__':
    main()
