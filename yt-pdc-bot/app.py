# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)

from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

# from bots import EchoBot
from config import DefaultConfig

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

import tbot

class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.text=="/start":
            return await turn_context.send_activity(
                MessageFactory.text("Hi! There\n\nSend/Share me YouTube URL\n\nDEMO :\nhttps://www.youtube.com/playlist?list=PLZDMziPRHWIrkfzKIXUOrir_gwD0cD9f8")
            )
        URL = turn_context.activity.text
        tbot.arg_check(3, URL)
        return await turn_context.send_activity(
            MessageFactory.text(f"Your Playlists Total Duration is : {str(tbot.fuc(3, URL))}")
        )

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity("Please give values in given format only.")
    # await context.send_activity("To continue to run this bot, please fix the bot source code.")
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)

ADAPTER.on_turn_error = on_error

# Create the Bot
BOT = EchoBot()

# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)


app = web.Application(middlewares=[aiohttp_error_middleware])
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=CONFIG.PORT)
