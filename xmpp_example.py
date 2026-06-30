import xml.etree.ElementTree as ET

def create_message_stanza(sender, recipient, body_text, message_id="chat123"):
    """
    Generates a basic XMPP <message> stanza.
    ejabberd processes these stanzas for instant messaging.
    """
    message = ET.Element("message", {
        "to": recipient,
        "from": sender,
        "type": "chat",
        "id": message_id
    })
    body = ET.SubElement(message, "body")
    body.text = body_text
    return ET.tostring(message, encoding='utf-8').decode('utf-8')

def create_presence_stanza(sender, type="available", status_text="Online and ready to chat!"):
    """
    Generates a basic XMPP <presence> stanza.
    ejabberd uses these to manage user presence (online/offline/away).
    """
    presence = ET.Element("presence", {
        "from": sender,
        "type": type
    })
    if status_text and type == "available":
        status = ET.SubElement(presence, "status")
        status.text = status_text
    return ET.tostring(presence, encoding='utf-8').decode('utf-8')

def parse_message_stanza(xml_string):
    """
    Parses an XMPP <message> stanza and extracts key information.
    Simulates how an XMPP server like ejabberd would process incoming messages.
    """
    root = ET.fromstring(xml_string)
    if root.tag != "message":
        return None

    parsed_data = {
        "to": root.get("to"),
        "from": root.get("from"),
        "type": root.get("type"),
        "id": root.get("id"),
        "body": None
    }

    body_element = root.find("body")
    if body_element is not None:
        parsed_data["body"] = body_element.text

    return parsed_data

if __name__ == "__main__":
    print("--- XMPP Stanza Generation Example ---")

    # Example 1: Generate a chat message
    sender_jid = "user1@example.com/resource"
    recipient_jid = "user2@example.com"
    chat_message_body = "Merhaba! ejabberd kurulumu hakkında konuşalım mı?"
    chat_stanza = create_message_stanza(sender_jid, recipient_jid, chat_message_body)
    print("\nGenerated Message Stanza:")
    print(chat_stanza)
    # This XML represents a chat message that an ejabberd server would route.

    # Example 2: Generate an 'available' presence
    presence_stanza = create_presence_stanza(sender_jid)
    print("\nGenerated Available Presence Stanza:")
    print(presence_stanza)
    # This XML indicates a user's online status, managed by ejabberd.

    # Example 3: Generate an 'away' presence
    away_presence_stanza = create_presence_stanza(sender_jid, type="away", status_text="Uzakta, sonra döneceğim.")
    print("\nGenerated Away Presence Stanza:")
    print(away_presence_stanza)
    # ejabberd uses this to update a user's presence state.

    print("\n--- XMPP Stanza Parsing Example ---")

    # Simulate an incoming message stanza (e.g., from another client via ejabberd)
    incoming_xml = """<message to="user1@example.com/resource" from="user2@example.com/mobile" type="chat" id="msg456"><body>Harika fikir! Ne zaman müsaitsin?</body></message>"""
    print("\nIncoming XML to Parse:")
    print(incoming_xml)

    parsed_message = parse_message_stanza(incoming_xml)
    print("\nParsed Message Data:")
    if parsed_message:
        print(f"  To: {parsed_message['to']}")
        print(f"  From: {parsed_message['from']}")
        print(f"  Type: {parsed_message['type']}")
        print(f"  ID: {parsed_message['id']}")
        print(f"  Body: {parsed_message['body']}")
    else:
        print("  Failed to parse message.")
    # This demonstrates how ejabberd or an XMPP client would interpret the XML.