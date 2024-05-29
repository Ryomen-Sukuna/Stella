#    Stella (Development)
#    Copyright (C) 2021 - meanii (Anil Chauhan)
#    Copyright (C) 2021 - SpookyGang (Neel Verma, Anil Chauhan)

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from Stella import StellaCli
from Stella.database.notes_mongo import is_pnote_on, set_private_note
from Stella.helper import custom_filter
from Stella.helper.anon_admin import anonadmin_checker
from Stella.helper.chat_status import isUserAdmin
from Stella.plugins.connection.connection import connection

PRIVATE_NOTES_TRUE = ["on", "true", "yes", "y"]
PRIVATE_NOTES_FALSE = ["off", "false", "no", "n"]


@StellaCli.on_message(custom_filter.command(commands=("privatenotes")))
@anonadmin_checker
async def PrivateNote(client, message):
    if await connection(message) is not None:
        chat_id = await connection(message)
    else:
        chat_id = message.chat.id

    if not await isUserAdmin(message):
        return

    if len(message.command) >= 2:
        if message.command[1] in PRIVATE_NOTES_TRUE:
            set_private_note(chat_id, True)
            await message.reply(
                "Stella will now send a message to your chat with a button redirecting to PM, where the user will receive the note.",
                quote=True,
            )

        elif message.command[1] in PRIVATE_NOTES_FALSE:
            set_private_note(chat_id, False)
            await message.reply(
                "Stella will now send notes straight to the group.", quote=True
            )
        else:
            await message.reply(
                f"failed to get boolean value from input: expected one of y/yes/on/true or n/no/off/false; got: {message.command[1]}",
                quote=True,
            )
    else:
        if is_pnote_on(chat_id):
            await message.reply(
                "Your notes are currently being sent in private. Stella will send a small note with a button which redirects to a private chat.",
                quote=True,
            )
        else:
            await message.reply(
                "Your notes are currently being sent in the group.", quote=True
            )
