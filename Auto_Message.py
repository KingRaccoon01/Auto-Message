import pywhatkit as kit

group_or_individual_question = input("Group Message or Individual:")
group_or_individual = group_or_individual_question.lower()

photo_or_message_question = input("Enter whether you will send a message or a photo:")
photo_or_message = photo_or_message_question.lower()

person_list = {}

group_list = {}

if group_or_individual == "individual":
    
    if photo_or_message == "message":

        message = input("Enter Message:")
        hat_number = input("Enter the line code:")
        person = person_list[input("Enter Who You Will Send the Message To:")]
        phone_number = hat_number + person
        hour = int(input("Enter Time:"))
        minute = int(input("Enter Minute:"))

        kit.sendwhatmsg(phone_number, message, hour, minute, 20, True, 5)

    elif photo_or_message == "photo":

        photo = input("Enter Photo:")
        hat_number = input("Enter the line code:")
        person = person_list[input("Enter Who You Will Send the Message To:")]
        phone_number = hat_number + person
        hour = int(input("Enter Time:"))
        minute = int(input("Enter Minute:"))

        kit.sendwhats_image(phone_number, photo, hour, minute, 20, True, 5)
    
    else:
        print("Select a Valid File Type")

if group_or_individual == "grup":

    if photo_or_message == "message":
        
        message = input("Enter message:")
        group_id = group_list[input("Enter Who You Will Send the Message To:")]
        hour = int(input("Enter Time:"))
        minute = int(input("Enter Minute:"))

        kit.sendwhatmsg_to_group(group_id, message, hour, minute, 20, True, 5)

    if photo_or_message  == "photo":

        photo = input("Enter Photo:")
        group_id = group_list[input("Enter Who You Will Send the Message To:")]
        hour = int(input("Enter Time:"))
        minute = int(input("Enter Minute:"))

        kit.sendwhats_image(group_id, photo, hour, minute)
    