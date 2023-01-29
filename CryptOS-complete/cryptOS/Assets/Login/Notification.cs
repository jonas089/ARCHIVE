using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Notification : MonoBehaviour
{
    public GameObject NotificationPanel;

    public void NotificationPanelOff()
    {
        NotificationPanel.SetActive(false);
    }
}
