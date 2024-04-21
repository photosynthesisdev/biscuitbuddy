import google.generativeai as genai
from typing import Dict, List
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import random

genai.configure(api_key='AIzaSyD5wXcOWaqhPxnD9dUiTbbqgbB39xDDf0o')


'''The brain of biscuit!'''
class BiscuitGemini():
    def __init__(self, conversation_history : List[Dict]):
        '''Loads in all of the previous conversation history for this user. Initalize model + conversation.'''
        self._model = genai.GenerativeModel(
            'models/gemini-1.5-pro-latest',
            tools = self.biscuit_brain,
            system_instruction = "You are a squirell named Biscuit. You are talking to a player. No emojis in responses."
        )
        self._chat = self._model.start_chat(
            history = conversation_history, 
            enable_automatic_function_calling=True
        )

    @property
    def biscuit_brain(self) -> List:
        '''This is biscuits brain! Represents all of her current cognitive capabilites. Returns all function tools.'''
        return [self.analyze_user_sentiment]

    def ask_biscuit(self, query : str) -> Dict:
        '''Puts user query in and gives biscuits response'''
        response = self._chat.send_message(query,             
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        print(type(part).to_dict(part) for part in self._chat.history[-1].parts)
        for content in self._chat.history:
            print(content.role, "->", [type(part).to_dict(part) for part in content.parts])
            print('-'*80)
        return response.text
    
    '''BISCUIT TOOLS'''
    def give_friendship(self, intimacy_level: int) -> float:
        """
        Calculate and return friendship points based on the cumulative intimacy level of a conversation.

        This function evaluates the depth of engagement over recent interactions, not just the most recent message, to determine the friendship points awarded. It uses an exponential function to scale the intimacy level, which is then adjusted to provide a more nuanced reflection of the relationship dynamics. High levels of continuous intimate interaction result in positive friendship points, whereas sporadic or shallow interactions lead to fewer or negative points.

        Parameters:
        - intimacy_level (int): The calculated intimacy level of the conversation, on a scale of 1 to 100, where 1 represents minimal intimacy and 100 represents maximum intimacy. This value should reflect an aggregate or average intimacy over a sequence of interactions to accurately gauge the relationship's depth.

        Returns:
        - float: The number of friendship points, ranging from -50 to +50. The points are calculated using a shifted exponential scale and are clipped at both ends of the spectrum to prevent extreme values. Positive points signify a strong, positive bond, while negative points indicate a weaker or negative relationship.

        The exponential scaling is designed to amplify the effects of sustained deep interactions, encouraging players to engage in meaningful conversations with the AI character. This mechanism also penalizes negative or non-engaging interactions, reflecting the natural dynamics of relationship building.
        """
        # Shift the intimacy level by subtracting 50 to center the scale around zero
        shifted_intimacy = intimacy_level - 50
        
        # Calculate friendship points using an exponential function adjusted by a factor of 10
        # This adjustment provides a smooth transition of points around the neutral point (intimacy level = 50)
        friendship_points = (math.exp(shifted_intimacy / 10) - math.exp(0)) / 2
        
        # Clip the points to limit them within the range of -50 to 50
        if friendship_points > 50:
            friendship_points = 50
        elif friendship_points < -50:
            friendship_points = -50
        
        return friendship_points

    def analyze_user_sentiment(
        self, 
        neutral: bool = False,
        happy: bool = False, 
        sad: bool = False, 
        angry: bool = False, 
        excited: bool = False) -> str:
        """
        Analyze the emotion of the user's query and determine the appropriate response style for Biscuit.

        This method selects a response strategy based on the predominant emotional tone of the user's input. It is designed to handle only one true emotional flag at a time, reflecting the user's current state. The response adjusts Biscuit's tone to appropriately match or counter the user's emotion, aiming to guide the conversation effectively.

        Parameters:
        - neutral (bool): If True, indicates the user's emotion is neutral. Biscuit's response should aim to gently elevate the conversation's positivity.
        - happy (bool): If True, indicates the user is happy. Biscuit should match this energy level and engage more actively.
        - sad (bool): If True, indicates the user is sad. Biscuit responds with comforting and wise advice, akin to a monk's counsel.
        - angry (bool): If True, indicates the user is angry. Biscuit will escalate the conversation by matching the anger, contrary to typical de-escalation strategies.
        - excited (bool): If True, indicates the user is excited. Biscuit matches this excitement, potentially amplifying the user's enthusiasm.

        Returns:
        - str: A string describing the type of response Biscuit should adopt based on the user's emotional state. If none of the parameters are True, Biscuit defaults to a neutral response.

        Note:
        - It is crucial that only one of these parameters is set to True at any given time. If multiple emotions are flagged as True, the method will respond based on the first true condition encountered in its sequence of checks.
        """
        if neutral:
            return "Biscuit should take the conversation from a neutral to postivive direction. Test out different vibes.", 'neutral'
        if happy:
            return "Biscuit should match the energy level of the users happiness and engage the conversation more.", 'happy'
        if sad:
            return "Biscuit should respond as a friend would. Biscuit gives advice as if she were a monk.", 'sad'
        if angry:
            return "Biscuit should respond with an even more angry tone to escalate the conversation.", 'angry'
        if excited:
            return "Biscuit should respond in back in a similar excited tone, getting hype for the user if necessary.", 'excited'
        return "Biscuit should respond completely neutrally."

    def go_to_sleep(self, sleep : bool) -> bool:
        '''Returns true if AND ONLY IF the user said "Biscuit go to sleep"'''
        return sleep

bicuit_gemini = BiscuitGemini([])
print(bicuit_gemini.ask_biscuit("Biscuit your so so so beautiful, I love your pretty hair and pretty eyes."))