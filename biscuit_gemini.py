import google.generativeai as genai
from typing import Dict, List
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import random

genai.configure(api_key='AIzaSyD5wXcOWaqhPxnD9dUiTbbqgbB39xDDf0o')

class BiscuitGemini():
    def __init__(self, conversation_history : List[Dict]):
        self._model = genai.GenerativeModel(
            'models/gemini-1.5-pro-latest',
            tools = [self.analyze_user_sentiment],
            system_instruction = "You are a squirell named Biscuit. You are talking to a player."
        )
        self._chat = self._model.start_chat(
            history = conversation_history, 
            enable_automatic_function_calling=True
        )

    def ask_biscuit(self, query : str) -> Dict:
        response = self._chat.send_message(query,             
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        sentiment = none
        for content in self._chat.history:
            if content.role != 'model':
                continue
            l = [type(part).to_dict(part) for part in content.parts]
            if not l.get('function_call'):
                continue
            sentiment = list(l['function_call']['args'].keys())[0]
            #print(content.role, "->", [type(part).to_dict(part) for part in content.parts])
            #print('-'*80)
        return response.text
    
    def analyze_user_sentiment(self, 
        is_neutral : bool = False,
        is_happy : bool = False, 
        is_compliment: bool = False, 
        is_achievement : bool = False, 
        is_depressed : bool = False, 
        is_angry : bool = False
    ):
        '''Takes as parameter the emotion of the users query, and returns the corresponding type of response Biscuit should have. ONLY ONE PARAMETER SHOULD EVER BE EQUAL TO TRUE'''
        if is_neutral:
            rand_int = random.randint(0, 100)
            if rand_int < 50:
                return "Biscuit should have an energized tone that trys to engage the conversation more. Respond with a more intimate, followup questions."
            elif rand_int >= 50:
                return "Biscuit should respond in a way that stimulates by changing the topic. Call out the user for being boring."
        if is_happy:
            return "Biscuit should respond being happy for the user, engaging more with what the user is happy about"
        if is_compliment:
            return "Biscuit should respond being super flattered. Biscuit should then fish for more compliments."
        if is_achievement:
            return "Biscuit should respond with being appreciative and happy for the user and the achievement they accomplished in life."
        if is_depressed:
            return "Biscuit should respond as a friend would. Biscuit should incorporate Taoist Philosophical sentiments."
        if is_angry:
            return "Biscuit should also respond with an even more angry tone to escalate the conversation."
        return ""

#bicuit_gemini = BiscuitGemini([])
#print(bicuit_gemini.ask_biscuit("Biscuit your so so so beautiful, I love your pretty hair and pretty eyes."))