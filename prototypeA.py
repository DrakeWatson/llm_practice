import openai
import json
from turtle import Turtle

# TODO Make this a file read instead of harcdcoded TODO TODO
openai.api_key = ""

_MARBLES = 30

_FUNCTION_MAPPING = {0: 'Nothing else would happen.',
                     1: "An object changes appearance.",
                     2: "An object changes what it is used for.",
                     3: "The magician says something.",
                     4: "A new object is created."}

_MAGIC_TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'new_magic_object',
            'description': 'Pulls a random new and wacky object out of the magical hat',
            "parameters": {
                "type": "object",
                "properties": {
                    'name': {
                        'type': 'string',
                        'description': 'Name of the wacky object'
                    },
                    'what_it_is_used_for': {
                        'type': 'string',
                        'description': 'A brief description of what the object is used for'
                    },
                    'appearance': {
                        'type': 'string',
                        'description': 'A brief description of what the object looks like'
                    },
                    'more_choices': {
                        'type': 'integer',
                        'description': 'What else would happen?'
                                       '0. Nothing else would happen'
                                       '1. An object changes appearance.'
                                       '2. An object changes what it is used for.'
                                       '3. The magician says something. '
                                       '5. An object changes its name.'

                    }

                },
                "required": ["name", "what_it_is_used_for", "appearance", 'more_choices']

            }

        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'change_appearance',
            'description': 'Changes the appearance of the object based on the prompt provided',
            "parameters": {
                "type": "object",
                "properties": {
                    'name_of_object': {
                        'type': 'string',
                        'description': 'The name of the object that is changing appearance.'
                    },

                    'new_appearance': {
                        'type': 'string',
                        'description': 'A brief description of what the object looks like after the appearance '
                                       'has changed based on the prompt.'
                    },
                    'more_choices': {
                        'type': 'integer',
                        'description': 'The integer value before which of these descriptions would for certain '
                                       'also happen: '
                                       '0. Nothing else would happen'
                                       '2. An object changes what it is used for.'
                                       '3. The magician says something. '
                                       '4. A new object is created. '
                                       '5. An object changes its name.'

                    }

                },
                "required": ["name_of_object", "new_appearance", 'more_choices']

            }

        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'change_what_it_is_used_for',
            'description': 'Changes what the object is used for based on the prompt provided',
            "parameters": {
                "type": "object",
                "properties": {
                    'name_of_object': {
                        'type': 'string',
                        'description': 'The name of the object that is changing appearance.'
                    },

                    'new_what_it_is_used_for': {
                        'type': 'string',
                        'description': 'A brief description of what the object is used for after the event or '
                                       'action in the prompt has occurred'
                    },
                    'more_choices': {
                        'type': 'integer',
                        'description': 'The integer value before which of these descriptions would for certain '
                                       'also happen: '
                                       '0. Nothing else would happen'
                                       '1. An object changes appearance.'
                                       '3. The magician says something. '
                                       '4. A new object is created. '
                                       '5. An object changes its name.'

                    }

                },
                "required": ["name_of_object", "new_what_it_is_used_for", "more_choices"]

            }

        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'change_name',
            'description': 'Changes the name of the object based on what has happened to the object in the '
                           'prompt. For example, if a snowball melted its name would change from snowball to '
                           'water.',
            "parameters": {
                "type": "object",
                "properties": {
                    'new_name': {
                        'type': 'string',
                        'description': 'The new name of the object after the prompt.'
                    },
                    'more_choices': {
                        'type': 'integer',
                        'description': 'The integer value before which of these descriptions would for certain '
                                       'also happen: '
                                       '0. Nothing else would happen'
                                       '1. An object changes appearance.'
                                       '2. An object changes what it is used for.'
                                       '3. The magician says something. '
                                       '4. A new object is created. '

                    }

                },
                "required": ["new_name", 'more_choices']

            }

        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'say_something',
            'description': 'For when the magician just needs to respond to the user with a statement. No magic '
                           'objects are changed or modified or created.',
            "parameters": {
                "type": "object",
                "properties": {
                    'what_to_say': {
                        'type': 'string',
                        'description': 'The magicians mysterious response to the prompt.'
                    },
                    'more_choices': {
                        'type': 'integer',
                        'description': 'The integer value before which of these descriptions would for certain '
                                       'also happen: '
                                       '0. Nothing else would happen'
                                       '1. An object changes appearance.'
                                       '2. An object changes what it is used for.'
                                       '4. A new object is created. '
                                       '5. An object changes its name.'
                    }

                },
                "required": ["what_to_say", 'more_choices']

            }

        }
    }]


