

version = (12, 3, 7)

from .. import loader, utils 
from telethon import events 
from telethon.errors.rpcerrorlist import YouBlockedUserError 
from asyncio.exceptions import TimeoutError 

@loader.tds
class SpotifyDownloaderMod(loader.Module):
    """Music search module"""
    strings = {
        "name": "MusicFinder",
        "yoq": "<b>🎧 Qidirilmagan!</b>",
        "qidiryapman": "<b>🐝 Qidirilmoqda...</b>",
        "eshe": "<b>♻️ Iltimos qayta urunib ko'ring!</b>",
        "topmadim": "<b>😔 Musiqa topilmadi, balki siz noto'g'ri ism yozgandirsiz?</b>"}
    
    async def client_ready(self, client, db):
        self.client = client
        self._db = db
        self._me = await client.get_me()
        
    @loader.unrestricted
    async def vkcmd(self, message):
        """music name"""
        args = utils.get_args_raw(message)
        if not args:
            return await message.edit(self.strings("yoq", message))

        message = await message.edit(self.strings("qidiryapman", message))
        try:
            message = message[0]
        except: pass
        music = await self.client.inline_query('spotifysavebot', args)
        for mus in music:
            if mus.result.type == 'audio':
                await self.client.send_file(message.peer_id, mus.result.document, reply_to=message.reply_to_msg_id, caption="🎧 <b>Musiqa topildi!\n🏙🎧<b>Musiqa</b> @one_frozen <b>tomonidan topildi</b>")
                return await message.delete()

        return await message.edit(self.strings("topmadim", message))

    async def spotycmd(self, message): 
        """music or album name""" 
        args = utils.get_args_raw(message) 
        reply = await message.get_reply_message() 
        if not args: 
            return await message.edit(self.strings("yoq", message))
        try: 
            await message.edit(self.strings("qidiryapman", message))
            music = await message.client.inline_query('lybot', args) 
            await message.delete() 
            await message.client.send_file(message.to_id, music[0].result.document, caption="🎧 <b>Musiqa topildi!\n🏙🎧<b>Musiqa</b> @one_frozen <b>tomonidan topildi</b>", reply_to=reply.id if reply else None) 
        except: return await message.client.send_message(message.chat_id, f"🎧 <b>{args}</b> - Spotifydan topilmadi!\n🏙️ <b>Bundan foydalanishingiz mumkin <code> .vk</code>?</b>")
