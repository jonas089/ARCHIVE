using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
using TMPro;

public class transaction : MonoBehaviour
{
    public GameObject Transaction_valid;
    public GameObject Transaction_failed;

    public Toggle tx_type;
    public TMP_InputField receipient;
    public TMP_InputField amount;
    public TMP_InputField password;
    public string username = "";
    public string host = "";
    public GameObject Transaction_Panel;
    public Slider Confirm_Transaction;

    public float interval = 1f;
    public float interval_reset = 1f;

    public void Start()
    {
        username = access.username;
        host = access.host;
    }

    public void Transaction()
    {
        StartCoroutine(Transaction_Request());
    }

    public IEnumerator Transaction_Request()
    {
        if (panel_c.Currency_Chosen_For_Transaction == 3)
        {
            if (tx_type.isOn && receipient.text.Length != 0 && password.text.Length != 0 && amount.text.Length != 0)
            {
                string receipient_string = receipient.text;
                string amount_string = amount.text;
                string password_string = WWW.EscapeURL(password.text);
                string url = host + "Transaction/" + username + "/" + receipient_string + "/" + amount_string + "/" + password_string;
                print(url);
                UnityWebRequest Transaction_req = UnityWebRequest.Get(url);
                yield return Transaction_req.SendWebRequest();

                if (Transaction_req.isNetworkError || Transaction_req.isHttpError)
                {
                    Debug.Log(Transaction_req.error);
                }
                else
                {
                    string Transaction_result = Transaction_req.downloadHandler.text;
                    Debug.Log(Transaction_result);
                    if (Transaction_result.Contains("fail"))
                    {
                        Transaction_failed.SetActive(true);
                    }
                    else if (Transaction_result.Contains("success"))
                    {
                        Transaction_valid.SetActive(true);
                    }
                }
            }
            else if (tx_type.isOn == false && receipient.text.Length != 0 && password.text.Length != 0 && amount.text.Length != 0)
            {
                string receipient_string = receipient.text;
                string amount_string = amount.text;
                string password_string = WWW.EscapeURL(password.text);
                string url = host + "Tx/" + username + "/" + receipient_string + "/" + amount_string + "/" + password_string;
                print(url);
                UnityWebRequest Tx_req = UnityWebRequest.Get(url);
                yield return Tx_req.SendWebRequest();

                if (Tx_req.isNetworkError || Tx_req.isHttpError)
                {
                    Debug.Log(Tx_req.error);
                }
                else
                {
                    string Tx_result = Tx_req.downloadHandler.text;
                    Debug.Log(Tx_result);
                    if (Tx_result.Contains("fail"))
                    {
                        Transaction_failed.SetActive(true);
                    }
                    else if (Tx_result.Contains("success"))
                    {
                        Transaction_valid.SetActive(true);
                    }
                }
            }
            Transaction_Panel.SetActive(false);
        }
        else if(panel_c.Currency_Chosen_For_Transaction == 2)
        {
            if ( receipient.text.Length != 0 && password.text.Length != 0 && amount.text.Length != 0)
            {
                string receipient_string = receipient.text;
                string amount_string = amount.text;
                string password_string = WWW.EscapeURL(password.text);
                string url = host + "BtcTransaction/" + username + "/" + password_string + "/" + receipient_string + "/" + amount_string;
                print(url);
                UnityWebRequest Tx_req = UnityWebRequest.Get(url);
                yield return Tx_req.SendWebRequest();

                if (Tx_req.isNetworkError || Tx_req.isHttpError)
                {
                    Debug.Log(Tx_req.error);
                }
                else
                {
                    string Tx_result = Tx_req.downloadHandler.text;
                    Debug.Log(Tx_result);
                    if (Tx_result.Contains("fail"))
                    {
                        Transaction_failed.SetActive(true);
                    }
                    else if (Tx_result.Contains("success"))
                    {
                        Transaction_valid.SetActive(true);
                    }
                }
            }
            Transaction_Panel.SetActive(false);
        }
        else if(panel_c.Currency_Chosen_For_Transaction == 1)
        {
            if (receipient.text.Length != 0 && password.text.Length != 0 && amount.text.Length != 0)
            {
                string receipient_string = receipient.text;
                string amount_string = amount.text;
                string password_string = WWW.EscapeURL(password.text);
                string url = host + "RvnTransaction/" + username + "/" + password_string + "/" + receipient_string + "/" + amount_string;
                print(url);
                UnityWebRequest Tx_req = UnityWebRequest.Get(url);
                yield return Tx_req.SendWebRequest();

                if (Tx_req.isNetworkError || Tx_req.isHttpError)
                {
                    Debug.Log(Tx_req.error);
                }
                else
                {
                    string Tx_result = Tx_req.downloadHandler.text;
                    Debug.Log(Tx_result);
                    if (Tx_result.Contains("fail"))
                    {
                        Transaction_failed.SetActive(true);
                    }
                    else if (Tx_result.Contains("success"))
                    {
                        Transaction_valid.SetActive(true);
                    }
                }
            }
            Transaction_Panel.SetActive(false);
        }
    }
}
