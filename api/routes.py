from fastapi import APIRouter
from app.generate_reply import generate_reply
from app.intent_extractor import IntentExtractor
from .schemas import BotReply, RefinedQuery

router = APIRouter()

@router.post("/voicebot",response_model = BotReply)
def voicebot(query: RefinedQuery):
    response = generate_reply(query)
    return BotReply(
        **response
    )