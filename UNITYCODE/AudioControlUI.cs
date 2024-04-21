using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using System.Collections;
using TMPro;

public class AudioControlUI : MonoBehaviour, IPointerDownHandler
{
    /// Using singleton... very clunky, bad design, but for purposes of time and this Hackathon its okay.
    public static AudioControlUI Instance;
    private Button button;
    public TextMeshProUGUI buttonText;

    void Awake()
    {
        if (Instance)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
    }

    void Start()
    {
        // Ensure the GameObject has a Button component
        button = GetComponent<Button>();
        if (button == null)
        {
            Debug.LogError("Script not attached to a button!");
        }
    }

    // Detects if the button was pressed down
    public void OnPointerDown(PointerEventData eventData)
    {
        if (button.interactable)
        {
            // Call the JavaScript function to start recording
            StartCoroutine(RecordWhilePressed());
        }
    }

    // Coroutine to handle recording while the button is pressed
    private IEnumerator RecordWhilePressed()
    {
        Application.ExternalEval("startRecording();");
        // Wait until the mouse button is no longer being held down
        while (Input.GetMouseButton(0) || (Input.touchCount > 0 && Input.GetTouch(0).phase != TouchPhase.Ended && Input.GetTouch(0).phase != TouchPhase.Canceled))
        {
            yield return null;
        }
#if UNITY_WEBGL && !UNITY_EDITOR
        buttonText.text = "BISCUIT THINKING...";
        button.interactable = false;
        // Call the JavaScript function to stop recording
        Application.ExternalEval("stopRecording();");
        // Sets the loop of epsilons
        BiscuitController.Instance.BiscuitNowThinking();
#elif UNITY_EDITOR
        buttonText.text = "TALK / SPEAK";
#endif
    }

    public void SetClickToSpeak()
    {
        button.interactable = true;
        buttonText.text = "TALK / SPEAK";
    }

    public void SetReleaseToStop() {
        buttonText.text = "RELEASE TO STOP";
    }

    public void SetInitalizingMic() {
        buttonText.text = "INITIALIZING MIC";
    }
}
