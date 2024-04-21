import google.generativeai as genai
from typing import Dict, List
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import random

genai.configure(api_key='AIzaSyD5wXcOWaqhPxnD9dUiTbbqgbB39xDDf0o')


'''Biscuit's Brain. Biscuit has three function tools (but in context of Biscuit lore, Cognitve Functinos). 
1) 

'''
class BiscuitGemini():
    def __init__(self, conversation_history : List[Dict]):
        self._model = genai.GenerativeModel(
            'models/gemini-1.5-pro-latest',
            tools = self.biscuit_brain,
            system_instruction = "You are a squirell named Biscuit. You are talking to a player."
        )
        self._chat = self._model.start_chat(
            history = conversation_history, 
            enable_automatic_function_calling=True
        )

    @property
    def biscuit_brain(self) -> List:
        '''This is biscuits brain! Represents all of her current cognitive capabilites'''
        return [self.give_friendship, self.analyze_user_sentiment, self.go_to_sleep]

    def ask_biscuit(self, query : str) -> Dict:
        response = self._chat.send_message(query,             
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        return response.text
    
    def give_friendship(intimacy_level : int, ):
        """
        Calculate and return friendship points based on the intimacy level of a conversation.
        Intimacy should be high only if the last few parts of the conversation (not just the most recent message) have been deep and intimate.
        The longer and more intimate the conversation, the closer the bond. The less intimate, the lesser the bond.
        """
        shifted_intimacy = intimacy_level - 50
        friendship_points = (math.exp(shifted_intimacy / 10) - math.exp(0)) / 2
        if friendship_points > 50:
            friendship_points = 50
        elif friendship_points < -50:
            friendship_points = -50
        return friendship_points

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

    def go_to_sleep(sleep : bool) -> bool:
        '''Returns true if the user said "Biscuit go to sleep"'''
        return sleep

#bicuit_gemini = BiscuitGemini([])
#print(bicuit_gemini.ask_biscuit("Biscuit your so so so beautiful, I love your pretty hair and pretty eyes."))