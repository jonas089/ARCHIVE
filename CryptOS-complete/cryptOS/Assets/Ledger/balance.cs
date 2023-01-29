using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class balance : MonoBehaviour
{
    public float balance_timer = 5f;
    public float balance_timer_reset = 5f;
    public TextMeshProUGUI Balance_Text;
    public TextMeshProUGUI Rvn_Balance_Text;
    public TextMeshProUGUI Btc_Balance_Text;

    public string host = "";
    public string username = "";

    public void Start()
    {
        host = access.host;
        username = access.username;
        Balance();
    }

    public void Update()
    {
        if (balance_timer > 0f)
        {
            balance_timer -= Time.deltaTime;
        }
        else if (balance_timer <= 0f)
        {
            Balance();
            balance_timer = balance_timer_reset;
        }
    }

    public void Balance()
    {
        StartCoroutine(Balance_Request());
        StartCoroutine(Rvn_Balance_Request());
        StartCoroutine(Btc_Balance_Request());
    }

    public IEnumerator Balance_Request()
    {
        string url = host + "Balance/" + username;
        UnityWebRequest balance_req = UnityWebRequest.Get(url);
        yield return balance_req.SendWebRequest();

        if (balance_req.isNetworkError || balance_req.isHttpError)
        {
            Debug.Log(balance_req.error);
        }
        else
        {
            string balance_result = balance_req.downloadHandler.text;
            if (balance_result.Length > 12)
            {
                balance_result = balance_result.Substring(0, 12);
            }
            if (balance_result == "0e-8")
            {
                balance_result = "0.00";
            }
            else if (balance_result.Contains("e-05"))
            {
                balance_result = "0.0000" + balance_result[0] + balance_result[2] + balance_result[3];
            }
            else if (balance_result.Length > 12)
            {
                balance_result = balance_result.Substring(0, 12);
            }
            Balance_Text.text = balance_result;
        }
    }
    public IEnumerator Btc_Balance_Request()
    {
        string url = host + "BtcBalance/" + username;
        UnityWebRequest balance_req = UnityWebRequest.Get(url);
        yield return balance_req.SendWebRequest();

        if (balance_req.isNetworkError || balance_req.isHttpError)
        {
            Debug.Log(balance_req.error);
        }
        else
        {
            string balance_result = balance_req.downloadHandler.text;
            if (balance_result == "0e-8")
            {
                balance_result = "0.00";
            }
            else if (balance_result.Contains("e-05"))
            {
                balance_result = "0.0000" + balance_result[0] + balance_result[2] + balance_result[3];
            }
            else if (balance_result.Length > 12)
            {
                balance_result = balance_result.Substring(0, 12);
            }
            Btc_Balance_Text.text = balance_result;
        }
    }
    public IEnumerator Rvn_Balance_Request()
    {
        string url = host + "RvnBalance/" + username;
        UnityWebRequest balance_req = UnityWebRequest.Get(url);
        yield return balance_req.SendWebRequest();

        if (balance_req.isNetworkError || balance_req.isHttpError)
        {
            Debug.Log(balance_req.error);
        }
        else
        {
            string balance_result = balance_req.downloadHandler.text;
            if (balance_result == "0e-8")
            {
                balance_result = "0.00";
            }
            else if (balance_result.Contains("e-05"))
            {
                balance_result = "0.0000" + balance_result[0] + balance_result[2] + balance_result[3];
            }
            else if (balance_result.Length > 12)
            {
                balance_result = balance_result.Substring(0, 12);
            }
            Rvn_Balance_Text.text = balance_result;
        }
    }
}