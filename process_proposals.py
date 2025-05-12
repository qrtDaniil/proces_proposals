import discord
from discord.ext import commands
import datetime
import asyncio
import json
import os

class ProcessProposals(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.voting_channel_id = 1329180590335066152 # ID канала для голосований
        # self.proposals_channel_id = 1136964819732398110 # ID канала предложений
        # self.frontier_voting_channel_id = 1329180628507164672 # ID канала для голосований Фронтира
        # self.frontier_proposals_channel_id = 1278737130411261982 # ID канала предложений Фронтира
        # self.deleted_proposals_channel_id = 1161692042511011870 # ID канала с логами
        # self.cooldown_tracker_file = os.path.join(os.path.dirname(__file__), "proposals_cooldown_tracker.json") # Имя файла для хранения данных
        # self.cooldown_tracker = self.load_post_limit() # Данные из файла
        self.event_announcements_channel_id = 1361750066104111204 # ID канала для анонса о ивенте
        self.event_forum_channel_id = 1150335616425398312 # ID канала ивент-форума
        self.event_schedule_channel_id = 1202319845551775794 # ID канала ивент-расписания

    # def load_post_limit(self):
    #     """Загружает данные из JSON-файла, если он существует."""
    #     if not os.path.exists(self.cooldown_tracker_file):
    #         return {}
            
    #     with open(self.cooldown_tracker_file, "r", encoding="utf-8") as file:
    #         try:
    #             data = json.load(file)
    #             # Конвертируем строки времени обратно в datetime
    #             return {int(user_id): datetime.datetime.fromisoformat(timestamp) for user_id, timestamp in data.items()}
    #         except (json.JSONDecodeError, ValueError):
    #             return {}

    # def save_post_limit(self):
    #     """Сохраняет данные в JSON-файл."""
    #     with open(self.cooldown_tracker_file, "w", encoding="utf-8") as file:
    #         # Конвертируем datetime в строки
    #         json.dump({str(user_id): timestamp.isoformat() for user_id, timestamp in self.cooldown_tracker.items()}, file)

    # @commands.slash_command(description="Принять предложение для голосования")
    # async def init_proposal(self, ctx, comment: str = discord.Option(default=None, description="Комментарий по предложению, который будет добавлен к сообщению голосования")):
    #     """
    #     Отправляет сообщение в канал где была прописана и сообщение в канал голосований с ссылкой на пост в ветке которого прописана.

    #     Аргументы:
    #     - comment: Комментарий по предложению, добавляемый к сообщению в канале голосований.
    #     """
    #     # Проверяем, вызвана ли команда в ветке форума для того что бы потом мы могли проверить parent_id
    #     if not ctx.channel.type == discord.ChannelType.public_thread:
    #         await ctx.respond("Эту команду можно использовать только в ветках форума.", ephemeral=True)
    #         return

    #     # Получаем канал голосований для конретного канала предложений
    #     if ctx.channel.parent_id == self.proposals_channel_id:
    #         target_channel = ctx.guild.get_channel(self.voting_channel_id)
    #     elif ctx.channel.parent_id == self.frontier_proposals_channel_id:
    #         target_channel = ctx.guild.get_channel(self.frontier_voting_channel_id)

    #     # Если не получили канал голосований то либо не совпал id изначального канала с id с одним из каналов предложений или ошибка в боте 
    #     if not target_channel:
    #         await ctx.respond(
    #             f"Эту команду можно использовать только в канале <#{self.proposals_channel_id}> или <#{self.frontier_proposals_channel_id}>.", ephemeral=True)
    #         return

    #     proposal_post_url = ctx.channel.jump_url # Получаем ссылку на текущую ветку форума
    #     proposal_post_autor = ctx.channel.owner_id # Получаем id автора поста
    #     command_autor = ctx.author.id # Получаем id автора команды

    #     # Формируем текст комментария (если он есть)
    #     comment_text = f"\nКомментарий от принявшего предложение: {comment}" if comment else ""

    #     try:
    #         # Отправляем сообщение в канал голосований
    #         target_message = await target_channel.send(
    #             f"Предложение {proposal_post_url} принято на голосование\n"
    #             f"Автор предложения: <@{proposal_post_autor}>\n"
    #             f"Предложения принял: <@{command_autor}>{comment_text}\n"
    #             "Дальнейшая судьба предложения будет решена по итогам голосования реакциями под этим сообщением.\n"
    #             "⭐ — Я за реализацию данного предложения.\n❌ — Я против реализации данного предложения."
    #         )
    #         # Добавляем реакции
    #         await target_message.add_reaction(emoji='⭐')
    #         await target_message.add_reaction(emoji='❌')

    #         # Отправляем сообщение в текущую ветку форума
    #         await ctx.respond(f"Предложение принято на голосование. Ссылка: {target_message.jump_url}.", ephemeral=False)

    #     except discord.HTTPException as e:
    #         await ctx.respond(f"Произошла ошибка при отправке сообщения: {e}.", ephemeral=True)

    # @commands.Cog.listener()
    # async def on_thread_create(self, thread):
    #     """
    #     Ограничивает создание постов в форуме предложений до одного поста раз в 24 часа.
    #     """
    #     # Проверяем, относится ли этот новый пост к каналам предложений
    #     if thread.parent_id not in { self.proposals_channel_id, self.frontier_proposals_channel_id }:
    #         return

    #     # Получаем автора ветки через первое сообщение в посте
    #     starter_message = await thread.fetch_message(thread.id)
    #     user_id = starter_message.author.id

    #     # Проверяем, создавал ли пользователь пост в последние 24 часа
    #     now = datetime.datetime.now(datetime.timezone.utc)
    #     if user_id not in self.cooldown_tracker:
    #         # Сохраняем время создания нового поста
    #         self.cooldown_tracker[user_id] = now
    #         self.save_post_limit() # Сохраняем изменения
    #         return
            
    #     last_post_time = self.cooldown_tracker[user_id]
    #     time_since_last_post = now - last_post_time
    #     if time_since_last_post >= datetime.timedelta(hours=24):
    #         return
    #     # Получим канал для логов
    #     log_channel = self.client.get_channel(self.deleted_proposals_channel_id)
    #     # Отправим уведомление
    #     await thread.send(
    #         f"<@{user_id}> вы можете создать новую публикацию только раз в 24 часа. "
    #         "Этот пост будет удален через 30 секунд."
    #     )
        
    #     await asyncio.sleep(30) # Ждём 30 секунд перед удалением поста что бы человек прочитал ответное сообщение

    #     # Проверяем, существует ли пост перед удалением
    #     if thread and thread.id not in [t.id for t in thread.parent.threads]:
    #         return
    #     try:
    #         await thread.delete()

    #         # Отправка лога об удалении поста
    #         if log_channel:
    #             await log_channel.send(
    #                 f"Пост с заголовком: {thread.name} был удалён. Автор: <@{user_id}>. "
    #                 f"Причина: превышен лимит публикаций."
    #                 f"Содержимое сообщения: {starter_message.content}"
    #             )
    #     except discord.HTTPException as e:
    #         if log_channel:
    #             await log_channel.send(
    #                 f"Не удалось удалить ветку {thread.name}. Автор: <@{user_id}>. Ошибка: {e}"
    #             )
    #             return

    #     # Сохраняем время создания нового поста
    #     self.cooldown_tracker[user_id] = now
    #     self.save_post_limit() # Сохраняем изменения

    @commands.slash_command(description="Отправить оповещение о ивенте")
    async def announce_event(self, ctx,
                             name: str = discord.Option(description="Название ивента"),
                             desc: str = discord.Option(description="Краткое описание ивента"),
                             location: str = discord.Option(description="Место и время проведения")
                             ):
        """
        Отправляет сообщение в канал где была прописана и сообщение в канал ивент-аносов с ссылкой на пост в ветке которого прописана.

        Аргументы:
        - name: Название ивента, добавляемое к описанию ивента.
        - desc: Краткое описание ивента, добавляемое к описанию ивента.
        - location: Место и время проведения, добавляемое к описанию ивента.
        """
        # Проверяем, вызвана ли команда в ветке форума для того что бы потом мы могли проверить parent_id
        if not ctx.channel.type == discord.ChannelType.public_thread:
            await ctx.respond("Эту команду можно использовать только в ветках форума.", ephemeral=True)
            return

        # Получаем канал ивент-анонсов
        if ctx.channel.parent_id == self.event_forum_channel_id or ctx.channel.parent_id == self.event_schedule_channel_id:
            target_channel = ctx.guild.get_channel(self.event_announcements_channel_id)

        # Если не получили канал анонсов то либо не совпал id изначального канала с id с ивент-форума или ошибка в боте 
        if not target_channel:
            await ctx.respond(
                f"Эту команду можно использовать только в канале <#{self.event_forum_channel_id}> или <#{self.event_schedule_channel_id}>", ephemeral=True)
            return

        post_url = ctx.channel.jump_url # Получаем ссылку на текущую ветку форума
        post_autor = ctx.channel.owner_id # Получаем id автора поста
        command_autor = ctx.author.id # Получаем id автора команды

        event_forum_url = f"\nСсылка на пост в ивент-форуме: {post_url}." if ctx.channel.parent_id == self.event_forum_channel_id else ""

        try:
            # Отправляем сообщение в канал ивент-аносов
            target_message = await target_channel.send(
                "Оповещение об ивенте\n"
                f"Заголовок ивента: {name}\n"
                f"Автор ивента: <@{post_autor}>\n"
                f"Оповещение отправил: <@{command_autor}>\n"
                f"Описание ивента: {desc}.\n"
                f"Место и время проведения: {location}.{event_forum_url}\n"
                f"<@&{1167175964988559526}>"
            )

            # Отправляем сообщение в текущую ветку форума
            await ctx.respond(f"Отправлено оповещение об ивенте. Ссылка: {target_message.jump_url}.", ephemeral=False)

        except discord.HTTPException as e:
            await ctx.respond(f"Произошла ошибка при отправке сообщения: {e}.", ephemeral=True)

def setup(client):
    client.add_cog(ProcessProposals(client))
