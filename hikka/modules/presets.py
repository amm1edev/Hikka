# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import logging

from .. import loader, utils
from ..inline.types import BotInlineMessage, InlineCall

logger = logging.getLogger(__name__)


PRESETS = {
    "fun": [
        "https://raw.githubusercontent.com/C0dwiz/H.Modules/main/AnimeQuotes.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/artai.py",
        "https://raw.githubusercontent.com/hikariatama/ftg/master/inline_ghoul.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/inline_lovemagic.py",
        "https://raw.githubusercontent.com/hikariatama/ftg/master/mindgame.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/love.py",
        "https://raw.githubusercontent.com/hikariatama/ftg/master/neko.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/purr.py",
        "https://raw.githubusercontent.com/hikariatama/ftg/master/rpmod.py",
        "https://raw.githubusercontent.com/hikariatama/host/master/nsfw.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/tictactoe.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/trashguy.py",
        "https://raw.githubusercontent.com/hikariatama/ftg/master/truth_or_dare.py",
        "https://raw.githubusercontent.com/hikariatama/host/master/kang.py",  
        "https://raw.githubusercontent.com/Fixyres/Modules/main/SQuotes.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/spam.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/IrisLab.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/mazemod.py",
        "https://raw.githubusercontent.com/Den4ikSuperOstryyPer4ik/Astro-modules/main/minesweeper.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/RPSgame.py",
    ],
    "chat": [
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/RPSgame.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/banstickers.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/hikarichat.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/inactive.py",
        "https://raw.githubusercontent.com/Fixyres/Modules/main/Triggers.py",
        "https://raw.githubusercontent.com/amm1edev/AmeMods/main/MentionAll.py",
        "https://0x0.st/s/_oHALCFwWA44brHA4VEeYw/8-3Z.py",
    ],
    "base": [
        "https://raw.githubusercontent.com/hikariatama/ftg/master/notes.py",
        "https://raw.githubusercontent.com/FajoX1/FAmods/main/avachanger.py",
        "https://raw.githubusercontent.com/Plovchikdeval/dev_modules/main/VoiceChat.py",
        "https://raw.githubusercontent.com/amm1edev/AmeMods/main/AmeMusic.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/InlineSystemInfo.py",
        "https://github.com/amm1edev/ame_repo/raw/main/uploader.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/hikarichat.py",
        "https://github.com/amm1edev/AmeMods/raw/main/YouTubeToMP3.py",
        "https://raw.githubusercontent.com/hikariatama/host/master/notes.py",
        "https://raw.githubusercontent.com/amm1edev/ame_repo/main/spoilers.py",
        "https://raw.githubusercontent.com/Fixyres/FHeta/main/FHeta.py",
        "https://raw.githubusercontent.com/Ruslan-Isaev/modules/main/ttf.py"
        "https://raw.githubusercontent.com/Ruslan-Isaev/modules/main/ttf.py",
        "https://raw.githubusercontent.com/Fixyres/Modules/main/Triggers.py",
        "https://raw.githubusercontent.com/KeyZenD/modules/master/filename.py",
    ],
}


@loader.tds
class Presets(loader.Module):
    """Suggests new Hikka users a packs of modules to load"""

    strings = {"name": "Presets"}

    async def client_ready(self):
        self._markup = utils.chunks(
            [
                {
                    "text": self.strings(f"_{preset}_title"),
                    "callback": self._preset,
                    "args": (preset,),
                }
                for preset in PRESETS
            ],
            1,
        )

        if self.get("sent"):
            return

        self.set("sent", True)
        await self._menu()

    async def _menu(self):
        await self.inline.bot.send_message(
            self._client.tg_id,
            self.strings("welcome"),
            reply_markup=self.inline.generate_markup(self._markup),
        )

    async def _back(self, call: InlineCall):
        await call.edit(self.strings("welcome"), reply_markup=self._markup)

    async def _install(self, call: InlineCall, preset: str):
        await call.delete()
        m = await self._client.send_message(
            self.inline.bot_id,
            self.strings("installing").format(preset),
        )
        for i, module in enumerate(PRESETS[preset]):
            await m.edit(
                self.strings("installing_module").format(
                    preset,
                    i,
                    len(PRESETS[preset]),
                    module,
                )
            )
            try:
                await self.lookup("loader").download_and_install(module, None)
            except Exception:
                logger.exception("Failed to install module %s", module)

            await asyncio.sleep(1)

        if self.lookup("loader").fully_loaded:
            self.lookup("loader").update_modules_in_db()

        await m.edit(self.strings("installed").format(preset))
        await self._menu()

    def _is_installed(self, link: str) -> bool:
        return any(
            link.strip().lower() == installed.strip().lower()
            for installed in self.lookup("loader").get("loaded_modules", {}).values()
        )

    async def _preset(self, call: InlineCall, preset: str):
        await call.edit(
            self.strings("preset").format(
                self.strings(f"_{preset}_title"),
                self.strings(f"_{preset}_desc"),
                "\n".join(
                    map(
                        lambda x: x[0],
                        sorted(
                            [
                                (
                                    "{} <b>{}</b>".format(
                                        (
                                            self.strings("already_installed")
                                            if self._is_installed(link)
                                            else "▫️"
                                        ),
                                        link.rsplit("/", maxsplit=1)[1].split(".")[0],
                                    ),
                                    int(self._is_installed(link)),
                                )
                                for link in PRESETS[preset]
                            ],
                            key=lambda x: x[1],
                            reverse=True,
                        ),
                    )
                ),
            ),
            reply_markup=[
                {"text": self.strings("back"), "callback": self._back},
                {
                    "text": self.strings("install"),
                    "callback": self._install,
                    "args": (preset,),
                },
            ],
        )

    async def aiogram_watcher(self, message: BotInlineMessage):
        if message.text != "/presets" or message.from_user.id != self._client.tg_id:
            return

        await self._menu()
