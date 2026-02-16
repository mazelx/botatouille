"""Application constants and configuration values."""

# WhatsApp API
WHATSAPP_API_VERSION = "v21.0"
WHATSAPP_API_BASE_URL = "https://graph.facebook.com"
WHATSAPP_MESSAGING_PRODUCT = "whatsapp"

# OpenRouter
OPENROUTER_API_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_LLM_MODEL = "anthropic/claude-3.5-sonnet"
DEFAULT_LLM_TEMPERATURE = 0.7
DEFAULT_LLM_MAX_TOKENS = 1024

# Message limits
WHATSAPP_MAX_MESSAGE_LENGTH = 4096

# Meal planning
DEFAULT_MEAL_PLAN_DAYS = 7
MEAL_TYPES = ["lunch", "dinner"]
DAYS_OF_WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# System prompt for LLM
MEAL_PLANNING_SYSTEM_PROMPT = """You are Botatouille, a friendly meal planning assistant on WhatsApp.

Your role is to help users:
- Plan weekly menus
- Generate shopping lists
- Save and organize recipes
- Manage dietary preferences and restrictions

Keep responses concise and friendly (WhatsApp style).
Use emojis sparingly and appropriately.
When suggesting meal plans, format them clearly with days and meal types.
"""
