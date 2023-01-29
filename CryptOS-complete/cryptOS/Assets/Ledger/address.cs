using System.Collections;
using UnityEngine.Networking;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class address : MonoBehaviour
{
    public Text Address_Field;
    public Text Bitcoin_Address;
    public Text Ravencoin_Address;
    public string host = "";
    public string username = "";

    public void Start()
    {
            host = access.host;
            username = access.username;
    }

    public void Address()
    {
        StartCoroutine(Address_Request());
        StartCoroutine(Bitcoin_Address_Request());
        StartCoroutine(Ravencoin_Address_Request());
    }

    public IEnumerator Address_Request()
    {
        string url = host + "Address/" + username;
        UnityWebRequest address_req = UnityWebRequest.Get(url);
        yield return address_req.SendWebRequest();

        if (address_req.isNetworkError || address_req.isHttpError)
        {
            Debug.Log(address_req.error);
        }
        else
        {
            string address_result = address_req.downloadHandler.text;
            Address_Field.text = address_result;
        }
    }
    public IEnumerator Bitcoin_Address_Request()
    {
        string url = host + "BtcAddress/" + username;
        UnityWebRequest address_req = UnityWebRequest.Get(url);
        yield return address_req.SendWebRequest();

        if (address_req.isNetworkError || address_req.isHttpError)
        {
            Debug.Log(address_req.error);
        }
        else
        {
            string address_result = address_req.downloadHandler.text;
            Bitcoin_Address.text = address_result;
        }
    }
    public IEnumerator Ravencoin_Address_Request()
    {
        string url = host + "RvnAddress/" + username;
        UnityWebRequest address_req = UnityWebRequest.Get(url);
        yield return address_req.SendWebRequest();

        if (address_req.isNetworkError || address_req.isHttpError)
        {
            Debug.Log(address_req.error);
        }
        else
        {
            string address_result = address_req.downloadHandler.text;
            Ravencoin_Address.text = address_result;
        }
    }
}
