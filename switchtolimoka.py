from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from hikkatl.types import Message
from .. import loader, utils
import asyncio

@loader.tds
class SwitchToLimoka(loader.Module):
    """Auto switching from Hikka to Limoka"""

    strings = {"name": "SwitchToLimoka"}
    
    async def client_ready(self, client, db):
        self._db = db

        if self.get("done"):
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text='Dev', url='https://t.me/ThisLyomi')],[
                InlineKeyboardButton(text='Github', url='https://github.com/amm1edev/limoka')
            ]]
            )
            await self.inline._bot.send_photo(
                self.tg_id, 
                "https://0x0.st/8osY.jpg",
                caption="<b>hi, you are on the t.me/thislyomi fork, thanks for installing!</b>"
                "\nModule for switching is unloaded.",
                reply_markup=keyboard,
            )

            self.set("done", None) # db need to be clear, for case if user backup db and switches once more
      await self.invoke('unloadmod', 'SwitchToLimoka', self.inline.bot_id)

    @loader.command()
    async def switch(self, message: Message):
        """ - Automatically switch to limoka fork."""

        await utils.answer(message, "<emoji document_id=5122933683820430249>⭕️</emoji><b> Wait...</b>
")

        if "amm1edev" in utils.get_git_info()[1]:
            return await utils.answer(message, "<emoji document_id=4927334452184482448>🔇</emoji> <b>are you serious? you're already on the fork.</b>
")

        await utils.answer(message, "<emoji document_id=5116298753917060171>🐍</emoji>
 <b>switching...</b>")

        await asyncio.create_subprocess_shell(
            "git remote set-url origin https://github.com/amm1edev/Limoka.git",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=utils.get_base_dir(),
        )

        await asyncio.create_subprocess_shell(
            "git pull",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=utils.get_base_dir(),
        )

        peer_id = self.inline.bot_id

        await self.invoke('fconfig', 'updater GIT_ORIGIN_URL https://github.com/amm1edev/Limoka', peer_id)

        await utils.answer(message, "restarting.")

        self.set("done", True)

        await self.invoke('update', '-f', peer_id)
