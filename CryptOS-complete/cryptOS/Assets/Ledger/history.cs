using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine.Networking;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using Newtonsoft.Json;

public class history : MonoBehaviour
{
    public string amount_tag = "history_block_amount";
    public string category_tag = "history_block_type";

    public float history_timer = 10f;
    public float history_timer_reset = 10f;

    public Sprite TxInSprite;
    public Sprite TxOutSprite;

    public string host = "";
    public string username = "";

    public string [] Category_Array = new string[10];
    public string [] Amount_Array = new string[10];

    public void Start()
    {
        host = access.host;
        username = access.username;
        History();
    }
    public void Update()
    {
        if (history_timer > 0f)
        {
            history_timer -= Time.deltaTime;
        }
        else if (history_timer <= 0f)
        {
            History();
            history_timer = history_timer_reset;
        }
    }
    public void History()
    {
        StartCoroutine(History_Request());
    }
    public IEnumerator History_Request()
    {
        string url = host + "History/" + username;
        UnityWebRequest history_req = UnityWebRequest.Get(url);
        yield return history_req.SendWebRequest();
        string history_result = history_req.downloadHandler.text;
        Dictionary<string, ArrayList> history_dict = JsonConvert.DeserializeObject<Dictionary<string, ArrayList>>(history_result);

        for (int i = 0; i < 10; i++)
        {
            try
            {
                Category_Array[Category_Array.Length - 1 - i] = history_dict["category"][i].ToString();
            }
            catch (Exception e)
            {
                print(e);
            }
            try
            {
                Amount_Array[Amount_Array.Length - 1 - i] = history_dict["amount"][i].ToString();
            }
            catch (Exception e)
            {
                print(e);
            }
        }

        if (history_req.isNetworkError || history_req.isHttpError)
        {
            Debug.Log(history_req.error);
        }
        else
        {
            bool instantiated = false;
            try
            {
                GameObject[] search_for_objects = GameObject.FindGameObjectsWithTag("history_block_transaction");
                int object_count = search_for_objects.Length;
                if (object_count != 0)
                {
                    instantiated = true;
                }
                else
                {
                    instantiated = false;
                }
            }
            catch (Exception e)
            {
                instantiated = false;
                //ignore.
            }

            if (instantiated == true)
            {
                //blocks[0].GetComponent<Image>().sprite = TxOutSprite;
                GameObject[] blocks = GameObject.FindGameObjectsWithTag("history_block_transaction");
                for (int i = 0; i < 10; i++)
                {
                    // Index 0 means "Category Text Field"
                    blocks[i].GetComponentsInChildren<Text>()[0].text = Category_Array[i].ToString();
                    if(Category_Array[i].ToString() == "send")
                    {
                        blocks[i].GetComponent<Image>().sprite = TxOutSprite;
                    }
                    else if(Category_Array[i].ToString() == "receive")
                    {
                        blocks[i].GetComponent<Image>().sprite = TxInSprite;
                    }
                    // Index 1 means "Amount Text Field"
                    blocks[i].GetComponentsInChildren<Text>()[1].text = Amount_Array[i].ToString();
                }
            }
        }
    }
}
                