def main():
    the_magic_hat(False)

    return 1


def turtle_tester():
    t = Turtle()
    t.screen.title("Whoa!")
    myVar = t.screen.textinput("The Title", "This is my prompt, respond!!!")
    t.screen.register_shape("triangle", ((5, -3), (0, 5), (-5, -3)))
    t.screen.register_shape("images\\anvil.gif")
    t.shape("images\\anvil.gif")
    print(myVar)
    t.screen.bgcolor("green")
    for i in range(100):
        t.right(20)
        t.fd(20)

    t.shape("triangle")
    t.screen.mainloop()
    return 1


class MagicObject:

    def __init__(self, name, what_it_is_used_for, appearance):
        self.name = name
        self.what_it_is_used_for = what_it_is_used_for
        self.appearance = appearance

    def __str__(self):
        return f"{self.name} used for {self.what_it_is_used_for} and looks like {self.appearance}\n"

    def change_appearance(self, new_appearance):
        self.appearance = new_appearance
        return self

    def change_what_it_is_used_for(self, new_what_it_is_used_for):
        self.appearance = new_what_it_is_used_for
        return self

    def change_name(self, new_name):
        self.appearance = new_name
        return self


class MagiciansBag:

    def __init__(self):
        self.items = []
        self.recent_actions = []

    def __str__(self):
        return f"The magician's bag contains {self.items}"

    def add_magic_object(self, object_of_magic):
        self.items.append(object_of_magic)

    def remove_magic_object(self, old_magic_object):
        self.items.remove(old_magic_object)

    def new_recent_action(self, recent_action):
        self.recent_actions.append(recent_action)

    def get_recent_actions(self):
        return self.recent_actions

    def clear_recent_actions(self):
        self.recent_actions = []


def the_magic_hat(debug):
    keep_running = True
    print("You have wandered into a magician's tent while attending a circus. The man stands before you holding a hat "
          "in one hand and a magic wand in the other. His raised eyebrow inquires at you- \'What shall I do for you?\'")

    magicians_magical_bag = MagiciansBag()
    magic_query = "user-input"
    user_query = ""
    while keep_running:
        if magic_query == "user-input":
            user_query = input("What to ask the magician?\n:")
            response = send_magician_function_query(user_query, magicians_magical_bag)
        else:
            response = send_magician_function_query(magic_query, magicians_magical_bag)

        keep_running, magic_query = perform_magic(response, magicians_magical_bag, user_query, debug)

    return 1


def send_magician_function_query(query, magicians_magical_bag):
    global _MAGIC_TOOLS
    bag_string = ""

    if len(magicians_magical_bag.items) != 0:
        bag_string = f"The magician has already pulled {magicians_magical_bag.items} out of the hat for them."
    else:
        bag_string = "The user has just walked into the circus tent."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"The user is inside a circus tent with a performing magician who can pull"
                                           f"magic objects out of a hat. The user will ask something of the magician. "
                                           f"Do not respond to the user's question. Select a function from the "
                                           f"provided list based on what would most likely given the user's query to "
                                           f"the magician."
                                           f"{bag_string}"},
            {"role": "user", "content": query}],
        tools=_MAGIC_TOOLS
    )
    return response


def send_magician_normal_query(query, magicians_magical_bag):
    global _MAGIC_TOOLS

    bag_string = ""
    if len(magicians_magical_bag.items) > 1:
        bag_string = f"The magician has the following magic items: {magicians_magical_bag.items}."
    else:
        bag_string = "The magician has not pulled anything out of the hat yet."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Describe the actions of a magician with a magic hat. The magician is "
                                          f"inside a circus tent and there is only one other person in the tent with "
                                          f"the magician. The magician is performing for this person. "
                                          f"{bag_string}"},
            {"role": "user", "content": query}]
    )

    return response


