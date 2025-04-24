import pywhatkit as kit
import json
import os
import argparse

# Help message
HELP_MESSAGE = """
📌 **Automatic WhatsApp Message Sender - Help Guide** 📌

This program uses the **pywhatkit** library to send scheduled messages or images (PNG, JPG) 
to individual contacts or groups via WhatsApp.

🔹 **Steps to Use**
1️⃣ **Open WhatsApp Web:**  
   - Before running the program, open **WhatsApp Web** in your browser.  
   - If WhatsApp Web is not open, the message-sending process may fail!  

2️⃣ **Run the Program:**  
   - **For Windows:**  
     ```bash
     python otomsg.py
     ```
   - **To display the help menu:**  
     ```bash
     python otomsg.py -h
     ```
   - **Follow the instructions in the program to send messages to a group or an individual.**  

3️⃣ **Adding Contacts or Groups**  
   - To **add a new individual contact**:  
     - When the program asks, **"Would you like to add a new contact?"**, type **"yes"**.  
     - Enter the person's name and phone number.  
     - The contact will be saved and available for future use.  
   - To **add a new group**:  
     - Obtain the group ID from WhatsApp.  
     - Follow the group addition steps when prompted by the program.  

4️⃣ **Sending Messages:**  
   - Choose whether to send an **individual message**, a **group message**, or a **bulk message**.  
   - Select the recipient(s) and enter the message.  
   - Specify the **hour and minute** for the message to be sent.  
   - The message will be **automatically sent via WhatsApp at the scheduled time!** 🎯  

💡 **Additional Information**
- Before running the program, you can manually edit **rehber.json** to manage contacts.  
- **Do not close WhatsApp Web while sending messages!**  
- Ensure that both your phone and computer have an active internet connection.  

🚀 **You are now ready to send automated WhatsApp messages!**  
If you have any questions, you can check the help menu again with:  
```bash
python otomsg.py -h" " \
    """

# Handle arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", action="store_true", help="Show help message")
args, _ = parser.parse_known_args()

# Show help message and exit if -h or --help is used
if args.help:
    print(HELP_MESSAGE)
    exit()

# Load contacts from JSON
def load_data(filename="contacts.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"person_list": {}, "group_list": {}}

# Save contacts to JSON
def save_data(data, filename="contacts.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Load saved contacts
data = load_data()
person_list = data["person_list"]
group_list = data["group_list"]

# Ask the user for message type
group_or_individual = input("Group Message or Individual or Bulk: ").lower()
photo_or_message = input("Enter whether you will send a message or a photo: ").lower()

if group_or_individual == "individual":

    add_person = input("Would you like to add a new contact? (yes/no): ").lower()
    if add_person == "yes":
        name = input("Enter the name of the person: ")
        phone = input("Enter their phone number (with country code, e.g. +1...): ")
        person_list[name] = phone
        save_data({"person_list": person_list, "group_list": group_list})

    recipient_name = input("Enter the contact name to send the message: ")
    if recipient_name in person_list:
        phone_number = person_list[recipient_name]
        hour = int(input("Enter Time (Hour): "))
        minute = int(input("Enter Minute: "))

        if photo_or_message == "message":
            message = input("Enter Message: ")
            kit.sendwhatmsg(phone_number, message, hour, minute, 20, True, 5)

        elif photo_or_message == "photo":
            photo = input("Enter Photo Path: ")
            kit.sendwhats_image(phone_number, photo, hour, minute, 20, True, 5)

        else:
            print("Select a Valid File Type")
    else:
        print("Contact not found. Please add it first.")

elif group_or_individual == "group":

    add_group = input("Would you like to add a new group? (yes/no): ").lower()
    if add_group == "yes":
        group_name = input("Enter the name of the group: ")
        group_id = input("Enter the group ID: ")
        group_list[group_name] = group_id
        save_data({"person_list": person_list, "group_list": group_list})

    group_name = input("Enter the group name to send the message: ")
    if group_name in group_list:
        group_id = group_list[group_name]

        hour = int(input("Enter Time (Hour): "))
        minute = int(input("Enter Minute: "))

        if photo_or_message == "message":
            message = input("Enter message: ")
            kit.sendwhatmsg_to_group(group_id, message, hour, minute, 20, True, 5)

        elif photo_or_message == "photo":
            photo = input("Enter Photo Path: ")
            kit.sendwhats_image(group_id, photo, hour, minute)

        else:
            print("Select a Valid File Type")
    else:
        print("Group not found. Please add it first.")

elif group_or_individual == "bulk":
    print("\nAvailable contacts:")
    for name in person_list:
        print(f"- {name}")

    selected_names = input("Enter names separated by commas (or type 'all' to message everyone): ").strip()

    if selected_names.lower() == "all":
        recipients = list(person_list.items())
    else:
        recipients = [(name.strip(), person_list[name.strip()]) for name in selected_names.split(",") if name.strip() in person_list]

    hour = int(input("Enter Time (Hour): "))
    minute = int(input("Enter Minute: "))
    message = input("Enter Message: ")

    for idx, (name, number) in enumerate(recipients):
        msg_minute = minute + idx
        adj_hour = hour + (msg_minute // 60)
        adj_minute = msg_minute % 60
        print(f"Scheduled message for {name} at {adj_hour}:{adj_minute:02}")
        kit.sendwhatmsg(number, message, adj_hour, adj_minute, 20, True, 5)

else:
    print("Invalid choice, please enter 'individual', 'group', or 'bulk'.")
