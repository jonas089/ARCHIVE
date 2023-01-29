using System.Collections;
using System.Collections.Generic;
using System.Net;
using TMPro;
using System;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using UnityEngine.Networking;

public class access : MonoBehaviour
{
    public Texture RegistrationFailedImage;
    public Texture RegistrationValidImage;
    public Texture LoginFailedImage;
    public GameObject NotificationPanel;
    public RawImage Notification;


    public TMP_InputField user_text;
    public TMP_InputField pass_text;
    public TMP_InputField email_text;
    public string star_string = "*";
    public string star_pass = "";
    public static int star_length = 0;
    public GameObject Email_Field;

    public GameObject Loading_panel;

    public Toggle I_accept;

    public static string host = "https://www.cryptosplatform.net/";
    public static string username = "";
    public static string email = "";

    public string user = "";
    public string pass = "";

    public void Start()
    {
        Email_Field.SetActive(false);
    }
    public void Add_Mail_Field()
    {
        if (I_accept.isOn == true)
        {
            Email_Field.SetActive(true);
        }
        else
        {
            Email_Field.SetActive(false);
        }
    }

    public void Update()
    {
        star_pass = "";
        user = user_text.text;
        pass = pass_text.text;
        email = email_text.text;
        username = user;
    }

    public void Login()
    {
        Loading_panel.SetActive(true);
        StartCoroutine(Login_Request());
        Loading_panel.SetActive(false);
    }

    public IEnumerator Login_Request()
    {
        string url = host + "Login/" + user + "/" + WWW.EscapeURL(pass);
        print(url);
        UnityWebRequest login_req = UnityWebRequest.Get(url);
        yield return login_req.SendWebRequest();

        if (login_req.isNetworkError || login_req.isHttpError)
        {
            Debug.Log(login_req.error);
        }
        else
        {
            string login_status = login_req.downloadHandler.text;
            if (login_status.Contains("Login valid"))
            {
                //ACTION ON LOGIN SUCCESS
                SceneManager.LoadScene("Ledger");
            }
            else if (login_status.Contains("Login failed"))
            {
                //ACTION ON LOGIN FAILURE
                Notification.texture = LoginFailedImage;
                NotificationPanel.SetActive(true);
            }
            else
            {
                Notification.texture = LoginFailedImage;
                NotificationPanel.SetActive(true);
            }
        }
    }

    public void Registration()
    {
        if (I_accept.isOn)
        {
            Loading_panel.SetActive(true);
            StartCoroutine(Registration_Request());
            Loading_panel.SetActive(false);
        }
        else
        {
            //ignore.
        }
    }

    public IEnumerator Registration_Request()
    {
        if (I_accept.isOn)
        {
            string url = host + "Registration/" + user + "/" + WWW.EscapeURL(pass) + "/" + email;
            print(url);
            UnityWebRequest registration_req = UnityWebRequest.Get(url);
            yield return registration_req.SendWebRequest();

            if (registration_req.isNetworkError || registration_req.isHttpError)
            {
                Debug.Log(registration_req.error);
            }
            else
            {
                string registration_status = registration_req.downloadHandler.text;
                if (registration_status.Contains("Registration valid"))
                {
                    //ACTION ON REGISTRATION SUCCESS
                    Notification.texture = RegistrationValidImage;
                    NotificationPanel.SetActive(true);
                }
                else if (registration_status.Contains("Registration failed"))
                {
                    //ACTION ON REGISTRATION FAILURE
                    Notification.texture = RegistrationFailedImage;
                    NotificationPanel.SetActive(true);
                }
                else
                {
                    Notification.texture = RegistrationFailedImage;
                    NotificationPanel.SetActive(true);
                }
            }
        }
        else
        {
            // ignore.
        }
    }
}