def perform_magic(ai_response, magicians_magical_bag, user_query, debug):
    global _FUNCTION_MAPPING

    keep_running = True
    action_string = ""

    if debug:
        print(f"DEBUG DEBUG DEBUG\n{ai_response}\nDEBUG DEBUG DEBUG")

    function_name = ai_response.choices[0].message.tool_calls[0].function.name
    arguments = ai_response.choices[0].message.tool_calls[0].function.arguments

    if debug:
        print(function_name)
        print(arguments)

    arguments = json.loads(arguments)
    return_val = globals()[function_name](**arguments)  # Call the function

    if function_name == "new_magic_object":
        action_string = f"The magician created the following new magic object {str(return_val)}. "
        magicians_magical_bag.add_magic_object(return_val)

    elif function_name == "change_appearance":
        for magic_item in magicians_magical_bag.items:
            if magic_item.name == return_val[0]:
                action_string = f"{magic_item.name}'s appearance changed from {magic_item.appearance} to {return_val[1]}. "
                magic_item.change_appearance(return_val[1])

    elif function_name == "change_what_it_is_used_for":
        for magic_item in magicians_magical_bag.items:
            if magic_item.name == return_val[0]:
                action_string = f"{magic_item.name}'s use changed from {magic_item.what_it_is_used_for} to {return_val[1]}. "
                magic_item.change_what_it_is_used_for(return_val[1])

    elif function_name == "change_name":
        for magic_item in magicians_magical_bag.items:
            if magic_item.name == return_val[0]:
                action_string = f"{magic_item.name}'s name changed to {return_val[1]}. "
                magic_item.change_name(return_val[1])

    elif function_name == "say_something":
        action_string = f"The magician tells the person '{return_val}'. "

    magicians_magical_bag.new_recent_action(action_string)

    if arguments["more_choices"]:
        next_function = _FUNCTION_MAPPING[arguments["more_choices"]]
        magic_query = f"The user just prompted you with: \'{user_query}\'. " \
                      f"You must call the function named {next_function} based on the user's prompt. " \
                      f"You have already selected these for the more_choices argument: " \
                      f"{magicians_magical_bag.get_recent_actions()} " \
                      f"Cannot repeat any already selected choices for {next_function}'s more_choices argument."

    else:
        recent_actions = ""
        for recent_action in magicians_magical_bag.get_recent_actions():
            recent_actions += f"{recent_action}. "

        magic_query = f'The person just asked the magician: \'{user_query}\'. ' \
                      f'Create a short description that includes these facts: {recent_actions}'

        if debug:
            print(magic_query)
        ai_response = send_magician_normal_query(magic_query, magicians_magical_bag)
        print(f'\n    {ai_response.choices[0].message.content}')

        magicians_magical_bag.clear_recent_actions()
        magic_query = "user-input"

    if debug:
        print(user_query)

    return keep_running, magic_query


def new_magic_object(name, what_it_is_used_for, appearance, more_choices):
    created_magic_object = MagicObject(name, what_it_is_used_for, appearance)

    return created_magic_object


def change_appearance(name_of_object, new_appearance, more_choices):
    return [name_of_object, new_appearance]


def change_what_it_is_used_for(name_of_object, new_what_it_is_used_for, more_choices):
    return [name_of_object, new_what_it_is_used_for]


def change_name(original_name, new_name, more_choices):
    return [original_name, new_name]


def say_something(what_to_say, more_choices):
    return what_to_say


def ask_questions():
    question = input("What is ur question?\n")
    while question != "Ok":

        question = input("What is your AI query?")

        ai_prompt = [{"role": "person with bag of marbles",
                      "content": ""},
                     {"role": "user",
                      "content": question
                      }]
        tries = 0
        while tries < 3:
            try:
                chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=ai_prompt)

                print(chat.choices[0].message.content)
                tries = 3
            except openai.error.APIError as e:
                if tries == 3:
                    return -1

            tries += 1

    return 1


def marble_exp():
    marble_tools = [
        {
            'type': 'function',
            'function': {
                'name': 'remove_marble',
                'description': 'Removes a marble from the bag',
                'parameters': {}
            }

        },
        {
            'type': 'function',
            'function': {
                'name': 'add_marble',
                'description': 'Adds a marble to the bag',
                'parameters': {}
            }

        },
        {
            'type': 'function',
            'function': {
                'name': 'shake_bag',
                'description': 'Shakes the bag of marbles',
                'parameters': {}
            }

        },
        {
            'type': 'function',
            'function': {
                'name': 'draw_random_marble',
                'description': 'Will take a marble out of the bag',
                'parameters': {}
            }

        }]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "I need a random marble out of the bag"}],
        tools=marble_tools

    )
    print(response)
    specific_response = response.choices[0].message.tool_calls[0].function.name
    print(specific_response)
    return 1


def remove_marble():
    global _MARBLES
    _MARBLES -= 1
    print(f"Removed a marble! # Of Marbles | {_MARBLES} |")
    return 1


def add_marble():
    global _MARBLES
    _MARBLES -= 1
    print(f"Added a marble! # Of Marbles | {_MARBLES} |")
    return 1


def shake_bag():
    print("Shook the bag")

    return 1


def draw_random_marble():
    print("I drew a marble!")

    return 1


if __name__ == "__main__":
    main()
