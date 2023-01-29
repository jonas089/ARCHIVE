using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
using TMPro;
public class BuyCryOS : MonoBehaviour
{
    public TMP_InputField Btc_amount_input;
    public TMP_InputField Btc_password_input;
    public TMP_InputField Rvn_amount_input;
    public TMP_InputField Rvn_password_input;

    public GameObject NotificationPanel;
    public RawImage Notification;
    public Texture TransactionFailedImage;
    public Texture TransactionSuccessImage;

    public string username = "";
    public string host = "";
    public void Start()
    {
        username = access.username;
        host = access.host;
    }
    public void Buy_With_Ravencoin()
    {
        StartCoroutine(Buy_With_Ravencoin_Action());
    }
    public void Buy_With_Bitcoin()
    {
        StartCoroutine(Buy_With_Bitcoin_Action());
    }
    public IEnumerator Buy_With_Ravencoin_Action()
    {
        if (Rvn_amount_input.text.Length != 0 && Rvn_password_input.text.Length != 0)
        {
            string amount_string = Rvn_amount_input.text;
            string password_string = WWW.EscapeURL(Rvn_password_input.text);
            string url = host + "RavenPurchase/" + username + "/" + password_string + "/" + amount_string;
            print(url);
            UnityWebRequest Transaction_req = UnityWebRequest.Get(url);
            yield return Transaction_req.SendWebRequest();

            if (Transaction_req.isNetworkError || Transaction_req.isHttpError)
            {
                Debug.Log(Transaction_req.error);
                Notification.texture = TransactionFailedImage;
                NotificationPanel.SetActive(true);
            }
            else
            {
                string Transaction_result = Transaction_req.downloadHandler.text;
                Debug.Log(Transaction_result);
                if(Transaction_result.Contains("Success"))
                {
                    Notification.texture = TransactionSuccessImage;
                    NotificationPanel.SetActive(true);
                }
                else
                {
                    Notification.texture = TransactionFailedImage;
                    NotificationPanel.SetActive(true);
                }
            }
            Rvn_amount_input.text = "";
            Rvn_password_input.text = "";
        }
    }
    public IEnumerator Buy_With_Bitcoin_Action()
    {
        if (Btc_amount_input.text.Length != 0 && Btc_password_input.text.Length != 0)
        {
            string amount_string = Btc_amount_input.text;
            string password_string = WWW.EscapeURL(Btc_password_input.text);
            string url = host + "BitcoinPurchase/" + username + "/" + password_string + "/" + amount_string;
            print(url);
            UnityWebRequest Transaction_req = UnityWebRequest.Get(url);
            yield return Transaction_req.SendWebRequest();

            if (Transaction_req.isNetworkError || Transaction_req.isHttpError)
            {
                Debug.Log(Transaction_req.error);
                Notification.texture = TransactionFailedImage;
                NotificationPanel.SetActive(true);
            }
            else
            {
                string Transaction_result = Transaction_req.downloadHandler.text;
                Debug.Log(Transaction_result);
                if(Transaction_result.Contains("Success"))
                {
                    Notification.texture = TransactionSuccessImage;
                    NotificationPanel.SetActive(true);
                }
                else
                {
                    Notification.texture = TransactionFailedImage;
                    NotificationPanel.SetActive(true);
                }
            }
            Btc_amount_input.text = "";
            Btc_password_input.text = "";
        }
    }
}