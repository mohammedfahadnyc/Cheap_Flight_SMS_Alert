# Cheap_Flight_SMS_Alert
For any given Destination and price point, this program searches cheap flights for given time frame (for example from tomorrow to next sixth months) for all those destinations and desired
price point and if found any desired flights, notifies the user via sms alert. I've used
kiwi Partners Tequila Location API to find IATA Codes and Tequila Search API to find cheap flights. Twillo API is used to send SMS Alert.
Update 1.0 : Extended Code has now been uploaded. Now any external users can signup to this service using external link and receieve flight alerts delivered to their email or phone everyday with new cheap deals.
Demo here :


https://user-images.githubusercontent.com/54411378/162666464-31629708-c2e8-473e-90a8-020fb3157224.mov





def create_invite_modal(invoking_id, adding_id):
    invite_modal = {
        "type": "modal",
        "callback_id": "invite-modal",
        "title": {
            "type": "plain_text",
            "text": "Preboarding Invite",
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hello *<@{}>*! :smile:".format(invoking_id)
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Which channels do you want to add *<@{}>* to?".format(adding_id)
                }
            }
            ,
            {
                "type": "divider"
            },
            {
                "type": "input",
                "block_id": "channel_selection",
                "element": {
                    "type": "multi_static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "#channel-name",
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "option-0",
                            },
                            "value": "value-0"
                        }
                    ],
                    "action_id": "multi_static_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Select one or more the following channels:"
                }
            },
            {
                "type": "divider"
            }
        ]
    }
    return invite_modal


def build_options(channel_names, channel_ids):
    options = []
    for i in range(len(channel_names)):
        options.append({
            "text": {
                "type": "plain_text",
                "text": "#{}".format(channel_names[i]),
                "emoji": True
            },
            "value": "{}".format(channel_ids[i])
        })
    return options


def message_display_channels(incoming_message):
    channel_message = [
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "{}".format(incoming_message)
            }
        },
        {
            "type": "divider"
        }
    ]
    return channel_message


def create_model_invite_modal():
    invite_modal = {
        "type": "modal",
        "callback_id": "invite-modal",
        "title": {
            "type": "plain_text",
            "text": "Preboarding: Invite"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "input",
                "block_id": "user_selection",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select user(s)"
                    },
                    "action_id": "multi_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Select up to 5 users to add to channels:"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "block_id": "channel_selection",
                "element": {
                    "type": "multi_static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "#channel-name"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "option-0"
                            },
                            "value": "value-0"
                        }
                    ],
                    "action_id": "multi_select-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Select channels to add for this user(s):"
                }
            },
            {
                "type": "divider"
            }
        ]
    }
    return invite_modal


# build field for channel message responses
def build_field(channel_ids, invalid_ids, valid_message, invalid_message):
    response = ""
    valid_ids = [f'*<#{channel}>*' for channel in channel_ids if channel not in invalid_ids]
    valid_string = ', '.join(str(e) for e in valid_ids)
    response = response + valid_string

    # response for valid ID's
    if len(valid_ids) > 0 and len(invalid_ids) == 0:
        # valid_ids = [f'*<#{channel}>*' for channel in valid_ids]
        response = '' + valid_message + "\n"
        # valid_string = ', '.join(str(e) for e in valid_ids)
        response = response + valid_string

    # response for invalid ID's
    elif len(invalid_ids) > 0 and len(valid_ids) == 0:
        invalid_ids = [f'*<#{channel}>*' for channel in invalid_ids]
        response = response + invalid_message + "\n"
        invalid_string = ', '.join(str(e) for e in invalid_ids)
        response = response + invalid_string

    # response for valid ID's and invalid ID's
    elif len(invalid_ids) > 0 and len(valid_ids) > 0:
        valid_ids = [f'*<#{channel}>*' for channel in valid_ids]
        response = '' + valid_message + "\n"
        # valid_string = ', '.join(str(e) for e in valid_ids)
        response = response + valid_string + "\n \n"
        invalid_ids = [f'*<#{channel}>*' for channel in invalid_ids]
        response = response + invalid_message + "\n"
        invalid_string = ', '.join(str(e) for e in invalid_ids)
        response = response + invalid_string

    return response


# oop
def return_help_message():
    message = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Preboarding Buddy - Help Page"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Command:* \n _/preboard-channels_"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Parameters:* \n _@[User]_ (optional)"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Description*:\nReturns a list of public channels the supplied user is a part of, THIS COMMAND IS DISABLED AND JUST A PLACEHOLDER. \n\n\n *Example Usage:* \n  "
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "/preboard-channels"
                },
                {
                    "type": "mrkdwn",
                    "text": "*_returns your public channels_*"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "/preboard-channels @Ashley"
                },
                {
                    "type": "mrkdwn",
                    "text": "*_returns the public channels Ashley is a part of_*"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Command:* \n _/preboard_"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Parameters:* \n _@[User]_ (optional)"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Description*:\n Opens a window that allows you to select up to 5 users to add to your (or a supplied user's) channels. \n\n\n *Example Usage:* \n"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "/preboard"
                },
                {
                    "type": "mrkdwn",
                    "text": "*_you can choose to add user(s) to any of YOUR public channels_*"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "/preboard @Bob"
                },
                {
                    "type": "mrkdwn",
                    "text": "*_you can choose to add user(s) to any of BOB's public channels_*"
                }
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Command:* \n _/preboard-help_"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Parameters:* \n *_(None)_*"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Description*:\nView this handy-dandy help window for future reference. \n\n\n *Example Usage:*"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "/preboard-help"
                }
            ]
        },
        {
            "type": "divider"
        }
    ]

    return message

