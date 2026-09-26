import sqlite3 

connection = sqlite3.connect("tickets.db")

cursor = connection.cursor()

cursor.execute( """
CREATE TABLE IF NOT EXISTS tickets (
        ticketsID INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        desciption TEXT NOT NULL, 
        priority TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'open'



)


"""
             
)
connection.commit()
#---------------------------
def create_tickets():

    print("\n---Creating new ticket---")

    while True:
        title = input("Title of ticket: ")
        if title:
            break
        print("title cant br empty")
    while True:
        desciption  = input("Description of ticket: ")
        if desciption:
            break
        print("description cant be empty")

    while True:
        priority = input("Priority lvl of the ticket(low/medioum/high): ").capitalize().strip()
        if priority in ["Low", "Medium", "High"]:
            break
        print("please enter valid input")

    cursor.execute("""
            INSERT INTO tickets(title, desciption, priority)
            VALUES(?,?,?)

        """, (title, desciption, priority)


    )
    connection.commit()
    print("\n---Ticket Created succesfully---")
    print("TicketID:", cursor.lastrowid)
#---------------------------------------
def view_tickets():
    print("\n---Tickets List----")
    cursor.execute(
        """
        SELECT * FROM tickets 
        
        """
    )
    tickets = cursor.fetchall()

    if not tickets:
        print("No tickets found")
        return
    for ticket in tickets:
        ticketID = ticket[0]
        title = ticket[1]
        description = ticket[2]
        priority = ticket[3]
        status = ticket[4]

        print("\n" + "=" * 40)
        print(f"TicketID: {ticketID}")
        print("=" * 40)

        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"priority: {priority}")
        print(f"Status: {status}")
    print("\n" + "=" * 40)
    print(f"Total tickets: {len(tickets)}")
#----------------------------------------
def ticket_summery():
    cursor.execute(
        """
        SELECT status, COUNT(*)
        FROM tickets 
        GROUP BY status
        """
    )
    results = cursor.fetchall()
    print("\n ------Loading Summary------")
    if not results:
        print("No tickets available")
        return

    for status, count in results:
        print(f"{status}: {count}")
#----------------------------------------
def search_ticket():
    print("\n ------search bar loaded--------")
    searchID = input("Search ticketID: ").strip()
    if not searchID.isdigit():
        print("please enter a vaild input")
    cursor.execute("""
                Select * FROM tickets WHERE ticketsID = ?
                   """, (searchID,)
    )
    search_result = cursor.fetchall()
    if search_result is None:
        print("there is no such ticket")
        return
    for search in search_result:
        print("\n" + "=" * 40)
        print(f"TicketID: {search[0]}")
        print("=" * 40)

        print(f"Title: {search[1]}")
        print(f"Description: {search[2]}")
        print(f"Priority:{search[3]} ")
        print(f"status: {search[4]}")

#----------------------------------------
def update_ticket_progress():

    print("\n ---Bringing up upadate menu---")

    select_ticket = input("Please enter ticketID: ")
    while True:
        new_status = input("New status(In progress/ resolved/open: ").strip().title()
        if new_status in ["In Progress", "Resolved", "Open"]:
            break
        print("invalid entry try again")

    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE ticketsID = ?
    
        """,(new_status, select_ticket)

    )

    connection.commit()

    if cursor.rowcount == 0:
        print("ticket not found")

    else:
        print("tick updated succesfully ")
#--------------------------------------------------------
def delete_ticket():
    print("\n----Delete menu loading")
    ticket_id = input("Put ticketID to delete: ")

    cursor.execute("""
          SELECT * FROM tickets WHERE ticketsID = ?
        """, (ticket_id,)

    )
    ticket = cursor.fetchall()
    if not ticket:
        print("Ticket not found")
        return 

    conformation = input("Are you sure you want to delete this ticket?(Y/N): ").lower().strip()
    if conformation == "y":
        cursor.execute(
            """ 
            DELETE FROM tickets WHERE ticketsID = ?
            """, (ticket_id,)
        )
        connection.commit()
        print("Deleted Successfull")
    else:
        print("Deletion failed")
#---------------------------------------------------------
def main_menu():
    while True:
        print("\n---IT Suporrt tickets---")
        print("--->Press 1 to create a ticket")
        print("--->Press 2 to view a ticket")
        print("--->Press 3 to update ticket progession")
        print("--->press 4 to delete a ticket")
        print("--->press 5 to view summary")
        print("--->press 6 to search with ticketID")
        print("--->press 7 to exist")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_tickets()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            update_ticket_progress()
        elif choice == "4":
            delete_ticket()
        elif choice == "5":
            ticket_summery()
        elif choice == "6":
                search_ticket()
       
        elif choice == "7":
            print("Exited Succesfully")
            break
        else:
            print("Invalid input please try again")
            
main_menu()
connection.close()
