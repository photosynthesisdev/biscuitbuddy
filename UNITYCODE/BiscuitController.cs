using System.Collections;
using UnityEngine;
using TMPro;
using System.Collections.Generic;

public class BiscuitController : MonoBehaviour
{
    public static BiscuitController Instance;
    [Header("Text Box")]
    public TextMeshProUGUI text;
    public AudioSource newResponseSource;
    public AudioClip newSoundClip;
    public AudioSource biscuitVoiceSource;
    public List<AudioClip> biscuitVoiceClips;
    public GameObject clickForNext;
    public GameObject chatBubble;
    public float letterPause = 0.1f; // Delay between letters
    //[Header("Biscuit Emotions")]


    private bool speakingOrThinking = false;
    private bool isWaitingForInput = false;
    private const int maxCharacters = 180; // Max characters per section

    private void Awake()
    {
        if (Instance) {
            Destroy(gameObject);
            return;
        }
        Instance = this;
    }

    /// Helper function
    void SetClickToSpeak()
    {
        speakingOrThinking = false;
        AudioControlUI.Instance.SetClickToSpeak();
    }

    /// Trying to get mic or talk to backend failed.
    public void GotError(string error)
    {
        Debug.LogError($"Got Error from JS: {error}");
        chatBubble.SetActive(false);
        SetClickToSpeak();
    }

    // We requested permissions to use mic, so set back to default click to speak state.
    public void PermissionsRequested()
    {
        //text.text = starting_text;
        chatBubble.SetActive(false);
        SetClickToSpeak();
    }

    ///We are aquiring microphone
    public void MicrophoneRequested()
    {
        AudioControlUI.Instance.SetInitalizingMic();
    }

    // Microphone is ready to go and listening. 
    public void MicrophoneReady()
    {
        AudioControlUI.Instance.SetReleaseToStop();
    }

    public void BiscuitNowThinking() {
        speakingOrThinking = true;
        chatBubble.SetActive(true);
        StopAllCoroutines();
        StartCoroutine(RepeatEpsilon());
    }

    /// We got a response. Display it.
    public void GotResponse(string response)
    {
        newResponseSource.PlayOneShot(newSoundClip);
        SetClickToSpeak();
        StopAllCoroutines(); // Stop any existing text animations and thinking animations
        StartCoroutine(TypeText(response)); // Start typing new response
    }

    public void Update()
    {
        bool pressedDown = Input.GetMouseButtonDown(0) || (Input.touchCount > 0 && Input.GetTouch(0).phase == TouchPhase.Began);
        if (pressedDown && isWaitingForInput && !speakingOrThinking)
        {
            isWaitingForInput = false; // User pressed, continue typing
            clickForNext.SetActive(false);
        }
        if (Input.GetKeyDown(KeyCode.K))
        {
            chatBubble.SetActive(true);
            StopAllCoroutines(); // Stop any existing text animations and thinking animations
            StartCoroutine(TypeText("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat."));
        }
    }

    IEnumerator RepeatEpsilon()
    {
        while (speakingOrThinking)
        {
            text.text = ".";
            yield return new WaitForSeconds(0.5f);
            text.text = "..";
            yield return new WaitForSeconds(0.5f);
            text.text = "...";
            yield return new WaitForSeconds(0.5f);
            text.text = ""; // Clear text to show nothing
            yield return new WaitForSeconds(0.5f);
        }
    }

    IEnumerator TypeText(string response)
    {
        List<string> sentences = new List<string>();
        string currentText = "";

        // Split response into sentences, preserving punctuation
        response += " "; // Ensuring last punctuation is included
        string tempSentence = "";
        foreach (char c in response)
        {
            tempSentence += c;
            if (c == '.' || c == '?' || c == '!')
            {
                sentences.Add(tempSentence.Trim());
                tempSentence = "";
            }
        }

        // Group sentences into sections under 180 characters
        foreach (string sentence in sentences)
        {
            if (currentText.Length + sentence.Length + 1 > maxCharacters)
            {
                yield return StartCoroutine(TypeSentenceByLetter(currentText));
                isWaitingForInput = true;
                clickForNext.SetActive(true);
                yield return new WaitUntil(() => !isWaitingForInput);
                currentText = sentence + " ";
            }
            else
            {
                currentText += sentence + " ";
            }
        }

        if (currentText.Length > 0)
        {
            yield return StartCoroutine(TypeSentenceByLetter(currentText));
            isWaitingForInput = true;
            clickForNext.SetActive(true);
            yield return new WaitUntil(() => !isWaitingForInput);
            chatBubble.SetActive(false);
        }
    }

    IEnumerator TypeSentenceByLetter(string sentence)
    {
        text.text = ""; // Clear text before typing
        foreach (char letter in sentence)
        {
            text.text += letter;
            PlayRandomVoiceClip();
            yield return new WaitForSeconds(letterPause);
        }
    }

    private void PlayRandomVoiceClip()
    {
        if (!biscuitVoiceSource.isPlaying)
        {
            int clipIndex = Random.Range(0, biscuitVoiceClips.Count);
            biscuitVoiceSource.clip = biscuitVoiceClips[clipIndex];
            biscuitVoiceSource.PlayOneShot(biscuitVoiceSource.clip);
        }
    }
}
