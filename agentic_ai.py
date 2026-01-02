"""
Support Ticket Management Agent
--------------------------------
This program simulates a simple ticket management chatbot system that interacts with
a JSON file (`tickets.json`). It can:

1. Retrieve ticket details by ticket ID.
2. List tickets by status (open, closed, pending).
3. Update ticket assignment to a different support agent.
4. Summarize ticket information.

This chatbot can read all tickets in memory, processes user queries with regex matching, and updates the JSON file when 
assignments change.
"""

import json
import re
# ==== Load tickets from JSON file ====

with open('tickets.json', 'r') as file:
    """
    Load ticket data from a JSON file.
    """
    tickets = json.load(file)


def get_ticket_by_id(ticket_id: int) -> dict:
    """
    Retrieve ticket details by ticket ID.

    Args: ticket_id (int): The ID of the ticket to retrieve.

    Returns: dict: The ticket details if found, else None.

    """
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            return ticket
    return None

# ==== Helper functions ====
    
def list_tickets_by_status(status: str) -> list:
    """
    List tickets by status (open, closed, pending).

    Args: status (str): The status to filter tickets by.

    Returns: list: A list of tickets matching the status.
    
    """
    return [ticket for ticket in tickets if ticket["status"].lower() == status.lower()]

def update_ticket_assignment(ticket_id: int, assigned_to: str) -> dict:
    """
    Update ticket assignment to a different support agent.

    Args: 
        ticket_id (int): The ID of the ticket to update.
        assigned_to (str): The name of the new support agent.

    Returns: dict: The updated ticket details if found and updated, else None.
    """
    updated_ticket = None

    # Search for the matching ticket
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            ticket["assigned_to"] = assigned_to
            updated_ticket = ticket
            break # Stop searching after updating the ticket
    
    # Save the updated tickets back to the JSON file
    if updated_ticket:
        with open('tickets.json', 'w') as file:
            json.dump(tickets, file, indent=4)
        return updated_ticket
    
    return None

# ==== Main agent logic ====
def process_query(query: str):
    """
    Process user queries related to ticket management.
    Args: query (str): The user query.
    Returns: str: The response to the user query.
    """
    # Normalize the query
    query = query.lower().strip()

    # Case 1: List tickets by status
    if "tickets" in query and ("open" in query or "closed" in query or "pending" in query):
        status_match = re.search(r'open|closed|pending', query)
        if status_match:
            status = status_match.group(0)  
            results = list_tickets_by_status(status)
            if not results:
                return f"No tickets found with status '{status}'."
            response_lines = [
                f"Tickets {t['ticket_id']}: {t['title']} (Assigned to {t['assigned_to']})"
                          for t in results
            ]
            return "\n".join(response_lines)
        else:
            return "Please specify a valid ticket status (open, closed, or pending)."
        
    
    #Case 2: Get ticket details by ID
    assign_match = assign_match = re.search(r"assign (?:ticket )?(\d+)(?: ticket)? to (\w+)", query)
    if assign_match:
        ticket_id = int(assign_match.group(1))
        new_assignee = assign_match.group(2).capitalize()
        ticket = get_ticket_by_id(ticket_id)

        # Check if ticket exists
        if not ticket:
            return f"Ticket {ticket_id} not found."
        
        # Check if already assigned to the same agent
        if ticket["assigned_to"].lower() == new_assignee.lower():
            return f"Ticket {ticket_id} is already assigned to {new_assignee}."
    
        # Update the assignment
        update_ticket_assignment(ticket_id, new_assignee)
        return f"Ticket {ticket_id} is now assigned to {new_assignee}."
    
    # Case 3: Check who is assigned to a ticket or summarize ticket information
    who_match = re.search(r"who (?:is working on|is assigned to) ticket (\d+)", query)
    if who_match:
        ticket_id = int(who_match.group(1))
        ticket = get_ticket_by_id(ticket_id)
        if not ticket:
            return f"Ticket {ticket_id} not found."
        return f"Ticket {ticket_id} is assigned to {ticket['assigned_to']}."
    
    #Case 4: Summarize ticket information
    summary_match = re.search(r"summarize ticket (\d+)", query)
    if summary_match:
        ticket_id = int(summary_match.group(1))
        ticket = get_ticket_by_id(ticket_id)
        if not ticket:
            return f"Ticket {ticket_id} not found."
        return (f"Summary of Ticket {ticket_id}:\n"
                f"Title: {ticket['title']}\n"
                f"Description: {ticket['description']}\n"
                f"Status: {ticket['status']}\n"
                f"Assigned to: {ticket['assigned_to']}")
    
    # Case 5: Fallback for unrecognized queries
    return "Sorry, I couldn't understand that query. Try asking about a ticket ID, status, or assignment."


def main():
    """
    Main function to run the Support Ticket Agent.
    """
    print("=== Support Ticket Agent ===")
    print("Type a question (e.g. 'Show me all open tickets.')")

    while True:
        query = input("You: ")

        # Exit condition
        if query.lower() in ['exit', 'quit']:
            print("Exiting the Support Ticket Agent. Goodbye!")
            break

        # Process the user query
        response = process_query(query)
        print("Support Ticket Agent:", response)

# ==== Run the agent ====
if __name__ == "__main__":
    main()

