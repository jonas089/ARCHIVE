using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class clipboard : MonoBehaviour
{
    public Text CryOS_Address;

    public Text bitcoin_address;
    public Text ravencoin_address;
    public void copy_raven()
    {
        GUIUtility.systemCopyBuffer = ravencoin_address.text;
    }
    public void copy_bitcoin()
    {
        GUIUtility.systemCopyBuffer = bitcoin_address.text;
    }
    public void copy_CryOS()
    {
        GUIUtility.systemCopyBuffer = CryOS_Address.text;
    }
}
