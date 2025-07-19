from fastapi import APIRouter
from app.generate_reply import Generate
from app.intent_extractor import IntentExtractor
from .schemas import BotReply, RefinedQuery

router = APIRouter()

@router.post("/voicebot",response_model = BotReply)
def voicebot(query: RefinedQuery):
    response = Generate(query)
    return BotReply(
        **response
    )